# Blogicum — Social Network for Personal Diaries

This repository combines projects developed as part of the Yandex Practicum curriculum. **Blogicum** is a web platform where users can share their thoughts, create personal pages, and organize publications into thematic categories.

![Python](https://img.shields.io/badge/python-black?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-black.svg?style=for-the-badge&logo=django&logoColor=3CB371)
![SQLite](https://img.shields.io/badge/sqlite-black.svg?style=for-the-badge&logo=sqlite&logoColor=87CEFA)
![bootstrap](https://img.shields.io/badge/bootstrap-black.svg?style=for-the-badge&logo=bootstrap&logoColor=9370DB)

## Purpose

 Blogicum demonstrates my Backend QA competencies within Django environments. It highlights my proficiency in Python and SQL, my approach to handling complex business logic, and my capacity to design clean, maintainable backend architectures

## Core Features

- **Posts and Categories:** Create posts linked to categories such as "Travel," "IT," or "Cooking."

- **Geolocation:** Option to specify a location for each publication.

- **Social Interaction:** Browse other users' pages, read feeds, and comment on posts.

- **Personalization:** Customize author profiles with unique names and page addresses.

- **Moderation:** Tools for content control and blocking spam accounts.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com
cd django-sprint4
```

### 2. Step-by-Step Installation

1. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Linux/macOS
   # or venv\Scripts\activate for Windows
   ```

2. **Upgrade pip and install dependencies:**

   ```bash
   python3 -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Run migrations:**

   ```bash
   python3 blogicum/manage.py migrate
   ```

4. **Load database fixtures:**

   ```bash
   python3 blogicum/manage.py loaddata db.json
   ```

5. **Create a superuser:**

   ```bash
   python3 blogicum/manage.py createsuperuser
   ```

### 3. Run the Project

Start the development server:

```bash
python3 blogicum/manage.py runserver
```
