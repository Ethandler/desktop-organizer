# Desktop Organizer

## Overview
The Desktop Organizer is a Python script designed to tidy up your desktop by organizing files into categorized folders based on their file types. It helps maintain a clean and visually appealing workspace by grouping files into logical categories such as Documents, Pictures, Videos, Music, Programs, Compressed files, and Others.

---

## Features
- Categorizes files on your desktop into predefined folders:
  - **Documents**: `.pdf`, `.doc`, `.docx`, `.txt`, `.xls`, `.xlsx`, `.ppt`, `.pptx`
  - **Pictures**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.svg`, `.tiff`
  - **Videos**: `.mp4`, `.mkv`, `.mov`, `.avi`, `.flv`, `.wmv`
  - **Music**: `.mp3`, `.wav`, `.aac`, `.flac`, `.ogg`, `.m4a`
  - **Programs**: `.exe`, `.msi`, `.bat`, `.sh`
  - **Compressed**: `.zip`, `.rar`, `.tar`, `.gz`, `.7z`
  - **Others**: Files that do not match any of the above categories.
- Automatically creates folders for each category if they do not already exist.
- Ensures files without an extension or uncategorized files are placed in the **Others** folder.

---

## Prerequisites
Before you begin, ensure you have the following installed:
- **Python 3.6 or later**

---

## Installation
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/your-username/desktop-organizer.git
   ```
2. Navigate to the project directory:
   ```bash
   cd desktop-organizer
   ```

---

## Usage
1. Save the `desktop_organizer.py` script in the directory.
2. Run the script:
   ```bash
   python desktop_organizer.py
   ```
3. Confirm the operation when prompted.
4. The script will categorize and move files into appropriate folders on your desktop.

---

## Example Directory Structure
Before running the script:
```
Desktop/
    file1.jpg
    file2.pdf
    file3.mp3
    randomfile
```

After running the script:
```
Desktop/
    Pictures/
        file1.jpg
    Documents/
        file2.pdf
    Music/
        file3.mp3
    Others/
        randomfile
```

---

## Future Enhancements
- Allow users to define custom categories and extensions.
- Add a dry-run mode to preview the changes before executing.
- Handle duplicate files intelligently (e.g., appending numbers to duplicates).

---

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests to improve this project.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments
Thanks to the Python community for their resources and support!
