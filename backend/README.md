# 🎓 CampusConnect

A full-stack web application designed to bring important college activities and student services together in one place.

CampusConnect allows students to explore campus events, view notices, connect with the student community, manage their profile, and receive notifications. It also includes an Admin Panel for managing events and notices.

---

## ✨ Features

### 🏠 Home
- Clean and professional landing page
- Quick access to important campus sections
- Latest notices
- Upcoming events
- Easy navigation

### 📅 Events
- View upcoming campus events
- Event details and dates
- Event registration
- Dynamically loaded events from the backend

### 📢 Notices
- View important college notices
- Dynamic notice display
- Organized notice cards
- Notifications for newly added notices

### 🗣️ Community
- Create student posts
- View community posts
- Like and comment options
- Simple space for students to share ideas and discussions

### 🔐 Authentication
- Student signup
- Student login
- Login information stored using local storage
- Automatic navigation to the profile after login

### 👤 Profile
- Student profile information
- Profile picture
- Course and year details
- Email information
- About Me section
- Skills section
- My Events section
- Edit Profile functionality

### 🔔 Notifications
- Displays important campus updates
- Notices added through the Admin Panel appear as notifications

### 🛡️ Admin Panel
- Add new notices
- Add new events
- Manage campus information through the backend

---

## 🛠️ Technologies Used

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- Flask
- Flask-CORS

### Database
- SQLite

### Development Tools
- Visual Studio Code
- Git
- GitHub

---

## 📁 Project Structure

```text
CampusConnect/
│
├── backend/
│   ├── app.py
│   └── campusconnect.db
│
├── frontend/
│   ├── css/
│   │   └── style.css
│   │
│   ├── images/
│   │
│   ├── js/
│   │   └── script.js
│   │
│   ├── index.html
│   ├── events.html
│   ├── notices.html
│   ├── community.html
│   ├── profile.html
│   ├── signup.html
│   ├── login.html
│   ├── notifications.html
│   └── admin.html
│
└── README.md