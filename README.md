# server_API-worker

A simple SMS provider Endpoints

Create virtual env (python -m venv name_of_your_choice)

activate virtual env and install all the dependencies (pip install -r requirements.txt)

run your local server by cmd - python manage.py runserver port_of_your_choice(default-8000)

to go through the API services have to login with the user credentials (localhost:8000/login/).

after successfully login you can now able to work on service-APIs.

# server_API-worker test_cases

we have provided with test cases for the API services(based on time I was unable to complete all the test cases).

the configuration to work on test cases is setup in pytest.ini file placed in project dir.

the commands to run the test cases is:
1. py.test (or) 
2. pytest (or)
3. py.test -p no:warning (which will be useful to get rid of warnings)