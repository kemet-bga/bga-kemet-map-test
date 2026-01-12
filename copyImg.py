# Generated with ChatGPT
import os
import sys
import shutil
from pathlib import Path
import traceback


def main():
    # Resolve script directory (script may be launched from another CWD)
    script_dir = Path(__file__).resolve().parent

    # Source root: ../drafts/assets/img/map/
    src_root = (script_dir / ".." / "drafts" / "assets" / "img" / "map").resolve()

    # Destination root: ./img/map/
    dst_root = (script_dir / "img" / "map").resolve()

    maps = [2, 3, 4, 5]

    # Allowed image extensions
    allowed_ext = {".png", ".jpg", ".jpeg"}

    total_found = 0
    total_copied = 0
    total_errors = 0

    print(f"Script directory: {script_dir}")
    print(f"Source root:      {src_root}")
    print(f"Destination root: {dst_root}")
    print("")

    if not src_root.exists():
        print(f"ERROR: Source root does not exist: {src_root}")
        return 2

    for m in maps:
        src_dir = src_root / f"map{m}p"
        dst_dir = dst_root / f"map{m}p"

        print(f"=== map{m}p ===")
        print(f"From: {src_dir}")
        print(f"To:   {dst_dir}")

        if not src_dir.exists():
            print("WARNING: Source folder not found, skipping.")
            print("")
            continue

        # Create destination folder and all missing parents
        dst_dir.mkdir(parents=True, exist_ok=True)

        # Only image files from the top level (no subfolders)
        img_files = [
            p for p in src_dir.iterdir()
            if p.is_file() and p.suffix.lower() in allowed_ext
        ]

        total_found += len(img_files)

        if not img_files:
            print("No image files found.")
            print("")
            continue

        for src_file in img_files:
            dst_file = dst_dir / src_file.name
            try:
                shutil.copy2(src_file, dst_file)
                total_copied += 1
                print(f"COPIED: {src_file.name}")
            except Exception:
                total_errors += 1
                print(f"ERROR copying: {src_file.name}")
                traceback.print_exc()

        print("")

    print("==== Summary ====")
    print(f"Images found:  {total_found}")
    print(f"Images copied: {total_copied}")
    print(f"Errors:        {total_errors}")

    return 1 if total_errors else 0


if __name__ == "__main__":
    try:
        exit_code = main()
    except Exception:
        print("FATAL ERROR:")
        traceback.print_exc()
        exit_code = 2
    finally:
        # Pause so the console window doesn't close
        input("\nPress Enter to exit...")

    sys.exit(exit_code)
