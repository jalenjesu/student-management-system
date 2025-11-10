# Author: Jalen Jesudasan
# Date: November 9 2025


import psycopg2
from psycopg2 import Error
from datetime import datetime
import sys


class StudentDatabase:
  

    def __init__(self, dbname="students_db", user="postgres", password="password", 
                 host="localhost", port="5432"):
        # Set database arugements
        # dbname is the database name
        # User is the database user 
        # Password is for database password
        # Host and port are for the database port and host respectivly 
        
       
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
        self.cursor = None

    def connect(self):
        # Connects to the Database and returns true if connected
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.connection.cursor()
            print("✓ Successfully connected to PostgreSQL database")
            return True
        except Error as e:
            print(f"✗ Error connecting to PostgreSQL database: {e}")
            return False

    def disconnect(self):
        # Closing database
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("✓ Database connection closed")

    def getAllStudents(self):
        # Displays all entries from student table using select query and then displays them 
        try:
            # Use SELECT query to retrieve all records
            query = "SELECT * FROM students ORDER BY student_id;"
            self.cursor.execute(query)
            
            # Fetch all results
            students = self.cursor.fetchall()
            
            # Display results
            if students:
                print("\n" + "="*90)
                print("ALL STUDENTS")
                print("="*90)
                print(f"{'ID':<5} {'First Name':<15} {'Last Name':<15} {'Email':<30} {'Enrollment Date':<15}")
                print("-"*90)
                
                for student in students:
                    student_id, first_name, last_name, email, enrollment_date = student
                    print(f"{student_id:<5} {first_name:<15} {last_name:<15} {email:<30} {enrollment_date}")
                
                print("-"*90)
                print(f"Total Students: {len(students)}")
                print("="*90 + "\n")
            else:
                print("\n⚠ No students found in the database.\n")
                
        except Error as e:
            print(f"\n✗ Error retrieving students: {e}\n")

    def addStudent(self, first_name, last_name, email, enrollment_date):
        # puts new student into table using same arguements as before
        try:
            # Making sure email is unique and returns false if it already exists
            check_query = "SELECT COUNT(*) FROM students WHERE email = %s;"
            self.cursor.execute(check_query, (email,))
            if self.cursor.fetchone()[0] > 0:
                print(f"\n✗ Error: Email '{email}' already exists in the database.\n")
                return False
            
            # Insert new student record
            insert_query = """
                INSERT INTO students (first_name, last_name, email, enrollment_date)
                VALUES (%s, %s, %s, %s)
                RETURNING student_id;
            """
            self.cursor.execute(insert_query, (first_name, last_name, email, enrollment_date))
            
            # Geting id of new student
            new_student_id = self.cursor.fetchone()[0]
            
            # Finalizing addition
            self.connection.commit()
            
            print(f"\n✓ Successfully added student: {first_name} {last_name}")
            print(f"  Student ID: {new_student_id}")
            print(f"  Email: {email}")
            print(f"  Enrollment Date: {enrollment_date}\n")
            
            return True
            
        except Error as e:
            self.connection.rollback()
            print(f"\n✗ Error adding student: {e}\n")
            return False

    def updateStudentEmail(self, student_id, new_email):
        # Takes student ID and new email in order to replace old email.
        try:
            # Check if student exists
            check_query = "SELECT first_name, last_name, email FROM students WHERE student_id = %s;"
            self.cursor.execute(check_query, (student_id,))
            student = self.cursor.fetchone()
            
            if not student:
                print(f"\n✗ Error: No student found with ID {student_id}\n")
                return False
            
            old_first_name, old_last_name, old_email = student
            
            # Check if new email already exists for a different student
            email_check_query = "SELECT COUNT(*) FROM students WHERE email = %s AND student_id != %s;"
            self.cursor.execute(email_check_query, (new_email, student_id))
            if self.cursor.fetchone()[0] > 0:
                print(f"\n✗ Error: Email '{new_email}' is already used by another student.\n")
                return False
            
            # Update email
            update_query = "UPDATE students SET email = %s WHERE student_id = %s;"
            self.cursor.execute(update_query, (new_email, student_id))
            
            # Finalize email update
            self.connection.commit()
            
            print(f"\n✓ Successfully updated email for student: {old_first_name} {old_last_name}")
            print(f"  Student ID: {student_id}")
            print(f"  Old Email: {old_email}")
            print(f"  New Email: {new_email}\n")
            
            return True
            
        except Error as e:
            self.connection.rollback()
            print(f"\n✗ Error updating student email: {e}\n")
            return False

    def deleteStudent(self, student_id):
        # Deletes record of student with unique id returns true if the entry was removed otherwise returns false
        try:
            # Check if student exists and get their info
            check_query = "SELECT first_name, last_name, email FROM students WHERE student_id = %s;"
            self.cursor.execute(check_query, (student_id,))
            student = self.cursor.fetchone()
            
            if not student:
                print(f"\n✗ Error: No student found with ID {student_id}\n")
                return False
            
            first_name, last_name, email = student
            
            # Delete student record
            delete_query = "DELETE FROM students WHERE student_id = %s;"
            self.cursor.execute(delete_query, (student_id,))
            
            # Finalize deletion
            self.connection.commit()
            
            print(f"\n✓ Successfully deleted student: {first_name} {last_name}")
            print(f"  Student ID: {student_id}")
            print(f"  Email: {email}\n")
            
            return True
            
        except Error as e:
            self.connection.rollback()
            print(f"\n✗ Error deleting student: {e}\n")
            return False


