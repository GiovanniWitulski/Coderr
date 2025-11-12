# Coderr - Backend API

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.2.4-green?logo=django)
![Django REST Framework](https://img.shields.io/badge/DRF-3.15-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

Welcome to the backend API for **Coderr**, a service and freelancer platform. This project is built with Django and Django REST Framework to serve as the complete backend for the Coderr application.

It handles user authentication, profiles (for customers and businesses), service listings (offers), orders, and reviews.

## 🚀 Features

* **Token Authentication:** Full user registration (`/api/registration/`) and login (`/api/login/`) using DRF Token Authentication.
* **Dual User Roles:** Clear separation between `customer` and `business` user types, each with different permissions.
* **Offer Management:** Business users can create, read, update, and delete service listings (Offers) with multiple detail tiers.
* **Ordering System:** Customers can create new orders based on a business's service offer.
* **Review System:** Customers can write and manage reviews for businesses they've worked with.
* **Aggregate Data:** A global endpoint (`/api/base-info/`) provides platform-wide statistics like total review count and average rating.

## 💻 Tech Stack

* **Backend:** Python
* **Framework:** Django (Version 5.2.4)
* **API:** Django REST Framework
* **CORS:** `django-cors-headers`
* **Database:** SQLite 3 (Default for development)
* **Authentication:** Django TokenAuthentication

## 🛠️ Installation & Setup

Follow these steps to get the project running locally.

### Prerequisites

* Python (3.10 or newer)
* `pip` (Python package installer)
* Git

### Local Setup

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
    cd YOUR-REPOSITORY
    ```

2.  **Create and Activate a Virtual Environment:**
    ```bash
    # Windows
    python -m venv env
    .\env\Scripts\activate
    
    # macOS / Linux
    python3 -m venv env
    source env/bin/activate
    ```

3.  **Install Dependencies:**
    Install all required packages from the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```
    *(See the `requirements.txt` content at the bottom of this README if you need to create it.)*

4.  **Run Database Migrations:**
    This command will create your `db.sqlite3` file and all necessary database tables.
    ```bash
    python manage.py migrate
    ```

5.  **(Optional) Create a Superuser:**
    To access the Django Admin panel (`/admin/`), you'll need an admin account.
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the Server:**
    ```bash
    python manage.py runserver
    ```
    The API is now running and accessible at `http://127.0.0.1:8000/`.

---

## 🌐 Core API Endpoints

All endpoints are prefixed with `/api/`.

| Endpoint | Method | Description | Permissions |
| --- | --- | --- | --- |
| `/registration/` | `POST` | Registers a new user (`customer` or `business`). | Public |
| `/login/` | `POST` | Logs in a user and returns an auth token. | Public |
| `/base-info/` | `GET` | Gets global platform statistics. | Public |
| `/profile/{user_id}/` | `GET`, `PATCH` | Reads or updates a specific user profile. | `GET`: Public, `PATCH`: Owner Only |
| `/profiles/business/` | `GET` | Lists all `business` profiles. | Public |
| `/profiles/customer/` | `GET` | Lists all `customer` profiles. | Public |
| `/offers/` | `GET`, `POST` | Lists all offers or creates a new one. | `GET`: Public, `POST`: Business Only |
| `/offers/{id}/` | `GET`, `PATCH`, `DELETE` | Reads, updates, or deletes a specific offer. | `GET`: Public, `PATCH`/`DELETE`: Owner Only |
| `/offerdetails/{id}/` | `GET` | Gets the details of a single offer package. | Public |
| `/orders/` | `GET`, `POST` | Lists a user's orders or creates a new one. | `GET`: Public (for now), `POST`: Customer Only |
| `/orders/{id}/` | `PATCH`, `DELETE` | Updates an order's status (Business only) or deletes (Admin only). | Role-Specific |
| `/reviews/` | `GET`, `POST` | Lists reviews or creates a new one. | `GET`: Public, `POST`: Customer Only |
| `/order-count/{biz_id}/` | `GET` | Counts active orders for a business user. | Public |
| `/completed-order-count/{biz_id}/` | `GET` | Counts completed orders for a business user. | Public |

---

## 📋 `requirements.txt`

If you need to re-create your `requirements.txt` file, here is the list of dependencies based on your `pip freeze` output and known project structure.

```txt
asgiref==3.9.1
Django==5.2.6
django-cors-headers==4.9.0
django-filter==25.2
djangorestframework==3.16.1
pillow==11.3.0
sqlparse==0.5.3
tzdata==2025.2
```