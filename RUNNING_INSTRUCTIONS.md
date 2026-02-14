# SafeEstate Project - Running Instructions

## Prerequisites

- Python 3.x installed on your system
- pip package manager

## Setup Instructions

### 1. Clone or Download the Project

If cloning from a repository:
```bash
git clone <repository-url>
cd safeestate
```

### 2. Create Virtual Environment

It's recommended to use a virtual environment for this project:

#### On Windows:
```bash
python -m venv safeestate_env
.\safeestate_env\Scripts\Activate.ps1
```

#### On macOS/Linux:
```bash
python -m venv safeestate_env
source safeestate_env/bin/activate
```

### 3. Install Dependencies

Install all required packages:
```bash
pip install -r requirements.txt
```

If requirements.txt doesn't exist, install the known dependencies:
```bash
pip install Django==5.2.6 Pillow django-crispy-forms crispy-tailwind
```

### 4. Database Setup

Run migrations to set up the database:
```bash
python manage.py migrate
```

Create a superuser account (optional but recommended):
```bash
python manage.py createsuperuser
```

### 5. Load Sample Data (Optional)

To populate the database with sample data:
```bash
python create_sample_data.py
```

### 6. Run the Development Server

Start the Django development server:
```bash
python manage.py runserver
```

The application will be accessible at http://127.0.0.1:8000/

### 7. Access the Application

- Main site: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/ (requires superuser login)

## Project Structure

The project consists of three main Django apps:
- `accounts`: Handles user authentication, registration, and KYC verification
- `properties`: Manages property listings and visit requests
- `admin_panel`: Provides administrative controls and verification tools

## Troubleshooting

If you encounter issues:
1. Ensure the virtual environment is activated
2. Check that all dependencies are installed
3. Verify database migrations have been run
4. Make sure the correct Python interpreter is being used