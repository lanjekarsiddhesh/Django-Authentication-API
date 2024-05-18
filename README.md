# Django Authentication CRUD Operations API

This API provides a set of endpoints for creating, reading, updating, and deleting , Send email user custom authentication data in a Django application.

## Prerequisites

- Familiarity with Python and Django
- Git installed on your local machine
- Familiarity with Postman
## Setup

1. Clone the repository: git clone https://github.com/your-username/your-repo-name.git
2. Install the required packages: pip install -r requirements.txt
3. Create a PostgreSQL database and update the settings.py file with your database credentials.
4. Run the migrations: python manage.py migrate.
5. Run the python manage.py runserer.
6. Import .json file for postman api endpoints.
7. set up .env file

## set up .env file

1. SECRET_KEY = ''
2. EMAIL_USER = "Your email address"
3. EMAIL_PASSWORD = "Your email password"
4. EMAIL_FROM = "Your email address"

## API Endpoints

1. POST http://127.0.0.1:8000/Auth/api/Registration/ -- (Register new user)
2. POST http://127.0.0.1:8000/Auth/api/Login/ -- (Login user)
3. GET, PUT, DELETE http://127.0.0.1:8000/Auth/api/Profile/ -- (View, Update and Delete profile)
4. PUT http://127.0.0.1:8000/Auth/api/changePassword/ -- (Change password)
5. POST http://127.0.0.1:8000/Auth/api/Send-Email-To-ResetPassword/ -- (Send email to reset password)
6. POST endpoint created dynamically by send email to reset password -- (link to reset password)

## Authentication:

The API uses Django's built-in authentication system to authenticate requests. Users must provide a valid username and password to access the API.

## Models
MyUser = Create custom model.

## Serializers

The API uses the following serializers:
1. AuthSerializer -- (For Register new user serializer)
2. LoginSerializer -- (For Login user serializer)
3. GetUserdataSerializer -- (For View, Update and Delete profile serializer)
4. PasswordChangeSerializer -- (For Change password serializer)
5. SendEmailToResetPasswordSerializer -- (For Send email to reset password serializer)
6. ResetPassword -- (For reset password serializer)

## Views

The API uses following views:
1. Registration_API -- (For Register new user views)
2. Login_API -- (For Login user views)
3. UserView -- (For View, Update and Delete profile views)
4. ChangePassword  -- (For Change password views)
5. SendEmailToResetPassword  -- (For Send email to reset password views)
6. resetPassword -- (For reset password views)
7. get_tokens_for_user -- (For Create refresh and access token)

## Database

Default database NoSQL.
