# Manifest format

The manifest is UTF-8 JSON. A lyric-only service needs `playlist_date` and `songs`; sermon keys are optional:

```json
{
  "playlist_date": "YYYY-MM-DD",
  "songs": [],
  "sermon_name": "YYYY-MM-DD",
  "sermon_title": ["Title", "Subtitle", "Bible reference"],
  "sermon_slides": []
}
```

Songs appear in playlist order. For an existing song:

```json
{"name": "Existing title", "use_existing": true,
 "fixes": [{"from": "exact phrase", "to": "corrected phrase", "expected_count": 1}]}
```

The `fixes` array is optional. A fix changes only that RTF text fragment and fails if its count differs. Use the exact library presentation name, including capitalization, for `name`.

For an optional looping background on any song, add:

```json
"background_video": {
  "source": "C:\\path\\verified-1920x1080.mp4",
  "duration": 15.02,
  "frame_rate": 60
}
```

The builder copies the MP4 into the show's `Media/Downloads/Service Backgrounds` folder and attaches it to the first cue with loop playback. `duration` is seconds; use the actual file values, not the stock-site listing. Keep source URL and license details in a separate download record for attribution and audit.

For a new song:

```json
{"name": "New title", "source_pptx": "C:\\path\\song.pptx", "key": "C",
 "sections": [{"name": "Verse 1", "slides": [1, 2]},
              {"name": "Chorus", "slides": [3, 4]}],
 "corrections": {"2": "Corrected line 1\nCorrected line 2"}}
```

Slide numbers are one-based PPTX positions. Every nonempty PPTX slide must appear in one section exactly once. Empty PPTX divider slides are skipped automatically. `corrections` replaces the full text of a chosen slide. Each new song gets a blank Background cue before the listed sections. The cue groups form ProPresenter's Master. If a section with the same name and text appears twice in the PPTX, the builder creates one Master group and repeats it in the Normal arrangement. See `examples/practice-service.json`.

Sermon slides appear in order after the title slide:

```json
{"type": "point", "text": "BOLDED ALL-CAPS PHRASE"}
{"type": "verse", "reference": "Hechos 20:17", "text": "17 Verse text"}
```

The builder places each verse on its own slide with the reference and `(RVR1960)` label. If a different translation is requested, update that label in the builder before use. Verse text must be checked against the translation rather than trusted from a rough PDF extraction. Leave the sermon keys out entirely if Bible access is unavailable; the song playlist can still be built. If a verse has no text, the builder skips the sermon, explains why, and still stages the lyric playlist.
