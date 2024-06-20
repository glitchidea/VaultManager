## VaultManager Solvent
### Features:

1. **Opening KDBX Files**:
   - Attempts to open the specified KDBX file with the password provided by the user.
   - File access is facilitated using the PyKeePass library.

2. **Parallel Password Testing**:
   - Executes password testing operations in parallel.
   - Increases processing speed by testing multiple passwords simultaneously.
   - Parallel testing is achieved using threading with the `concurrent.futures` and `multiprocessing` modules.

3. **Password Generation and Testing**:
   - Provides the option for users to create a password file.
   - Generates random passwords using specified character sets and length ranges.
   - Tests generated passwords to open the KDBX file.

### Usage:

1. **Opening KDBX Files**:
   - When the application starts, the user is prompted to enter the path to the KDBX file and its password.
   - If access to the file is successful, its contents are displayed or the correctness of the password is verified.

2. **Using an Existing Password File**:
   - Users can enter the path to an existing password file.
   - Passwords from this file can be tested in parallel, and the process can be terminated upon finding the correct password.

3. **Creating Your Own Password File**:
   - Optionally allows users to create a new password file.
   - Users can select specific character sets such as uppercase letters, lowercase letters, digits, and special characters.
   - Users can define minimum and maximum password lengths, and passwords can be automatically generated.
   - Generated passwords can be tested to open the KDBX file.

The application is designed to enhance the security of KeePass KDBX database files and facilitate password management through a user-friendly interface.

## VaultManager Converter

### Features:

1. **Creating a New KDBX File**:
   - Prompts the user to enter the full path to the file and its password to create a new KDBX database.
   - Uses the `create_database` function to create the database, which is then saved to the specified location.

2. **Changing the Password of an Existing KDBX File**:
   - Prompts the user to enter the path to the existing KDBX file and its current password.
   - Upon successfully opening the file, allows the user to set a new password.
   - After confirming the new password, changes are made to the file's password and saved.

3. **Additional Features**:
   - Uses the `clear_screen` function to clear the terminal screen.
   - Safely handles password inputs using the `getpass` module.
   - Provides appropriate feedback to the user in case of entering an invalid option in the main menu.

### Usage:

1. **Creating a New KDBX File**:
   - When the application starts, it presents a main menu to the user.
   - The user selects the option to create a new KDBX file by pressing "1".
   - They are prompted for the file path and password, and after verification, a new KDBX file is created.

2. **Changing the Password of an Existing KDBX File**:
   - The user selects the option to change the password of an existing KDBX file by pressing "2".
   - After entering the file path and current password, they define a new password.
   - Once the new password is confirmed, the file's password is changed and the changes are saved.

3. **Exiting**:
   - Users can exit the application by pressing "q".

## VaultManager Reader
### Features:

1. **Listing (`list_entries` function)**:
   - Lists entries from the database, displaying information such as title, username, password, URL, and notes in a tabular format.
   - Data is converted to a DataFrame using the Pandas library and printed to the terminal.

2. **Adding Entries (`add_entry` function)**:
   - Adds a new entry to the database by collecting information such as title, username, password, URL, and notes from the user.
   - Uses the `kp.add_entry` method to add a new entry under the specified group and saves changes using `kp.save()`.

3. **Editing Entries (`edit_entry` function)**:
   - Edits information of an existing entry.
   - Prompts the user to enter the information to be changed and saves changes using `kp.save()`.

4. **Deleting Entries (`delete_entry` function)**:
   - Deletes an entry from the database by prompting the user for the entry number to be deleted.
   - Uses the `kp.delete_entry` method to delete the entry and saves changes using `kp.save()`.

5. **Password Generation (`generate_password` function)**:
   - Allows users to generate a random password using uppercase letters, lowercase letters, digits, and punctuation marks.
   - Generates a password by selecting random characters from the specified character set using the `random.choice` function.

6. **Showing Passwords (`show_password` function)**:
   - Displays all information of a specified entry, especially the password.

7. **Main Menu Management (`main` function)**:
   - Displays the main menu to the user and calls relevant functions based on the selected operation.
   - Clears the screen using the `clear_screen` function and provides appropriate feedback to the user.

### Usage:

- When the program starts, the user is prompted for the path and password of the KeePass database file.
- Based on the selected operation number (`1`-`6`) from the main menu, the corresponding operation is performed, or the user can exit the program by entering `q`.
- After each operation, appropriate feedback is provided to the user, and the operation is completed.
- In case of errors, appropriate error messages are shown to the user, prompting them to press ENTER to continue.

