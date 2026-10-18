# ProPresenter Service Builder

**[Leer esta guía en español →](README.es.md)**

Turn the files you already receive for Sunday into a ProPresenter playlist. Give Codex the song PowerPoints, the worship order, and, if you have them, sermon notes. It can prepare editable lyrics, put the songs in order, and add simple sermon slides. You review the result in ProPresenter before the service.

![ProPresenter showing the library and dated playlists on the left](docs/images/propresenter-overview.png)

## Try it in a few minutes

Start ProPresenter and enable **Settings → Network → Enable Network** before
preparing a service. Run `python check_setup.py` first. It reads the configured
Windows port and checks the local API, stopping immediately if Network is off
or after at most eight seconds if the API does not respond. There are no retries
or computer-use fallback. On another platform, or with a different endpoint,
pass `--api-url http://127.0.0.1:PORT` (or set `PROPRESENTER_API_URL`).

Normal `service_builder.py` staging performs the same check before reading
service files. The later `--apply` step intentionally skips it because
ProPresenter must be closed. Repository instructions in `AGENTS.md` authorize
routine graceful restarts and the standard quit confirmation, and require a
maximized window for visual review. Discarding unsaved work is not authorized.

The practice files contain an original four-slide song. They are safe to use for a rehearsal and need no Bible license.

1. Download this repository and open its folder in Codex. Start ProPresenter once on this computer so it creates its show folder.
2. Paste this message into Codex:

   > Use the `propresenter-service-builder` skill in this repository. Try `examples/practice-song.pptx` with `examples/practice-service.json`. Find my ProPresenter show folder. Check the setup, stage the practice playlist, install it when ProPresenter is closed, then reopen ProPresenter and show me what to review. Do not add a sermon or video for this practice run.

3. Look for playlist **2099-01-01**. Open **Luz en el camino (Practice)**. It should begin with a blank **Background** cue, then Verse 1, Chorus, Verse 2, and Chorus again. The song's **Master** groups contain one copy of the chorus; the **Normal** arrangement repeats it in the running order. Delete the practice playlist in ProPresenter when you are done.

You can also open [the practice sermon notes](examples/practice-sermon-notes.pdf). They show what a short sermon outline looks like. Preparing its Bible slide requires access to the requested Bible text; the lyric practice does not.

## Your usual Sunday workflow

**What you give Codex:** the service date and song order, one PPTX per new song, and any key or capo notes. Optionally add a PDF or DOCX of the sermon notes and ask for a motion background. A screenshot of an existing ProPresenter style also helps.

**What Codex prepares:**

- A dated playlist, with songs in the order you gave.
- Editable lyrics in the **Lyrics** library. Existing songs are reused when their lyrics and arrangement fit. Codex checks the PPTX against the library, calls out missing phrases, and can make reviewed text corrections. New songs receive section groups such as Verse, Chorus, and Bridge, a **Master** group list, a **Normal** running arrangement, and a blank first **Background** cue.
- Optional Full HD (1920 × 1080) video on the Background cue. Codex checks the actual video size and records where it came from. Video files are optional and are not included in this repository.
- Optional sermon presentation in **Central en Espanol**. It has a title slide, a slide for each bold, ALL CAPS main point, and slides for the cited Bible passages. Other outline notes stay off screen.

Try this weekly message, changing the date and attaching your files:

> Prepare our ProPresenter service for 2026-10-04. Songs, in order: [list titles]. I attached one PPTX per song and the pastor's sermon notes. Reuse songs already in Lyrics when they match. Use our bundled lyric theme for new songs. Make a dated playlist and a simple sermon in Central en Espanol. Use Reina-Valera 1960 for Bible verses if it is available. Tell me what needs review before Sunday. If that Bible is unavailable, finish the lyrics and explain what I need to ask our ProPresenter administrator for.

Codex first checks the files and the existing library, then prepares a reviewable draft. Installation happens while ProPresenter is closed so the app does not overwrite the new files. Open the playlist afterwards and inspect the slides on the actual output screen.

### What the result looks like

The screenshot above shows where ProPresenter keeps **Libraries** and dated **Playlists**. In a song, the first cue is **Background**, followed by the lyric groups. A sermon starts with its title, then shows Bible passages using **Central Bible Format** and large main points on a black background. Song slides use **Lyrics Centered → Top Third - White**. Your media and preview panes may look different.

## Libraries, themes, and a new computer

| Name in ProPresenter | What goes there |
| --- | --- |
| **Lyrics** library | Song presentations. The tool reuses an existing song when possible. |
| **Central en Espanol** library | Sermon presentations. |
| A playlist named by date | The service running order. |

The repository includes three portable themes in [`themes/`](themes/README.md):

| Theme | Used for |
| --- | --- |
| **Lyrics Centered → Top Third - White** | All song lyrics, including reused songs. |
| **Black** | Sermon title and main points. |
| **Plain Text → Central Bible Format** | Bible verses and references. This is the renamed plain Bible layout. |

