import requests
import os
import shutil
import time
import json
import sys
import urllib.request
from tqdm import tqdm

MODS_DIRECTORY = "path/to/mods/directory"
CONFIG_FILE = "config.json"
BACKUP_DIRECTORY = "path/to/backup/directory"

# Function to search for mods
def search_mods(query):
    url = f"https://mod-database.example.com/api/search?query={query}"
    response = requests.get(url)
    mods = response.json()

    for mod in mods:
        print(f"Mod ID: {mod['id']}")
        print(f"Mod Name: {mod['name']}")
        print(f"Author: {mod['author']}")
        print(f"Description: {mod['description']}")
        print("------------------------")

# Function to install a mod
def install_mod(mod_id):
    url = f"https://mod-database.example.com/api/mods/{mod_id}"
    response = requests.get(url)
    mod_details = response.json()

    mod_url = mod_details['download_url']
    mod_file = os.path.basename(mod_url)
    download_file(mod_url, mod_file)

    mod_destination = os.path.join(MODS_DIRECTORY, mod_file)
    shutil.move(mod_file, mod_destination)

    print(f"Mod '{mod_details['name']}' installed successfully!")

    # Update installed mods in the configuration file
    update_config(mod_id, mod_details['name'], mod_details['version'])

# Function to uninstall a mod
def uninstall_mod(mod_id):
    config = load_config()
    if 'installed_mods' not in config or mod_id not in config['installed_mods']:
        print("Mod is not installed.")
        return

    mod_name = config['installed_mods'][mod_id]['name']
    mod_file = os.path.join(MODS_DIRECTORY, mod_name)
    if os.path.exists(mod_file):
        os.remove(mod_file)
        print(f"Mod '{mod_name}' uninstalled successfully!")
    else:
        print("Mod file not found.")

    # Remove mod entry from the configuration file
    config['installed_mods'].pop(mod_id)
    save_config(config)

# Function to update a mod
def update_mod(mod_id):
    config = load_config()
    if 'installed_mods' not in config or mod_id not in config['installed_mods']:
        print("Mod is not installed.")
        return

    mod_name = config['installed_mods'][mod_id]['name']
    mod_version = config['installed_mods'][mod_id]['version']

    url = f"https://mod-database.example.com/api/mods/{mod_id}"
    response = requests.get(url)
    mod_details = response.json()

    if mod_details['version'] > mod_version:
        print(f"Updating mod '{mod_name}'...")
        uninstall_mod(mod_id)
        install_mod(mod_id)
    else:
        print(f"Mod '{mod_name}' is already up to date.")

# Function to view installed mods
def view_installed_mods():
    config = load_config()
    if 'installed_mods' not in config:
        print("No installed mods found.")
        return

    print("Installed Mods:")
    for mod_id, mod_data in config['installed_mods'].items():
        print(f"Mod ID: {mod_id}")
        print(f"Mod Name: {mod_data['name']}")
        print(f"Version: {mod_data['version']}")
        print("------------------------")

# Function to check for mod updates
def check_mod_updates():
    config = load_config()
    if 'installed_mods' not in config:
        print("No installed mods found.")
        return

    print("Checking for mod updates...")
    for mod_id, mod_data in config['installed_mods'].items():
        mod_name = mod_data['name']
        mod_version = mod_data['version']

        url = f"https://mod-database.example.com/api/mods/{mod_id}"
        response = requests.get(url)
        mod_details = response.json()

        if mod_details['version'] > mod_version:
            print(f"Mod '{mod_name}' has an update available (Version {mod_details['version']})")
        else:
            print(f"Mod '{mod_name}' is up to date.")

# Function to create a backup of installed mods
def create_mods_backup():
    backup_folder = f"mods_backup_{int(time.time())}"
    backup_path = os.path.join(BACKUP_DIRECTORY, backup_folder)

    config = load_config()
    if 'installed_mods' not in config:
        print("No installed mods found.")
        return

    os.makedirs(backup_path, exist_ok=True)

    print("Creating mods backup...")
    for mod_id, mod_data in config['installed_mods'].items():
        mod_name = mod_data['name']
        mod_file = os.path.join(MODS_DIRECTORY, mod_name)
        backup_file = os.path.join(backup_path, mod_name)

        if os.path.exists(mod_file):
            shutil.copy(mod_file, backup_file)
            print(f"Mod '{mod_name}' backed up successfully.")
        else:
            print(f"Mod '{mod_name}' file not found.")

