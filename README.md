# Fitness Studio Booking API

## Project Overview

A simple Django REST API for a fictional fitness studio where clients can view classes and book spots. Built with Django and Django REST Framework using SQLite as the database.

## Features
- View upcoming fitness classes (Yoga, Zumba, HIIT, etc.)
- Book a class if slots are available
- Prevent duplicate bookings for same user & class
- View bookings by client email
- Input validation and timezone-aware class filtering
- Logging for key actions

## Requirements

- Python 3.8+
- Django 4.x
- Django REST Framework
- SQLite

---

## API Endpoints

### **1. View All Upcoming Classes**

**Request:**

```
GET /classes/
```

**Response:**

```
[
    {
        "id": 4,
        "name": "Zumba",
        "date_time": "2025-07-17T18:00:00+05:30",
        "instructor": "Wick",
        "available_slots": 13
    },
    {
        "id": 6,
        "name": "Boxing",
        "date_time": "2025-07-17T06:00:00+05:30",
        "instructor": "Kabilan",
        "available_slots": 15
    }
]
```

### **2. Book a Class**

**Request:**

```
POST /book/
```

**Response:**

```
{
    "message": "Booking successful",
    "booking_id": 3,
    "available_slots": 7
}
```

### **3. View Bookings by Email**

**Request:**

```
GET /bookings/?email=r@r.com
```

**Response:**

```
[
    {
        "client_name": "rice",
        "client_email": "r@r.com"
    }
]
```

---

## Local Setup Instructions

### Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/aboobacker-bilal/fitness_studio.git
cd fitness_studio
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 5. Run the Development Server
```bash
python manage.py runserver
```
---

This project is open source.