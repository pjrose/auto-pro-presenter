"""Install the bundled ProPresenter themes into a show's Themes folder."""
from __future__ import annotations

import argparse
from datetime import datetime
import os
from pathlib import Path
import shutil
import subprocess

THEMES = ("Black", "Lyrics Centered", "Plain Text")


def app_is_running() -> bool:
    if os.name != "nt":
        return False
    result = subprocess.run(["tasklist", "/FI", "IMAGENAME eq ProPresenter.exe", "/FO", "CSV"],
                            capture_output=True, text=True, check=True)
    return '"ProPresenter.exe"' in result.stdout


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--show-root", type=Path, required=True)
    parser.add_argument("--name", action="append", choices=THEMES,
                        help="Install only this theme; repeat to choose more than one")
    parser.add_argument("--replace-existing", action="store_true",
                        help="Back up and replace themes already installed")
    args = parser.parse_args()
    if app_is_running():
        raise RuntimeError("Close ProPresenter before installing themes")
    show = args.show_root.resolve()
    names = args.name or THEMES
    backup = show / "ThemeBackups" / datetime.now().strftime("%Y%m%d-%H%M%S")
    for name in names:
        source = Path(__file__).parent / "themes" / name / "Theme"
        if not source.is_file():
            raise FileNotFoundError(source)
        target = show / "Themes" / name / "Theme"
        if target.exists():
            if not args.replace_existing:
                print(f"Skipped existing {name}")
                continue
            saved = backup / name / "Theme"
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, saved)
        target.parent.mkdir(parents=True, exist_ok=True)
        temp = target.with_name("Theme.codex-new")
        shutil.copy2(source, temp)
        os.replace(temp, target)
        print(f"Installed {name}: {target}")
    if backup.exists():
        print(f"Backups: {backup}")


if __name__ == "__main__":
    main()
