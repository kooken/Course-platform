# Learning Platform

A Django-based platform for managing online courses, lessons, and subscriptions with integrated payment processing via Stripe. Key features include:

- **Course Management**: CRUD functionality for courses and lessons.
- **Subscriptions**: Users can subscribe to courses with automated payments.
- **Stripe Integration**: Seamless payment handling using Stripe API.
- **Technologies**: Python, Django, DRF, PostgreSQL, Stripe API.

To run it, you need to:

- Make sure that Docker Desktop is available on your device
- After deploying the project, you need to create a .env file in which to specify the data for the environment variables
- The variables are in the .env.example file
- Dependencies are written in the requirements.txt file
- Build and run the project using the command: docker-compose up --build
- After starting the server in Docker, follow the link
