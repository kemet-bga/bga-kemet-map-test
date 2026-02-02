#! python3.13
# This script was generated with the help of ChatGPT
#
# Purpose:
# Copy selected files from source to destination using rules from JSON file.
# Overwrite destination ONLY if it doesn't exist OR its content differs from the source.
#
# Optimization:
# - First compares file size.
# - If sizes match, then compares file content (filecmp.cmp(..., shallow=False)).
#
# Dual-use design:
# - When run directly (e.g., double-click from Explorer): prints errors and pauses on error only.
# - When imported and called from other scripts: raises exceptions (no pause) and returns results.
#
# Notes:
# - By default, copyFiles.json must be located near this script
# - Relative paths are resolved relative to the script folder (or a provided base_dir)
# - Destination folders are created automatically
# - If destination ends with "\" or "/" -> treated as directory
# - Copy preserves timestamps/metadata (shutil.copy2)

from __future__ import annotations

try:
    import os
    import shutil
    import json
    import filecmp
    from typing import Iterable, List, Tuple, Optional, Dict


    class CopyRuleError(ValueError):
        """Raised when copy rules format is invalid."""


    def get_script_dir() -> str:
        """Return directory of this script file."""
        return os.path.dirname(os.path.abspath(__file__))


    def resolve_path(path: str, base_dir: str) -> str:
        """Resolve path relative to base_dir and normalize."""
        abs_path = os.path.join(base_dir, path)
        return os.path.normpath(abs_path)


    def destination_is_directory(dst_path: str) -> bool:
        """Treat destination as directory if it ends with a slash."""
        return dst_path.endswith("\\") or dst_path.endswith("/")


    def build_destination_path(dst_path: str, src_abs_path: str, base_dir: str) -> str:
        """
        If dst_path ends with slash -> treat as directory and append source file name.
        Otherwise treat as full destination file path.
        """
        dst_abs = resolve_path(dst_path, base_dir)

        if destination_is_directory(dst_path):
            src_name = os.path.basename(src_abs_path)
            return os.path.normpath(os.path.join(dst_abs, src_name))

        return dst_abs


    def load_rules_from_json(config_path: str) -> List[Tuple[str, str]]:
        """
        Load rules from a JSON file. Expects:
          { "copy_rules": [ ["src", "dst"], ... ] }
        Returns list of (src, dst) strings (as given in JSON).
        """
        if not os.path.isfile(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        rules = data.get("copy_rules")
        if not isinstance(rules, list):
            raise CopyRuleError("'copy_rules' must be a list")

        parsed: List[Tuple[str, str]] = []
        for rule in rules:
            if not isinstance(rule, list) or len(rule) != 2:
                raise CopyRuleError(f"Invalid rule format: {rule!r}. Expected [src, dst].")
            src_path, dst_path = rule
            if not isinstance(src_path, str) or not isinstance(dst_path, str):
                raise CopyRuleError(f"Invalid rule types: {rule!r}. src and dst must be strings.")
            parsed.append((src_path, dst_path))

        return parsed


    def same_size(src_abs: str, dst_abs: str) -> bool:
        """Return True if both files exist and have the same size in bytes."""
        try:
            return os.path.getsize(src_abs) == os.path.getsize(dst_abs)
        except OSError:
            return False


    def files_are_identical(src_abs: str, dst_abs: str) -> bool:
        """
        Return True if dst exists and has exactly the same content as src.

        Optimization:
        - If destination doesn't exist -> False
        - If file sizes differ -> False
        - If sizes match -> compare file content (byte-for-byte)
        """
        if not os.path.isfile(dst_abs):
            return False

        # Fast reject: different sizes => different content
        if not same_size(src_abs, dst_abs):
            return False

        # Sizes match: compare content
        return filecmp.cmp(src_abs, dst_abs, shallow=False)


    def ensure_parent_dir(path_abs: str) -> None:
        """Create parent directories for path_abs if needed."""
        dst_dir = os.path.dirname(path_abs)
        if dst_dir:
            os.makedirs(dst_dir, exist_ok=True)


    def copy_file_if_needed(src_abs: str, dst_abs: str) -> bool:
        """
        Copy src_abs -> dst_abs ONLY if:
        - dst_abs does not exist, OR
        - dst_abs content differs from src_abs

        Returns True if copied, False if skipped.
        """
        if not os.path.isfile(src_abs):
            raise FileNotFoundError(f"Source file not found: {src_abs}")

        if files_are_identical(src_abs, dst_abs):
            return False  # skip

        ensure_parent_dir(dst_abs)
        shutil.copy2(src_abs, dst_abs)
        return True


    def copy_by_rules(
        rules: Iterable[Tuple[str, str]],
        *,
        base_dir: str,
        verbose: bool = True,
    ) -> Dict[str, int]:
        """
        Copy files by explicit rules [(src, dst), ...].
        - base_dir controls how relative paths are resolved.
        - Returns a dict with counters: {"copied": X, "skipped": Y}
        - Raises exceptions on any error (good for importing/automation).
        """
        copied = 0
        skipped = 0

        for src_path, dst_path in rules:
            src_abs = resolve_path(src_path, base_dir)
            dst_abs = build_destination_path(dst_path, src_abs, base_dir)

            did_copy = copy_file_if_needed(src_abs, dst_abs)
            if did_copy:
                copied += 1
                if verbose:
                    print(f"Copied:  {src_abs} -> {dst_abs}")
            else:
                skipped += 1
                if verbose:
                    print(f"Skipped (identical): {src_abs} -> {dst_abs}")

        return {"copied": copied, "skipped": skipped}


    def copy_by_config(
        config_path: str,
        *,
        base_dir: Optional[str] = None,
        verbose: bool = True,
    ) -> Dict[str, int]:
        """
        Copy files using rules from JSON config.
        - If base_dir is None, defaults to directory of the config file.
        - Returns dict with counters: {"copied": X, "skipped": Y}
        - Raises exceptions on any error.
        """
        config_abs = os.path.abspath(config_path)

        if base_dir is None:
            base_dir = os.path.dirname(config_abs)

        rules = load_rules_from_json(config_abs)
        return copy_by_rules(rules, base_dir=base_dir, verbose=verbose)


    def default_config_path_near_script() -> str:
        """Default config path: copy_rules.json near this script."""
        return os.path.join(get_script_dir(), "copyFiles.json")


    def run_as_explorer_script() -> int:
        """
        Entry point for double-click/Explorer usage:
        - catches any exception
        - prints error
        - pauses only on error
        Returns an exit code: 0 success, 1 error.
        """
        had_error = False
        try:
            config_path = default_config_path_near_script()
            result = copy_by_config(config_path, base_dir=get_script_dir(), verbose=True)

            print("-" * 40)
            print(f"Total copied:  {result['copied']}")
            print(f"Total skipped: {result['skipped']}")
            print("Done.")
            return 0

        except Exception as e:
            had_error = True
            print("ERROR:")
            print(e)
            return 1

        finally:
            if had_error:
                input("Press Enter to exit...")


    if __name__ == "__main__":
        run_as_explorer_script()

except Exception as _fatal:
    # Catch any import-time / top-level errors so Explorer users can see them.
    print("FATAL ERROR:")
    print(_fatal)
    input("Press Enter to exit...")
