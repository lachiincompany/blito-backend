# 🚌 بلیتو (Blito) - سامانه خرید آنلاین بلیط اتوبوس

<div dir="rtl">

## 🌟 درباره بلیتو
بلیتو یک سامانه هوشمند و کاربرپسند برای خرید آنلاین بلیط اتوبوس است. با بلیتو می‌توانید به راحتی و در کمترین زمان ممکن، بلیط سفر خود را تهیه کنید و با خیال راحت سفر کنید! 🎫✨

### ✨ ویژگی‌های اصلی
- 🔍 جستجوی سریع و آسان مسیرها
- 💳 پرداخت امن و آنلاین
- 🎟️ صدور آنی بلیط
- 📱 رابط کاربری ساده و زیبا
- 🔔 اطلاع‌رسانی وضعیت سفر
- 💺 امکان انتخاب صندلی دلخواه

## Screenshots

### Admin Panel (Jazzmin)

**Dashboard**
نمای کلی از داشبورد پنل ادمین که وضعیت پروژه و آمارها را نمایش می‌دهد.
![Admin Dashboard](core/screenshots/admin_dashboard.png)

**List View (e.g., fleet)**
نمایش لیست آیتم‌ها (مانند اتوبوس ها) با قابلیت جستجو و مرتب‌سازی.
![fleet List](core/screenshots/admin_fleet_list.png)

**Detail / Edit Form**
فرم جزئیات و ویرایش یک رکورد، شامل فیلدها و دکمه‌های عملیات.
![terminals Edit](core/screenshots/admin_terminal_edit.png)

---

### API Documentation (Swagger)

**Swagger UI – Overview**
نمایش کل Endpointهای پروژه با گروه‌بندی و مستندات.
![Swagger Overview](core/screenshots/swagger_overview.png)

**Endpoint Example – Trips**
نمایش یک Endpoint خاص، شامل پارامترها و توضیحات.
![Swagger reservations Endpoint](core/screenshots/swagger_reservations.png)

**Try It Out – cities Endpoint**
امکان تست مستقیم Endpointها از داخل Swagger.
![Swagger Try It Out](core/screenshots/swagger_cities_tryitout.png)

## 🚀 راه‌اندازی پروژه

### پیش‌نیازها
- Python 3.8 یا بالاتر
- Docker و Docker Compose
- Git
- PostgreSQL 13+
### مراحل نصب و راه‌اندازی

1️⃣ کلون کردن مخزن:
```bash
git clone https://github.com/YourUsername/blito-backend.git
cd blito-backend
```

2️⃣ ساخت محیط مجازی و نصب وابستگی‌ها:
```bash
python -m venv venv
source venv/bin/activate  # برای لینوکس و مک
# یا
.\venv\Scripts\activate  # برای ویندوز

pip install -r requirements.txt
```

3️⃣ راه‌اندازی با داکر:
```bash
docker-compose up -d
```
4️⃣ اجرای مایگریشن‌ها:
```bash
docker-compose exec web python manage.py migrate
```

5️⃣ دسترسی به برنامه:
- پنل ادمین: `http://localhost:8000/admin` 🔐
- API داکیومنت: `http://localhost:8000/api/docs` 📚

## 👨‍💻 تیم توسعه‌دهندگان

پروژه «بلیتو» حاصل تلاش جمعی از توسعه‌دهندگان پرتلاش، خلاق و متعهد است که با دقت و حساسیت بالا، زیرساختی پایدار و قابل‌اعتماد برای کاربران فراهم کرده‌اند.

---

### 🛠️ تیم فنی و مشارکت‌کنندگان

- **شاهین زمانی** – مدیر پروژه و توسعه‌دهنده ارشد  
  💻 متخصص در توسعه وب با تمرکز بر Django و طراحی معماری‌های مقیاس‌پذیر  
  🔗 [مشاهده در GitHub](https://github.com/shahinzam101)

- **علیرضا شیخ احمدی** – مدیر دیزاین
  
   🎨 طراح هویت بصری، خالق لوگوهای حرفه‌ای، و مسئول خلق جلوه‌های گرافیکی منحصربه‌فرد  
  🔗 [مشاهده در GitHub](https://github.com/Alirezasha1)

- **آویسا فیضی** – توسعه‌دهنده و مدیر داده  
  🗃️ مسئول مدیریت ساختار داده‌ها، طراحی اصولی پایگاه داده، و تضمین یکپارچگی اطلاعات  
  🔗 [مشاهده در GitHub](https://github.com/Avisaoops)
  
- **مریم سرخوش** – هماهنگ‌کننده تجربه انسانی و کیفیت پروژه  
  👥 نقش‌آفرین در ایجاد فضای تیمی مثبت، بررسی تجربه کاربری و ارائه بازخوردهای انسانی  
  🔍 مشارکت در بررسی کیفیت و نظم بخش‌هایی از پروژه برای حفظ استانداردها  
  🔗 [مشاهده در GitHub](https://github.com/maryamsar)

---

### 🤝 سایر مشارکت‌کنندگان

از تمامی توسعه‌دهندگانی که با ایده‌ها، کدها و بازخوردهای ارزشمند خود به ارتقاء پروژه بلیتو کمک کرده‌اند، صمیمانه سپاسگزاریم. همراهی شما مایه دلگرمی ماست. ❤️


## 👥 مشارکت در پروژه
از مشارکت شما در پروژه استقبال می‌کنیم! برای مشارکت:
1. یک فورک از پروژه ایجاد کنید
2. برنچ جدید بسازید (`git checkout -b feature/amazing-feature`)
3. تغییرات را کامیت کنید (`git commit -m 'Add amazing feature'`)
4. برنچ را پوش کنید (`git push origin feature/amazing-feature`)
5. یک Pull Request ایجاد کنید

## 📝 لایسنس
این پروژه تحت لایسنس MIT منتشر شده است.

## 📞 تماس با ما
- 📧 ایمیل: shahinzam1402@gmail.com
- 📱 تلگرام: @blitoSupport

## 🎉 با بلیتو، سفر خوش!
سفر با بلیتو = سفری بی‌دغدغه و راحت! 🚌✨

</div>
