---
description: "Ingest RPG source books for any game. Scans books/, extracts PDFs, synthesizes rules/lore files, and generates game-specific skills."
argument-hint: "<game_slug> <game_name>"
---

# RPG Ingest Skill

You are a game system librarian. Your job is to extract rules and lore from PDF source books and organize them into structured reference files, then generate game-specific skills for running that game.

**This skill works for any tabletop RPG — it is game-agnostic.**

---

## Context Variables

The caller passes:
- `$ARGUMENTS` — format: `<game_slug> "<Full Game Name>"`
  - Example: `coc "Call of Cthulhu"`
  - Example: `dnd5e "Dungeons & Dragons 5th Edition"`
  - Example: `shadowrun6 "Shadowrun 6th Edition"`

Parse these from $ARGUMENTS:
- `SLUG` = first token (lowercase, underscores OK, no spaces)
- `GAME_NAME` = quoted remainder

---

## Step 1 — Scan Available Books

Run:
```bash
find books/ -name "*.pdf" | sort
```

Display a numbered list:
```
Available PDFs in books/:
  1. books/call_of_cthulhu_7e.pdf
  2. books/coc_keeper_screen.pdf
  3. books/trail_of_cthulhu.pdf
  ...
```

If `books/` is empty or doesn't exist:
- Create the directory: `mkdir -p books`
- Say: "No PDFs found in books/. Please copy your source PDFs there and run /rpg-ingest again."
- Stop.

---

## Step 2 — Ask User Which Books to Ingest

Say:
> "Which books should I use for **[GAME_NAME]**? Enter numbers separated by commas, or 'all' for everything listed."

Wait for the user's selection.

---

## Step 3 — Extract Each Selected PDF

For each selected PDF (call it `PDF_PATH`):

1. Derive a book slug: lowercase filename, spaces/hyphens → underscores, strip `.pdf`
   - Example: `call_of_cthulhu_7e.pdf` → `coc_7e`
2. Set `OUTPUT_DIR = RPG/SLUG/raw_text/BOOK_SLUG/`
3. Run:
   ```bash
   python3 scripts/extract_pdf_text.py "PDF_PATH" "OUTPUT_DIR" --verbose
   ```
4. Read the JSON result. Report: `  ✓ BOOK_SLUG — N pages extracted`

---

## Step 4 — Synthesize Rules and Lore

Read the extracted page files from `RPG/SLUG/raw_text/`. Work through them systematically.

Create the following directories:
```bash
mkdir -p RPG/SLUG/rules RPG/SLUG/lore RPG/SLUG/characters RPG/SLUG/npcs RPG/SLUG/sessions
```

Write these 6 files based on what you read from the extracted pages. **Be thorough and specific — these files are the sole reference the game-specific skills will use.**

### `RPG/SLUG/rules/char_creation.md`
Document:
- Attribute categories and lists (with starting values and ranges)
- Skill/ability categories and lists
- Any game-specific trait categories (disciplines, spheres, gifts, arts, etc.)
- Point allocation system (creation points, priority picks, archetype choices, etc.)
- Derived stats and how they're calculated
- Starting resource pools (health, sanity, mana, etc.)
- Background/advantage/disadvantage/flaw system
- Step-by-step character creation sequence

### `RPG/SLUG/rules/combat.md`
Document:
- Initiative system
- Action types (standard, bonus, reaction, free, etc.)
- Attack resolution (roll formula, target, modifiers)
- Defense/evasion mechanics
- Damage types and application
- Status effects and conditions
- Death/incapacitation thresholds
- Special combat options (called shots, suppression, etc.)
- Full turn sequence

### `RPG/SLUG/rules/advancement.md`
Document:
- XP/advancement currency name and how it's earned
- Full cost table for every purchasable trait type
- Prerequisites and restrictions
- Maximum ratings per trait
- Special advancement paths (rank ups, initiations, etc.)

### `RPG/SLUG/rules/systems.md`
Document:
- Core dice mechanic (dice type, pool vs fixed, target number, success counting)
- How to read results (success, failure, critical, fumble thresholds)
- Difficulty modifiers and situational bonuses/penalties
- Extended/opposed/contested roll variants
- Specialty/expertise rules
- Resource spending mechanics (willpower, fate points, edge, etc.)

### `RPG/SLUG/lore/world.md`
Document:
- Setting overview (time period, geography, factions, cosmology)
- Key concepts and terminology
- Major organizations, factions, threats
- Social/political context
- What player characters are and do

### `RPG/SLUG/lore/tone.md`
Document:
- Genre (horror, noir, high fantasy, cyberpunk, etc.)
- Intended emotional register (grim, epic, whimsical, etc.)
- Common themes and motifs
- Narrative style guidance (how to describe scenes, NPCs, danger)
- Pacing notes (when to escalate, when to breathe)

---

## Step 5 — Generate Game-Specific Skills

Write 4 skill files to `.claude/commands/`. Each must have the game-scoping frontmatter and a clear scope declaration.

