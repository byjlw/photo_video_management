import os
import shutil
import argparse
import datetime
import exifread
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
import pathlib
import sys

def get_video_creation_date(path):
    """Extract the creation date of a video file."""
    try:
        parser = createParser(path)
        if not parser:
            print(f"Unable to create parser for {path}")
            return None
        metadata = extractMetadata(parser)
        if not metadata:
            print(f"Unable to extract metadata for {path}")
            return None

        creation_date = metadata.get('creation_date')
        return creation_date
    except Exception as e:
        print(f"Error reading video metadata for {path}: {e}")
    return None

def get_date_taken(path):
    """Extract the date the media was taken from its metadata, file creation date, or video creation date."""
    # Attempt to extract date for images
    if path.lower().endswith(('.png', '.jpg', '.jpeg', '.cr2', '.nef')):
        try:
            with open(path, 'rb') as f:
                tags = exifread.process_file(f, details=False)
                date_taken_tag = tags.get('EXIF DateTimeOriginal', None)
                if date_taken_tag:
                    return datetime.datetime.strptime(str(date_taken_tag), '%Y:%m:%d %H:%M:%S')
        except Exception as e:
            print(f"Error reading metadata for {path}: {e}")

    # Attempt to extract date for videos
    elif path.lower().endswith(('.mov', '.mp4', '.m4v')):
        return get_video_creation_date(path)

    # Fallback on file creation date if EXIF data is missing or unsupported file type
    try:
        return datetime.datetime.fromtimestamp(os.path.getctime(path))
    except Exception as e:
        print(f"Error getting creation date for {path}: {e}")

    return None

def organize_photos_and_videos(source_directory, target_directory):
    """Organize photos and videos into year/month/day folder structure."""
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.cr2', '.mov', '.mp4', '.nef', '.m4v')):
                file_path = os.path.join(root, file)
                date_taken = get_date_taken(file_path)
                if date_taken:
                    new_dir = os.path.join(target_directory, str(date_taken.year), str(date_taken.month).zfill(2), str(date_taken.day).zfill(2))
                    os.makedirs(new_dir, exist_ok=True)
                    print(f"Moving {file} to {new_dir}")
                    shutil.move(file_path, os.path.join(new_dir, file))
                else:
                    print(f"No valid date found for {file}, skipping.")

def delete_empty_folders(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in dirs:
            folder_path = os.path.join(root, name)
            dirList = os.listdir(folder_path)
            if not dirList:  # Check if the folder is empty
                os.rmdir(folder_path)  # Delete the empty folder
                print(f"Deleted empty folder: {folder_path}")
            else:
                print(f"{folder_path} contains {dirList}")

def delete_ds_store(starting_directory):
    starting_path = pathlib.Path(starting_directory)
    for current_directory, directories, files in os.walk(starting_path):
        for file in files:
            if file.endswith(('.DS_Store', 'Thumbs.db', '.LRF', '.SRT')):
                file_path = pathlib.Path(current_directory) / file
                file_path.unlink()
                print(f"Deleted: {file_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Organize photos and videos by date.')
    parser.add_argument('--source_dir', help='The source directory containing the photos and videos to organize.')
    parser.add_argument('--target_dir', help='The target directory where the organized photos and videos will be stored.')
    parser.add_argument('--clean_up', action='store_true', help='Delete empty folders and .DS_Store files after organizing.')

    args = parser.parse_args()

    organize_photos_and_videos(args.source_dir, args.target_dir)

    if args.clean_up:
        delete_ds_store(args.source_dir)
        delete_empty_folders(args.source_dir)