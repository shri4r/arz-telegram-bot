import asyncio
import importlib
import sqlite3
import tempfile
import unittest
from contextlib import closing
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import requests

import currency_crawler as crawler
import db_functions as db
import telegram_bot as bot


def html(prices=("600,000", "750,000", "650,000")):
    return "<table>" + "".join(
        f'<tr data-market-row="{market}"><td><span>{price}</span></td></tr>'
        for market, price in zip(crawler.MARKETS, prices)
    ) + "</table>"


class DatabaseCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.db_patch = patch.object(db, "DB_PATH", Path(self.temp.name) / "test.db")
        self.db_patch.start()
        self.addCleanup(self.db_patch.stop)

    def test_missing_and_empty_database(self):
        self.assertIsNone(db.retrieve_latest())
        self.assertIsNone(db.retrieve_dollar())
        self.assertIsNone(db.retrieve_pound())
        self.assertIsNone(db.retrieve_euro())

    def test_latest_valid_snapshot_and_timestamp(self):
        db.create_table()
        db.add_row(60000, 75000, 65000)
        db.add_row(61000, 76000, 66000)
        snapshot = db.retrieve_latest()
        self.assertEqual(snapshot["dollar"], 61000)
        self.assertEqual(snapshot["updated_at"].tzinfo, timezone.utc)

    def test_invalid_legacy_row_does_not_hide_last_good_prices(self):
        db.create_table()
        db.add_row(60000, 75000, 65000)
        with closing(db.get_db_connection()) as con, con:
            con.execute("INSERT INTO tgju(dollar, pound, euro) VALUES ('', 'N/A', '')")
        self.assertEqual(db.retrieve_dollar(), 60000)

    def test_invalid_insert_preserves_snapshot(self):
        db.create_table()
        db.add_row(60000, 75000, 65000)
        with self.assertRaises(ValueError):
            db.add_row(0, 75000, 65000)
        self.assertEqual(db.retrieve_dollar(), 60000)

    def test_connection_error_propagates_without_unbound_variables(self):
        with patch.object(db, "get_db_connection", side_effect=sqlite3.OperationalError):
            with self.assertRaises(sqlite3.Error):
                db.retrieve_latest()

    def test_failed_refresh_preserves_prices_and_timestamp(self):
        db.create_table()
        db.add_row(60000, 75000, 65000)
        before = db.retrieve_latest()
        for failure in (requests.Timeout("timeout"), ValueError("missing cell")):
            with self.subTest(failure=failure):
                with patch.object(crawler, "fetch_prices", side_effect=failure):
                    with self.assertRaises(type(failure)):
                        crawler.refresh_prices()
                self.assertEqual(db.retrieve_latest(), before)

    def test_successful_refresh_saves_complete_snapshot(self):
        with patch.object(crawler, "fetch_prices", return_value=(60000, 75000, 65000)):
            crawler.refresh_prices()
        self.assertEqual(db.retrieve_latest()["euro"], 65000)


