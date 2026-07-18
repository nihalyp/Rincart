# 🛒 RinCart - Full-Stack Django E-Commerce Platform

RinCart is a feature-rich, responsive, and robust full-stack e-commerce web application built using the **Django** framework. This project successfully showcases the transition from a local development environment to a production-ready cloud deployment (hosted on Render), resolving complex configuration challenges along the way.

---

## 📌 Project Journey & Resolution Summary

During the deployment and production setup phase, several critical production-level challenges were identified and successfully resolved:

1. **Admin Panel Layout Fix (WhiteNoise Integration):** 
   Resolved broken Django Admin CSS/JS styling in production by optimizing the `INSTALLED_APPS` load order and leveraging `whitenoise.runserver_nostatic` alongside `django.contrib.staticfiles`.
2. **Persistent Media Storage (Cloudinary Integration):** 
   Since Render uses an ephemeral (temporary) file system, uploading media files locally would result in data loss. This was resolved by integrating **Cloudinary Storage** to host and serve product images dynamically.
3. **Dynamic Image URL Rendering:** 
   Fixed broken image links across templates by refactoring hardcoded media paths to use dynamic Django URL properties (e.g., swapping `/media/{{ item.image }}` with `{{ item.image.url }}`). This ensures smooth delivery of images hosted on Cloudinary's CDN.

---

## 🚀 Key Features

* **User Authentication & Social Login:** Integrated with `django-allauth` for seamless Google and Facebook OAuth onboarding.
* **Enhanced Security (OTP Workflow):** Features an automated workflow that redirects users to an OTP verification page (`/verify-otp/`) right after signup and login.
* **Cloud Media Management:** Media files and product images are directly handled, cached, and stored securely using **Cloudinary Storage**.
* **Production-Ready Static Delivery:** Leverages **WhiteNoise** (`CompressedManifestStaticFilesStorage`) for efficient, compressed static asset (CSS/JS) rendering in production environments.
* **Production Database:** Configured to run flawlessly on high-performance **Neon PostgreSQL** database clusters.
* **Automated Transactional Emails:** Uses **Anymail (Brevo Backend)** to trigger transactional emails and OTP notifications safely.
* **Responsive UI:** A clean, modern Bootstrap 5 interface tailored for an optimal shopping experience across mobile, tablet, and desktop viewports.

---

## 🛠️ Tech Stack

* **Backend Framework:** Django 6.x / Python 3.12+
* **Database:** Neon PostgreSQL (Production), SQLite (Local/Development fallback)
* **Cloud Media Storage:** Cloudinary (`django-cloudinary-storage`)
* **Static Asset Management:** WhiteNoise
* **Email Service:** Anymail (Brevo Backend)
* **Hosting Platform:** Render

---

## 💻 Local Setup & Installation

Follow these steps to get the project running on your local machine for evaluation or development:

### 1. Clone the Repository
```bash
git clone [https://github.com/nihalyp/RinCart.git](https://github.com/nihalyp/RinCart.git)
cd RinCart
```
### 2. Set Up a Virtual Environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```
### 3. Install Dependencies
```bash
#All required packages (including django-allauth, django-cloudinary-storage, anymail, and whitenoise) are pre-configured in the requirements file. Install them with:
pip install -r requirements.txt
```
### 4. Environment Variables Configuration (.env)
```plaintext 
# Create a file named .env in the root directory (the same directory where manage.py exists) and populate it with your configuration credentials:
SECRET_KEY="your-django-secret-key"
DATABASE_URL="your-postgresql-database-url"
BREVO_API_KEY="your-brevo-api-key"
CLOUDINARY_CLOUD_NAME="your-cloudinary-cloud-name"
CLOUDINARY_API_KEY="your-cloudinary-api-key"
CLOUDINARY_API_SECRET="your-cloudinary-api-secret"
```
### 5. Apply Migrations & Collect Static Files
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```
### 6. Start the Local Server
```bash
python manage.py runserver
```
## The application will now be accessible locally at http://127.0.0.1:8000/.

## 🌐 Live Demo
Experience the live application hosted on Render here: rincart.onrender.com

