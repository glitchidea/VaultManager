# VaultManager

VaultManager is a powerful and user-friendly console-based password management tool that helps you securely store, manage, and organize your sensitive information. With its user-friendly interface, users can easily add, edit, and delete entries in KeePass databases, ensuring that passwords and personal data are well protected.

## Features

- **Manage Passwords**: Effortlessly add, edit, or delete passwords and notes.
- **Secure Storage**: Store your passwords securely in a KeePass database.
- **Data Import/Export**: Easily import or export your entries in CSV or JSON formats.
- **Password Generation**: Generate strong, random passwords based on your requirements.
- **Password Recovery**: Attempt to recover lost database passwords using a variety of methods.
- **User-Friendly Interface**: Navigate easily through the application with a clean and simple design.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/glitchidea/VaultManager.git
   cd VaultManager
   ```

2. **Install dependencies**:
   Ensure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python VaultManager.py
   ```

## Usage

### Main Menu
- **List Entries**: View all stored entries.
- **Create New KDBX Database**: Set up a new KeePass database to store your passwords.
- **Change Existing Database Password**: Modify the password of your existing KeePass database.
- **Password Cracking**: Attempt to recover a forgotten password using various techniques.
- **Settings**: Configure database paths for easier access.

### Entry Management
- **Adding Entries**: Easily add new entries with title, username, password, URL, and notes.
- **Editing Entries**: Modify existing entries while preserving other details.
- **Deleting Entries**: Remove unwanted entries from your database.
- **Show Password**: Safely view the password for a specific entry.

### Password Generation
- Customize the generated password using options for upper/lowercase letters, digits, and special characters.
- Specify the desired length for the password.

### Import/Export
- Import existing data from a KDBX file.
- Export your entries to CSV or JSON formats for backup or sharing.
