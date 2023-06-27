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

    print("Checking for updates...")
    for mod_id, mod_data in config['installed_mods'].items():
        mod_name = mod_data['name']
        mod_version = mod_data['version']

        url = f"https://mod-database.example.com/api/mods/{mod_id}"
        response = requests.get(url)
        mod_details = response.json()

        if mod_details['version'] > mod_version:
            print(f"Update available for mod '{mod_name}' (Current version: {mod_version}, Latest version: {mod_details['version']})")
            print("Run the 'update' command to update the mod.")
            print("------------------------")

# Function to download a file
def download_file(url, filename):
    with urllib.request.urlopen(url) as response, open(filename, 'wb') as out_file:
        total_size = int(response.headers['content-length'])
        block_size = 1024
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)

        while True:
            data = response.read(block_size)
            if not data:
                break
            progress_bar.update(len(data))
            out_file.write(data)

        progress_bar.close()

# Function to load the configuration file
def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}

    with open(CONFIG_FILE, 'r') as file:
        config = json.load(file)

    return config

# Function to save the configuration file
def save_config(config):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file, indent=4)

# Function to update the installed mods in the configuration file
def update_config(mod_id, mod_name, mod_version):
    config = load_config()
    if 'installed_mods' not in config:
        config['installed_mods'] = {}

    config['installed_mods'][mod_id] = {
        'name': mod_name,
        'version': mod_version,
        'enabled': True  # By default, enable the mod after installation
    }

    save_config(config)

# Function to load mods from a backup
def load_mods_from_backup(backup_directory):
    backup_folders = [folder for folder in os.listdir(backup_directory) if folder.startswith("mods_backup_")]

    if not backup_folders:
        print("No mods backup found.")
        return

    print("Available Mods Backups:")
    for i, folder in enumerate(backup_folders):
        print(f"{i+1}. {folder}")

    choice = input("Enter the number of the backup to load: ")
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

    config = load_config()
    if 'installed_mods' in config:
        print("Installed mods already exist. Loading mods from backup will overwrite the existing mods.")
        confirmation = input("Are you sure you want to continue? (y/n): ")
        if confirmation.lower() != 'y':
            print("Aborted.")
            return

    shutil.rmtree(MODS_DIRECTORY)
    shutil.copytree(backup_folder, MODS_DIRECTORY)
    print("Mods loaded from backup successfully.")

# Function to enable/disable a mod
def enable_mod(mod_id, enable=True):
    config = load_config()
    if 'installed_mods' not in config or mod_id not in config['installed_mods']:
        print("Mod is not installed.")
        return

    mod_data = config['installed_mods'][mod_id]
    mod_data['enabled'] = enable
    save_config(config)

    mod_status = "enabled" if enable else "disabled"
    print(f"Mod '{mod_data['name']}' is now {mod_status}.")

# Function to backup installed mods
def backup_mods(backup_directory):
    timestamp = time.strftime("%Y%m%d%H%M%S")
    backup_folder = os.path.join(backup_directory, f"mods_backup_{timestamp}")
    shutil.copytree(MODS_DIRECTORY, backup_folder)
    print("Mods backed up successfully.")

# Main function to handle user commands
def main():
    if not os.path.exists(MODS_DIRECTORY):
        os.makedirs(MODS_DIRECTORY)

    if not os.path.exists(BACKUP_DIRECTORY):
        os.makedirs(BACKUP_DIRECTORY)

    command = input("Enter a command (search/install/uninstall/update/view/check_updates/backup/load_mods/enable/disable/exit): ")

    if command == "search":
        query = input("Enter a search query: ")
        search_mods(query)
    elif command == "install":
        mod_id = input("Enter the ID of the mod to install: ")
        install_mod(mod_id)
    elif command == "uninstall":
        mod_id = input("Enter the ID of the mod to uninstall: ")
        uninstall_mod(mod_id)
    elif command == "update":
        mod_id = input("Enter the ID of the mod to update: ")
        update_mod(mod_id)
    elif command == "view":
        view_installed_mods()
    elif command == "check_updates":
        check_mod_updates()
    elif command == "backup":
        backup_mods(BACKUP_DIRECTORY)
    elif command == "load_mods":
        load_mods_from_backup(BACKUP_DIRECTORY)
    elif command == "enable":
        mod_id = input("Enter the ID of the mod to enable: ")
        enable_mod(mod_id, enable=True)
    elif command == "disable":
        mod_id = input("Enter the ID of the mod to disable: ")
        enable_mod(mod_id, enable=False)
    elif command == "exit":
        sys.exit()
    else:
        print("Invalid command.")

# Run the main function
if __name__ == "__main__":
    while True:
        main()