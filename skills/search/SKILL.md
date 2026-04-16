# Skill: search
# Locates files across nested folder structures

## Purpose
When a CSV file is missing from its expected location, the search skill
scans all subfolders until the file is found or all paths are exhausted.

## Function: `find_file(filename, folders, main_folder) → str | None`

```python
import os

def find_file(filename, folders, main_folder):
    """
    Search for `filename` inside each folder under `main_folder`.

    Returns:
        Full path (str) if found, else None.
    """
    for folder in folders:
        path = os.path.join(main_folder, folder, filename)
        if os.path.exists(path):
            return path
    return None
```

## Usage
```python
folders = [d for d in os.listdir("Output")
           if os.path.isdir(os.path.join("Output", d))]

path = find_file("csv_3.csv", folders, "Output")
if path:
    print(f"Found at: {path}")
else:
    print("File not found in any folder — skipping")
```

## Behavior
- Search order follows `os.listdir()` order (filesystem order)
- Returns on **first match** — does not continue after finding
- Returns `None` (never raises) if not found — caller decides how to handle
- Does **not** recurse deeper than one level (folder → file, not folder → subfolder → file)

## Extension Ideas
- Add `recursive=True` flag for deep search
- Accept a list of extensions to match (e.g., only `.csv`)
- Return all matches instead of just the first