# Manifest format

The manifest is UTF-8 JSON with these top-level keys:

```json
{
  "playlist_date": "YYYY-MM-DD",
  "sermon_name": "YYYY-MM-DD",
  "sermon_title": ["Title", "Subtitle", "Bible reference"],
  "songs": [],
  "sermon_slides": []
}
```

Songs appear in playlist order. For an existing song:

```json
{"name": "Existing title", "use_existing": true,
 "fixes": [{"from": "exact phrase", "to": "corrected phrase", "expected_count": 1}]}
```

The `fixes` array is optional. A fix changes only that RTF text fragment and fails if its count differs. Use the exact library presentation name, including capitalization, for `name`.

For a new song:

```json
{"name": "New title", "source_pptx": "C:\\path\\song.pptx", "key": "C",
 "sections": [{"name": "Verse 1", "slides": [1, 2]},
              {"name": "Chorus", "slides": [3, 4]}],
 "corrections": {"2": "Corrected line 1\nCorrected line 2"}}
```

Slide numbers are one-based PPTX positions. Every nonempty PPTX slide must appear in one section exactly once. Empty PPTX divider slides are skipped automatically. `corrections` replaces the full text of a chosen slide. Each new song gets a blank Background cue before the listed sections.

Sermon slides appear in order after the title slide:

```json
{"type": "point", "text": "BOLDED ALL-CAPS PHRASE"}
{"type": "verse", "reference": "Hechos 20:17", "text": "17 Verse text"}
```

The builder places each verse on its own slide with the reference and `(RVR1960)` label. If a different translation is requested, update that label in the builder before use. Verse text must be checked against the translation rather than trusted from a rough PDF extraction.
