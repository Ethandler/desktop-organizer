import os
import shutil

# Define categories and corresponding file extensions
CATEGORIES = {
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"],
    "Pictures": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".tiff"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv"],
    "Music": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
    "Programs": [".exe", ".msi", ".bat", ".sh"],
    "Compressed": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Others": []  # Files not matching any category
}

def organize_desktop(directory):
    """
    Organizes the desktop into categorized folders.
    """
    if not os.path.exists(directory):
        print(f"The directory '{directory}' does not exist!")
        return

    # Create folders for categories
    for category in CATEGORIES:
        folder_path = os.path.join(directory, category)
        os.makedirs(folder_path, exist_ok=True)

    # Move files into corresponding categories
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)

        # Skip directories (don't organize folders)
        if os.path.isdir(file_path):
            continue

        # Determine the file's category
        file_ext = os.path.splitext(file)[1].lower()
        moved = False
        for category, extensions in CATEGORIES.items():
            if file_ext in extensions:
                shutil.move(file_path, os.path.join(directory, category, file))
                moved = True
                break

        # If the file doesn't match any category, move to "Others"
        if not moved:
            shutil.move(file_path, os.path.join(directory, "Others", file))

    print("Desktop has been organized into categories!")

if __name__ == "__main__":
    # Get the desktop path
    desktop_path = os.path.join(os.environ["USERPROFILE"], "Desktop")

    # Confirm the operation
    print(f"Organizing files on your desktop: {desktop_path}")
    proceed = input("Do you want to proceed? (yes/no): ").strip().lower()
    if proceed in ["yes", "y"]:
        organize_desktop(desktop_path)
    else:
        print("Operation cancelled.")
