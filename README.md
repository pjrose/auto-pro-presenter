# ProPresenter service builder

This local tool creates editable lyric presentations, a simple sermon presentation, a dated playlist, and optional looping motion backgrounds from a reviewed JSON manifest. It targets ProPresenter 18's Protocol Buffer files. Existing songs are reused; specified text fixes are applied in place without rebuilding their arrangements.

## Setup

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The `vendor` directory contains generated Python bindings for the [unofficial ProPresenter file schema](https://github.com/greyshirtguy/ProPresenter7-Proto), whose MIT license is included. ProPresenter does not publish this file format as a stable interface, so inspect the staged result after app updates.

`themes/` contains the three theme files used by the builder: `Black`, `Lyrics Centered`, and `Plain Text`. The Bible layout within `Plain Text` is named `Central Bible Format`. The builder reads these bundled files, so the source computer does not need the themes installed. To make the layouts available in ProPresenter's Theme browser on another computer, close ProPresenter and run:

```powershell
.venv\Scripts\python.exe install_themes.py --show-root 'C:\Users\USER\Documents\ProPresenter'
```

Existing themes are skipped by default. Add `--replace-existing` to back them up and replace them. The themes use system fonts, including Helvetica Light; ProPresenter may substitute a font if it is unavailable on the destination computer.

## Run

```powershell
.venv\Scripts\python.exe service_builder.py service.json `
  --show-root 'C:\Users\USER\OneDrive\Documents\ProPresenter' `
  --stage '.\stage\service-date'
```

This only writes staged files. Review the files and the printed song order. When ProPresenter is closed, add `--apply` to back up the original playlist and any modified song files, then install the staged files. The script refuses to apply while ProPresenter is running. Reopen ProPresenter and inspect the playlist, song groups, backgrounds, verse text, and output preview.

The Codex skill in `skill/propresenter-service-builder` describes how to prepare the manifest from the worship order, song PPTX files, and sermon outline. The manifest is deliberately explicit: a reviewer chooses section boundaries and the exact passages and phrases to display. The tool does not infer those from names alone.
