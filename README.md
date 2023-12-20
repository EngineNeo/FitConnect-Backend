# FitConnect-Backend
Backend for fitness application

Step 1:
In workbench run 
```
DROP SCHEMA IF EXISTS fitness;
CREATE SCHEMA fitness;
USE fitness;
```

Step 2: 
In the folder you cloned the repo to, create and activate a python virtual environment. 

Step 3:
Run `pip install -r requirements.txt`

Step 4:
Create an environment variable DB_PASSWORD and set it to the password for you MySQL 'root' user

Step 5:
Run `python manage.py makemigrations FitConnect`

Step 6:
Run `python manage.py migrate`

Step 7: 
Run `python mangage.py loaddata dumpeddata.json`

Step 8:
`python manage.py runserver` will bring the backend server up at localhost:8000/
