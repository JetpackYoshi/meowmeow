import os

def dir_to_file_list(dir_path, file_type=None):
    """
    Generate a list of full file paths for all files in the specified directory,
    optionally filtering by file type.

    Parameters
    ----------
    dir_path : str
        The path to the directory to scan for files.
    file_type : str, optional
        The file extension to filter by (e.g., '.txt'). Defaults to None.

    Returns
    -------
    list of str
        A list of strings, where each string is the full path to a file in the directory.
    """
    folder_path = dir_path
    file_paths = [
        os.path.join(folder_path, file)
        for file in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, file)) and (file_type is None or file.endswith(file_type))
    ]

    return file_paths

class DirectoryTree:
    """
    A class that represents a directory tree structure.
    
    Parameters
    ----------
    root_dir : str
        The root directory where the tree will be created.
    directory_structure_definition : dict
        A dictionary defining the directory tree structure. Keys can be folder names, file names (with extensions), 
        or tuples. If a key is a tuple, the first element is the name, and the second is the unique reference name. 
        If a key is a folder, its value should be a dictionary defining its contents. If a key is a file, its value 
        should be None.

    Examples
    --------
    >>> root_dir = "/path/to/root"
    >>> directory_structure = {
    ...     ("folder1", "unique_folder1"): {
    ...         ("subfolder1", "unique_subfolder1"): {
    ...             ("file1.txt", "unique_file_reference"): None
    ...         },
    ...         "subfolder2": {}
    ...     },
    ...     "folder2": {
    ...         "file2.txt": None
    ...     }
    ... }
    >>> d = DirectoryTree(root_dir, directory_structure)
    """

    def __init__(self, root_dir, directory_structure_definition):
        """
        Initialize the DirectoryTree object.
        """
        self.root_dir = root_dir
        self.directory_structure_definition = directory_structure_definition
        self.dir = self._define_by_dict()

    def _define_by_dict(self):
        """
        Create a dictionary of file path objects based on the provided definition.

        Returns
        -------
        dict
            A dictionary where keys are folder/file reference names and values are pathlib.Path objects.

        Examples
        --------
        This will create a dictionary with the following structure:
        {
            "unique_folder1": Path("/path/to/root/folder1"),
            "unique_subfolder1": Path("/path/to/root/folder1/subfolder1"),
            "unique_file_reference": Path("/path/to/root/folder1/subfolder1/file1.txt"),
            ...
        }
        """
        paths = {}
        for key, value in self.directory_structure_definition.items():
            if isinstance(key, tuple):
                folder_name, unique_reference_name = key
            else:
                folder_name = key
                unique_reference_name = None

            folder_path = Path(self.root_dir) / folder_name

            if unique_reference_name:
                paths[unique_reference_name] = folder_path

            if isinstance(value, dict):
                sub_directories = DirectoryTree(folder_path, value)
                sub_directories._define_by_dict()
                paths.update(sub_directories._define_by_dict())

            if unique_reference_name:
                paths[unique_reference_name] = folder_path
            else:
                paths[folder_name] = folder_path

        return paths

    def get_dir(self, strip_root=False):
        """
        Get the entire directory structure as a dictionary.

        Parameters
        ----------
        strip_root : bool, optional
            If True, strip the root directory from the paths. Defaults to False.

        Returns
        -------
        dict
            A dictionary representing the directory structure.
            
        Examples
        --------
        >>> d = DirectoryTree("/path/to/root", {"folder1": {}})
        >>> d.get_dir()
        {'folder1': '/path/to/root/folder1'}
        >>> d.get_dir(strip_root=True)
        {'folder1': 'folder1'}
        """
        if strip_root:
            return {k: str(v.relative_to(self.root_dir)) for k, v in self.dir.items()}
        return {k: str(v) for k, v in self.dir.items()}

    def create_directory_structure(self, create_files=False):
        """
        Create the directory structure based on the defined paths.

        By default, it only creates folders (paths not ending in a file extension). If `create_files` is True, it will 
        also create empty files.

        Parameters
        ----------
        create_files : bool, optional
            If True, create empty files in the directory structure. Defaults to False.
        """
        for key, path in self.dir.items():
            if not path.suffix:
                # Create the directory if it doesn't exist
                path.mkdir(parents=True, exist_ok=True)

        # Create files if specified
        if create_files:
            for key, path in self.dir.items():
                if path.suffix:
                    # Create the file if it doesn't exist
                    path.touch(exist_ok=True)

def create_directory_tree(root_dir, directory_structure, create_files=True, __counter=None, __path_tracker=None):
    """
    Create a directory tree based on a given structure and return a dictionary of all folders and their unique paths.

    Parameters
    ----------
    root_dir : str
        The root directory where the tree will be created.
    directory_structure : dict
        A dictionary defining the directory tree structure. Keys can be folder names, file names (with extensions), 
        or tuples. If a key is a tuple, the first element is the name, and the second is the unique reference name. 
        If a key is a folder, its value should be a dictionary defining its contents. If a key is a file, its value 
        should be None.
    create_files : bool, optional
        Whether to create empty files for file entries. Defaults to True.
    __counter : dict, optional
        A dictionary to keep track of duplicate names. Used internally.
    __path_tracker : dict, optional
        A dictionary to track unique references for paths. Used internally.

    Returns
    -------
    dict
        A dictionary where keys are folder/file names and values are their unique full paths.

    Examples
    --------
    >>> directory_structure = {
    ...     ("folder1", "unique_folder1"): {
    ...         ("subfolder1", "unique_subfolder1"): {
    ...             ("file1.txt", "unique_file1.txt"): None
    ...         },
    ...         "subfolder2": {}
    ...     },
    ...     "folder2": {
    ...         "file2.txt": None
    ...     }
    ... }
    >>> create_directory_tree("/tmp", directory_structure)
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