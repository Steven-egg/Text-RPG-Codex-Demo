# Naming Lexicon v0.1

Purpose: lightweight naming lexicon and batch worksheet for Element Maze display
canon passes. This file helps generate and select names for monsters, Bosses,
items, equipment, materials, quests, dungeons, skills, books, recipes, and
facility flavor. It does not approve runtime logic, data IDs, schema, save,
combat formulas, GUI implementation, bridge expansion, or asset-pipeline work.

Use this file with:

- `01_content/world-content-skeleton-v0.1.md`
- `01_content/blueprints/regional-canon-debt-policy-v0.1.md`
- `01_content/blueprints/regional-data-template-v0.1.md`
- `01_content/blueprints/regional-data-instantiation-plan-v0.1.md`

## Core Rule

Separate stable logic identifiers from changeable display canon.

First-pass naming work should change only player-facing fields such as:

- `name`
- `title`
- `desc`
- short facility copy
- quest display text

Do not change these in a display canon pass:

- runtime IDs
- flags
- unlock keys
- turn-in requirements
- stats
- drops
- prices
- formulas
- registry grouping
- schema contracts
- save data

Internal IDs can stay slot-like or older-semantic while display names evolve.
Formal ID cleanup is a later identifier canon pass and requires a read-only
runtime / data / schema planning gate.

## Naming Workflow

Use this small workflow before any batch rename:

1. Pick one region or one display category.
2. Select terms from this lexicon.
3. Generate 2-3 candidate names per slot.
4. Owner chooses the names.
5. Patch display fields only.
6. Run focused validation.
7. Record any adopted words back into this file if they become reusable.

For large batches, prefer this order:

1. Dungeons and region hub.
2. Bosses.
3. Normal monsters.
4. Materials.
5. Quest titles and descriptions.
6. Items, equipment, books, skills, recipes.
7. Facility flavor and NPC text.

## Formula Basics

Keep common names short enough for CLI display.

### Monster Formulas

| Formula | Example |
|---|---|
| `region_trait + creature_type` | 霜根獵蛛 |
| `place_trait + role_type` | 殘塔弩手 |
| `condition + creature_type` | 鎖誓亡者 |
| `material_trait + construct_type` | 霜鐵禁衛 |
| `hazard_trait + spirit_type` | 裂碑幽魂 |

### Boss Formulas

| Formula | Example |
|---|---|
| `title + personal_name` | 霜冠誓王 亞爾溟 |
| `place_title + personal_name` | 幽帆舵主 維爾洛 |
| `role_title + personal_name` | 斷階守誓者 奧登 |
| `entity_title + personal_name` | 霜根母株 葛魯姆 |

### Material Formulas

| Formula | Example |
|---|---|
| `place_trait + object` | 幽帆朽木片 |
| `hazard_trait + fragment` | 裂碑碎石塊 |
| `region_material + refined_form` | 霜鐵精煉合金 |
| `story_concept + proof` | 溟藍誓約之證 |

### Equipment Formulas

| Formula | Example |
|---|---|
| `material + equipment_type` | 霜鐵長劍 |
| `place_trait + equipment_type` | 幽帆短弓 |
| `role_trait + armor_type` | 守誓者鎧甲 |
| `story_trait + relic_like_noun` | 終印護符 |

## Shared Word Pools

### Creature Types

| Group | Words |
|---|---|
| Humanlike | 水手、船員、弩手、守衛、禁衛、騎士、法師、斥候、獵人、祭司、工匠、盜匪 |
| Beast | 狼、熊、犬、蟹、蛇、蛛、蟲、甲獸、殼獸、翼獸 |
| Plant / Fungus | 根、藤、母株、花、蕈妖、苔靈、孢子體、樹靈 |
| Spirit / Undead | 幽魂、亡者、殘影、怨靈、洞靈、白靈、陰影、骸骨、鏈奴 |
| Construct | 石衛、石像兵、哨衛、魔偶、鎧甲、守門者、刻印靈 |

### Boss Titles

舵主、母株、守誓者、誓王、看守者、守門者、領主、主祭、將軍、隊長、守衛長、逆法師、封印者、殘王、古王。

### Material Objects

木片、帆布、碎石、粉塵、核心、結晶、合金、鎖鏈、印記、殘片、甲殼、爪、牙、骨、皮、根鬚、孢子、花粉、羽、角、油、液、證物。

