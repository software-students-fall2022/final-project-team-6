# Overview

This is a course forum with Albert courses data, comments and rate my professor link

Admin can search add,delete courses to the mongoDB to maintain the course the correctness of the information

Users can search add,comment and view all the course information

# Subsystems
- a **admin** - a program that demonstrates the courses information from API and demonstrate on screen for admin to add and delete to maintain
- a **users** - an interface through which web visitors can see the course information and maintain the database
- a **database** - stores the data used by both other parts

# Running the Project
1. Navigate to the root folder of this project, then run:
   ```
   docker compose up
   ```

2. The admin client (if run by Docker) will run at `127.0.0.1:7001`. The users client will run at `127.0.0.1:6001`. A database container will also be created.

# API 

[Schedge](https://schedge.a1liu.com/)

Schedge is an API to NYU's course catalog. Please note that this API is currently under active development and is subject to change.

# Schema

User:

```javascript
{
    userSchema = new mongoose.Schema({
        username: {type: String, required: true},
        password: {type: String},
        courses:  [{ type: mongoose.Schema.Types.ObjectId, ref: 'course' }],
    });
}
```

Course:

```javascript
{
    courseSchema = new mongoose.Schema({
        name:{type: String},
        deptCourseId: {type: String},
        description: {type: String},
        subjectCode: {
            code: {type: String},
            school: {type: String}
        },
        rmpUrl:{type: String},
        registrationNumber: {type: Number},
        code: {type: String},
        instructors: [],
        type: {type: String},
        status: {type: String},
        time: {type: String},
        recitations: [],
        waitlistTotal: {type: Number},
        instructionMode: {type: String},
        campus: {type: String},
        minUnits: {type: Number},
        maxUnits: {type: Number},
        grading: {type: String},
        location: {type: String},
        notes: {type: String},
        prerequisites: {type: String},
        subject:{type: String},
        school:{type: String},
        ID:{type: String}
    });
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
