# Skill: file_writer
# Handles all file and folder creation, copying, and deletion

## Functions

### `create_folder(path)`
```python
import os

def create_folder(path):
    os.makedirs(path, exist_ok=True)
    print(f"[folder_writer] Created: {path}")
```

---

### `copy_file(src, dst)`
```python
import shutil, os

def copy_file(src, dst):
    if os.path.exists(src):
        shutil.copy(src, dst)
        print(f"[file_writer] Copied: {src} → {dst}")
    else:
        print(f"[file_writer] WARNING: Source not found: {src}")
```

---

### `delete_file(path)`
```python
def delete_file(path):
    if os.path.exists(path):
        os.remove(path)
        print(f"[file_writer] Deleted: {path}")
    else:
        print(f"[file_writer] SKIP: File not found: {path}")
```

---

### `build_folder_assignments(files, files_per_folder=3)`
Generates circular combos to assign files across folders.

```python
def build_folder_assignments(files, files_per_folder=3):
    n = len(files)
    return [
        [files[(i + j) % n] for j in range(files_per_folder)]
        for i in range(n)
    ]
```

## Notes
- All operations are idempotent — safe to re-run
- Failures are logged but do not raise exceptions (warn and continue)
- `build_folder_assignments` wraps around using modulo arithmetic