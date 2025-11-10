This is a python application that provides the actions of create, read, update and delete.

Overview
This project is used to create a student management system using sql to store data on the back end, it has a menu (coded in python) to apply the commands of create, read, update and delete.
It has also come with a few entries to start with that the professor provided in the assignment page.

Prerequistes 
1. PostgreSQL must be set up and password made by user upon installation is needed to run program.
2. Python must be installed for the menu section and main function to operate correctly
3. Install needed packages by entering this line into command prompt:
4. pip install psycopg2-binary
   
How to run
Open pgAdmin and create a database and name it students_db. 
Run the schema.sqlfile and open it. 
Excute and ensure all entries are as they should be.

Navigate to the correct directory where you have the files saved.
Run the student_managemment.py files using the following command in terminal:
  python student_management.py

It will ask you for details to connect to the database enter the next lines in order of how the prompts show up.
Database name: students_db
Username: postgres
Password: (enter your own password you created when you installed PostgreSQL)
Host: localhost
Port: 5432

NOTE!!! 
All of the commands are esstienally the default settings that will be printed with each entries prompt.

After all this the program should finally run and read the menu and follow the instructions printed out for what needs to be provided for each function.

1. Displays all students and all other connected info and formats them by id
2. Allows for inserting new students into the database.
3. Replaces a current students email. (must be a unique email)
4. Deletes a students entry based on student id.
5. Simply exits the program.

FILE DESCRIPTIONS
schema.sql
  Creates students table and inserts initial data
requirements.txt 
  Package dependencies that need to be installed
student_management.py
  Contains all database operations and used for making the menu.

Demo Video : https://youtu.be/DoV-MprzGDE 
