# SkySender

Sky Sender is a Django-based application for managing users, clients, messages, and mailings. This project includes an admin interface, user roles, and various functionalities to handle mailing and client management.

## Table of Contents

- [Installation](#installation)
- [Environment Configuration](#environment-configuration)
- [Usage](#usage)

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL
- Redis
- pip (Python package installer)

### Clone the Repository

```bash
git clone https://github.com/yourusername/sky_sender.git
cd sky_sender
```

### Create and Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Environment Configuration
Create a .env file in the project root directory and add the following configurations.

**You can use *.env.sample* to understand all the variables.**

## Usage
### Apply Migrations
```bash
python manage.py migrate
```

### Create users and fixtures
```bash
python manage.py setup_initial_data
```

### Run the Development Server
```bash
python manage.py runserver
```