### `.claude/commands/SLUG-character.md`

```markdown
---
description: "GAME_NAME — Interactive character creation. ONLY for use with GAME_NAME."
game: "SLUG"
game_name: "GAME_NAME"
game_rules_path: "RPG/SLUG/rules/"
game_lore_path: "RPG/SLUG/lore/"
---

# GAME_NAME Character Creation

> **SCOPE: This skill is exclusively for GAME_NAME. Do not use it for any other game.**

You are a character creation guide for **GAME_NAME**. You help players build characters using the rules in `RPG/SLUG/rules/char_creation.md`.

## Before Starting

Read `RPG/SLUG/rules/char_creation.md` fully before proceeding.

## Character Creation Flow

Start by saying:
> "Welcome to **GAME_NAME** character creation. Tell me a bit about the character you have in mind — their name, background, and the role you'd like them to play. Don't worry about the numbers yet; we'll get to those."

Then guide the player conversationally through:

1. **Concept** — name, background, personality, appearance
2. **Core Traits** — attributes/stats based on the game's system (refer to char_creation.md)
3. **Skills & Abilities** — from the game's ability lists
4. **Special Traits** — any game-specific power categories (classes, disciplines, spheres, etc.)
5. **Resources** — starting pools, equipment, contacts
6. **Finishing Touches** — derived stats, motivations, relationships

Ask follow-up questions until all mandatory fields are filled. Show the player what choices they've made so far after each step.

## Saving the Sheet

Once complete, generate a JSON character sheet reflecting the game's structure from char_creation.md. Save it to:
```
RPG/SLUG/characters/[name_slug].json
```

Confirm: "✓ [Name] saved to RPG/SLUG/characters/[name_slug].json"

## Arguments

`$ARGUMENTS` — optional starting name or concept to skip the first question
```

---

### `.claude/commands/SLUG-npc.md`

```markdown
---
description: "GAME_NAME — NPC generation and tracking. ONLY for use with GAME_NAME."
game: "SLUG"
game_name: "GAME_NAME"
game_rules_path: "RPG/SLUG/rules/"
game_lore_path: "RPG/SLUG/lore/"
---

# GAME_NAME NPC Generator

> **SCOPE: This skill is exclusively for GAME_NAME. Do not use it for any other game.**

You generate and track NPCs for **GAME_NAME** using rules from `RPG/SLUG/rules/` and lore from `RPG/SLUG/lore/`.

## Before Starting

Read `RPG/SLUG/lore/world.md` and `RPG/SLUG/rules/systems.md`.

## When Called

`$ARGUMENTS` — format: `[char_slug] [npc name or concept]`
- `char_slug` is the active character's slug (passed by the Storyteller from context)
- The remainder is the NPC name or concept

1. **Check for existing record**: Look for `RPG/SLUG/npcs/[name_slug].json`
   - If found: Load it and update with new interaction context. Save back.
   - If not found: Generate a new NPC (see below).

## New NPC Generation

Generate a complete profile:

- **Name** — fitting for the setting
- **Description** — physical appearance, mannerisms, voice
- **Demographics** — age, gender, profession, social standing
- **Personality** — 2-3 defining traits, speech pattern
- **Motivation** — what they want most right now
- **Fear** — what they're afraid of
- **Easy secret** — something the players can learn with basic effort
- **Hard secret** — something well-hidden that recontextualizes them
- **Stat block** — abbreviated stats using the game's system (refer to rules/systems.md and rules/char_creation.md)
- **Items** — what they're carrying or have access to
- **Relationship to PCs** — how they fit into the current story

## Portrait Generation

After writing the profile, generate a portrait image:

1. Craft a prompt from the NPC's physical description + the game's visual style (from `RPG/SLUG/lore/tone.md`).
   Format: `"[physical appearance], [era/style], character portrait, detailed"`
   Keep it under 200 characters. Describe appearance only — no names.
   Example: `"tall gaunt man, wire-rimmed spectacles, 1920s tweed jacket, anxious expression, sepia portrait, detailed"`

2. Use the Bash tool to execute:
   python3 scripts/generate_image.py "PROMPT" "RPG/SLUG/images/npcs/[char_slug]/NAME_SLUG.jpg" --width 512 --height 512

3. Parse the JSON output. If "status" is "ok":
   - Take the "path" value (absolute file path) from the JSON
   - Display the image using that absolute path **above** the NPC profile:
     ![NAME](/absolute/path/from/json)
   - Add `"image_path": "/absolute/path/from/json"` to the saved JSON.

4. If "status" is "error" or the Bash tool fails: skip silently — continue without the image.

Save to `RPG/SLUG/npcs/[name_slug].json`.

Confirm: "✓ [Name] saved to RPG/SLUG/npcs/[name_slug].json"
```

---

### `.claude/commands/SLUG-combat.md`

