# Universal RPG Platform

A game-agnostic tabletop RPG platform powered by Claude Code. Any RPG can be set up from its PDF source books. The platform extracts rules and lore automatically, generates game-specific AI skills, and runs full interactive sessions with a Storyteller AI — including dice mechanics, NPC tracking, session logs, character advancement, and AI-generated scene and portrait images.

---

## How It Works

```
/play <game name>
```

That's the only command you need. The platform handles everything:

- If the game hasn't been set up, it scans `books/` for PDFs, asks which ones to use, extracts the rules and lore, and generates a full set of game skills automatically.
- If the game is already set up, it shows your existing characters and prior sessions.
- Pick a character (or create one) and choose to continue a session or start a new adventure.
- The Storyteller activates with full knowledge of the game's rules, your character sheet, and the session history.

---

## Quickstart

### 1. Add source books

Copy your RPG PDF source books into the `books/` directory:

```
books/
  call_of_cthulhu_7e.pdf
  coc_keeper_rulebook.pdf
```

### 2. Start playing

```
/play Call of Cthulhu
```

The platform will detect that the game hasn't been ingested yet, scan `books/`, ask which PDFs to use, and set everything up. When it's done, you'll go straight into character creation.

### 3. Pick up where you left off

Run the same command again at any time:

```
/play Call of Cthulhu
```

Your characters and session history are shown. Select a character and session to resume exactly where you left off.

---

## Skills

### Permanent (any game)

| Skill | Usage | Description |
|-------|-------|-------------|
| `/play` | `/play <game name>` | Universal entry point. Routes to ingest, character selection, or session resume. |
| `/rpg-ingest` | `/rpg-ingest <slug> "<Game Name>"` | Manually ingest PDFs for a game. Extracts rules/lore and generates the 4 game-specific skills. |

### Game-Specific (generated per game)

After ingesting a game with slug `SLUG`, four skills are created automatically. They only work for that specific game.

| Skill | Description |
|-------|-------------|
| `/SLUG-character` | Interactive, conversational character creation |
| `/SLUG-npc` | Generate a full NPC profile with portrait image |
| `/SLUG-combat` | Run structured combat with dice tracking |
| `/SLUG-advance` | Spend XP and raise traits |

Each generated skill has `game:` and `game_name:` frontmatter that scopes it exclusively to its game — they cannot be accidentally used for another system.

---

## Player Controls During a Session

| Input | Effect |
|-------|--------|
| `{action in curly braces}` | In-game character action |
| `"speech in quotes"` | Character dialogue |
| `<angle brackets>` | Out-of-character note or question |
| `<advance X>` | Spend XP to raise a trait |
| `<award N xp>` | Award XP manually |
| `<save>` | Force an immediate session log write |
| `<quit>` | End session and save everything |

---

## Storyteller Format

Every response from the Storyteller:

- 1000–3000 characters of narrative — vivid scene-setting, NPC dialogue, sensory detail
- Opens with an AI-generated scene image (via Pollinations.ai)
- Ends with exactly **5 numbered choices** in `{curly braces}`
- All dice rolls shown in `(parentheses)` with full breakdown
- Out-of-character notes in `<angle brackets>`

---

## Image Generation

The platform generates images automatically using [Pollinations.ai](https://pollinations.ai) — free, no API key, no account required.

- **Scene images** — generated at the start of each new scene; wide landscape format
- **NPC portraits** — generated when a new NPC is introduced; square portrait format

Images are saved locally and isolated per character so multiple characters in the same game never overwrite each other's images. If there is no network connection, the session continues normally with text only.

---

## Directory Structure

```
books/                          ← Drop PDF source books here before ingesting
RPG/
  [game_slug]/
    _meta.json                  ← Game name, source books, ingest date
    rules/
      char_creation.md          ← Attributes, point allocation, creation steps
      combat.md                 ← Initiative, actions, damage, conditions
      advancement.md            ← XP costs, prerequisites, maximums
      systems.md                ← Core dice mechanic, modifiers, resources
    lore/
      world.md                  ← Setting, factions, cosmology
      tone.md                   ← Genre, atmosphere, narrative style
    characters/
      [name_slug].json          ← Character sheet, updated live during play
    npcs/
      [name_slug].json          ← NPC profile and interaction history
    sessions/
      [char_slug]_YYYY-MM-DD.md ← Session log, scene by scene
    images/
      scenes/
        [char_slug]/            ← Scene images scoped to each character
          scene_1.jpg
      npcs/
        [char_slug]/            ← NPC portraits scoped to each character
          [name_slug].jpg

scripts/
  extract_pdf_text.py           ← Generic PDF → page text extractor
  extract_wod_pdfs.py           ← Column-aware PDF parser (used by extractor)
  generate_image.py             ← Pollinations.ai image downloader

.claude/
  commands/
    play.md                     ← /play skill
    rpg-ingest.md               ← /rpg-ingest skill (also templates for generated skills)
    [slug]-character.md         ← Generated per game — character creation
    [slug]-npc.md               ← Generated per game — NPC generation
    [slug]-combat.md            ← Generated per game — combat management
    [slug]-advance.md           ← Generated per game — XP advancement
```

---

## Scripts

| Script | Description |
|--------|-------------|
| `extract_pdf_text.py` | Extracts all pages from any PDF into numbered `page_NNNN.txt` files. Handles single and two-column layouts. Used by `/rpg-ingest` to process source books. |
| `extract_wod_pdfs.py` | Column-detection and page-text logic. Imported by `extract_pdf_text.py`. |
| `generate_image.py` | Downloads an AI-generated image from Pollinations.ai and saves it locally. Takes a text prompt and output path. Returns JSON. Exits non-zero on failure without crashing the session. |

---

## Requirements

- [Claude Code](https://claude.ai/code) — the CLI or VSCode extension
- Python 3.8+
- [PyMuPDF](https://pymupdf.readthedocs.io/) for PDF extraction: `pip install pymupdf`
- Internet connection for image generation (optional — degrades gracefully without it)

---

## Adding a New Game

1. Copy source PDFs to `books/`
2. Run `/play <game name>`

The platform detects the game is unknown, lists available PDFs, asks which to use, and handles the rest.

To ingest manually with a specific slug:
```
/rpg-ingest my_slug "My Game Name"
```

---

## Notes

- Character JSON files are updated live using atomic writes (temp file → rename) to prevent data loss
- Session logs append scene-by-scene and are never overwritten
- Game-specific skills are fully self-contained — they do not reference other games' rules
- All generated content (game data, characters, images, sessions) stays local and is not pushed to git