On a new ProPresenter installation, start the app once. When Codex installs the first service, the builder creates the missing **Lyrics** and **Central en Espanol** folders, playlist file, and bundled themes. Existing themes are left alone. If the themes are missing from the Theme browser, close ProPresenter and ask Codex to run `install_themes.py`. Fonts may vary slightly between computers. Check the projector preview before Sunday. [Renewed Vision explains themes here](https://support.renewedvision.com/hc/en-us/articles/11910559859603-Themes-in-ProPresenter).

The repository does **not** bundle a ProPresenter license, Bible translation, worship songs, or stock videos. Keep the congregation's source files and any media downloads in the church's approved storage.

## Bible access and sermon notes

The lyric workflow works without a paid Bible. For sermon verses, Codex must verify the exact text and translation. If **Reina-Valera 1960 (RV1960)** is unavailable in ProPresenter, it should finish the song playlist, leave the sermon Bible slides pending, and tell you what is missing. You may also provide verse text that your church is authorized to use. It will not silently switch translations.

To check in ProPresenter, open **Bible → Options → Bibles**. Ask your ProPresenter administrator for the church's registered license and the RV1960 Bible if needed. Renewed Vision says licensed translations require a registered ProPresenter license and an unlock purchase; its [Bible installation guide](https://support.renewedvision.com/hc/en-us/articles/360041814913-Installing-Bibles-in-ProPresenter) explains the steps. RV1960 appears on its [available translation list](https://support.renewedvision.com/hc/en-us/articles/33122394289043-Bible-Translations-Available-for-ProPresenter).

For a sermon PDF or DOCX, the assistant reads the title, Bible references, and phrases that are **both bold and in ALL CAPS**. It checks the extracted text with you if the PDF is scanned or formatting is ambiguous. Each main point gets its own slide. Bible text is added only after the requested translation has been checked. The lower-level builder expects a reviewed list of exact slide text; it does not perform Bible lookup on its own.

## The short Sunday review

Before projection, check the playlist order, song keys and section order, repeated choruses, spelling and accents, video playback, Bible wording and reference, and sermon main points. Review the **audience output** on your 1920 × 1080 screen. The first Background cue may be blank or have a looping video; the lyric cues stay editable. The assistant can help fix anything you spot.

## For the person setting up the tool

The Codex skill lives at [`skill/propresenter-service-builder/SKILL.md`](skill/propresenter-service-builder/SKILL.md). When this folder is open in Codex, ask it to use that skill. You can copy the skill folder into your Codex skills directory if you want it available from other folders. The skill is the friendly workflow: it reads PPTX/PDF/DOCX, checks the ProPresenter library and Bible availability, prepares the reviewed manifest, runs the scripts, and checks the app. The Python script only builds from a manifest.

For a manual run on Windows, install Python dependencies and change the show path to the folder ProPresenter uses on your computer:

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe check_setup.py --show-root 'C:\Users\YOURNAME\Documents\ProPresenter'
.venv\Scripts\python.exe service_builder.py examples\practice-service.json `
  --show-root 'C:\Users\YOURNAME\Documents\ProPresenter' `
  --stage '.\stage\practice'
```

Run from the repository folder so the example's relative PPTX path resolves. The first builder run **stages** files only. With ProPresenter closed, repeat the command with `--apply` to back up changed files and install them. The program refuses to apply while ProPresenter is running. [Manifest fields and examples](skill/propresenter-service-builder/references/manifest.md) are available for people who want to prepare one by hand.

The workflow was tested with ProPresenter 18.4.1 on Windows. The generated files use [community Protocol Buffer bindings](https://github.com/greyshirtguy/ProPresenter7-Proto) under their included MIT license. ProPresenter does not publish this file format as a stable interface; verify the staged and installed result after app upgrades. The starter presentation and playlist in [`templates/`](templates/) contain no song lyrics. Existing songs keep their cue IDs, arrangements and media, receive the lyric theme and Full HD sizing, and receive text corrections only when explicitly requested; adding missing sections to an existing presentation needs a reviewed edit in ProPresenter or a deliberate rebuild.

### Consistent lyrics and Full HD slides

The builder applies **Lyrics Centered → Top Third - White** to new and reused songs, preserving the text stroke, background blur and text-line mask. It retains the theme’s RTF styling and applies its capitalization to the whole lyric instead of copying placeholder character ranges. Reused slides with multiple text elements stop for review rather than being overlaid.

All generated song and sermon slides are **1920×1080**. Every older cue in a reused song is resized too, including the first Background cue, because that cue can determine ProPresenter’s presentation size. Element bounds scale with the canvas. Reused files are staged and backed up on installation. This does not change the configured audience screen resolution; check that separately and review the composed output with the Valley background playing.

Regression checks: `python -m unittest discover -s tests -v` (requires local loopback access for the network tests).
