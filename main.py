from typing import Iterable, Union
import logging
import time
import os

from config import *


# Ensure the logs folder exists before configuring logging.
# `LOGS_FOLDER` is expected to be a Path object imported from `config`.
LOGS_FOLDER.mkdir() if not LOGS_FOLDER.exists() else None


# Configure global logging for the script. Logs are written to
# `logs/file_sorter.log` at DEBUG level with a simple time + level + message format.
logging.basicConfig(
    filename=f"logs/file_sorter.log",
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    encoding="utf-8",
)


class Folder:
    """Utility class that represents a folder and provides methods to
    inspect and sort files inside it.

    The class is intentionally lightweight: it stores a path (either a
    Path or a string) and offers helpers that iterate directory
    entries using os.scandir for efficiency.
    """

    def __init__(self, path: Union[Path, str]) -> None:
        # Store the path to operate on. Expectation: `path` supports
        # `/` operator (i.e., is a pathlib.Path), but Union allows
        # callers to pass a string as well.
        self.path = path

    def _get_subfolder_paths(self) -> Iterable:
        """Yield subfolder paths inside this folder.

        Uses os.scandir which is faster than listdir for large
        directories. Returns generator of path-like strings that can
        be converted to Path objects by the caller.
        """
        return (folder.path for folder in os.scandir(self.path) if folder.is_dir())

    def _get_file_paths(self) -> Iterable:
        """Yield file paths (non-directories) inside this folder.

        This generator excludes directories. Each yielded item is the
        raw path string returned by os.DirEntry.path.
        """
        return (file.path for file in os.scandir(self.path) if not file.is_dir())

    def _create_subfolder(self, subfolder_name: str) -> None:
        """Create a subfolder with the given name if it doesn't exist.

        The method uses the `/` operator to build a path relative to
        `self.path` (so `self.path` should be a pathlib.Path). If the
        subfolder already exists, this is a no-op.
        """
        subfolder_path = self.path / subfolder_name
        if not subfolder_path.exists():
            subfolder_path.mkdir()

    def sort_files_by_extensions(self) -> None:
        """Move files into subfolders based on their file extensions.

        For each file in the folder, determine the extension (text after
        the last dot) and, if the extension is known (present in the
        EXTENSIONS mapping from `config`), move the file into the
        corresponding subfolder named by `get_subfolder_name_by_extension`.

        The original file is renamed (moved) into the new path and an
        INFO log is written for each move.
        """
        for filepath in self._get_file_paths():
            path = Path(filepath)
            # Determine file extension by splitting on '.' and taking the
            # last segment. This treats filenames without a dot as having
            # the filename itself as 'extension' which will typically not
            # match any entry in EXTENSIONS.
            extension = filepath.split(".")[-1]

            # Only process known extensions defined in config. `EXTENSIONS`
            # is expected to be a collection (e.g., set or dict keys)
            # imported from `config`.
            if extension in EXTENSIONS:
                subfolder_name = get_subfolder_name_by_extension(extension)
                # Create target subfolder if it doesn't exist.
                self._create_subfolder(subfolder_name)

                # Build the new destination path and rename (move) the file.
                new_path = Path(self.path, subfolder_name, path.name)
                logging.info(f'{path.name} ---> {"/".join(new_path.parts[-2:])}')
                path.rename(new_path)


def main() -> None:
    """Entry point for the script's sorting action.

    Instantiates a Folder for the configured `FOLDER_PATH`, logs and
    prints what it's doing, then triggers the sorting operation.
    """
    folder = Folder(FOLDER_PATH)
    print("Sorting files by extensions in", FOLDER_PATH)
    logging.info(f"Sorting files by extensions in {FOLDER_PATH}")
    folder.sort_files_by_extensions()


if __name__ == "__main__":
    # Measure execution time for basic reporting and logging.
    start_time = time.monotonic()
    main()
    end_time = time.monotonic() - start_time
    print(f"Script execution time: {end_time} seconds")
    logging.info(f"Script execution time: {end_time} seconds")
