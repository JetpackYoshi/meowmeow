import os

def dir_to_file_list(dir_path):
    """Get the list of full paths of all files in a folder"""
    folder_path = dir_path  # Use the existing variable 'directory_path'
    file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]

    return file_paths

def create_directory_tree(root_dir, directory_structure, create_files=True, __counter=None, __path_tracker=None):
    """
    Create a directory tree based on a given structure and return a dictionary of all folders and their unique paths.

    Args:
        root_dir (str): The root directory where the tree will be created.
        directory_structure (dict): A dictionary defining the directory tree structure. 
                                     Keys can be folder names, file names (with extensions), or tuples.
                                     If a key is a tuple, the first element is the name, and the second is the unique reference name.
                                     If a key is a folder, its value should be a dictionary defining its contents.
                                     If a key is a file, its value should be None.
        create_files (bool): Whether to create empty files for file entries.
        __counter (dict): A dictionary to keep track of duplicate names.
        __path_tracker (dict): A dictionary to track unique references for paths.

    Returns:
        dict: A dictionary where keys are folder/file names and values are their unique full paths.

    Example:
        directory_structure = {
            ("folder1", "unique_folder1"): {
                ("subfolder1", "unique_subfolder1"): {
                    ("file1.txt", "unique_file1.txt"): None
                },
                "subfolder2": {}
            },
            "folder2": {
                "file2.txt": None
            }
        }
    """
    if __counter is None:
        __counter = {}
    if __path_tracker is None:
        __path_tracker = {}

    paths = {}
    for key, content in directory_structure.items():
        # Handle tuple keys for unique reference names
        if isinstance(key, tuple):
            name, unique_name = key
        else:
            name = unique_name = key

        # Generate a unique reference for the name if not provided
        original_name = name
        if unique_name in __counter:
            __counter[unique_name] += 1
            base_name, ext = os.path.splitext(unique_name)
            unique_name = f"{base_name}_{__counter[unique_name]}{ext}"
        else:
            __counter[unique_name] = 0

        path = os.path.join(root_dir, name)
        unique_path = os.path.join(root_dir, unique_name)

        if isinstance(content, dict):  # It's a folder
            os.makedirs(path, exist_ok=True)
            paths[unique_name] = path
            __path_tracker[unique_name] = path
            sub_paths = create_directory_tree(path, content, create_files, __counter, __path_tracker)
            paths.update(sub_paths)
        elif content is None:  # It's a file
            os.makedirs(os.path.dirname(path), exist_ok=True)
            if create_files:
                with open(path, 'w') as f:
                    pass  # Create an empty file
            paths[unique_name] = path
            __path_tracker[unique_name] = path

    return paths