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

# Running Tests
Running tests does not require you to setup a MongoDB database, but does require you to have Internet connection.

<br>

Simply navigate to `/users` or `/admin`, then:
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
.
├── admin
│   ├── common
│   │   └── libs
│   ├── config
│   ├── controllers
│   ├── static
│   │   ├── css
│   │   └── plugins
│   │       ├── bootstrap_v3
│   │       │   ├── css
│   │       │   ├── fonts
│   │       │   └── js
│   │       └── layer
│   │           ├── mobile
│   │           │   └── need
│   │           └── skin
│   │               └── default
│   ├── templates
│   │   ├── common
│   │   └── courses
│   └── tests
└── users
    ├── common
    │   └── libs
    ├── config
    ├── controllers
    ├── static
    │   ├── css
    │   └── plugins
    │       ├── bootstrap_v3
    │       │   ├── css
    │       │   ├── fonts
    │       │   └── js
    │       └── layer
    │           ├── mobile
    │           │   └── need
    │           └── skin
    │               └── default
    ├── templates
    │   ├── common
    │   └── courses
    └── tests
```

# Contributors

[Tim Chen](https://github.com/cty288)

[James Liu](https://github.com/liushuchen2025)

[Wenni Fan](https://github.com/fwenni)

[Yanchong Xu](https://github.com/yx-xyc)

[Iris Qian](https://github.com/okkiris)

[Jiawei Zhang](https://github.com/jiawei-zhang-a)
