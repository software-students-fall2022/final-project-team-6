![Admin Status](https://github.com/software-students-fall2022/final-project-team-6/actions/workflows/admin_workflow.yml/badge.svg?event=push)
![Client Status](https://github.com/software-students-fall2022/final-project-team-6/actions/workflows/client_workflow.yml/badge.svg?event=push)

# Overview

This is an NYU course forum with Albert courses data, comments and rate my professor link. It contains three subsystems: User app, Admin app, and a MongoDB database.

Admin app can add, delete courses to the mongoDB to maintain the course the correctness of the information. They can also delete comments for a specific course, and refresh all courses with Schedge API when NYU updates its academic calender

Users app is more like a "Rate my NYU Courses" website. They can browse all courses and their detailed information, search, rate, and add their comments for a specific course.

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

<br>

# CI/CD
[Admin App CI/CD workflow](https://github.com/software-students-fall2022/final-project-team-6/actions/workflows/admin_workflow.yml)
<br>
[Client App CI/CD workflow](https://github.com/software-students-fall2022/final-project-team-6/actions/workflows/client_workflow.yml)
<br>
*Note: Test coverages are also included in our GitHub Action workflows.

# Admin Functionalities
### Refresh All Schools/Subjects/Courses
   1. On the top of the main Page, click "Refresh All Courses from Schedge API"
   2. This will take some time to refresh all schools / subjects/ courses to the database

### View All Courses of a particular subject
1.  On the main page, click the school of the subject you want to view
2.  Find the subject you want to explore
3.  You will see a list of all displayed courses. You can click on those courses to view details

### Hide/Show Courses
1. On the same page, the switch on the top indicates whether you are viewing displayed courses or hidden courses.
2. You can change the display status of each course on this page 
   1. For example, if you are viewing displayed courses, you can change their status to `hidden` when you press "Hide All Selected Courses" button. Then, they will be removed from this list.
   2. When you turn the switch to the other side, you will view all the `hidden` courses and you will be able to change their status back to  `displayed`

### Delete Comments
1. When you view details of a course, you can also see all its comments
2. You can choose to delete a particular comment

<br>

# Client Functionalities
### Login / Register / Logout
1. You can login / register when you first use this app, and your session will be kept
2. You can logout on the top-right corner in the App

### Browse Courses / Dashboard
1. By default, the school and subject on your dashboard are your major set during your registeration process
2. You can change them and view all courses of your selected subject
3. You can click on the title of a course to view all its sections.
4. You can view the details of a specific section by pressing the "Details" button

### Post Comments
1. In the details panel of each section, you can post your comments and ratings to the course, which will affect this section's overall rating.
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
    "image": str (url)
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
   "courseName" : str,
    "schoolFullname" : str,
    "campus" : str,
    "deptCourseId" : str,
    "description" : str,
    "display" : boolean,
    "grading" : str,
    "instructionMode" : str,
    "instructors" : [
        str
    ],
    "location" : str,
    "notes" : str,
    "overallRating" : int,
    "rawCourseName" : str,
    "registrationNumber" : int,
    "rmpURLs" : [
        str
    ],
    "schoolAbbr" : str
    "sectionName" : str
    "section_code" : str,
    "status" : str,
    "subjectAbbr" : str,
    "subjectFullname" : str,
    "type" : str,
    "units" : float
}
```

Comments:
```javascript
{
    "course_id" : ObjectId,
    "comments" : [
        {
            "username" : str,
            "comment" : str,
            "rating" : str,
            "comment_id": ObjectId
        }
    ],
    "overall_rating": float
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
