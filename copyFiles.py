# This script was generated with ChatGPT

import os
import sys
import shutil
from pathlib import Path
import traceback


def main():
    # Resolve script directory (script may be launched from another CWD)
    script_dir = Path(__file__).resolve().parent

    # -----------------------------
    # IMAGE COPY SETTINGS
    # -----------------------------

    # Source root: ../drafts/assets/img/map/
    src_root_img = (script_dir / ".." / "drafts" / "assets" / "img" / "map").resolve()

    # Destination root: ./img/map/
    dst_root_img = (script_dir / "img" / "map").resolve()

    maps = [2, 3, 4, 5]

    allowed_img_ext = {".png", ".jpg", ".jpeg"}

    # -----------------------------
    # META JSON COPY SETTINGS
    # -----------------------------

    # Source: ../drafts/assets/meta/map/*.json
    src_root_meta = (script_dir / ".." / "drafts" / "assets" / "meta" / "map").resolve()

    # Destination: ./data/map/
    dst_root_meta = (script_dir / "data" / "map").resolve()

    # -----------------------------
    # IMAGE COPY
    # -----------------------------

    total_img_found = 0
    total_img_copied = 0
    total_img_errors = 0

    print("=== IMAGE COPY ===")
    print(f"Script directory: {script_dir}")
    print(f"Source root:      {src_root_img}")
    print(f"Destination root: {dst_root_img}")
    print("")

    if not src_root_img.exists():
        print(f"ERROR: Image source root does not exist: {src_root_img}")
    else:
        for m in maps:
            src_dir = src_root_img / f"map{m}p"
            dst_dir = dst_root_img / f"map{m}p"

            print(f"--- map{m}p ---")
            print(f"From: {src_dir}")
            print(f"To:   {dst_dir}")

            if not src_dir.exists():
                print("WARNING: Source folder not found, skipping.\n")
                continue

            dst_dir.mkdir(parents=True, exist_ok=True)

            img_files = [
                p for p in src_dir.iterdir()
                if p.is_file() and p.suffix.lower() in allowed_img_ext
            ]

            total_img_found += len(img_files)

            if not img_files:
                print("No image files found.\n")
                continue

            for src_file in img_files:
                dst_file = dst_dir / src_file.name
                try:
                    shutil.copy2(src_file, dst_file)
                    total_img_copied += 1
                    print(f"COPIED: {src_file.name}")
                except Exception:
                    total_img_errors += 1
                    print(f"ERROR copying: {src_file.name}")
                    traceback.print_exc()

            print("")

    # -----------------------------
    # META JSON COPY
    # -----------------------------

    total_json_found = 0
    total_json_copied = 0
    total_json_errors = 0

    print("=== META JSON COPY ===")
    print(f"Source:      {src_root_meta}")
    print(f"Destination: {dst_root_meta}")
    print("")

    if not src_root_meta.exists():
        print(f"ERROR: Meta source folder does not exist: {src_root_meta}")
    else:
        dst_root_meta.mkdir(parents=True, exist_ok=True)

        json_files = [
            p for p in src_root_meta.iterdir()
            if p.is_file() and p.suffix.lower() == ".json"
        ]

        total_json_found = len(json_files)

        if not json_files:
            print("No JSON files found.")
        else:
            for src_file in json_files:
                dst_file = dst_root_meta / src_file.name
                try:
                    shutil.copy2(src_file, dst_file)
                    total_json_copied += 1
                    print(f"COPIED: {src_file.name}")
                except Exception:
                    total_json_errors += 1
                    print(f"ERROR copying: {src_file.name}")
                    traceback.print_exc()

    # -----------------------------
    # SUMMARY
    # -----------------------------

    print("\n==== SUMMARY ====")
    print(f"Images found:   {total_img_found}")
    print(f"Images copied:  {total_img_copied}")
    print(f"Image errors:   {total_img_errors}")
    print("")
    print(f"JSON found:     {total_json_found}")
    print(f"JSON copied:    {total_json_copied}")
    print(f"JSON errors:    {total_json_errors}")

    return 1 if (total_img_errors or total_json_errors) else 0


if __name__ == "__main__":
    try:
        exit_code = main()
    except Exception:
        print("FATAL ERROR:")
        traceback.print_exc()
        exit_code = 2
    finally:
        input("\nPress Enter to exit...")

    sys.exit(exit_code)
