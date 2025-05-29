# 🛍️ E-Commerce REST API

**To‘liq autentifikatsiya, OTP orqali SMS, savat, buyurtma va sharh tizimi bilan zamonaviy E-Commerce API**

---

## 🎯 Loyihaning Maqsadi

Foydalanuvchilar uchun quyidagi funksiyalarni RESTful API orqali taqdim etish:
- OTP orqali ro’yxatdan o’tish (SMS + Redis + Celery)
- Mahsulotlar katalogi
- Savatni boshqarish
- Buyurtma qilish
- Profil va sharhlar
- Swagger orqali hujjatlash

---
## ⚙️ Texnologiyalar
- Django 4.2+
- Django REST Framework
- Celery + Redis (📨 OTP yuborish)
- PostgreSQL
- drf-yasg (Swagger)
- Twilio / Mock SMS service
- Docker (opsional)
---
## 📲 OTP Autentifikatsiya (SMS)
- 1. Foydalanuvchi telefon raqamini yuboradi

- 2. SMS orqali OTP yuboriladi

- 3. Foydalanuvchi OTP ni tasdiqlaydi

- 4. JWT access & refresh token qaytariladi


## 🔐 Authentication Endpoints
| Method | Endpoint                          | Description                          |
|--------|-----------------------------------|--------------------------------------|
| POST   | `/api/v1/auth/register/`          | 📲 OTP kod yuborish                  |
| POST   | `/api/v1/auth/verify/`            | ✅ OTP tasdiqlash                    |
| POST   | `/api/v1/auth/login/`             | 🔑 Parol orqali login                |
| POST   | `/api/v1/auth/logout/`            | 🔓 Logout qilish                     |
| POST   | `/api/v1/auth/refresh/`           | 🔄 Access tokenni yangilash          |
| POST   | `/api/v1/auth/forget-password/`   | ❓ Parolni tiklashga so‘rov          |
| POST   | `/api/v1/auth/reset-password/`    | 🔁 Yangi parol o‘rnatish             |

## 🛍️ Product Endpoints
| Method | Endpoint                              | Description              |
|--------|---------------------------------------|--------------------------|
| GET    | `/api/v1/shop/products/`              | 📦 Mahsulotlar ro‘yxati  |
| POST   | `/api/v1/shop/products/`              | ➕ Yangi mahsulot qo‘shish |
| GET    | `/api/v1/shop/products/{id}/`         | 🔍 Mahsulot tafsilotlari  |


## 🛒 Cart (Savat) Endpoints
| Method | Endpoint                                      | Description                     |
|--------|-----------------------------------------------|---------------------------------|
| GET    | `/api/v1/shop/cart/`                          | 🧺 Savatni ko‘rish              |
| POST   | `/api/v1/shop/cart/`                          | ➕ Mahsulotni savatga qo‘shish  |
| DELETE | `/api/v1/shop/cart/remove/{id}/`              | ❌ Savatdan mahsulotni o‘chirish|


## 📦 Order Endpoints
| Method | Endpoint                        | Description                  |
|--------|---------------------------------|------------------------------|
| GET    | `/api/v1/shop/orders/`          | 📃 Buyurtmalar ro‘yxati      |
| POST   | `/api/v1/shop/orders/`          | 🛍️ Buyurtma yaratish         |


## 👤 Profile Endpoints
| Method | Endpoint                     | Description                    |
|--------|------------------------------|--------------------------------|
| GET    | `/api/v1/user/profile/`      | 👤 Profilni ko‘rish            |
| PATCH  | `/api/v1/user/profile/`      | ✏️ Profilni tahrirlash         |


## 📝 Review Endpoints
| Method | Endpoint                                    | Description                     |
|--------|---------------------------------------------|---------------------------------|
| POST   | `/api/v1/shop/products/{id}/review/`        | 💬 Mahsulotga sharh qoldirish   |

## 📄 API hujjatlari

| Dokumentatsiya | URL manzili | Tavsif                        |
|----------------|-------------|-------------------------------|
| 🔹 **Swagger** | `/swagger/` | Interaktiv API hujjatlari     |
| 🔸 **ReDoc**   | `/redoc/`   | Statik va toza API ko‘rinishi |


## 🚀 Loyihani Ishga Tushurish
````
Klonlash
git clone https://github.com/Bunyodjon-Mamadaliyev/E-commerce-API.git
cd E-commerce-API

Virtualenv
python -m venv venv
source venv/bin/activate

Talablar
pip install -r requirements/development.txt

Redis ishga tushiring (local or Docker)
redis-server

Migratsiyalar
python manage.py migrate

Django server
python manage.py runserver
````
## 🧪 Testlash
````
python manage.py test
````