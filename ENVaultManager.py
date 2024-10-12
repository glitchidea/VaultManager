import os
import getpass  
import platform
import sys
import json
import random
import string
import itertools
import pandas as pd
import concurrent.futures
import multiprocessing
from pykeepass import PyKeePass, create_database

# Reader
def clear_screen():
    """Clears the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def list_entries(kp):
    """Lists the entries in the database"""
    entries = kp.entries
    data = {
        'No': [i + 1 for i in range(len(entries))],
        'Title': [entry.title for entry in entries],
        'Username': [entry.username if entry.username else '-' for entry in entries],
        'Password': [entry.password[:2] + '*' * (len(entry.password) - 2) if entry.password else '-' for entry in entries],
        'URL': [entry.url if entry.url else '-' for entry in entries],
        'Notes': [entry.notes if entry.notes else '-' for entry in entries]
    }
    df = pd.DataFrame(data)
    clear_screen()
    print(df)

def add_entry(kp):
    """Adds a new entry"""
    clear_screen()
    new_title = input("New entry title: ")
    new_username = input("New username: ")
    new_password = getpass.getpass("New password: ")
    new_url = input("New URL: ")
    new_notes = input("New notes: ")

    default_group = kp.find_groups(name='Root')[0]
    kp.add_entry(default_group, title=new_title, username=new_username, password=new_password, url=new_url, notes=new_notes)
    kp.save()  # Save changes
    clear_screen()
    print(f"A new entry with the title '{new_title}' has been successfully added.")

def edit_entry(kp):
    """Edits an entry"""
    entries = kp.entries
    list_entries(kp)
    try:
        entry_num = int(input("\nEnter the number of the entry you want to edit (press q to exit): "))
        if entry_num <= 0 or entry_num > len(entries):
            raise ValueError("Invalid entry number!")
        
        entry = entries[entry_num - 1]
        clear_screen()
        print("Selected Entry Information:")
        print(f"Title: {entry.title}")
        print(f"Username: {entry.username if entry.username else '-'}")
        print(f"Password: {entry.password if entry.password else '-'}")
        print(f"URL: {entry.url if entry.url else '-'}")
        print(f"Notes: {entry.notes if entry.notes else '-'}")
        print("\nEnter the information you want to edit (leave fields unchanged if you don't want to change them):")

        new_title = input(f"New title ({entry.title}): ")
        new_username = input(f"New username ({entry.username if entry.username else '-'}): ")
        new_password = getpass(prompt=f"New password ({entry.password if entry.password else '-'}): ")
        new_url = input(f"New URL ({entry.url if entry.url else '-'}): ")
        new_notes = input(f"New notes ({entry.notes if entry.notes else '-'}): ")

        if new_title:
            entry.title = new_title
        if new_username:
            entry.username = new_username
        if new_password:
            entry.password = new_password
        if new_url:
            entry.url = new_url
        if new_notes:
            entry.notes = new_notes

        kp.save()  # Save changes
        clear_screen()
        print(f"Entry has been successfully updated.")
        input("Press ENTER to return to the main menu.")

    except ValueError as ve:
        clear_screen()
        print(f"Error: {ve}")
        input("Press ENTER to continue.")

def delete_entry(kp):
    """Deletes an entry"""
    entries = kp.entries
    list_entries(kp)
    try:
        entry_num = int(input("\nEnter the number of the entry you want to delete (press q to exit): "))
        if entry_num <= 0 or entry_num > len(entries):
            raise ValueError("Invalid entry number!")
        
        entry = entries[entry_num - 1]
        kp.delete_entry(entry)
        kp.save()  # Save changes
        clear_screen()
        print(f"The entry has been successfully deleted.")
        input("Press ENTER to return to the main menu.")

    except ValueError as ve:
        clear_screen()
        print(f"Error: {ve}")
        input("Press ENTER to continue.")

def import_data(kp):
    """Imports data"""
    clear_screen()
    try:
        file_path = input("Enter the path of the KDBX file you want to import: ")
        new_kp = PyKeePass(file_path)

        # Copy all entries from the current database to the new database
        for entry in kp.entries:
            default_group = new_kp.find_groups(name='Root')[0]
            new_kp.add_entry(default_group, title=entry.title, username=entry.username, password=entry.password, url=entry.url, notes=entry.notes)

        new_kp.save()  # Save the new database
        clear_screen()
        print("Data has been successfully imported.")
        input("Press ENTER to return to the main menu.")

    except Exception as e:
        clear_screen()
        print(f"Error: {e}")
        input("Press ENTER to continue.")

def export_data(kp):
    """Exports data"""
    clear_screen()
    try:
        export_format = input("Select the format to export the data (type 'csv' for CSV, 'json' for JSON): ").strip().lower()

        if export_format not in ['csv', 'c', 'C', 'json', 'j', 'J']:
            raise ValueError("Invalid format selection! Please enter 'csv' or 'json'.")

        file_path = input("Enter the path for the file to be exported (if left blank, default filename will be used): ")
        
        if not file_path.strip():
            file_path = 'exported_data.' + export_format  # Default filename
        
        if export_format in ['csv', 'c', 'C']:
            df = pd.DataFrame({
                'Title': [entry.title for entry in kp.entries],
                'Username': [entry.username if entry.username else '-' for entry in kp.entries],
                'Password': [entry.password for entry in kp.entries],
                'URL': [entry.url if entry.url else '-' for entry in kp.entries],
                'Notes': [entry.notes if entry.notes else '-' for entry in kp.entries]
            })
            df.to_csv(file_path, index=False)
        
        elif export_format in ['json', 'j', 'J']:
            data = [{
                'Title': entry.title,
                'Username': entry.username if entry.username else '-',
                'Password': entry.password,
                'URL': entry.url if entry.url else '-',
                'Notes': entry.notes if entry.notes else '-'
            } for entry in kp.entries]
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

        clear_screen()
        print(f"Data has been successfully exported to '{file_path}'.")
        input("Press ENTER to return to the main menu.")

    except Exception as e:
        clear_screen()
        print(f"Error: {e}")
        input("Press ENTER to continue.")

def generate_password():
    """Generates a random password"""
    clear_screen()
    try:
        use_upper = input("Should uppercase letters be used? (Press 'y' for Yes, any other key for No): ").lower() == 'y'
        use_lower = input("Should lowercase letters be used? (Press 'y' for Yes, any other key for No): ").lower() == 'y'
        use_digits = input("Should digits be used? (Press 'y' for Yes, any other key for No): ").lower() == 'y'
        use_punctuation = input("Should punctuation be used? (Press 'y' for Yes, any other key for No): ").lower() == 'y'
        
        length = int(input("Enter the desired password length: "))

        if not (use_upper or use_lower or use_digits or use_punctuation):
            raise ValueError("At least one character type must be selected!")

        characters = ''
        if use_upper:
            characters += string.ascii_uppercase
        if use_lower:
            characters += string.ascii_lowercase
        if use_digits:
            characters += string.digits
        if use_punctuation:
            characters += string.punctuation

        password = ''.join(random.choice(characters) for _ in range(length))
        clear_screen()
        print(f"Generated password: {password}")
        input("Press ENTER to return to the main menu.")

    except ValueError as ve:
        clear_screen()
        print(f"Error: {ve}")
        input("Press ENTER to continue.")

def show_password(kp):
    """Displays the password of an entry"""
    entries = kp.entries
    list_entries(kp)
    try:
        entry_num = int(input("\nEnter the number of the entry whose password you want to see (press q to exit): "))
        if entry_num <= 0 or entry_num > len(entries):
            raise ValueError("Invalid entry number!")
        
        entry = entries[entry_num - 1]
        clear_screen()
        print(f"Title: {entry.title}")
        print(f"Username: {entry.username if entry.username else '-'}")
        print(f"Password: {entry.password if entry.password else '-'}")
        print(f"URL: {entry.url if entry.url else '-'}")
        print(f"Notes: {entry.notes if entry.notes else '-'}")
        input("\nPress ENTER to return to the main menu.")

    except ValueError as ve:
        clear_screen()
        print(f"Error: {ve}")
        input("Press ENTER to continue.")

# Solvent
def open_kdbx(filepath, password):
    try:
        kp = PyKeePass(filepath, password=password)
        return kp
    except Exception:
        return None

def generate_passwords(charset, min_length, max_length):
    for length in range(min_length, max_length + 1):
        for password in itertools.product(charset, repeat=length):
            yield ''.join(password)

def try_password(filepath, password):
    kp = open_kdbx(filepath, password)
    if kp:
        print(f"\nPassword found: {password}")
        return password
    return None

def try_passwords(filepath, passwords):
    found_password = None
    total_passwords = len(passwords)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        future_to_password = {executor.submit(try_password, filepath, password): password for password in passwords}
        
        for i, future in enumerate(concurrent.futures.as_completed(future_to_password)):
            password = future_to_password[future]
            sys.stdout.write(f"\rTrying ({i+1}/{total_passwords}): {password}")
            sys.stdout.flush()
            
            try:
                result = future.result()
                if result:
                    found_password = result
                    break
            except Exception as exc:
                continue

    if found_password:
        print(f"\nPassword found: {found_password}")
        return True
    else:
        print("\nPassword not found.")
        return False

# Converter

def create_new_database():
    db_name = input("Enter the full path for the new KDBX file (e.g., C:\\Users\\mydatabase.kdbx): ")
    password = getpass.getpass("Enter the database password: ")
    confirm_password = getpass.getpass("Re-enter the database password: ")

    if password != confirm_password:
        print("Passwords do not match. Please try again.")
        return

    try:
        kp = create_database(db_name, password)
        kp.save()
        print(f"New database '{db_name}' has been successfully created.")
    except Exception as e:
        print(f"An error occurred while creating the database: {e}")

def change_existing_password():
    db_path, _, _ = load_settings()  # Load settings
    if not db_path:
        print("Database path not set. Please configure settings first.")
        return

    old_password = getpass.getpass("Enter the current database password: ")
    try:
        kp = PyKeePass(db_path, password=old_password)
    except Exception as e:
        print(f"An error occurred while opening the file: {e}")
        return

    new_password = getpass.getpass("Enter the new database password: ")
    confirm_password = getpass.getpass("Re-enter the new database password: ")

    if new_password != confirm_password:
        print("New passwords do not match. Please try again.")
        return

    kp.password = new_password
    kp.save()
    print(f"The password for the database '{db_path}' has been successfully changed.")

# Settings
def load_settings():
    """Loads the settings file and returns current settings."""
    try:
        with open("settings.json", "r") as file:
            settings = json.load(file)
            return settings.get("db_path", None), settings.get("csv_path", None), settings.get("json_path", None)
    except FileNotFoundError:
        return None, None, None  # Default values if file not found
    except json.JSONDecodeError:
        return None, None, None  # JSON error

def save_settings(db_path, csv_path, json_path):
    """Saves the settings to the specified file."""
    settings = {
        "db_path": db_path,
        "csv_path": csv_path,
        "json_path": json_path
    }
    with open("settings.json", "w") as file:
        json.dump(settings, file, indent=4)

def settings_menu():
    """Displays the settings menu and updates file path settings."""
    while True:
        clear_screen()
        print("Settings Menu")
        
        # Load current settings
        db_path, csv_path, json_path = load_settings()
        
        # Show current paths
        print(f"Current Database File Path: {db_path if db_path else 'Not specified'}")
        print(f"Current CSV File Path: {csv_path if csv_path else 'Not specified'}")
        print(f"Current JSON File Path: {json_path if json_path else 'Not specified'}")
        
        print("\nKDBX Path")
        print("\n1 - Set database file path")
        print("\nExport")
        print("\n2 - Set CSV file path")
        print("3 - Set JSON file path")
        print("4 - Show current settings")
        print("q - Exit")

        choice = input("Select an option: ")

        if choice == "1":
            new_db_path = input("Enter the new database file path: ")
            csv_path, json_path = load_settings()[1:3]  # Get current CSV and JSON paths
            save_settings(new_db_path, csv_path, json_path)
            print(f"New database file path saved as '{new_db_path}'.")
            input("Press ENTER to continue...")
        elif choice == "2":
            new_csv_path = input("Enter the new CSV file path: ")
            db_path, json_path = load_settings()[0], load_settings()[2]  # Get current DB and JSON paths
            save_settings(db_path, new_csv_path, json_path)
            print(f"New CSV file path saved as '{new_csv_path}'.")
            input("Press ENTER to continue...")
        elif choice == "3":
            new_json_path = input("Enter the new JSON file path: ")
            db_path, csv_path = load_settings()[0:2]  # Get current DB and CSV paths
            save_settings(db_path, csv_path, new_json_path)
            print(f"New JSON file path saved as '{new_json_path}'.")
            input("Press ENTER to continue...")
        elif choice == "4":
            db_path, csv_path, json_path = load_settings()
            print(f"Current database file path: {db_path if db_path else 'Not specified'}")
            print(f"Current CSV file path: {csv_path if csv_path else 'Not specified'}")
            print(f"Current JSON file path: {json_path if json_path else 'Not specified'}")
            input("Press ENTER to continue...")
        elif choice.lower() == "q":
            break
        else:
            print("Invalid option, please try again.")
            input("Press ENTER to continue...")

# Menu
def main():
    while True:
        clear_screen()
        print("1 - List")
        print("2 - Create new KDBX file")
        print("3 - Change the password of the existing KDBX file")
        print("4 - Password cracking")
        print("5 - Settings")
        print("q - Exit")

        choice = input("Select an option: ")

        if choice == "1":
            # Reader function
            try:
                db_path, _, _ = load_settings()  # Load settings
                user_db_path = input("Enter the path of the KeePass database file (Default): ")

                if not user_db_path:  # If user left it blank, use settings
                    user_db_path = db_path
                    if not user_db_path:
                        raise ValueError("Database path not defined in the settings file.")

                password = getpass.getpass(prompt='Enter KeePass database password: ')
                kp = PyKeePass(user_db_path, password=password)

                while True:
                    clear_screen()
                    print("1- List")
                    print("2- Add")
                    print("3- Edit")
                    print("4- Delete")
                    print("5- Generate Password")
                    print("6- Show Password")
                    print("q- Exit")

                    choice = input("\nSelect an operation: ").strip().lower()

                    if choice == '1':
                        list_entries(kp)
                        input("\nPress ENTER to continue...")
                    elif choice == '2':
                        add_entry(kp)
                    elif choice == '3':
                        edit_entry(kp)
                    elif choice == '4':
                        delete_entry(kp)
                    elif choice == '5':
                        generate_password()
                    elif choice == '6':
                        show_password(kp)
                    elif choice == 'q':
                        clear_screen()
                        print("Operation completed. Exiting the program...")
                        break
                    else:
                        clear_screen()
                        print("Invalid option! Please try again.")
                        input("\nPress ENTER to continue...")
            except Exception as e:
                clear_screen()
                print(f"An error occurred: {str(e)}")
                input("\nPress ENTER to continue...")

        elif choice == "2":
            clear_screen()
            create_new_database()
        elif choice == "3":
            clear_screen()
            change_existing_password()
        elif choice == "4":
            clear_screen()
            filepath = input("Please enter the location of the KDBX file: ")
            use_password_file = input("Do you have a password file? (Y/N): ").strip().lower() == 'y'
            if use_password_file:
                password_file = input("Please enter the location of the password file: ")
                
                if not os.path.isfile(password_file):
                    print("Password file not found.")
                    continue
                
                with open(password_file, 'r') as f:
                    passwords = f.read().splitlines()
                
                if input(f"{len(passwords)} passwords will be tried. Do you want to try? (Y/N): ").strip().lower() == 'y':
                    if try_passwords(filepath, passwords):
                        print("Password correct!")
                        continue
                    else:
                        print("\nCould not open the file with the passwords in the password file.")
            
            create_password_file = input("Do you want to create your own password file? (Y/N): ").strip().lower() == 'y'
            if create_password_file:
                charset = ""
                if input("Should uppercase letters be used? (Y/N): ").strip().lower() == 'y':
                    charset += string.ascii_uppercase
                if input("Should lowercase letters be used? (Y/N): ").strip().lower() == 'y':
                    charset += string.ascii_lowercase
                if input("Should digits be used? (Y/N): ").strip().lower() == 'y':
                    charset += string.digits
                if input("Should ASCII characters be used? (Y/N): ").strip().lower() == 'y':
                    charset += string.punctuation
                
                if not charset:
                    print("No character set was selected.")
                    continue
                
                min_length = int(input("Minimum password length: "))
                max_length = int(input("Maximum password length: "))
                
                generated_password_file = "generated_passwords.txt"
                with open(generated_password_file, 'w') as f:
                    for password in generate_passwords(charset, min_length, max_length):
                        f.write(password + '\n')
                print(f"Password file created: {generated_password_file}")
                
                with open(generated_password_file, 'r') as f:
                    passwords = f.read().splitlines()
                
                print(f"The generated file contains {len(passwords)} passwords.")
                if input(f"Do you want to try the passwords in the generated file? (Y/N): ").strip().lower() == 'y':
                    if try_passwords(filepath, passwords):
                        print("Password correct!")
                        continue
                    else:
                        print("\nCould not open the file with the passwords in the generated password file.")

        elif choice == "5":
            clear_screen()
            settings_menu() 
        elif choice.lower() == "q":
            break
        else:
            print("Invalid option, please try again.")

        input("\nPress Enter to return to the main menu...")
if __name__ == "__main__":
    main()