### Equipment Types

劍、長劍、短劍、匕首、戰斧、長槍、弓、法杖、錘、盾、鎧甲、皮甲、長袍、兜帽、護符、戒指、披風、靴、手套、頭盔。

### Item / Consumable Types

藥水、藥膏、香、符、投擲瓶、炸彈、護符、抗性藥、解毒劑、回魔藥、補給包、營火石、冷卻粉、鎮靜劑。

## Regional Lexicon

### Fire / Border Route

Current role: legacy demo route and fire-route reference. Do not reopen broad
Fire runtime without a planning gate.

Mood words:

- 灰燼、焦土、熔岩、爐心、燼印、火痕、黑煙、燃渣、裂谷、灼石

Place words:

- 苔洞、焦礦、灰燼峽、燼印深窟、封爐、火脈、熔岩井、燒毀礦道

Creature words:

- 灰鼠、火蜥、熔犬、焦骨、熔岩蟲、爐心守衛、灰燼亡者、火印法師

Boss title words:

- 灰燼守衛、熔岩看守者、燼印哨兵、火痕領主、爐心守門者

Material words:

- 火石、熔岩碎片、精煉火石、灰燼粉、焦黑骨片、爐心渣、火痕殘片

### Ice

Current role: first display canon pilot region. IDs stay stable; display names
may evolve.

Adopted hub / dungeon direction:

| Slot | Display canon |
|---|---|
| Region hub | 霧笛港 |
| Minor A | 幽帆沉船 |
| Minor B | 霜根岩窟 |
| Main phase 1 | 霜鐵古城 - 斷階外城 |
| Main phase 2 | 霜鐵古城 - 終印誓殿 |

Mood words:

- 霧笛、霜潮、冷海、碎冰、鹽霧、濕石、幽帆、霜根、霜鐵、終印、誓約、溟藍、石鏈、深海封印

Place words:

- 港、沉船、底艙、岩窟、外城、斷階、殘塔、迴廊、誓殿、王座、封印、斷橋、海岬、冰礁

Adopted normal monster names:

| Dungeon | Display names |
|---|---|
| 幽帆沉船 | 黑牙亡水手、鹽霧弩手、鐵鉤船員、幽帆瞭望手 |
| 霜根岩窟 | 霜根獵蛛、凍爪穴熊、冰刺蕈妖、藍光洞靈 |
| 斷階外城 | 斷階石衛、裂碑幽魂、殘塔弩手、迴廊石像兵 |
| 終印誓殿 | 霜鐵禁衛、鎖誓亡者、封印鏈奴、碎印法師 |

Adopted Boss names:

| Slot | Display canon |
|---|---|
| Minor A Boss | 幽帆舵主 維爾洛 |
| Minor B Boss | 霜根母株 葛魯姆 |
| Main phase 1 Boss | 斷階守誓者 奧登 |
| Main phase 2 Boss | 霜冠誓王 亞爾溟 |

Useful material candidates:

- 海風濕石粉、幽帆朽木片、結霜幽苔、裂碑碎石塊、斷誓鐵鎖鏈、霜鐵精煉合金、溟藍誓約之證、逆流珊瑚法杖頭

Useful item / equipment candidates:

- 霧笛藥水、鹽霧抗寒藥、幽帆短弓、霜鐵長劍、斷階守衛盾、終印護符、溟藍法杖、鎖誓者鎧甲

### Earth

Current role: playable skeleton landed; display canon still open.

Mood words:

- 根、苔、森林環、古木、菌光、毒霧、採石場、地脈石、腐殖土、石脈、深根、蘑菇洞

Place words:

- 根落林、老採石場、地脈林、深心樹庭、根網、菌洞、苔橋、石環、古井、地下根廳

Creature words:

- 根靈、苔獸、蕈妖、孢子蟲、石殼獸、採石傀儡、藤縛亡者、地脈看守、毒苔獵手

Boss title words:

- 根守者、採石巨像、地脈領主、深心守衛、菌冠母株、古根誓者

Material words:

- 苔壤、根纖維、琥珀孢子、風化採石、地脈碎片、深根核心、古木樹脂、菌光粉

Item / equipment words:

- 苔壤藥膏、根網護符、採石戰錘、地脈長槍、菌光法袍、深根盾、古木弓

### Thunder

Current role: playable skeleton landed; display canon still open.

