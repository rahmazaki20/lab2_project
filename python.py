
import re
from datetime import datetime


users = {}
projects = []


def val_phone(phone):
    """Validate Egyptian phone numbers."""
    return bool(re.match(r"^(010|011|012|015)\d{8}$", phone))

def val_email(email):
    """Validate email format."""
    return bool(re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email))

def val_date(date_str):
    """Validate date format (YYYY-MM-DD)."""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def register():
    """Handles user registration."""
    f_name = input("Enter your first name: ")
    l_name = input("Enter your last name: ")
    email = input("Enter your email: ")
    
  
    if email in users:
        print("This email is already registered.")
        return None
    
    if not val_email(email):
        print("Invalid email format.")
        return None
    
    password = input("Enter your password: ")
    confirm_password = input("Confirm your password: ")
    
    if password != confirm_password:
        print("Passwords do not match.")
        return None
    
    phone = input("Enter your phone number: ")
    if not val_phone(phone):
        print("Invalid phone number format.")
        return None
    

    users[email] = {
        'f_name': f_name,
        'l_name': l_name,
        'password': password,
        'phone': phone
    }
    
    print(f"{f_name} {l_name} registered successfully!")
    return email

def login():
    """Handles user login."""
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    if email in users and users[email]['password'] == password:
        print("Login successful!")
        return email
    else:
        print("Invalid email or password.")
        return None


def create_project(user_email):
    """Create a new project."""
    title = input("Enter project title: ")
    details = input("Enter project details: ")
    try:
        target = float(input("Enter target amount (EGP): "))
    except ValueError:
        print("Invalid target amount!")
        return None
    
    start_date = input("Enter start date (YYYY-MM-DD): ")
    if not val_date(start_date):
        print("Invalid date format.")
        return None
    
    end_date = input("Enter end date (YYYY-MM-DD): ")
    if not val_date(end_date):
        print("Invalid date format.")
        return None
    
    if datetime.strptime(start_date, '%Y-%m-%d') >= datetime.strptime(end_date, '%Y-%m-%d'):
        print("Start date must be before end date.")
        return None
    
 
    project = {
        'title': title,
        'details': details,
        'target': target,
        'start_date': start_date,
        'end_date': end_date,
        'owner_email': user_email
    }
    
    projects.append(project)
    print(f"Project '{title}' created successfully!")
    
def view_projects():
    """View all projects."""
    if not projects:
        print("No projects available.")
        return
    
    for idx, project in enumerate(projects):
        print(f"{idx + 1}. {project['title']} - Target: {project['target']} EGP - Start: {project['start_date']} - End: {project['end_date']}")

def edit_project(user_email):
    """Edit an existing project."""
    view_projects()
    
    project_id = int(input("Enter project number to edit: ")) - 1
    if project_id < 0 or project_id >= len(projects):
        print("Invalid project number.")
        return
    
    project = projects[project_id]
    if project['owner_email'] != user_email:
        print("You can only edit your own projects!")
        return
    
    title = input(f"Enter new title (Current: {project['title']}): ")
    details = input(f"Enter new details (Current: {project['details']}): ")
    
    try:
        target = float(input(f"Enter new target (Current: {project['target']}): "))
    except ValueError:
        print("Invalid target amount!")
        return
    
    start_date = input(f"Enter new start date (Current: {project['start_date']}): ")
    if not val_date(start_date):
        print("Invalid date format.")
        return
    
    end_date = input(f"Enter new end date (Current: {project['end_date']}): ")
    if not val_date(end_date):
        print("Invalid date format.")
        return
    
    if datetime.strptime(start_date, '%Y-%m-%d') >= datetime.strptime(end_date, '%Y-%m-%d'):
        print("Start date must be before end date.")
        return
    
    
    project['title'] = title
    project['details'] = details
    project['target'] = target
    project['start_date'] = start_date
    project['end_date'] = end_date
    
    print(f"Project '{title}' updated successfully!")

def delete_project(user_email):
    """Delete an existing project."""
    view_projects()
    
    project_id = int(input("Enter project number to delete: ")) - 1
    if project_id < 0 or project_id >= len(projects):
        print("Invalid project number.")
        return
    
    project = projects[project_id]
    if project['owner_email'] != user_email:
        print("You can only delete your own projects!")
        return
    
    projects.pop(project_id)
    print("Project deleted successfully!")




def main():
    current_user_email = None
    
    while True:
        if current_user_email is None:
            print("\n1. Register\n2. Login\n3. Exit")
            choice = input("Choose an option: ")

            if choice == '1':
                current_user_email = register()
            elif choice == '2':
                current_user_email = login()
            elif choice == '3':
                break
            else:
                print("Invalid choice!")
        else:
            print(f"\nWelcome, {users[current_user_email]['f_name']}!")
            print("\n1. Create Project\n2. View Projects\n3. Edit Project\n4. Delete Project\n5. Search Projects\n6. Logout")
            choice = input("Choose an option: ")

            if choice == '1':
                create_project(current_user_email)
            elif choice == '2':
                view_projects()
            elif choice == '3':
                edit_project(current_user_email)
            elif choice == '4':
                delete_project(current_user_email)
            elif choice == '6':
                current_user_email = None  # Log out
                print("Logged out successfully!")
            else:
                print("Invalid choice!")

# Run the app
if __name__ == "__main__":
    main()