class CrawlerTests(unittest.TestCase):
    def test_numeric_toman_conversion(self):
        for value, expected in (
            ("600,000", 60000), ("123,456", 12345), (" ۶۰۰٬۰۰۰ ", 60000),
        ):
            with self.subTest(value=value):
                self.assertEqual(crawler.fix_string(value), expected)

    def test_invalid_prices_are_rejected(self):
        for value in ("N/A", "", "0", "-100", "600000 rial", "12.5"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                crawler.fix_string(value)

    def test_nested_cell_text(self):
        self.assertEqual(crawler.parse_prices(html()), (60000, 75000, 65000))

    def test_missing_or_invalid_currency_rejects_entire_snapshot(self):
        for page in (html().replace("price_gbp", "missing"), html(("600,000", "N/A", "650,000"))):
            with self.subTest(page=page), self.assertRaises(ValueError):
                crawler.parse_prices(page)

    def test_import_does_not_make_network_requests(self):
        with patch("requests.get") as get:
            importlib.reload(crawler)
        get.assert_not_called()

    def test_fetch_checks_status_and_timeout(self):
        with patch("requests.get") as get:
            response = get.return_value.__enter__.return_value
            response.text = html()
            self.assertEqual(crawler.fetch_prices(), (60000, 75000, 65000))
            response.raise_for_status.assert_called_once()
            self.assertTrue(get.call_args.args[0].startswith("https://"))
            self.assertEqual(get.call_args.kwargs["timeout"], (5, 15))

    def test_http_errors_are_not_parsed(self):
        with patch("requests.get") as get, patch.object(crawler, "parse_prices") as parse:
            response = get.return_value.__enter__.return_value
            response.raise_for_status.side_effect = requests.HTTPError("503")
            with self.assertRaises(requests.HTTPError):
                crawler.fetch_prices()
            parse.assert_not_called()


class ReplyTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self.snapshot = {"dollar": 60000, "updated_at": self.now}

    def test_price_unit_and_timestamp(self):
        message = bot.format_price("dollar", self.snapshot, self.now)
        self.assertIn("60,000 tomans", message)
        self.assertIn("2026-01-01 00:00:00 UTC", message)
        self.assertNotIn("Warning", message)

    def test_stale_threshold(self):
        for age, stale in ((899, False), (900, True), (3600, True)):
            with self.subTest(age=age):
                message = bot.format_price(
                    "dollar", self.snapshot, self.now + timedelta(seconds=age)
                )
                self.assertEqual("Warning" in message, stale)

    def test_missing_data_message(self):
        self.assertIn("not available yet", bot.format_price("dollar", None))


class PollingStartupTests(unittest.TestCase):
    def test_polling_starts_without_an_existing_event_loop(self):
        # Python 3.14 no longer creates an implicit main-thread event loop.
        asyncio.set_event_loop(None)
        with patch.object(bot, "TOKEN", "123456:offline-test-token"):
            application = bot.build_application()

        async def stop_after_initialization(app):
            app.stop_running()

        application.post_init = stop_after_initialization
        # Exercise the real polling entry point without contacting Telegram.
        with patch.object(
            type(application), "_bootstrap_initialize", new_callable=AsyncMock
        ) as initialize:
            try:
                application.run_polling(stop_signals=None)
                initialize.assert_awaited_once()
            finally:
                asyncio.set_event_loop(None)


class BotTests(unittest.IsolatedAsyncioTestCase):
    async def test_database_failure_gets_friendly_reply(self):
        update = SimpleNamespace(effective_chat=SimpleNamespace(id=123))
        context = SimpleNamespace(bot=SimpleNamespace(send_message=AsyncMock()))
        with patch.object(bot, "retrieve_latest", side_effect=sqlite3.OperationalError):
            with self.assertLogs(bot.logger, level="ERROR"):
                await bot.dollar(update, context)
        self.assertIn("temporarily unavailable", context.bot.send_message.call_args.kwargs["text"])

    async def test_empty_database_gets_friendly_reply(self):
        update = SimpleNamespace(effective_chat=SimpleNamespace(id=123))
        context = SimpleNamespace(bot=SimpleNamespace(send_message=AsyncMock()))
        with patch.object(bot, "retrieve_latest", return_value=None):
            await bot.euro(update, context)
        self.assertIn("not available yet", context.bot.send_message.call_args.kwargs["text"])

    async def test_refresh_failure_is_logged_and_does_not_stop_scheduler(self):
        for failure in (requests.Timeout(), ValueError(), sqlite3.OperationalError()):
            with self.subTest(failure=failure):
                with patch.object(bot, "refresh_prices", side_effect=failure):
                    with self.assertLogs(bot.logger, level="ERROR"):
                        await bot.refresh_job(None)

    async def test_startup_refresh_and_repeating_schedule(self):
        job = SimpleNamespace(run=AsyncMock())
        queue = SimpleNamespace(run_repeating=MagicMock(return_value=job))
        application = SimpleNamespace(job_queue=queue)
        with patch.object(bot, "create_table"):
            await bot.post_init(application)
        job.run.assert_awaited_once_with(application)
        self.assertEqual(queue.run_repeating.call_args.kwargs["interval"], 300)
        self.assertEqual(queue.run_repeating.call_args.kwargs["job_kwargs"]["max_instances"], 1)

    async def test_application_has_scheduler_without_contacting_telegram(self):
        with patch.object(bot, "TOKEN", "123456:offline-test-token"):
            application = bot.build_application()
        self.assertIsNotNone(application.job_queue)
        self.assertEqual(len(application.handlers[0]), 5)
        await application.bot.shutdown()


if __name__ == "__main__":
    unittest.main()
