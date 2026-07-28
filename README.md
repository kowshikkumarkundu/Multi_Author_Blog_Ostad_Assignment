\# Multi-Author Blog System



A feature-rich web application built with Python and Django that enables multiple authors to register, compose, publish, edit, and manage their own blog articles. The system features user authentication, category-wise filtering, and role-based access control.



\---



\## Key Features



\- User Authentication \& Authorization: Secure User Registration, Login, Logout, and Profile management.

\- Multi-Author Content Management: Registered authors can create, update, and delete their own posts (CRUD operations).

\- Categorization \& Filtering: Articles categorized for seamless navigation and user discovery.

\- Search \& Pagination: Quick article search along with paginated blog listings for optimal user experience.

\- Environment Management: Sensitive configurations (Secret Key, Debug mode) securely managed using python-decouple.

\- Responsive UI: Clean, modern, and mobile-friendly frontend layout.



\---



\## Tech Stack \& Requirements



\- Language: Python 3.x

\- Framework: Django

\- Environment \& Security: python-decouple

\- Database: SQLite

\- Frontend: HTML5, CSS3



\---



\## How to Run the Project Locally



Follow these step-by-step instructions to set up and run the project on your machine.



**1. Clone the Repository**



git clone https://github.com/kowshikkumarkundu/Multi\_Author\_Blog\_Ostad\_Assignment



**2. Create and Activate Virtual Environment**

\# On Windows

python -m venv venv

venv\\Scripts\\activate



\# On Mac/Linux

python3 -m venv venv

source venv/bin/activate



**3. Install Dependencies**

pip install -r requirements.txt



**4. Configure Environment Variables**

SECRET\_KEY=your-django-secret-key-here

DEBUG=True

ALLOWED\_HOSTS=127.0.0.1,localhost



**5. Run Migrations \& Create Superuser**

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser



**6. Start the Development Server**

python manage.py runserver

































































in/activate

