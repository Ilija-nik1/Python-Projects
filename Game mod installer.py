import requests
import os
import shutil
import argparse
import json
from tqdm import tqdm

# Constants for API endpoints and directories
MODS_DIRECTORY = "path/to/mods/directory"
CONFIG_FILE = "config.json"
BACKUP_DIRECTORY = "path/to/backup/directory"
API_BASE_URL = "https://mod-database.example.com/api"

# Function to make API requests (unchanged)
def make_api_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error while making API request: {e}")
        return None

# Function to search for mods
def search_mods(query):
    url = f"{API_BASE_URL}/search?query={query}"
    mods = make_api_request(url)

    if mods:
        for mod in mods:
            print_mod_details(mod)

def print_mod_details(mod):
    print(f"Mod ID: {mod['id']}")
    print(f"Mod Name: {mod['name']}")
    print(f"Author: {mod['author']}")
    print(f"Description: {mod['description']}")
    print("------------------------")

# Function to install a mod
def install_mod(mod_id):
    url = f"{API_BASE_URL}/mods/{mod_id}"
    mod_details = make_api_request(url)

    if not mod_details:
        print("Mod not found.")
        return

    mod_url = mod_details['download_url']
    mod_file = os.path.basename(mod_url)
    download_file(mod_url, mod_file)

    mod_destination = os.path.join(MODS_DIRECTORY, mod_file)
    shutil.move(mod_file, mod_destination)

    print(f"Mod '{mod_details['name']}' installed successfully!")
    update_config(mod_id, mod_details['name'], mod_details['version'])

# Function to uninstall a mod
def uninstall_mod(mod_id):
    # Remove the mod file from the mods directory
    mod_config = load_config()
    if mod_id in mod_config:
        mod_file = mod_config[mod_id]['filename']
        mod_path = os.path.join(MODS_DIRECTORY, mod_file)
        if os.path.exists(mod_path):
            os.remove(mod_path)
            print(f"Mod '{mod_id}' uninstalled successfully!")
            del mod_config[mod_id]
            save_config(mod_config)
        else:
            print("Mod file not found.")
    else:
        print("Mod ID not found in the configuration.")

# Function to update a mod
def update_mod(mod_id):
    # Uninstall the current version and install the latest version
    uninstall_mod(mod_id)
    install_mod(mod_id)

# Function to view installed mods
def view_installed_mods():
    mod_config = load_config()
    for mod_id, mod_data in mod_config.items():
        print_mod_details(mod_data)

# Function to check for updates
def check_mod_updates():
    mod_config = load_config()
    for mod_id, mod_data in mod_config.items():
        mod_version = mod_data['version']
        url = f"{API_BASE_URL}/mods/{mod_id}"
        latest_mod_details = make_api_request(url)
        if latest_mod_details and latest_mod_details['version'] > mod_version:
            print(f"Mod '{mod_data['name']}' has an update available.")

# Function to download a file (unchanged)
def download_file(url, filename):
    response = requests.get(url, stream=True)
    with open(filename, 'wb') as file:
        total_length = int(response.headers.get('content-length'))
        for data in tqdm(response.iter_content(chunk_size=1024), total=total_length / 1024, desc="Downloading"):
            file.write(data)

# Function to load the mod configuration from a file
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    return {}

# Function to save the mod configuration to a file
def save_config(mod_config):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(mod_config, file)

# Function to update the mod configuration
def update_config(mod_id, mod_name, mod_version):
    mod_config = load_config()
    mod_config[mod_id] = {
        'name': mod_name,
        'version': mod_version,
        'filename': f"{mod_id}-{mod_version}.zip",
        'enabled': True
    }
    save_config(mod_config)

# Function to enable or disable a mod
def enable_mod(mod_id, enable=True):
    mod_config = load_config()
    if mod_id in mod_config:
        mod_config[mod_id]['enabled'] = enable
        save_config(mod_config)
        print(f"Mod '{mod_id}' {'enabled' if enable else 'disabled'} successfully.")
    else:
        print("Mod ID not found in the configuration.")

# Function to perform backups of installed mods
def backup_mods(backup_directory):
    if not os.path.exists(backup_directory):
        os.makedirs(backup_directory)

    mod_config = load_config()
    for mod_id, mod_data in mod_config.items():
        mod_file = mod_data['filename']
        mod_path = os.path.join(MODS_DIRECTORY, mod_file)
        if os.path.exists(mod_path):
            backup_file = os.path.join(backup_directory, mod_file)
            shutil.copy(mod_path, backup_file)
            print(f"Mod '{mod_id}' backed up successfully.")
        else:
            print(f"Mod file for '{mod_id}' not found.")

# Function to load mods from a backup
def load_mods_from_backup(backup_directory):
    if not os.path.exists(backup_directory):
        print("Backup directory not found.")
        return

    backup_files = os.listdir(backup_directory)
    if not backup_files:
        print("No backup files found.")
        return

    for backup_file in tqdm(backup_files, desc="Restoring backups"):
        backup_path = os.path.join(backup_directory, backup_file)
        mod_destination = os.path.join(MODS_DIRECTORY, backup_file)

        if os.path.exists(mod_destination):
            print(f"Skipping '{backup_file}' - Mod already exists.")
            continue

        shutil.copy(backup_path, mod_destination)
        print(f"Mod '{backup_file}' restored successfully.")

# Function to handle command-line arguments (unchanged)
def parse_arguments():
    commands = [
        "search", "install", "uninstall", "update", "view",
        "check_updates", "backup", "load_mods", "enable", "disable", "exit"
    ]
    parser = argparse.ArgumentParser(description="Mod Manager")
    parser.add_argument("command", choices=commands, help="Choose a command")
    parser.add_argument("--mod_id", help="Mod ID")
    parser.add_argument("--query", help="Search query")
    return parser.parse_args()

# Main function to handle user commands (unchanged)
def main():
    if not os.path.exists(MODS_DIRECTORY):
        os.makedirs(MODS_DIRECTORY)

    if not os.path.exists(BACKUP_DIRECTORY):
        os.makedirs(BACKUP_DIRECTORY)

    args = parse_arguments()

    if args.command == "search":
        search_mods(args.query)
    elif args.command == "install":
        install_mod(args.mod_id)
    elif args.command == "uninstall":
        uninstall_mod(args.mod_id)
    elif args.command == "update":
        update_mod(args.mod_id)
    elif args.command == "view":
        view_installed_mods()
    elif args.command == "check_updates":
        check_mod_updates()
    elif args.command == "backup":
        backup_mods(BACKUP_DIRECTORY)
    elif args.command == "load_mods":
        load_mods_from_backup(BACKUP_DIRECTORY)
    elif args.command == "enable":
        enable_mod(args.mod_id, enable=True)
    elif args.command == "disable":
        enable_mod(args.mod_id, enable=False)
    elif args.command == "exit":
        import sys
        sys.exit()
    else:
        print("Invalid command.")

if __name__ == "__main__":
    main()