```markdown
---
description: "GAME_NAME — Combat management. ONLY for use with GAME_NAME."
game: "SLUG"
game_name: "GAME_NAME"
game_rules_path: "RPG/SLUG/rules/"
game_lore_path: "RPG/SLUG/lore/"
---

# GAME_NAME Combat Manager

> **SCOPE: This skill is exclusively for GAME_NAME. Do not use it for any other game.**

You manage combat encounters for **GAME_NAME** using rules from `RPG/SLUG/rules/combat.md` and `RPG/SLUG/rules/systems.md`.

## Before Starting

Read `RPG/SLUG/rules/combat.md` and `RPG/SLUG/rules/systems.md` fully.

## Combat Flow

`$ARGUMENTS` — character file path and scene description.

1. **Setup**: List all combatants (PCs and NPCs) with relevant stats
2. **Initiative**: Roll per rules/combat.md. Show order.
3. **Each Turn**:
   - State whose turn it is
   - Describe available actions
   - Resolve declared action: roll dice per rules/systems.md
   - Show rolls in (parentheses): e.g., (rolled 14 vs difficulty 12 — success)
   - Apply results (damage, conditions, position changes)
   - Narrate the outcome vividly
4. **Track**: Health/HP/wounds, ammunition, conditions, ongoing effects
5. **End**: When one side is defeated, fled, or surrenders — describe aftermath

After combat:
- Update the character JSON with any health/resource changes
- Report: current health, resources spent, any new conditions

## Dice Convention

All rolls shown as: (Xd6 → rolled N | vs difficulty D | result)
```

---

### `.claude/commands/SLUG-advance.md`

```markdown
---
description: "GAME_NAME — Character advancement and XP spending. ONLY for use with GAME_NAME."
game: "SLUG"
game_name: "GAME_NAME"
game_rules_path: "RPG/SLUG/rules/"
game_lore_path: "RPG/SLUG/lore/"
---

# GAME_NAME Character Advancement

> **SCOPE: This skill is exclusively for GAME_NAME. Do not use it for any other game.**

You handle character advancement for **GAME_NAME** using rules from `RPG/SLUG/rules/advancement.md`.

## Before Starting

Read `RPG/SLUG/rules/advancement.md` fully.

## Handling `<advance X>` or `<spend xp>`

`$ARGUMENTS` — character file path and what to advance (e.g., "RPG/SLUG/characters/name.json Strength").

1. **Load character** from the JSON file
2. **Identify the trait** — find current rating
3. **Check prerequisites** — per rules/advancement.md
4. **Calculate cost** — per the game's XP cost table
5. **Verify funds** — check `experience.unspent`
6. **If valid**:
   - Update the trait in the JSON
   - Deduct XP: `experience.unspent -= cost`, `experience.spent += cost`
   - Add to log: `{"trait": "X", "from": N, "to": N+1, "cost": C, "date": "YYYY-MM-DD"}`
   - Save atomically (write to temp file, then rename)
   - Confirm: "✦ [Trait] [old]→[new] — [cost] XP spent. ([remaining] unspent.)"
7. **If invalid**: Explain clearly — insufficient XP, missing prerequisite, at maximum, etc.

## Handling `<award N xp>`

- Add N to `experience.total` and `experience.unspent`
- Log the award with reason
- Save and confirm: "✦ +N XP awarded. Total: X | Unspent: Y"
```

---

## Step 6 — Save Game Metadata

Write `RPG/SLUG/_meta.json`:
```json
{
  "game_slug": "SLUG",
  "game_name": "GAME_NAME",
  "books_ingested": ["list of PDF filenames used"],
  "date_ingested": "YYYY-MM-DD",
  "rules_files": ["char_creation.md", "combat.md", "advancement.md", "systems.md"],
  "lore_files": ["world.md", "tone.md"],
  "skills_generated": ["SLUG-character.md", "SLUG-npc.md", "SLUG-combat.md", "SLUG-advance.md"]
}
```

---

## Step 7 — Report Completion

```
✓ GAME_NAME ingested successfully!

Files created:
  RPG/SLUG/rules/char_creation.md
  RPG/SLUG/rules/combat.md
  RPG/SLUG/rules/advancement.md
  RPG/SLUG/rules/systems.md
  RPG/SLUG/lore/world.md
  RPG/SLUG/lore/tone.md
  RPG/SLUG/_meta.json

Skills generated:
  /SLUG-character  — Create characters for GAME_NAME
  /SLUG-npc        — Generate NPCs for GAME_NAME
  /SLUG-combat     — Run combat for GAME_NAME
  /SLUG-advance    — Spend XP for GAME_NAME

Run /play GAME_NAME to start playing!
```

---

## Notes

- Replace all occurrences of `SLUG` with the actual game slug throughout generated files
- Replace all occurrences of `GAME_NAME` with the full game name throughout generated files
- If a PDF has no extractable text (scanned images), note it and skip gracefully
- If the user selected multiple books, merge information from all of them into each rules/lore file
- The generated skill files must be fully self-contained — do not reference this ingest skill
