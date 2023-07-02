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

def get_mod_details(mod_id):
    url = f"{API_BASE_URL}/mods/{mod_id}"
    mod_details = make_api_request(url)

    if mod_details:
        print_mod_details(mod_details)
    else:
        print("Mod not found.")

def enable_mod(mod_id, enable=True):
    mod_config = load_config()
    if mod_id in mod_config:
        mod_config[mod_id]['enabled'] = enable
        save_config(mod_config)
        status = "enabled" if enable else "disabled"
        print(f"Mod '{mod_id}' {status} successfully.")
    else:
        print("Mod ID not found in the configuration.")


def enable_all_mods():
    mod_config = load_config()
    for mod_id in mod_config:
        enable_mod(mod_id, enable=True)

def disable_all_mods():
    mod_config = load_config()
    for mod_id in mod_config:
        enable_mod(mod_id, enable=False)

def delete_mod(mod_id):
    uninstall_mod(mod_id)
    mod_config = load_config()
    if mod_id in mod_config:
        del mod_config[mod_id]
        save_config(mod_config)
        print(f"Mod '{mod_id}' deleted successfully.")
    else:
        print("Mod ID not found in the configuration.")

def view_enabled_mods():
    mod_config = load_config()
    for mod_id, mod_data in mod_config.items():
        if mod_data['enabled']:
            print_mod_details(mod_data)

def view_disabled_mods():
    mod_config = load_config()
    for mod_id, mod_data in mod_config.items():
        if not mod_data['enabled']:
            print_mod_details(mod_data)

def get_total_installed_mods():
    mod_config = load_config()
    total_installed_mods = len(mod_config)
    print(f"Total installed mods: {total_installed_mods}")

def is_mod_installed(mod_id):
    mod_config = load_config()
    return mod_id in mod_config

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
        mod_file = mod_config[mod_id]['file']
        mod_path = os.path.join(MODS_DIRECTORY, mod_file)

        if os.path.exists(mod_path):
            os.remove(mod_path)
            print(f"Mod '{mod_config[mod_id]['name']}' uninstalled successfully!")
        else:
            print("Mod file not found.")
    else:
        print("Mod ID not found in the configuration.")

    # Remove the mod entry from the config
    if mod_id in mod_config:
        del mod_config[mod_id]
        save_config(mod_config)

# Function to update a mod
def update_mod(mod_id):
    mod_config = load_config()
    if mod_id not in mod_config:
        print("Mod ID not found in the configuration.")
        return

    mod_details = make_api_request(f"{API_BASE_URL}/mods/{mod_id}")
    if not mod_details:
        print("Mod not found.")
        return

    current_version = mod_config[mod_id]['version']
    latest_version = mod_details['version']

    if current_version == latest_version:
        print("Mod is already up to date.")
        return

    uninstall_mod(mod_id)
    install_mod(mod_id)

def backup_mods(backup_directory):
    mod_config = load_config()
    if not os.path.exists(backup_directory):
        os.makedirs(backup_directory)

    for mod_id, mod_data in mod_config.items():
        mod_file = mod_data['file']
        mod_path = os.path.join(MODS_DIRECTORY, mod_file)

        if os.path.exists(mod_path):
            shutil.copy(mod_path, backup_directory)
        else:
            print(f"Mod file '{mod_file}' not found. Skipping backup.")

    print("Mods backup completed successfully.")

def load_mods_from_backup(backup_directory):
    mod_files = os.listdir(backup_directory)
    for mod_file in mod_files:
        mod_path = os.path.join(backup_directory, mod_file)
        if os.path.isfile(mod_path):
            mod_id = os.path.splitext(mod_file)[0]
            install_mod(mod_id)

def download_file(url, filename):
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        total_size = int(response.headers.get("content-length", 0))
        progress_bar = tqdm(total=total_size, unit="B", unit_scale=True)

        with open(filename, "wb") as file:
            for data in response.iter_content(chunk_size=1024):
                file.write(data)
                progress_bar.update(len(data))

        progress_bar.close()

# Function to parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Mod Manager CLI")
    parser.add_argument("command", choices=["install", "uninstall", "update", "search", "view", "enable", "disable", "backup", "load_backup", "details", "total_installed", "exit"], help="Command to execute")
    parser.add_argument("--mod_id", help="ID of the mod")
    parser.add_argument("--query", help="Search query for mod search")
    parser.add_argument("--backup_dir", default=BACKUP_DIRECTORY, help="Directory to store mod backups")
    return parser.parse_args()

# Function to load mod configuration from file
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    else:
        return {}

# Function to save mod configuration to file
def save_config(mod_config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(mod_config, file)

# Function to update mod configuration after installation
def update_config(mod_id, mod_name, mod_version):
    mod_config = load_config()
    mod_config[mod_id] = {
        'name': mod_name,
        'file': f"{mod_id}.zip",
        'version': mod_version,
        'enabled': True
    }
    save_config(mod_config)

# Main function to handle commands
def main():
    args = parse_arguments()

    if args.command == "install":
        install_mod(args.mod_id)
    elif args.command == "uninstall":
        uninstall_mod(args.mod_id)
    elif args.command == "update":
        update_mod(args.mod_id)
    elif args.command == "search":
        search_mods(args.query)
    elif args.command == "view":
        view_enabled_mods() if args.status == "enabled" else view_disabled_mods()
    elif args.command == "enable":
        enable_mod(args.mod_id, enable=True)
    elif args.command == "disable":
        enable_mod(args.mod_id, enable=False)
    elif args.command == "backup":
        backup_mods(args.backup_dir)
    elif args.command == "load_backup":
        load_mods_from_backup(args.backup_dir)
    elif args.command == "details":
        get_mod_details(args.mod_id)
    elif args.command == "total_installed":
        get_total_installed_mods()
    elif args.command == "exit":
        print("Exiting Mod Manager CLI.")
        return
    else:
        print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()