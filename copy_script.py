"""
Example Usage:

1. Basic Copy:
   This will copy all files from the source folder to the destination folder.
   
   Command:
   python copy_script.py "C:/SourceFolder" "C:/DestinationFolder"

2. Copy Specific File Types (e.g., only .jpg files):
   This will copy only .jpg files from the source folder to the destination folder.

   Command:
   python copy_script.py "C:/SourceFolder" "C:/DestinationFolder" --filter '*.jpg'

3. Simulate (Dry Run) Without Actually Copying:
   This will simulate the copy process without actually copying any files. Useful for testing.

   Command:
   python copy_script.py "C:/SourceFolder" "C:/DestinationFolder" --dry-run

4. Use Multiple Threads for Faster Copying:
   This will copy files using multiple threads (in this case, 8 threads), which can improve speed when copying a large number of files.

   Command:
   python copy_script.py "C:/SourceFolder" "C:/DestinationFolder" --threads 8

5. Synchronize Directories (Remove Extra Files from Destination):
   This will delete files in the destination that do not exist in the source (for a full sync).

   Command:
   python copy_script.py "C:/SourceFolder" "C:/DestinationFolder" --sync

6. Verbose Output for Debugging:
   This will increase the verbosity of logging to see more details on operations.

   Command:
   python copy_script.py "C:/SourceFolder" "C:/DestinationFolder" --verbose
"""

import shutil
import os
import glob
import logging
import argparse
import concurrent.futures
from tqdm import tqdm

def setup_logging(log_file=None, level=logging.INFO):
    """Setup logging configuration."""
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=level, format=log_format, filename=log_file, filemode='a')
    if log_file:
        console = logging.StreamHandler()
        console.setLevel(level)
        console.setFormatter(logging.Formatter(log_format))
        logging.getLogger().addHandler(console)

def copy_file(source_file, destination_file, overwrite, dry_run):
    """Helper function to copy a single file."""
    try:
        # Check if destination file exists
        if os.path.exists(destination_file):
            source_mtime = os.path.getmtime(source_file)
            dest_mtime = os.path.getmtime(destination_file)
            source_size = os.path.getsize(source_file)
            dest_size = os.path.getsize(destination_file)

            # Skip if destination is up to date (based on size and modification time)
            if not overwrite and dest_mtime >= source_mtime and source_size == dest_size:
                logging.info(f"Skipping {os.path.basename(source_file)} (up to date).")
                return False

        # Perform dry run
        if dry_run:
            logging.info(f"DRY RUN: Would copy {os.path.basename(source_file)} to {destination_file}")
        else:
            shutil.copy2(source_file, destination_file)  # Copy with metadata
            logging.info(f"Copied {os.path.basename(source_file)} to {destination_file}")
        return True

    except Exception as e:
        logging.error(f"Failed to copy {os.path.basename(source_file)}: {e}")
        return False

def remove_extra_files(source_path, destination_path, dry_run):
    """Remove files in the destination that do not exist in the source (for sync)."""
    destination_files = glob.glob(os.path.join(destination_path, '**', '*'), recursive=True)
    source_files_set = {os.path.relpath(file, source_path) for file in glob.glob(os.path.join(source_path, '**', '*'), recursive=True)}

    files_removed = 0

    for dest_file in destination_files:
        relative_path = os.path.relpath(dest_file, destination_path)
        if relative_path not in source_files_set:
            if dry_run:
                logging.info(f"DRY RUN: Would remove {dest_file}")
            else:
                os.remove(dest_file)
                logging.info(f"Removed {dest_file}")
            files_removed += 1

    logging.info(f"{files_removed} extra files removed from {destination_path}.")
    return files_removed

def copy_files(source_path, destination_path, overwrite=True, file_filter='*', dry_run=False, threads=4, sync=False):
    """Copy files from source to destination, with options for filtering, dry run, multi-threading, and sync."""
    try:
        # Validate source and destination paths
        if not os.path.exists(source_path):
            logging.error(f"Source path does not exist: {source_path}")
            return
        
        # Ensure the destination path exists
        os.makedirs(destination_path, exist_ok=True)

        # Get a list of files matching the filter in the source directory
        source_files = glob.glob(os.path.join(source_path, '**', file_filter), recursive=True)

        if not source_files:
            logging.info(f"No files found matching '{file_filter}' in {source_path}")
            return

        total_files_copied = 0
        total_files_skipped = 0

        # Progress bar for visual feedback
        with tqdm(total=len(source_files), desc="Copying files", unit="file") as pbar:
            # Use thread pool for concurrent file copying
            with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
                futures = []
                for source_file in source_files:
                    relative_path = os.path.relpath(source_file, source_path)
                    destination_file = os.path.join(destination_path, relative_path)
                    os.makedirs(os.path.dirname(destination_file), exist_ok=True)

                    futures.append(executor.submit(copy_file, source_file, destination_file, overwrite, dry_run))

                # Update progress bar and gather results
                for future in concurrent.futures.as_completed(futures):
                    result = future.result()
                    if result:
                        total_files_copied += 1
                    else:
                        total_files_skipped += 1
                    pbar.update(1)

        logging.info(f"File copy operation completed. {total_files_copied} files copied, {total_files_skipped} files skipped.")

        # Perform synchronization by removing extra files in the destination
        if sync:
            files_removed = remove_extra_files(source_path, destination_path, dry_run)
            logging.info(f"Synchronization complete. {files_removed} files removed.")

    except Exception as e:
        logging.error(f"An error occurred during file copying: {e}")

def main():
    # Command-line argument parsing
    parser = argparse.ArgumentParser(description="Copy files from one directory to another with options.")
    parser.add_argument('source', help="Source directory path")
    parser.add_argument('destination', help="Destination directory path")
    parser.add_argument('-o', '--overwrite', action='store_true', help="Overwrite existing files at destination")
    parser.add_argument('-f', '--filter', default='*', help="File filter (e.g., '*.txt' to copy only text files)")
    parser.add_argument('-d', '--dry-run', action='store_true', help="Simulate the file copy without making changes")
    parser.add_argument('-t', '--threads', type=int, default=4, help="Number of threads for concurrent copying")
    parser.add_argument('-l', '--log', help="Log to a file (default: log to console)")
    parser.add_argument('-s', '--sync', action='store_true', help="Remove extra files in the destination not present in the source")
    parser.add_argument('-v', '--verbose', action='store_true', help="Increase output verbosity")

    args = parser.parse_args()

    # Setup logging
    logging_level = logging.DEBUG if args.verbose else logging.INFO
    setup_logging(log_file=args.log, level=logging_level)

    # Safety check to avoid copying to the same directory
    if os.path.abspath(args.source) == os.path.abspath(args.destination):
        logging.error("Source and destination paths are the same. Aborting operation.")
    else:
        copy_files(args.source, args.destination, overwrite=args.overwrite, 
                   file_filter=args.filter, dry_run=args.dry_run, threads=args.threads, sync=args.sync)

if __name__ == "__main__":
    main()