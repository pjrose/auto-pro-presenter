# Bundled ProPresenter themes

These `Theme` files were extracted from the source ProPresenter show for this workflow. They are ProPresenter Protocol Buffer documents, not XML. The associated `Assets` folders were empty; no media files are required by these layouts.

- `Black`: title and main-point slides.
- `Lyrics Centered`: `Top Third - White` lyric slides.
- `Plain Text`: `Central Bible Format` Scripture slides (renamed from `Theme Slide`).

The builder reads the bundled files directly, including when the destination show does not have these themes installed. Run `install_themes.py` with ProPresenter closed to add them to its Theme browser. Existing themes are skipped unless `--replace-existing` is supplied.
