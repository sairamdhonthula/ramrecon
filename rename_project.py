import os
import re

def update_file_contents(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content = content.replace("Argus", "RAMRecon")
        new_content = new_content.replace("ARGUS", "RAMRECON")
        new_content = new_content.replace("argus", "ramrecon")

        if content != new_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated content in: {filepath}")
    except Exception as e:
        # Ignore binary files or files that can't be read
        pass


def rename_files_and_directories(root_dir):
    # Rename directories (bottom-up to avoid path issues)
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        for filename in filenames:
            if "argus" in filename.lower():
                new_filename = filename.replace("Argus", "RAMRecon").replace("ARGUS", "RAMRECON").replace("argus", "ramrecon")
                old_path = os.path.join(dirpath, filename)
                new_path = os.path.join(dirpath, new_filename)
                os.rename(old_path, new_path)
                print(f"Renamed file: {old_path} -> {new_path}")
            
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        for dirname in dirnames:
            if "argus" in dirname.lower():
                new_dirname = dirname.replace("Argus", "RAMRecon").replace("ARGUS", "RAMRECON").replace("argus", "ramrecon")
                old_path = os.path.join(dirpath, dirname)
                new_path = os.path.join(dirpath, new_dirname)
                os.rename(old_path, new_path)
                print(f"Renamed directory: {old_path} -> {new_path}")

def process_directory(root_dir):
    # First update file contents
    for dirpath, _, filenames in os.walk(root_dir):
        if '.git' in dirpath:
            continue
        for filename in filenames:
            if filename == 'rename_project.py' or filename.endswith('.pyc') or filename.endswith('.png') or filename.endswith('.jpg'):
                continue
            filepath = os.path.join(dirpath, filename)
            update_file_contents(filepath)

    # Then rename files and directories
    rename_files_and_directories(root_dir)

if __name__ == '__main__':
    root = r'c:\Users\Sairam\Downloads\Argus-main\Argus-main'
    process_directory(root)