Mood words:

- 風暴、高原、浮石、雷塔、導電水渠、雲橋、電弧、雷冠、風道、響雷、天路、暴雨

Place words:

- 風暴高原、導電水道、低層陣列、雷冠塔、浮石道路、避雷尖塔、雲階、雷鳴平台

Creature words:

- 雷雀、電弧蛇、風暴狼、導電甲蟲、雲路哨兵、雷塔弩手、電流法師、浮石魔偶

Boss title words:

- 高原信標、通道守衛、雷冠領主、風暴司令、雲橋看守、雷塔主祭

Material words:

- 風暴玻璃、導電礦砂、浮石碎片、雷鳴芯、雲鐵、電弧結晶、雨蝕銅線

Item / equipment words:

- 風暴藥劑、導電護符、雷冠長槍、雲鐵甲、浮石靴、電弧匕首、雷鳴法杖

### Final

Current role: composite endgame region, not a fifth core element. Playable CLI
skeleton and ending flow have landed; naming polish remains open.

Mood words:

- 回聲、深界、空洞、王座、裂隙、虛無、四印、終門、封王、迷宮核心、暗潮、灰霜根雷回響

Place words:

- 前線營地、回聲戰線、破封遺跡、元素回聲門、封印核心、王座之門、深界階梯、終末回廊

Creature words:

- 灰燼回聲、霜影、根脈亡者、雷鳴殘像、虛無守衛、深界法師、裂隙獸、王座侍從

Boss title words:

- 回聲守衛、破封看守、元素門衛、深界將軍、虛無領主、魔王、王座之主

Material words:

- 灰燼回聲、霜記憶、根脈殘片、風暴玻璃、深界精華、虛無碎片、魔王核心碎片

Item / equipment words:

- 終門藥劑、深界護符、四印長劍、王座法杖、虛無鎧甲、回聲披風、封王戒

## Batch Naming Worksheet

Use this worksheet shape in future sessions. Fill only the relevant rows for
the approved slice.

| Region | Category | Runtime ID | Current display | Candidate display | Status | Notes |
|---|---|---|---|---|---|---|
| Ice | monster | `mon_ice_cave_mite` | Blue-Rime Mite | 凍爪穴熊 | adopted | Display-only. ID unchanged. |
| Ice | Boss | `boss_ice_final_seal_lord` | Final Seal Lord | 霜冠誓王 亞爾溟 | adopted | Avoids conflict with Final region naming. |
| Earth | monster | TBD from runtime | TBD | TBD | open | Choose from Earth creature words. |
| Thunder | equipment | TBD from runtime | TBD | TBD | open | Keep role and item type readable. |
| Final | material | TBD from runtime | TBD | TBD | open | Avoid making Final a fifth element. |

Status values:

- `candidate`: generated but not selected.
- `adopted`: owner-selected display canon.
- `placeholder`: current working name, not yet canon.
- `defer`: leave unchanged for now.
- `needs-preflight`: may require ID, flag, schema, or logic changes.

## Next Batch Pass Scope

Recommended next session target:

```text
Batch display naming pass for current CLI skeleton content.
Do not rename IDs.
Do not change flags, unlocks, turn_in, stats, drops, prices, registry, schema, save, combat, or GUI bridge.
Generate and select display names for:
- Earth dungeons, monsters, Bosses, materials, quest titles/descriptions.
- Thunder dungeons, monsters, Bosses, materials, quest titles/descriptions.
- Final dungeons, monsters, Bosses, materials, quest titles/descriptions.
- Current item/equipment/book/skill display names only if they are already present in runtime data.
```

Suggested validation after a display-only data patch:

```powershell
C:\Users\User\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe 06_tools\validate_data.py
C:\Users\User\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe element_maze.py --smoke-test
git diff --check
```

Run broader smoke tests only if the slice touches progression, combat, bridge,
registry, schema, or other logic surfaces.

## Boundaries

This lexicon does not approve:

- new runtime data entries
- ID renames
- registry rewiring
- schema edits
- save migration or manual `save.json` work
- combat formula changes
- GUI static prototype implementation
- GUI runtime bridge expansion
- formal asset-pipeline work
- optional elite implementation
- class transfer, promotion, or relic-effect implementation

Before any non-display naming work, start with the smallest matching read-only
planning gate and name exact files, risks, and validation commands.
