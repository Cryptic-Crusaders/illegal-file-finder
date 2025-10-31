# File sorter

![GitHub last commit](https://img.shields.io/github/last-commit/Cryptic-Crusaders/illegal-file-finder)
![GitHub repo size](https://img.shields.io/github/repo-size/Cryptic-Crusaders/illegal-file-finder)

Python script for finding illegal files in a Cyber Patriot competiton. Fork of [lesskop/file-sorter](https://github.com/lesskop/file-sorter).

## Quick start

1. Open [config.py](config.py) and write the path to the folder where the sort will be performed:

```python
FOLDER_PATH = Path('drive:/folder/another-folder/yet-another-folder')
```

Example

```python
FOLDER_PATH = Path('D:/Downloads')
```

2. Set up a dictionary `SUBFOLDER_NAME_TO_EXTENSIONS` for your sorting method.

**Key** - subfolder name, **value** - tuple of file extensions for this subfolder.

```python
SUBFOLDER_NAME_TO_EXTENSIONS = {
    'video': ('mp4', 'mov', 'avi', 'mkv', 'wmv', 'mpg', 'mpeg', 'm4v', 'h264'),
    'audio': ('mp3', 'wav', 'ogg', 'flac', 'aif', 'mid', 'midi', 'wma'),
    'image': ('jpg', 'png', 'bmp', 'jpeg', 'svg', 'tif', 'tiff'),
    'archive': ('zip', 'rar', '7z', 'z', 'gz', 'pkg', 'deb'),
    'text': ('pdf', 'txt', 'doc', 'docx', 'rtf', 'odt'),
    'spreadsheet': ('xlsx', 'xls', 'xlsm'),
    'presentation': ('pptx', 'ppt'),
    'book': ('fb2', 'epub', 'mobi'),
    'gif': ('gif',),
    # 'subfolder-name': ('extension', 'another-extension')
}
```

## Logs

You can check the logs in `logs/file_sorter.log` after script execution.

```
[18:08:01] INFO - Sorting files by extensions in d:\downloads
[18:08:01] INFO - winrar.zip ---> archive/winrar.zip
[18:08:01] INFO - cute cat.png ---> image/cute cat.png
[18:08:01] INFO - dissertation.docx ---> text/dissertation.docx
[18:08:01] INFO - Morbius.mkv ---> video/Morbius.mkv
[18:08:01] INFO - mvp.pptx ---> presentation/mvp.pptx
[18:08:01] INFO - salary.xlsx ---> spreadsheet/salary.xlsx
[18:08:01] INFO - there are no passwords.txt ---> text/there are no passwords.txt
[18:08:01] INFO - Script execution time: 0.01600000000144064 seconds
```
