"""Read-only setup check for a ProPresenter show folder."""
from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--show-root", type=Path, required=True)
    args = parser.parse_args()
    show = args.show_root.expanduser().resolve()
    print(f"ProPresenter show folder: {show}")
    if not show.is_dir():
        print("Not found. Start ProPresenter once and ask Codex to locate its show folder.")
        return
    if not any(show.iterdir()):
        print("This folder is empty. Start ProPresenter once before installing a service.")
        return
    for label, rel in (
        ("Lyrics library", "Libraries/Lyrics"),
        ("Central en Espanol library", "Libraries/Central en Espanol"),
        ("Playlist library", "Playlists/Library"),
        ("Lyrics Centered theme", "Themes/Lyrics Centered/Theme"),
        ("Black theme", "Themes/Black/Theme"),
        ("Plain Text theme", "Themes/Plain Text/Theme"),
    ):
        print(f"{'Ready' if (show / rel).exists() else 'Will create when applied'}: {label}")
    print("Bible access: check in ProPresenter > Bible > Options > Bibles.")
    print("For sermon verses, install Reina-Valera 1960 (RV1960) with the church license, or provide approved verse text.")
    print("Lyrics and playlists can be prepared without Bible access.")


if __name__ == "__main__":
    main()