def display_menu():
   # Displays menu options
    print("\n" + "="*50)
    print("STUDENT MANAGEMENT SYSTEM")
    print("="*50)
    print("1. View All Students")
    print("2. Add New Student")
    print("3. Update Student Email")
    print("4. Delete Student")
    print("5. Exit")
    print("="*50)


def main():
    # Main function to run the app and runs interactive menu
    print("\n" + "="*50)
    print("WELCOME TO STUDENT MANAGEMENT SYSTEM")
    print("="*50)
    
    # Get database entry parameters
    print("\nEnter database connection details:")
    dbname = input("Database name (default: students_db): ").strip() or "students_db"
    user = input("Username (default: postgres): ").strip() or "postgres"
    password = input("Password: ").strip() or "password"
    host = input("Host (default: localhost): ").strip() or "localhost"
    port = input("Port (default: 5432): ").strip() or "5432"
    
    # Connect to database
    db = StudentDatabase(dbname=dbname, user=user, password=password, host=host, port=port)
    
    if not db.connect():
        print("\n✗ Failed to connect to database. Exiting...")
        return
    
    # Main application loop
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            # View all students
            db.getAllStudents()
            input("Press Enter to continue...")
            
        elif choice == "2":
            # Add new student
            print("\n" + "-"*50)
            print("ADD NEW STUDENT")
            print("-"*50)
            first_name = input("First Name: ").strip()
            last_name = input("Last Name: ").strip()
            email = input("Email: ").strip()
            enrollment_date = input("Enrollment Date (YYYY-MM-DD): ").strip()
            
            if first_name and last_name and email and enrollment_date:
                db.addStudent(first_name, last_name, email, enrollment_date)
            else:
                print("\n✗ All fields are required!\n")
            
            input("Press Enter to continue...")
            
        elif choice == "3":
            # Update student email
            print("\n" + "-"*50)
            print("UPDATE STUDENT EMAIL")
            print("-"*50)
            try:
                student_id = int(input("Student ID: ").strip())
                new_email = input("New Email: ").strip()
                
                if new_email:
                    db.updateStudentEmail(student_id, new_email)
                else:
                    print("\n✗ Email cannot be empty!\n")
            except ValueError:
                print("\n✗ Invalid Student ID!\n")
            
            input("Press Enter to continue...")
            
        elif choice == "4":
            # Delete student
            print("\n" + "-"*50)
            print("DELETE STUDENT")
            print("-"*50)
            try:
                student_id = int(input("Student ID: ").strip())
                
                # Confirmation
                confirm = input(f"Are you sure you want to delete student with ID {student_id}? (yes/no): ").strip().lower()
                if confirm == "yes":
                    db.deleteStudent(student_id)
                else:
                    print("\n✗ Deletion cancelled.\n")
            except ValueError:
                print("\n✗ Invalid Student ID!\n")
            
            input("Press Enter to continue...")
            
        elif choice == "5":
            # Exit
            print("\nThank you for using Student Management System!")
            db.disconnect()
            break
            
        else:
            print("\n✗ Invalid choice! Please select 1-5.\n")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()