# Function to delete a backup
def delete_backup(backup_directory):
    backup_folders = [folder for folder in os.listdir(backup_directory) if folder.startswith("mods_backup_")]

    if not backup_folders:
        print("No mods backup found.")
        return

    print("Available Mods Backups:")
    for i, folder in enumerate(backup_folders):
        print(f"{i+1}. {folder}")

    choice = input("Enter the number of the backup to delete: ")
    try:
        choice = int(choice)
        if choice < 1 or choice > len(backup_folders):
            print("Invalid choice.")
            return
    except ValueError:
        print("Invalid choice.")
        return

    selected_backup = backup_folders[choice - 1]
    backup_folder = os.path.join(backup_directory, selected_backup)

    shutil.rmtree(backup_folder)
    print("Mods backup deleted successfully.")

# Function to rename a mod
def rename_mod(mod_id, new_name):
    config = load_config()
    if 'installed_mods' not in config or mod_id not in config['installed_mods']:
        print("Mod is not installed.")
        return

    mod_data = config['installed_mods'][mod_id]
    old_name = mod_data['name']

    mod_file = os.path.join(MODS_DIRECTORY, old_name)
    new_mod_file = os.path.join(MODS_DIRECTORY, new_name)

    if os.path.exists(mod_file):
        os.rename(mod_file, new_mod_file)
        mod_data['name'] = new_name
        save_config(config)
        print(f"Mod '{old_name}' renamed to '{new_name}' successfully!")
    else:
        print("Mod file not found.")

# Function to display mod details
def display_mod_details(mod_id):
    url = f"https://mod-database.example.com/api/mods/{mod_id}"
    response = requests.get(url)
    mod_details = response.json()

    print(f"Mod ID: {mod_details['id']}")
    print(f"Mod Name: {mod_details['name']}")
    print(f"Author: {mod_details['author']}")
    print(f"Description: {mod_details['description']}")
    print(f"Version: {mod_details['version']}")
    print(f"Download URL: {mod_details['download_url']}")

# Helper function to download a file
def download_file(url, filename):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)

    with open(filename, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)

    progress_bar.close()

# Helper function to load configuration from file
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    return {}

# Helper function to save configuration to file
def save_config(config):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file)

# Function to display the available commands
def display_commands():
    print("Available Commands:")
    print("1. search <query> - Search for mods")
    print("2. install <mod_id> - Install a mod")
    print("3. uninstall <mod_id> - Uninstall a mod")
    print("4. update <mod_id> - Update a mod")
    print("5. view - View installed mods")
    print("6. check - Check for mod updates")
    print("7. backup - Create a backup of installed mods")
    print("8. delete <backup_directory> - Delete a mods backup")
    print("9. rename <mod_id> <new_name> - Rename a mod")
    print("10. details <mod_id> - Display mod details")
    print("11. help - Display available commands")
    print("12. exit - Exit the program")

# Main program loop
def main():
    print("Welcome to Mod Manager!")
    display_commands()

    while True:
        command = input("Enter a command: ")

        if command.startswith("search"):
            query = command.split(' ', 1)[1]
            search_mods(query)
        elif command.startswith("install"):
            mod_id = command.split(' ', 1)[1]
            install_mod(mod_id)
        elif command.startswith("uninstall"):
            mod_id = command.split(' ', 1)[1]
            uninstall_mod(mod_id)
        elif command.startswith("update"):
            mod_id = command.split(' ', 1)[1]
            update_mod(mod_id)
        elif command == "view":
            view_installed_mods()
        elif command == "check":
            check_mod_updates()
        elif command == "backup":
            create_mods_backup()
        elif command.startswith("delete"):
            backup_directory = command.split(' ', 1)[1]
            delete_backup(backup_directory)
        elif command.startswith("rename"):
            mod_id, new_name = command.split(' ', 2)[1:]
            rename_mod(mod_id, new_name)
        elif command.startswith("details"):
            mod_id = command.split(' ', 1)[1]
            display_mod_details(mod_id)
        elif command == "help":
            display_commands()
        elif command == "exit":
            print("Goodbye!")
            sys.exit()
        else:
            print("Invalid command. Enter 'help' to see the available commands.")

# Start the program
if __name__ == "__main__":
    main()