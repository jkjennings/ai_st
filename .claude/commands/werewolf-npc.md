---
description: "Werewolf: The Apocalypse 20th Anniversary — NPC generation and tracking. ONLY for use with Werewolf: The Apocalypse 20th Anniversary Edition."
game: "werewolf"
game_name: "Werewolf: The Apocalypse 20th Anniversary Edition"
game_rules_path: "RPG/werewolf/rules/"
game_lore_path: "RPG/werewolf/lore/"
---

# Werewolf: The Apocalypse 20th Anniversary — NPC Generator

> **SCOPE: This skill is exclusively for Werewolf: The Apocalypse 20th Anniversary Edition. Do not use it for any other game.**

You generate and track NPCs for **Werewolf: The Apocalypse 20th Anniversary Edition** using rules from `RPG/werewolf/rules/` and lore from `RPG/werewolf/lore/`.

## Before Starting

Read `RPG/werewolf/lore/world.md`, `RPG/werewolf/lore/tone.md`, and `RPG/werewolf/rules/systems.md`.

## When Called

Arguments provide the NPC name or concept (e.g., "elder Fianna Galliard", "Pentex VP", "lost Kinfolk girl").

### 1. Check for Existing Record
Look for `RPG/werewolf/npcs/[name_slug].json`.
- **Found:** Load it, update with new interaction context and any changed details, save back.
- **Not found:** Generate a new NPC (see below).

---

## New NPC Generation

### Types of W20 NPCs
Consider which category applies before building:
- **Garou NPC:** Tribe, Auspice, Breed, Rank, Gifts, Renown
- **Kinfolk:** Human or wolf relative of a Garou; aware of the world but cannot shapeshift
- **Human NPC:** Corporate, criminal, civilian, hunter, etc.
- **Fomori:** Wyrm-possessed human or animal; partially monstrous
- **Black Spiral Dancer:** Corrupted Garou; always hostile
- **Spirit:** Totem, Bane, Lune, Engling, etc. — treat as NPCs with Essence pools instead of Willpower
- **Other Supernatural:** Vampire, mage, changeling encountered in the World of Darkness

### Generate a Complete Profile

```json
{
  "name": "Full Name",
  "name_slug": "lowercase_underscores",
  "type": "garou|kinfolk|human|fomori|spirit|bsd|other",
  "tribe": "(if Garou)",
  "auspice": "(if Garou)",
  "breed": "(if Garou)",
  "rank": "(1-6 if Garou)",
  "physical_description": "Appearance, bearing, notable features",
  "personality": ["Trait 1", "Trait 2", "Defining quirk"],
  "voice_and_manner": "How they speak; what their presence feels like",
  "motivation": "What they want most right now",
  "fear": "What keeps them up at night",
  "easy_secret": "What players can learn with basic effort",
  "hard_secret": "What is well-hidden and recontextualizes them",
  "stats": {
    "attributes": {"strength": 0, "dexterity": 0, "stamina": 0,
                   "charisma": 0, "manipulation": 0, "appearance": 0,
                   "perception": 0, "intelligence": 0, "wits": 0},
    "abilities_notable": ["Brawl 4", "Melee 3", "Stealth 3"],
    "rage": 0,
    "gnosis": 0,
    "willpower": 0,
    "health_levels": 7,
    "gifts": [],
    "special_notes": ""
  },
  "items": ["What they carry or have access to"],
  "relationship_to_pcs": "How they connect to the current story",
  "first_impression": "One sentence the player characters would form on meeting them",
  "interaction_history": []
}
```

### Stat Guidelines by NPC Role
| Type | Attributes | Rage | Gnosis | Willpower |
|------|------------|------|--------|-----------|
| Minor human | 2–3 in most | 0 | 0 | 2–3 |
| Experienced human | 3–4 in specialty | 0 | 0 | 3–4 |
| Kinfolk | 2–4 | 0 | 0–2 | 3–5 |
| Rank 1–2 Garou | 2–4 | 1–4 | 1–4 | 3–4 |
| Rank 3–4 Garou | 3–5 | 3–6 | 3–6 | 4–6 |
| Elder (Rank 5–6) | 4–6 | 5–8 | 4–8 | 5–8 |
| Fomori (weak) | 3–5 | 0 | 0 | 2–4 |
| Black Spiral Dancer | 3–6 | 3–8 | 2–6 | 3–6 |

---

## Updating Existing NPCs

When the NPC appears again:
1. Load the JSON.
2. Add a new entry to `interaction_history`: `{"session": "YYYY-MM-DD", "summary": "what happened", "attitude_change": "if any"}`
3. Update `motivation`, `fear`, or stats if events changed them.
4. Save back to the file.

---

## Saving

Save to: `RPG/werewolf/npcs/[name_slug].json`

Confirm: "✓ [Name] saved to RPG/werewolf/npcs/[name_slug].json"

Then provide a 2–3 sentence in-world description of how the NPC would appear to the characters.
