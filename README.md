<a id="choose-language"></a>
**Choose your language / زبان را انتخاب کنید**

[English](#english) | [فارسی](#persian)

---

<a id="english"></a>

# Arz Telegram Bot — Iranian Currency Prices in Tomans

A Python Telegram bot for checking **US Dollar (USD), Euro (EUR), and British Pound (GBP) prices in Iranian tomans**. Arz Telegram Bot fetches exchange-rate data from [TGJU](https://www.tgju.org/), stores it in SQLite, and answers Telegram commands with the latest successfully fetched prices.

Prices refresh every **5 minutes** while the bot is running. Each reply includes the currency, price in tomans, source, and last successful update time.

[Setup](#english-setup) · [Commands](#english-commands) · [Troubleshooting](#english-troubleshooting) · [فارسی](#persian)

## Features

- **Three currencies:** USD, EUR, and GBP prices against the Iranian toman.
- **Explicit units:** source prices are converted from rials to tomans; **1 toman = 10 rials**.
- **Automatic refresh:** fetches at startup and every 5 minutes, without a separate cron job.
- **Update timestamps:** shows the last successful fetch time in UTC.
- **Stale-price warnings:** warns when a snapshot is 15 minutes old or older.
- **Safe storage:** a failed request or an incomplete/invalid scrape preserves the last successful snapshot.
- **Friendly fallback:** missing prices and database failures produce helpful messages.
- **Lightweight storage:** SQLite requires no separate database server.
- **Offline regression tests:** cover conversion, parsing, storage, replies, and scheduling.

> This README is bilingual. The bot's current replies are in English; choosing a README language does not change the bot's language.

<a id="english-setup"></a>

## Installation and setup

### 1. Get the project

Install Python **3.10 or newer** and Git. Python **3.14** is supported, including installation from prebuilt packages on 64-bit Windows. Run:

```bash
git clone https://github.com/shri4r/arz-telegram-bot.git
cd arz-telegram-bot
python -m venv venv
```

Activate the virtual environment using the command for your terminal:

| Terminal | Command |
| --- | --- |
| Windows PowerShell | `.\venv\Scripts\Activate.ps1` |
| Windows Command Prompt | `venv\Scripts\activate.bat` |
| macOS / Linux | `source venv/bin/activate` |

On systems where Python is named `python3`, use `python3` to create the environment.

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

The requirements include `python-telegram-bot[job-queue]` for scheduled updates, Requests for HTTP fetching, and Beautiful Soup with lxml for HTML parsing.

If you already installed an older version of this project, update the code and upgrade dependencies inside your existing virtual environment:

```bash
python -m pip install --upgrade -r requirements.txt
```

You can keep Python 3.14 installed. The updated lxml dependency has a prebuilt Windows x86-64 package, so this installation does not require Microsoft C++ Build Tools.

### 3. Configure your Telegram bot token

Create a bot through [@BotFather](https://t.me/BotFather) on Telegram using `/newbot`. Copy the token into your local `config.py`:

```python
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
```

Keep the token private. Do not commit your real token or include it in screenshots, issues, or pull requests.

### 4. Start the bot

```bash
python telegram_bot.py
```

Open your bot in Telegram and send `/start`. Keep this process running for scheduled refreshes. For a server installation, configure your process manager to restart the bot after a reboot.

The bot creates `currencies.db` beside the source files automatically. No manual database setup or separate crawler process is required.

<a id="english-commands"></a>

## Telegram commands

| Command | What it does |
| --- | --- |
| `/start` | Shows a welcome message and available commands |
| `/dollar` | Shows the US Dollar price in tomans |
| `/euro` | Shows the Euro price in tomans |
| `/pound` | Shows the British Pound price in tomans |

Example reply (illustrative, not a live quote):

```text
US Dollar: 60,000 tomans
Last successful update: 2026-01-01 12:00:00 UTC
Source: TGJU
```

If that snapshot becomes stale, the reply also includes:

```text
Warning: this price is stale (15 minutes or older).
```

## How prices are fetched and stored

1. The crawler requests TGJU over HTTPS and checks the HTTP response status.
2. It extracts and validates all three currency prices before saving anything.
3. Prices are converted numerically from rials to whole tomans, rounding down any fractional toman.
4. A complete snapshot is saved to SQLite with a UTC timestamp.
5. Telegram commands read the latest valid saved snapshot.

Requests use a **5-second connection timeout** and a **15-second read timeout**. Network errors, HTTP failures, and missing or invalid prices are logged; failed refreshes leave previous prices and their timestamp intact.

**Freshness matters:** the displayed time is when this bot successfully fetched the data, not when the market or TGJU last published a price. A successful fetch does not guarantee that a quote has changed.

## Configuration and maintenance

The refresh settings are defined in `telegram_bot.py`:

| Setting | Default | Purpose |
| --- | --- | --- |
| `REFRESH_INTERVAL_SECONDS` | `300` | Time between scheduled refreshes |
| `STALE_AFTER_SECONDS` | `900` | Snapshot age that triggers a warning |

To fetch and save one snapshot manually:

```bash
python currency_crawler.py
```

Existing databases from the original version remain compatible: their prices were already converted to tomans. **Do not divide those saved values by 10 again.** Invalid legacy rows are skipped when reading prices. If an older installation created its database outside the project directory, stop the bot and move that database beside the source files before restarting.

## Project structure

```text
arz-telegram-bot/
├── telegram_bot.py       # Commands, replies, and scheduled refreshes
├── currency_crawler.py   # TGJU fetching, parsing, and toman conversion
├── db_functions.py       # SQLite storage and snapshot retrieval
├── config.py             # Local Telegram bot token
├── requirements.txt      # Python dependencies
├── tests/
│   └── test_prices.py    # Offline regression tests
└── README.md             # English and Persian documentation
```

## Tests

```bash
python -m unittest discover -s tests -v
```

Tests use temporary databases and mocked HTTP/Telegram calls. They do not require a real bot token or contact Telegram.

<a id="english-troubleshooting"></a>

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Bot does not start | Confirm the token in `config.py` and reinstall `requirements.txt` inside your active virtual environment. |
| Prices are not available yet | Check the logs for a failed initial fetch; the bot retries on its next scheduled refresh. |
| Stale-price warning | Check network access and the refresh logs. The bot is showing the last successful snapshot. |
| Scraping fails after previously working | TGJU may have changed its HTML or blocked a request; inspect the source and parsing logs. |
| Database is unavailable | Check write permissions and available disk space in the project directory. |
| PowerShell blocks environment activation | Use the virtual environment directly: `.\venv\Scripts\python.exe -m pip install -r requirements.txt`, then `.\venv\Scripts\python.exe telegram_bot.py`. |

## Contributing, data source, and license

Bug reports and focused pull requests are welcome through [GitHub Issues](https://github.com/shri4r/arz-telegram-bot/issues) and [Pull requests](https://github.com/shri4r/arz-telegram-bot/pulls). Include steps to reproduce a problem, but remove tokens and other private information.

Prices come from TGJU. This is an independent project and is not affiliated with Telegram or TGJU. Review the data provider's terms and access policies, respect request limits, and avoid unnecessarily frequent scraping. Quotes may be delayed or unavailable; verify prices independently before making financial decisions.

Released under the [MIT License](LICENSE). See the license for its warranty and liability terms.

[Choose language / انتخاب زبان](#choose-language)

---

<a id="persian"></a>

<div dir="rtl">

# ربات تلگرام ارز — قیمت دلار، یورو و پوند به تومان

**Arz Telegram Bot** یک ربات تلگرام با پایتون برای دریافت **قیمت دلار آمریکا، یورو و پوند انگلیس به تومان** است. این پروژه نرخ ارز را از [شبکه اطلاع‌رسانی طلا، سکه و ارز (TGJU)](https://www.tgju.org/) دریافت می‌کند، در پایگاه داده SQLite نگه می‌دارد و با دستورهای تلگرام نمایش می‌دهد.

تا زمانی که ربات در حال اجرا باشد، قیمت‌ها هر **۵ دقیقه** به‌روزرسانی می‌شوند. پاسخ هر دستور شامل نام ارز، قیمت به تومان، منبع و زمان آخرین دریافت موفق است.

[نصب و راه‌اندازی](#persian-setup) · [دستورها](#persian-commands) · [رفع اشکال](#persian-troubleshooting) · [English](#english)

## امکانات

- **پشتیبانی از سه ارز:** دلار آمریکا (USD)، یورو (EUR) و پوند انگلیس (GBP).
- **نمایش قیمت به تومان:** تبدیل عددی قیمت منبع از ریال به تومان؛ **هر تومان برابر با ۱۰ ریال است**.
- **به‌روزرسانی خودکار:** دریافت قیمت هنگام شروع و سپس هر ۵ دقیقه، بدون نیاز به کران‌جاب جداگانه.
- **نمایش زمان دریافت:** زمان آخرین دریافت موفق با منطقه زمانی UTC.
- **هشدار قدیمی بودن قیمت:** نمایش هشدار وقتی از آخرین دریافت موفق ۱۵ دقیقه یا بیشتر گذشته باشد.
- **حفظ قیمت‌های معتبر:** در صورت خطای شبکه یا دریافت داده ناقص و نامعتبر، اطلاعات موفق قبلی حفظ می‌شوند.
- **پیام مناسب هنگام خطا:** مدیریت نبود قیمت و خطاهای پایگاه داده.
- **ذخیره‌سازی سبک:** استفاده از SQLite بدون نیاز به سرور پایگاه داده جداگانه.
- **آزمون‌های آفلاین:** بررسی تبدیل واحد، استخراج قیمت، ذخیره‌سازی، پاسخ‌ها و زمان‌بندی.

> این راهنما دوزبانه است، اما پاسخ‌های فعلی ربات به زبان انگلیسی هستند. انتخاب زبان در README زبان خود ربات را تغییر نمی‌دهد.

<a id="persian-setup"></a>

## نصب و راه‌اندازی

### ۱. دریافت پروژه

پایتون **۳٫۱۰ یا جدیدتر** و Git را نصب کنید و دستورهای زیر را اجرا کنید. پایتون **۳٫۱۴** نیز پشتیبانی می‌شود و بسته‌های آماده برای ویندوز ۶۴ بیتی موجود هستند:

<div dir="ltr">

```bash
git clone https://github.com/shri4r/arz-telegram-bot.git
cd arz-telegram-bot
python -m venv venv
```

</div>

محیط مجازی را متناسب با ترمینال خود فعال کنید:

| ترمینال | دستور |
| --- | --- |
| ویندوز — PowerShell | `.\venv\Scripts\Activate.ps1` |
| ویندوز — Command Prompt | `venv\Scripts\activate.bat` |
| مک یا لینوکس | `source venv/bin/activate` |

اگر نام دستور پایتون در سیستم شما `python3` است، برای ساخت محیط مجازی از همان دستور استفاده کنید.

### ۲. نصب وابستگی‌ها

<div dir="ltr">

```bash
python -m pip install -r requirements.txt
```

</div>

فایل وابستگی‌ها شامل `python-telegram-bot[job-queue]` برای زمان‌بندی، Requests برای دریافت صفحه و Beautiful Soup به همراه lxml برای استخراج اطلاعات HTML است.

اگر نسخه قدیمی پروژه را نصب کرده‌اید، کد پروژه را به‌روز کنید و داخل همان محیط مجازی، وابستگی‌ها را ارتقا دهید:

<div dir="ltr">

```bash
python -m pip install --upgrade -r requirements.txt
```

</div>

نیازی به تغییر نسخه پایتون ۳٫۱۴ ندارید. نسخه جدید lxml بسته آماده برای ویندوز ۶۴ بیتی دارد و نصب آن به Microsoft C++ Build Tools نیاز ندارد.

### ۳. تنظیم توکن ربات تلگرام

در تلگرام به [@BotFather](https://t.me/BotFather) مراجعه کنید و با دستور `/newbot` یک ربات بسازید. توکن دریافتی را در نسخه محلی فایل `config.py` قرار دهید:

<div dir="ltr">

```python
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
```

</div>

توکن را محرمانه نگه دارید. توکن واقعی را در گیت ثبت نکنید و در تصویر، گزارش خطا یا درخواست ادغام قرار ندهید.

### ۴. اجرای ربات

<div dir="ltr">

```bash
python telegram_bot.py
```

</div>

ربات خود را در تلگرام باز کنید و دستور `/start` را بفرستید. برای ادامه به‌روزرسانی خودکار، فرایند ربات باید در حال اجرا بماند. روی سرور، ابزار مدیریت فرایند خود را طوری تنظیم کنید که پس از راه‌اندازی مجدد سرور، ربات نیز اجرا شود.

فایل `currencies.db` به‌صورت خودکار کنار فایل‌های پروژه ساخته می‌شود. راه‌اندازی دستی پایگاه داده یا اجرای جداگانه خزنده لازم نیست.

<a id="persian-commands"></a>

## دستورهای ربات

| دستور | کاربرد |
| --- | --- |
| `/start` | نمایش پیام خوشامد و فهرست دستورها |
| `/dollar` | نمایش قیمت دلار آمریکا به تومان |
| `/euro` | نمایش قیمت یورو به تومان |
| `/pound` | نمایش قیمت پوند انگلیس به تومان |

نمونه پاسخ زیر صرفاً برای نمایش قالب است و قیمت زنده نیست:

<div dir="ltr">

```text
US Dollar: 60,000 tomans
Last successful update: 2026-01-01 12:00:00 UTC
Source: TGJU
```

</div>

اگر از زمان دریافت این اطلاعات ۱۵ دقیقه یا بیشتر گذشته باشد، پیام زیر نیز نمایش داده می‌شود:

<div dir="ltr">

```text
Warning: this price is stale (15 minutes or older).
```

</div>

## روش دریافت و ذخیره قیمت‌ها

۱. خزنده صفحه TGJU را از طریق HTTPS دریافت می‌کند و وضعیت پاسخ HTTP را بررسی می‌کند.

۲. قیمت هر سه ارز استخراج و اعتبارسنجی می‌شود؛ تا پیش از تأیید همه قیمت‌ها، داده‌ای ذخیره نمی‌شود.

۳. قیمت‌ها به‌صورت عددی از ریال به تومان تبدیل می‌شوند. بخش کسری تومان به پایین گرد می‌شود.

۴. مجموعه کامل قیمت‌ها همراه با زمان دریافت به UTC در SQLite ذخیره می‌شود.

۵. دستورهای تلگرام آخرین مجموعه معتبر ذخیره‌شده را نمایش می‌دهند.

مهلت اتصال شبکه **۵ ثانیه** و مهلت خواندن پاسخ **۱۵ ثانیه** است. خطاهای شبکه، پاسخ ناموفق HTTP و قیمت‌های نامعتبر در گزارش‌ها ثبت می‌شوند. دریافت ناموفق، قیمت قبلی و زمان آن را تغییر نمی‌دهد.

**معنای زمان به‌روزرسانی:** زمان نمایش‌داده‌شده مربوط به دریافت موفق اطلاعات توسط ربات است؛ این زمان الزاماً زمان انتشار قیمت در بازار یا TGJU نیست. دریافت موفق صفحه به معنی تغییر قیمت بازار نیست.

## تنظیمات و نگهداری

تنظیمات زمان‌بندی در فایل `telegram_bot.py` قرار دارند:

| تنظیم | مقدار پیش‌فرض | کاربرد |
| --- | --- | --- |
| `REFRESH_INTERVAL_SECONDS` | `300` | فاصله دریافت‌های خودکار، به ثانیه |
| `STALE_AFTER_SECONDS` | `900` | سن اطلاعات برای نمایش هشدار، به ثانیه |

برای دریافت و ذخیره یک‌باره قیمت‌ها:

<div dir="ltr">

```bash
python currency_crawler.py
```

</div>

پایگاه داده نسخه اولیه همچنان قابل استفاده است؛ قیمت‌های آن قبلاً به تومان تبدیل شده‌اند. **مقادیر ذخیره‌شده را دوباره بر ۱۰ تقسیم نکنید.** ردیف‌های نامعتبر نسخه قدیمی هنگام خواندن نادیده گرفته می‌شوند. اگر نسخه قبلی پایگاه داده را بیرون از پوشه پروژه ساخته است، ربات را متوقف کنید و فایل پایگاه داده را پیش از اجرای مجدد به کنار فایل‌های پروژه منتقل کنید.

## ساختار پروژه

| فایل | مسئولیت |
| --- | --- |
| `telegram_bot.py` | دستورها، پاسخ‌ها و زمان‌بندی دریافت قیمت |
| `currency_crawler.py` | دریافت صفحه TGJU، استخراج قیمت و تبدیل به تومان |
| `db_functions.py` | ذخیره و بازیابی اطلاعات در SQLite |
| `config.py` | توکن محلی ربات تلگرام |
| `requirements.txt` | وابستگی‌های پایتون |
| `tests/test_prices.py` | آزمون‌های آفلاین |
| `README.md` | راهنمای انگلیسی و فارسی |

## اجرای آزمون‌ها

<div dir="ltr">

```bash
python -m unittest discover -s tests -v
```

</div>

آزمون‌ها از پایگاه داده موقت و پاسخ‌های شبیه‌سازی‌شده HTTP و تلگرام استفاده می‌کنند. به توکن واقعی نیاز ندارند و به تلگرام متصل نمی‌شوند.

<a id="persian-troubleshooting"></a>

## رفع اشکال

| مشکل | چه چیزی را بررسی کنیم؟ |
| --- | --- |
| ربات اجرا نمی‌شود | توکن فایل `config.py` را بررسی کنید و وابستگی‌ها را داخل محیط مجازی فعال نصب کنید. |
| هنوز قیمتی موجود نیست | گزارش خطای دریافت اولیه را بررسی کنید؛ ربات در نوبت زمان‌بندی‌شده بعدی دوباره تلاش می‌کند. |
| هشدار قدیمی بودن قیمت نمایش داده می‌شود | اتصال شبکه و گزارش‌های دریافت قیمت را بررسی کنید؛ ربات آخرین اطلاعات موفق را نمایش می‌دهد. |
| استخراج قیمت دیگر کار نمی‌کند | ممکن است HTML سایت TGJU تغییر کرده باشد یا درخواست مسدود شده باشد؛ منبع صفحه و گزارش استخراج را بررسی کنید. |
| پایگاه داده در دسترس نیست | مجوز نوشتن و فضای خالی دیسک در پوشه پروژه را بررسی کنید. |
| PowerShell اجازه فعال‌سازی محیط را نمی‌دهد | مستقیماً از پایتون محیط مجازی استفاده کنید: ابتدا `.\venv\Scripts\python.exe -m pip install -r requirements.txt` و سپس `.\venv\Scripts\python.exe telegram_bot.py`. |

## مشارکت، منبع داده و مجوز

برای گزارش مشکل از [بخش Issues](https://github.com/shri4r/arz-telegram-bot/issues) و برای پیشنهاد تغییر از [درخواست ادغام](https://github.com/shri4r/arz-telegram-bot/pulls) استفاده کنید. مراحل بازتولید خطا را بنویسید و اطلاعات خصوصی و توکن را حذف کنید.

منبع قیمت‌ها TGJU است. این پروژه مستقل است و وابستگی رسمی به تلگرام یا TGJU ندارد. شرایط استفاده و سیاست دسترسی منبع داده را بررسی کنید، محدودیت درخواست‌ها را رعایت کنید و از دریافت غیرضروری با فاصله بسیار کوتاه خودداری کنید. قیمت‌ها ممکن است با تأخیر یا موقتاً خارج از دسترس باشند؛ پیش از تصمیم مالی، قیمت را از منابع مستقل بررسی کنید.

پروژه تحت [مجوز MIT](LICENSE) منتشر شده است. شرایط ضمانت و مسئولیت در متن مجوز آمده است.

[انتخاب زبان / Choose language](#choose-language)

</div>
