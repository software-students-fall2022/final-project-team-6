![Admin Status](https://github.com/software-students-fall2022/final-project-team-6/actions/workflows/admin_workflow.yml/badge.svg?event=push)
![Client Status](https://github.com/software-students-fall2022/final-project-team-6/actions/workflows/client_workflow.yml/badge.svg?event=push)

# Overview

This is a course forum with Albert courses data, comments and rate my professor link

Admin can search add,delete courses to the mongoDB to maintain the course the correctness of the information

Users can search add,comment and view all the course information

# Subsystems
- a **admin** - a program that demonstrates the courses information from API and demonstrate on screen for admin to add and delete to maintain
- a **users** - an interface through which web visitors can see the course information and maintain the database
- a **database** - stores the data used by both other parts

# Running the Project
1. Make sure you have a `.env` file exists in both `users` and `admin` directory. Within the `.env` file, make sure you have the following environment variables
   ```
   DB_CONNECTION_STRING=YOUR_DB_CONNECTION_STRING
   DB_NAME=YOUR_DB_NAME
   ```
   where `DB_CONNECTION_STRING` is the connection string to your MongoDB database, and `DB_NAME` is the Database name.

## Running with Docker
1. Navigate to the root folder of this project, then run:
   ```
   docker compose up
   ```

2. The admin client will run at `127.0.0.1:7001`. The users client will run at `127.0.0.1:6001`.
   
3.  A database container will also be created in your Docker. Make sure your `.env` file has the connection string to your database in the container. i.e. `DB_CONNECTION_STRING=mongodb://db:27017/`

## Running without Docker
### User
1. Navigate to `/users`, then:
```
pip3 install -r requirements.txt

python -m flask run --port=6001
```
### Admin
1. Navigate to `/admin`, then:
```
pip3 install -r requirements.txt

python -m flask run --port=6001
```

# Running the Project for the First Time
If the database in your `.env` files are new, you need to have some initial data in your databases before you run the User app.

1. Launch the Admin App
   ```
   cd admin
   python -m flask run --port=6001
   ```
2. On the main page, click "Refresh All Courses from Schedge API"
3. Then, all NYU courses, schools, subjects info will be saved to your MongoDB. This is an asynchronous process, and it will take about 30 minutes to import everything. But you can still run User App while the Admin is importing data.
4. In the future, if NYU updates its academic calender, you can always click the Refresh button to update existing courses. 
# Running Tests

IMPORTANT: Before you run tests, make sure both `.env` files in `users` and `admin` are as follows (since some tests require some pre-existing data):
```
DB_CONNECTION_STRING=mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689
DB_NAME=App
```

<br>

Then, simply navigate to `/users` or `/admin`, and:
```
python -m pytest --cov
``` 

# Deployed Apps
We have deployed both of our apps. You can try them using the links below:
<br>
[Admin App](https://urchin-app-52ddx.ondigitalocean.app/)
<br>
[Visitor App](https://stingray-app-2-3m4gq.ondigitalocean.app/) 


# Docker Images
We have pushed our custom subsystem images to DockerHub:
<br>
[Admin App](https://hub.docker.com/repository/docker/cty288/course-admin)
<br>
[Visitor App](https://hub.docker.com/repository/docker/cty288/course-client) 

# API Used 

[Schedge](https://schedge.a1liu.com/)

Schedge is an API to NYU's course catalog. Please note that this API is currently under active development and is subject to change.

# Collections

User:

```javascript
{
    "username" : str
    "password" : str,
    "school" : str,
    "subject" : str
}
```

Schools:
```javascript
{
    "schoolAbbr" : str,
    "schoolFullname" : str,
    "subjects" : [
        {
            "subjectAbbr" : str,
            "subjectFullname" : str
        }
    ]
}
```


Course:

```javascript
{  
    "deptCourseId" : str,
    "registrationNumber" : float,
    "instructors" : str,
    "type" : str,
    "status" : str,
    "instructionMode" : str,
    "location" : str,
    "units" : float,
    "schoolAbbr" : str,
    "schoolFullname" : str,
    "subjectAbbr" :str,
    "subjectFullname" : str,
    "courseName" : str 
}
```

Comments:
```javascript
{
    "courseName" : str,
    "comments" : [
        {
            "username" : str,
            "comment" : str,
            "rating" : str
        }
    ]
}
```
# File Structure

```
├── LICENSE
├── README.md
├── admin
│   ├── Dockerfile
│   ├── README.md
│   ├── app.py
│   ├── common
│   │   └── libs
│   │       ├── Url_Manager.py
│   │       └── __init__.py
│   ├── config
│   │   └── base_setting.py
│   ├── controllers
│   │   ├── __init__.py
│   │   ├── comment.py
│   │   ├── course.py
│   │   ├── database.py
│   │   └── index.py
│   ├── crawl.py
│   ├── modules
│   │   ├── editDatabase.py
│   │   └── requestCourses.py
│   ├── requirements.txt
│   ├── rmpData.json
│   ├── static
│   │   ├── css
│   │   │   └── photo_demo.css
│   │   ├── images
│   │   │   ├── empty_star.png
│   │   │   └── filled_star.png
│   │   └── plugins
│   │       ├── bootstrap_v3
│   │       │   ├── css
│   │       │   ├── fonts
│   │       │   └── js
│   │       ├── jquery.min.js
│   │       └── layer
│   │           ├── layer.js
│   │           ├── mobile
│   │           │   ├── layer.js
│   │           │   └── need
│   │           │       └── layer.css
│   │           └── skin
│   ├── templates
│   │   ├── common
│   │   │   └── layout.html
│   │   └── courses
│   │       ├── course_details.html
│   │       ├── courses.html
│   │       ├── schools.html
│   │       └── subjects.html
│   └── tests
│       ├── test_comment.py
│       ├── test_course.py
│       ├── test_database.py
│       ├── test_editDatabase.py
│       ├── test_index.py
│       └── test_requestCourse.py
├── docker-compose.yaml
└── users
    ├── Dockerfile
    ├── app.py
    ├── common
    │   └── libs
    │       ├── Url_Manager.py
    │       └── __init__.py
    ├── config
    │   └── base_setting.py
    ├── controllers
    │   ├── __init__.py
    │   ├── course.py
    │   ├── dashboard.py
    │   ├── index.py
    │   └── login.py
    ├── models
    │   ├── __init__.py
    │   ├── comment.py
    │   ├── database.py
    │   └── user.py
    ├── requirements.txt
    ├── static
    │   ├── css
    │   │   └── dashboard.css
    │   ├── images
    │   │   ├── empty_star.png
    │   │   └── filled_star.png
    │   └── plugins
    │       ├── bootstrap_v3
    │       │   ├── css
    │       │   ├── fonts
    │       │   └── js
    │       ├── jquery.min.js
    │       └── layer
    │           ├── layer.js
    │           ├── mobile
    │           │   ├── layer.js
    │           │   └── need
    │           │       └── layer.css
    │           └── skin
    ├── templates
    │   ├── common
    │   │   ├── layout.html
    │   │   └── layout_authenticated.html
    │   ├── courses
    │   │   ├── course_details.html
    │   │   ├── dashboard.html
    │   │   ├── dashboard_search.html
    │   │   ├── hello_world.html
    │   │   └── index.html
    │   ├── hello_world.html
    │   ├── login.html
    │   └── sign_up.html
    └── tests
        ├── test_database.py
        ├── test_login_route.py
        └── test_test.py
```

# Contributors

[Tim Chen](https://github.com/cty288)

[James Liu](https://github.com/liushuchen2025)

[Wenni Fan](https://github.com/fwenni)

[Yanchong Xu](https://github.com/yx-xyc)

[Iris Qian](https://github.com/okkiris)

[Jiawei Zhang](https://github.com/jiawei-zhang-a)
