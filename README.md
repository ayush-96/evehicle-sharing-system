README - eVehicleSystem
Project Overview
The eVehicleSystem is an electric vehicle share program implemented as a web application using the Django framework, with a front-end built using Bootstrap. This system allows customers to rent and return electric vehicles (such as scooters and bikes), pay for their rentals, report defects, and perform other tasks. Operators can track, charge, repair, and manage vehicles, while managers can view reports on system activity. The database is implemented using PostgreSQL.

Project Structure
1. eVehicleSystem/
This is the root directory of the project containing all necessary configuration files and initial settings.
2. eVehicleSystemApp/
The main Django application containing the core functionality, views, models, templates, and URL configurations.
3. models/
Contains Python files defining database models used for storing customer data, vehicles, charging points, locations, and other essential entities.
4. manage.py
A command-line utility that lets you interact with the Django project in various ways, such as running the development server, creating migrations, and managing the database.

Objective
The primary objective of the eVehicleSystem is to create a functional end-to-end prototype of an electric vehicle share system. The application should provide interfaces for:
- Customers to reserve, return, and pay for vehicle rentals.
- Operators to assess and manage the state of the vehicles.
- Managers to generate and view detailed usage reports.

Key Features:

Customer Capabilities:
Rent a Vehicle: Customers can rent a vehicle at any available location in the city.
Return a Vehicle: Allows customers to return rented vehicles to any location and charges their account based on usage duration and vehicle type.
Report a Defective Vehicle: Option to report vehicle issues.
Payment Management: Pay any outstanding charges on their accounts.
Buy: Customer can buy a vehicle which is available for rent.

Operator Capabilities:
Track Vehicles: View the real-time location of all vehicles across the city.
Vehicle Charging: Charge vehicles when their battery is low.
Repair Defective Vehicles: Manage repairs of reported vehicles.
Relocate Vehicles: Move vehicles to optimize location availability.

Manager Capabilities:
Generate Reports: Create usage reports with data visualizations to monitor the system's activity over specified time periods.

Technologies Used:
Backend:
Django: https://www.djangoproject.com/
A high-level Python web framework that simplifies web development by providing pre-built components.
PostgreSQL: A powerful, open-source object-relational database system for production.

Frontend:
Bootstrap: https://getbootstrap.com/
A framework for developing responsive and user-friendly web applications.
Development Setup
Clone the repository:

bash
Copy code
git clone <repository-url>
cd eVehicleSystem
Set up a virtual environment (recommended):

bash
Copy code
python -m venv env
source env/bin/activate  # On Windows: .\env\Scripts\activate

Database Configuration:

Modify settings.py to configure PostgreSQL settings:
python
Copy code
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<your_db_name>',
        'USER': '<your_db_user>',
        'PASSWORD': '<your_db_password>',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
Run migrations:
Copy code
python manage.py makemigrations
python manage.py migrate

Start the development server:
Copy code
python manage.py runserver

Usage Instructions
Customer Interface: Provides functionalities for registering, logging in, renting, and returning vehicles.
Operator Dashboard: Accessible by operators to view and manage vehicle conditions, status, and locations.
Manager Dashboard: Allows managers to generate and view reports on the system's performance.

Contact and Support
For any queries or support, please reach out to the development team. Lab 02-05 Programming and Systems Development
3043532A@student.gla.ac.uk