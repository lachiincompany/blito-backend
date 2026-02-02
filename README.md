# 🚌 بلیتو (Blito) — سامانه خرید آنلاین بلیط اتوبوس

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-Backend-092E20?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Swagger](https://img.shields.io/badge/Swagger-API%20Docs-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)

</div>

<div dir="rtl">

## 🌟 درباره بلیتو
**بلیتو** یک پلتفرم آنلاین و مدرن برای خرید بلیط اتوبوس است که به کاربران امکان می‌دهد با چند کلیک ساده، سفرها را جستجو کنند، صندلی موردنظر را انتخاب کنند و فرآیند رزرو را به‌صورت آنلاین انجام دهند.

این ریپو مربوط به **Backend** پروژه است و با هدف پیاده‌سازی یک سیستم واقعی و قابل دیپلوی (Production-like) طراحی شده است.

### ✨ ویژگی‌های اصلی
- 🎫 **رزرو آنلاین** بلیط اتوبوس
- 🔍 **جستجوی هوشمند** مسیرها و سفرها
- 💺 **انتخاب صندلی دلخواه** و مدیریت ظرفیت
- 💳 **پرداخت امن** و ثبت تراکنش‌ها
- 🧑‍💼 **پنل ادمین آنلاین** برای مدیریت کامل سیستم
- 📄 **Swagger آنلاین** برای مستندسازی و تست API
- 🐳 اجرای سرویس‌ها با **Docker / Docker Compose**

</div>

## Screenshots

### Admin Panel (Jazzmin)

**Dashboard**
نمای کلی از داشبورد پنل ادمین که وضعیت پروژه و آمارها را نمایش می‌دهد.
![Admin Dashboard](screenshots/admin_dashboard.png)

**List View (e.g., fleet)**
نمایش لیست آیتم‌ها (مانند اتوبوس ها) با قابلیت جستجو و مرتب‌سازی.
![fleet List](screenshots/admin_fleet_list.png)

**Detail / Edit Form**
فرم جزئیات و ویرایش یک رکورد، شامل فیلدها و دکمه‌های عملیات.
![terminals Edit](screenshots/admin_terminal_edit.png)

---

### API Documentation (Swagger)

**Swagger UI – Overview**
نمایش کل Endpointهای پروژه با گروه‌بندی و مستندات.
![Swagger Overview](screenshots/swagger_overview.png)

**Endpoint Example – Trips**
نمایش یک Endpoint خاص، شامل پارامترها و توضیحات.
![Swagger reservations Endpoint](screenshots/swagger_reservations.png)

**Try It Out – cities Endpoint**
امکان تست مستقیم Endpointها از داخل Swagger.
![Swagger Try It Out](screenshots/swagger_cities_tryitout.png)

## 🚀 راه‌اندازی پروژه

### پیش‌نیازها
- Python 3.8+
- Django
- SQLite (پیش‌فرض)
- pip (مدیریت پکیج‌های پایتون)

### مراحل نصب و راه‌اندازی

1️⃣ کلون کردن مخزن:
```bash
git clone https://github.com/your-username/blito-backend.git
cd blito-backend/core
```

2️⃣ ساخت محیط مجازی:
```bash
python -m venv venv
# در ویندوز
venv\Scripts\activate
# در لینوکس/مک
source venv/bin/activate
```

3️⃣ نصب وابستگی‌ها:
```bash
pip install -r requirements.txt
```

4️⃣ اجرای مایگریشن‌های دیتابیس:
```bash
python manage.py migrate
```

5️⃣ ساخت یک کاربر ادمین:
```bash
python manage.py createsuperuser
```

6️⃣ اجرای سرور توسعه:
```bash
python manage.py runserver
```

حالا می‌توانید به آدرس `http://localhost:8000` مراجعه کنید! 🎉

## 📁 ساختار پروژه
- `accounts/`: مدیریت کاربران و احراز هویت
- `bus_companies/`: مدیریت شرکت‌های اتوبوسرانی
- `city/`: مدیریت شهرها و مسیرها
- `fleet/`: مدیریت ناوگان اتوبوس‌ها
- `payments/`: سیستم پرداخت
- `reservations/`: سیستم رزرو بلیط
- `seat/`: مدیریت صندلی‌ها
- `trips/`: مدیریت سفرها و برنامه‌ریزی


.

## 📞 تماس با ما
- 📧 ایمیل: support@blito.ir
- 🌐 وبسایت: https://blito.ir
- 📱 تلگرام: @BlitoSupport

## 🎯 شعار ما
> سفری امن و راحت، با یک کلیک! 🚌✨

</div> 
