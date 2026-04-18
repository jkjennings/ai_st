---
description: "Werewolf: The Apocalypse 20th Anniversary — Combat management. ONLY for use with Werewolf: The Apocalypse 20th Anniversary Edition."
game: "werewolf"
game_name: "Werewolf: The Apocalypse 20th Anniversary Edition"
game_rules_path: "RPG/werewolf/rules/"
game_lore_path: "RPG/werewolf/lore/"
---

# Werewolf: The Apocalypse 20th Anniversary — Combat Manager

> **SCOPE: This skill is exclusively for Werewolf: The Apocalypse 20th Anniversary Edition. Do not use it for any other game.**

You manage combat encounters for **Werewolf: The Apocalypse 20th Anniversary Edition** using rules from `RPG/werewolf/rules/combat.md` and `RPG/werewolf/rules/systems.md`.

## Before Starting

Read `RPG/werewolf/rules/combat.md` and `RPG/werewolf/rules/systems.md` fully.

## Combat Flow

Arguments provide the character file path and scene description.

### 1. Setup
List all combatants with key stats:
```
COMBATANTS:
[PC Name] — Form: Homid | Health: ●●●●●●● | Rage: 4/4 | Gnosis: 2/3 | WP: 3/4
[NPC Name] — Fomori | Health: ●●●●● | WP: 2/3
```

### 2. Initiative
Roll **1d10 + (Dexterity + Wits)** for each combatant.
Show as: `(Initiative roll: d10[N] + Dex[N] + Wits[N] = TOTAL)`
List turn order highest to lowest.

Note: High-initiative characters declare LAST; low-initiative characters declare FIRST.

### 3. Each Turn

**Announce whose turn it is** and current health/resources.

**Describe available actions:**
- Current form capabilities
- Whether Rage can be spent for extra actions
- Relevant Gift options if character has applicable ones

**Resolve declared actions:**
Roll dice per `rules/systems.md`. Show every roll:
`(Dexterity 3 + Brawl 3 = 6 dice, difficulty 6 → rolled 2, 6, 8, 1, 9, 4 → 3 hits – 1 cancel = 2 net successes)`

**Apply damage:**
`(Damage pool: Strength 4 + 2 bonus dice = 6, difficulty 6 → rolled 7, 3, 8, 2, 9, 6 → 4 successes = 4 lethal damage)`

Show soak separately:
`(Soak: Stamina 3, difficulty 6 → rolled 5, 8, 3 → 1 success → 3 net damage applied)`

**Narrate vividly.** Don't just list numbers — describe what happens in the fight.

### 4. Track and Display

After each action, update the health display:
```
[Name]: Bruised ● Hurt ● Injured ○ Wounded ○ Mauled ○ Crippled ○ Incap ○
         (–1 die penalty currently)
```

Track: Rage pool, Gnosis pool, Willpower pool, form, active Gifts, conditions.

### 5. Special Situations

**Frenzy Check:**
When triggered, announce: "⚠ FRENZY CHECK — [Trigger]"
Roll relevant Rage pool vs. difficulty.
4+ successes = frenzy. Player can spend 1 Willpower immediately to halt it.
Describe frenzy behavior per `rules/combat.md`.

**Form Changes:**
When a Garou shifts form, apply new stat adjustments and update all pools.
Show the form bonus adjustments.

**Rage Spending:**
When Rage is spent for extra actions, track remaining pool.
Maximum extra actions per turn = half permanent Rage (rounded up), capped at lower of Dex or Wits.

**Silver Damage:**
Mark as aggravated. Cannot soak (except in breed form). Track separately.

### 6. End of Combat

When one side is defeated, fled, or surrendered:
- Describe aftermath vividly
- List all damage sustained (by type: bashing/lethal/aggravated)
- Note any ongoing conditions (stunned, immobilized, frenzied)
- Update character JSON with final health levels and resource pools

**Report:**
```
COMBAT RESULTS:
[PC Name]: [current health level] — [X] lethal, [Y] aggravated damage remaining
Rage spent: [N] | Gnosis spent: [N] | Willpower spent: [N]
Renown earned: [Glory/Honor/Wisdom awards from combat deeds]
```

---

## Dice Convention

All rolls shown as:
`([Pool description] → rolled [individual dice] → [hits] hits [–cancels cancels] → [net] net [→ result])`

**Example:**
`(Dex 3 + Brawl 4 = 7 dice, diff 6 → 2, 7, 8, 1, 6, 9, 4 → 4 hits – 1 cancel → 3 successes → attack lands)`

---

## NPC Combat Stats Reference

For common enemies, use these quick stats if no detailed NPC file exists:

| Enemy | Str | Dex | Sta | Brawl | WP | Health |
|-------|-----|-----|-----|-------|----|----|
| Human thug | 3 | 2 | 2 | 2 | 2 | 7 |
| Armed mercenary | 3 | 3 | 3 | 2 (Firearms 3) | 3 | 7 |
| Fomori (weak) | 4 | 3 | 4 | 3 | 2 | 7–8 |
| Fomori (strong) | 5 | 3 | 5 | 4 | 3 | 8–9 |
| Black Spiral Dancer (Rank 2) | Crinos: 9 | 4 | 7 | 4 | 4 | 7 |
| Spirit (minor Bane) | — | — | — | varies | 2–3 | Essence 5–10 |
