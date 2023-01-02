# cscb20
Course website redesign developed as a project for the CSCB20 course. Complete with user reigistration, authentication, and authorization for different pages depending on user type. Deployed to Heroku at: https://cscb20-araikatdim.herokuapp.com/

## Note: 
The website is temporarily down since Heroku removed their free tier hosting. 

# Table of contents
   * [Website Overview](#website-overview)
      * [Instructor Specific Pages and Functionality](#instructor-specific-pages-and-functionality)
      * [Student Specific Pages and Functionality](#student-specific-pages-and-functionality)
   * [Database Diagram](#database-diagram)

# Website Overview
Users are greeted with the following page when first opening the website:

![image](https://user-images.githubusercontent.com/87666671/210258927-3b467503-6aa3-4579-88ff-e7c2aca86f74.png)

Users can log in as either an instructor or student. Account types are determined during sign up, and determine authorization for different pages. Utorids are used as primary keys in an SQLite Database, and passwords are hashed using Bcrypt before being stored. For accounts with example data, use instructor1 and student1 (passwords are the same as utorids).

![image](https://user-images.githubusercontent.com/87666671/210259147-f0f13433-03a7-4320-bfd1-b43cdd1a000a.png)

Once users are authenticated, a Flask session is created and users are authorized to view a number of pages based on account type. Shared pages between instructors and students include static course information and content.

![image](https://user-images.githubusercontent.com/87666671/210260254-224ff3c8-7998-4c14-8951-51c8f3f2dfe2.png)

## Instructor Specific Pages and Functionality
Instructors are able to view feedback submitted specifically to them by the students in the course. Feedback is fetched through a GET request, and the SQLite DB is queried using server-side session info about the current user.

![image](https://user-images.githubusercontent.com/87666671/210260960-36ecc8a0-4b03-4c35-8cf0-8403edd38e22.png)

Instructors are also able to view and edit all student marks.

![image](https://user-images.githubusercontent.com/87666671/210261272-1df2c8ab-e135-49a2-b0ea-58e68de15a53.png)

Likewise they can act on remark requests from students. Requests are automatically marked as closed once the grade has been updated, or the same grade is resubmitted. 

![image](https://user-images.githubusercontent.com/87666671/210261348-93248515-12ef-40d3-b131-c920060dff8c.png)

Or submit new marks.

![image](https://user-images.githubusercontent.com/87666671/210261540-ed4e3f97-00c5-451c-be09-25505ead614b.png)

## Student Specific Pages and Functionality

Students are able to fill out a feedback form for any of the instructors that exist in the DB.  

![image](https://user-images.githubusercontent.com/87666671/210261725-8c0f70a6-0e40-4ae8-a765-304ea99f52c2.png)

They can also view their own marks and send remark requests. If remark requests are closed by an instructor, then any new remark request for the same course component would overwrite the old request.

![image](https://user-images.githubusercontent.com/87666671/210262006-6f37524c-b7a4-4fc0-b15d-43e26d05cd31.png)

And view the status of their requests.

![image](https://user-images.githubusercontent.com/87666671/210262100-d016fc62-b93f-450d-bf5d-f1ad13442e26.png)

# Database Diagram
![image](https://user-images.githubusercontent.com/87666671/210264642-5d3fd643-94ac-437d-8664-3aefee09ce10.png)


