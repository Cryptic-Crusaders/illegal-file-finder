from typing import Iterable, Union
import time
import os

from config import *

from pathlib import Path


# Ensure the logs folder exists before configuring logging.
# Use parents=True and exist_ok=True to be safe on repeated runs.
LOGS_FOLDER.mkdir(parents=True, exist_ok=True)


class Folder:
    """Utility class that represents a folder and provides methods to
    inspect and sort files inside it.

    The class is intentionally lightweight: it stores a path (either a
    Path or a string) and offers helpers that iterate directory
    entries using os.scandir for efficiency.
    """

    def __init__(self, path: Union[Path, str]) -> None:
        # Store the path to operate on as a pathlib.Path for consistent
        # path operations. Accept either a Path or a string.
        self.path = Path(path)

    def _get_subfolder_paths(self) -> Iterable:
        """Yield subfolder paths inside this folder.

        Uses os.scandir which is faster than listdir for large
        directories. Returns generator of path-like strings that can
        be converted to Path objects by the caller.
        """
        # Return actual Path objects for convenience when recursing.
        return (Path(entry.path) for entry in os.scandir(self.path) if entry.is_dir())

    def _get_file_paths(self) -> Iterable:
        """Yield file paths (non-directories) inside this folder.

        This generator excludes directories. Each yielded item is the
        raw path string returned by os.DirEntry.path.
        """
        # Yield Path objects for files inside this folder (non-directories).
        return (
            Path(entry.path) for entry in os.scandir(self.path) if not entry.is_dir()
        )

    def _create_subfolder(self, subfolder_name: str) -> None:
        """Create a subfolder with the given name if it doesn't exist.

        The method uses the `/` operator to build a path relative to
        `self.path` (so `self.path` should be a pathlib.Path). If the
        subfolder already exists, this is a no-op.
        """
        subfolder_path = self.path / subfolder_name
        if not subfolder_path.exists():
            subfolder_path.mkdir(parents=True, exist_ok=True)

    def sort_files_by_extensions(self, recursive: bool = True) -> None:
        """Move files into subfolders based on their file extensions.

        For each file in the folder, determine the extension (text after
        the last dot) and, if the extension is known (present in the
        EXTENSIONS mapping from `config`), move the file into the
        corresponding subfolder named by `get_subfolder_name_by_extension`.

        The original file is renamed (moved) into the new path and an
        INFO log is written for each move.
        """
        # Process files in the current directory first.
        for path in self._get_file_paths():
            # Determine file extension by splitting on '.' and taking the
            # last segment. Files without an extension will be ignored.
            extension = path.name.rsplit(".", 1)[-1] if "." in path.name else ""

            if extension and extension in EXTENSIONS:
                subfolder_name = get_subfolder_name_by_extension(extension)
                # Create target subfolder if it doesn't exist.
                self._create_subfolder(subfolder_name)

                # Build the new destination path and rename (move) the file.
                new_path = self.path / subfolder_name / path.name
                path.rename(new_path)

        # Optionally recurse into existing subfolders to process their files.
        if recursive:
            for subfolder_path in self._get_subfolder_paths():
                # Skip the log folder or any target subfolders to avoid
                # repeatedly moving files between the same subfolders.
                # Only recurse into directories that are not one of the
                # configured SUBFOLDER_NAMES or the logs directory.
                if (
                    subfolder_path.name in SUBFOLDER_NAMES
                    or subfolder_path.name == LOGS_FOLDER.name
                ):
                    # Still recurse into subfolders inside target folders in case
                    # there are nested directories to process; but skip recursing
                    # into the top-level target subfolders to avoid infinite loops.
                    continue

                # Create a Folder for the subfolder and process its files.
                Folder(subfolder_path).sort_files_by_extensions(recursive=True)


def main() -> None:
    """Entry point for the script's sorting action.

    Instantiates a Folder for the configured `FOLDER_PATH`, logs and
    prints what it's doing, then triggers the sorting operation.
    """
    folder = Folder(FOLDER_PATH)
    print("Sorting files by extensions in", FOLDER_PATH)
    folder.sort_files_by_extensions()


if __name__ == "__main__":
    # Measure execution time for basic reporting and logging.
    start_time = time.monotonic()
    main()
    end_time = time.monotonic() - start_time
    print(f"Script execution time: {end_time} seconds")
