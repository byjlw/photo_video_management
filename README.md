# photo and video management
# Media Organizer and Cleanup Script

This Python script organizes photos and videos based on their creation dates into a structured folder hierarchy.

It will move the media from the source to the target and will optionally clean up the now empty directories

## Features

- **Organize photos and videos**: Files are sorted into year/month/day folders based on their creation dates extracted from metadata or file creation timestamps.
- **Cleanup**: Optionally delete empty folders and specific unwanted files (`*.DS_Store`, `Thumbs.db`, etc.) after organizing.

## Requirements

- Python 3.x
- Required Python packages: `hachoir`, `exifread`

## Usage

### Example: Organize files from a laptop to a network drive

Assume your laptop's source directory contains unorganized photos and videos, and you want to organize them into a network drive's target directory.

1. **Clone or download** this repository to your local machine.

2. **Install dependencies**:

```bash
   pip install hachoir
   pip install exifread
```
3. **Run the script**:

   Open a terminal or command prompt and navigate to the directory where the script (`organize_and_cleanup.py`) is located.

   Use the following command to organize files from your laptop's source directory to a network drive's target directory:

```bash
   python organize_and_cleanup.py --source_dir "/path/to/laptop/source_directory" --target_dir "/path/to/network_drive/target_directory" --clean_up
```
Replace /path/to/laptop/source_directory with the path to the directory on your laptop containing the photos and videos you want to organize.

Replace /path/to/network_drive/target_directory with the path to the directory on your network drive where you want the organized files to be stored.

**Explanation**:

- The script will organize the files from the source directory (`/path/to/laptop/source_directory`) into a structured hierarchy in the target directory (`/path/to/network_drive/target_directory`).

- **Finding the Network Drive Path**: To determine the path to a network drive on your system:
- **Windows**: Open File Explorer, navigate to the network drive, right-click on the folder, and select "Properties". The "Location" field will show you the network path (e.g., `\\server\share`).
- **Mac**: Open Finder, navigate to the network drive, right-click on the folder, and select "Get Info". The "Where" field will display the network path (e.g., `smb://server/share`).

 

**Parameters**:
- `--source_dir`: Specifies the source directory containing photos and videos to organize.
- `--target_dir`: Specifies the target directory where organized files will be stored.
- `--clean_up`: Optional flag to trigger cleanup operations after organizing. Deletes empty folders and unwanted files from the source directory.
