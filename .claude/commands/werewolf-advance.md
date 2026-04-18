---
description: "Werewolf: The Apocalypse 20th Anniversary — Character advancement and XP spending. ONLY for use with Werewolf: The Apocalypse 20th Anniversary Edition."
game: "werewolf"
game_name: "Werewolf: The Apocalypse 20th Anniversary Edition"
game_rules_path: "RPG/werewolf/rules/"
game_lore_path: "RPG/werewolf/lore/"
---

# Werewolf: The Apocalypse 20th Anniversary — Character Advancement

> **SCOPE: This skill is exclusively for Werewolf: The Apocalypse 20th Anniversary Edition. Do not use it for any other game.**

You handle character advancement for **Werewolf: The Apocalypse 20th Anniversary Edition** using rules from `RPG/werewolf/rules/advancement.md`.

## Before Starting

Read `RPG/werewolf/rules/advancement.md` fully.

## Handling `<advance X>` or `<spend xp>`

Arguments provide the character file path and what to advance (e.g., "RPG/werewolf/characters/name.json Strength" or "Brawl 4" or "Gift: Razor Claws").

### Process

1. **Load the character** from their JSON file.

2. **Identify the trait** — find current rating. If the trait is a Gift, check its level.

3. **Check prerequisites:**
   - Gifts: Character's Rank must be ≥ Gift level.
   - Abilities: No special prerequisites unless Storyteller has set them.
   - Rage: Note that higher Rage increases frenzy risk (roleplay warning).
   - Gifts from other breed/auspice/tribe: Requires appropriate spirit teacher and Storyteller approval.
   - Traits can only be raised by 1 dot per story.

4. **Calculate XP cost** per `advancement.md`:

   | Trait | Cost |
   |-------|------|
   | Attribute | Current rating × 4 |
   | Ability (existing) | Current rating × 2 |
   | Ability (new, 0 dots) | 3 |
   | Gift (own breed/auspice/tribe) | Level × 3 |
   | Gift (other) | Level × 5 |
   | Rage | Current rating × 1 |
   | Gnosis | Current rating × 2 |
   | Willpower | Current rating × 1 |
   | Rite | Level × 2 |
   | Renown (perm dot) | 3 |

5. **Verify funds** — check `experience.unspent` in the character JSON.

6. **If valid:**
   - Update the trait value in the JSON.
   - Deduct XP: `experience.unspent -= cost`, `experience.spent += cost`
   - Add to log:
     ```json
     {"trait": "TraitName", "from": N, "to": N+1, "cost": C, "date": "YYYY-MM-DD"}
     ```
   - Save atomically (write to temp file, then rename to original).
   - Confirm:
     > "✦ [Trait] [old]→[new] — [cost] XP spent. ([remaining] unspent XP remaining.)"
   - Resume scene with one brief flavor line describing how the character feels the new capability taking hold.

7. **If invalid — explain clearly:**
   - Insufficient XP: "You need [cost] XP but only have [unspent] unspent."
   - Missing prerequisite: "Rank [N] required to learn a Level [N] Gift. You are currently Rank [current]."
   - At maximum: "[Trait] is already at its maximum rating of [max]."
   - Restricted: "[Trait] cannot be raised with XP (only through Storyteller-driven play)."
   - Already advanced this story: "You've already raised a Trait once this story. Wait for the next story."

---

## Handling `<award N xp>`

When the Storyteller awards XP:
1. Add N to `experience.total` and `experience.unspent`.
2. Add to log:
   ```json
   {"award": N, "reason": "Scene/session description", "date": "YYYY-MM-DD"}
   ```
3. Save the character JSON.
4. Confirm:
   > "✦ +[N] XP awarded. Total: [total] | Unspent: [unspent]"

---

## Handling Renown Awards

When the Storyteller awards Renown:
1. Add the specified permanent Renown to the appropriate category (glory/honor/wisdom) in the character JSON.
2. Check if the new total meets the threshold for rank advancement (see advancement.md).
3. If rank advancement is possible, announce:
   > "⬆ [Name]'s permanent [Glory/Honor/Wisdom] is now [N]. Total permanent renown: [sum]. [They may now seek advancement to Rank X / They have reached the threshold for Rank X advancement — a challenge must be arranged.]"
4. Save the character JSON.

---

## Rank Advancement Process

When a character's renown meets the threshold AND they complete a challenge:
1. Update `rank` in the JSON: `rank += 1`
2. Add to advancement log.
3. Note: new Gifts of the new Rank level are now available for purchase.
4. Confirm:
   > "⬆⬆ [Name] advances to Rank [N] ([Rank Title])! New Level [N] Gifts are now available."

---

## Saving the File

Always save atomically:
1. Write updated JSON to a temp file (same directory, `.tmp` extension).
2. Rename temp file to replace the original.
3. This prevents data loss if writing is interrupted.
