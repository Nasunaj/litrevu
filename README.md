# LITReview  - Book and article review social network

> **Description**: LITReview is a web application developed with Django, allowing users to post requests for reviews (tickets) and publish reviews of books or articles. Users can also follow other members to stay updated on their activities.

---

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- [Python 3.10 or higher](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- SQLite database manager (included with Python)
- A modern web browser (Chrome, Firefox, Edge, etc.)

---

## Installation and setup

### 1. Clone the repository

```bash
git clone https://github.com/Nasunaj/litrevu.git
cd LITRevu
```

---
### 2. Create a virtual environment
To isolate the project dependencies, create a virtual environment using `venv`:
```bash
python -m venv venv
```

#### Activate the virtual environment
- **On Windows**:
  ```bash
  venv\Scripts\activate
  ```
- **On macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```
---

### 3. Install dependencies
With the virtual environment activated, install the project dependencies:
```bash
pip install -r requirements.txt
```
---

### 4. Configure environment variables

Create a `.env` file at the root of the project to store sensitive variables (such as the Django secret key). Here is an example of its content:

```env
SECRET_KEY=your_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

To generate a secret key, you can use [this online generator](https://djecrety.ir/) or run the following Python code:
 ```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```
---

### 5. Apply migrations

Django uses migrations to manage the database. Run the following commands to create and apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 7. Run the Development Server

Start the Django server with the following command:

```bash
python manage.py runserver
```

> **Access the Application**:
>
> - Open your browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
> - To access the admin interface: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Project Structure

Here is an overview of the project structure:

```
├── authentification              # User management application
│   ├── admin.py            # Django admin configuration
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations          # Database migrations
│   ├── models.py
│   ├── static              # Static files (CSS)
│   ├── templates           # HTML templates
│   └── views.py
├── db.sqlite3
├── flake8_report                 # Flake8 Report (generated)
├── litrevu
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py             # URLs
│   └── wsgi.py
├── manage.py                     # Django management script
├── media                         # Uploaded files (ticket images)
├── README.md                     # This file
├── requirements.txt              # Python dependencies
├── reviews
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── __init__.py
│   ├── migrations
│   ├── models.py          # Models: Ticket, Review, UserFollows
│   ├── templates
│   └── views.py
             
```
---