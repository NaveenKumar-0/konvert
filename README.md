# konvert
# 🚀 Konvert – File Conversion Web Application

**Konvert** is a secure web-based file conversion application that allows users to convert images into multiple formats and videos into MP3 audio. It includes authentication with email verification, conversion history tracking, and cloud storage integration.

---

## ✨ Features

- User authentication with email verification
- Image conversion to multiple formats: PDF, PNG, JPG, GIF, WEBP
- Video to MP3 conversion (max 30 seconds)
- Secure file storage using AWS S3
- Conversion history per user
- JWT-based protected APIs
- Clean and simple UI

---

## 🧱 Architecture

- Type: Monolithic application
- Single FastAPI backend
- Server-side rendered frontend using Jinja2
- REST APIs + HTML pages in one service
- Ideal for MVP; can be split into microservices later if needed

---

## 🖥️ Frontend Stack

- HTML (Jinja2 templates)
- CSS (custom styling)
- Vanilla JavaScript (Fetch API)
- **No frontend framework** (React/Vue not used)

**Responsibilities:**

- Login & signup
- File upload
- Trigger conversions
- Show download links
- Display conversion history

---

## ⚙️ Backend Stack

- Python
- FastAPI
- SQLAlchemy ORM
- JWT authentication
- Pillow (PIL) – image processing
- FFmpeg – video to MP3 conversion
- Boto3 – AWS S3 integration

---

## 🗄️ Database

- PostgreSQL (recommended)
- SQLAlchemy ORM

**Tables:**

### `users`
Stores authentication and verification data.

| Column       | Description                |
|--------------|---------------------------|
| id           | Primary key               |
| email        | User email                |
| password_hash| Hashed password           |
| is_verified  | Email verification status |
| created_at   | Timestamp                 |

### `files`
Stores conversion metadata.

| Column            | Description                   |
|-------------------|-------------------------------|
| id                | Primary key                   |
| user_id (FK → users)| Reference to users           |
| file_type         | image / video                 |
| original_s3_key   | Original file S3 key          |
| converted_s3_key  | Converted file S3 key         |
| created_at        | Timestamp                     |

> **Note:** Actual files are not stored in the database. Only S3 object keys are stored.

---

## ☁️ File Storage

**AWS S3**

**Folders used:**

- `originals/images`
- `originals/videos`
- `converted/images`
- `converted/audio`

> Files are accessed using pre-signed download URLs.

---

## 🔐 Authentication & Security

- JWT-based authentication
- Email verification required before login
- Protected API routes
- Tokens stored in browser localStorage

---

## 🔌 API Endpoints

### Authentication
- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/resend-verification`

### Conversion
- `POST /convert/image`
- `POST /convert/video-to-mp3`

### History
- `GET /convert/my-files`

---

## 📁 Project Structure

konvert_app/
├── core/
│ ├── database.py
│ ├── security.py
├── models/
│ ├── user.py
│ ├── file.py
├── routers/
│ ├── auth.py
│ ├── convert.py
│ ├── pages.py
├── services/
│ ├── image_converter.py
│ ├── video_converter.py
│ ├── s3.py
├── templates/
│ ├── index.html
│ ├── dashboard.html
│ ├── image.html
│ ├── video.html
│ ├── base.html
│ ├── login.html
│ ├── signup.html
├── static/
│ ├── css/
│ ├── js/
└── requirements.txt
└── main.py

---

## ✅ Current Status

- Backend APIs: ✅ Complete  
- Frontend UI: ✅ Functional MVP  
- Image conversion: ✅ Working  
- Video conversion: ✅ Working  
- Conversion history: ✅ Working  
- Cloud storage: ✅ Integrated  

---

