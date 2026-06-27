# 美術資產生產清單 v0.1 (Asset Production Inventory)

本文件定義了《元素迷宮》（Element Maze）世界觀中核心視覺資產的正式生產清冊。清單內容與 Python 運行時代碼中的實體 ID、顯示名稱與地區拓撲完全對齊。

> [!IMPORTANT]
> - **本清單為唯讀規劃**，不代表直接開始資產管線導入。不修改任何 Python 運行時、數據、Schema 或 GUI 靜態原型。
> - **Border / Fire 區域**: 僅進行基準審計（Baseline Audit），不提供生成用的 Prompt Spec，因為該路線已結構性完整。
> - **Ice 區域**: 首個面向生產的區域（Production Target），提供完整且高品質的 prompt-spec 描述，供 Codex 或後續資產管線生成使用。

---

## 資產範疇說明 (Scope Boundaries)

### 啟用資產類別 (In-Scope)
- 怪物頭像 (Monster Portrait)
- 首領頭像 (Boss Portrait)
- 設施背景 (Facility Hero)
- 地城探索場景 (Dungeon Exploration Scene)
- 戰鬥背景 (Combat Background)
- 地區區域圖 (Region Hub Background)
- 城鎮中心背景 (Town Hub Background)

### 關閉資產類別 (Out of Scope - 嚴禁規劃)
- 技能特效 (Skill VFX)
- 轉職角色美術 (Class-change Character Art)
- 元素克制特效 (Element-counter VFX)
- 神器主動/被動效果特效 (Relic active/passive visuals)
- 終局流派視覺 (Endgame build visuals)
- 職業專精視覺 (Class specialization visuals)
- 神器光環視覺 (Relic aura visuals)

---

## 資產生產清冊 (Asset Inventory Table)

| 建議資產 ID (asset_id) | 來源運行時 ID (source runtime id) | 來源文件/數據表 | 基準顯示名稱 (base label) | 區域運行時名稱 (regional display name) | 區域/路線 (region / route) | 圖像類型 (image type) | 優先級 (priority) | 預期用途 (intended use) | 基準審計 / 生產目標 | 生成提示詞準備狀態 (prompt-spec readiness) | 備註與視覺約束 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **城鎮與地區中心** | | | | | | | | | | | |
| `img_town_border_fire` | `border_fire` | `regions.py` | 邊境城鎮艾爾姆 | 邊境城鎮艾爾姆 | Border / Fire | Town Hub Background | High | 城鎮中心畫面背景 | Fire baseline audit | needs owner decision | 荒涼的邊境小鎮，木石建築，有焦黑痕跡，窗戶透出溫暖爐光。 |
| `img_town_ice_hub` | `ice` | `regions.py` | 霜潮港 | 霜潮港 | Ice | Town Hub Background | High | 城鎮中心畫面背景 | Ice production target | ready | 霜潮海岸港口，濕漉石造碼頭，積雪的屋頂，海風與霧氣，暖色窗光。**詳見下方 Prompt 說明**。 |
| **設施背景 (設施外觀/內部)** | | | | | | | | | | | |
| `img_facility_border_guild` | `guild` | `display_names.py` | 冒險者公會 | 冒險者工會 | Border / Fire | Facility Hero | Medium | 公會設施介面背景 | Fire baseline audit | needs owner decision | 粗獷木質大廳，委託佈告欄，壁爐。 |
| `img_facility_border_inn` | `inn` | `display_names.py` | 旅店 | 旅館 | Border / Fire | Facility Hero | Low | 旅店設施介面背景 | Fire baseline audit | needs owner decision | 石造壁爐，溫暖的木質吧台與桌椅。 |
| `img_facility_border_shop` | `shop` | `display_names.py` | 道具屋 | 旅人小鋪 | Border / Fire | Facility Hero | Medium | 商店設施介面背景 | Fire baseline audit | needs owner decision | 擺滿藥水、卷軸與旅行裝備的雜貨舖。 |
| `img_facility_border_weapon_workshop` | `weapon_workshop` | `display_names.py` | 鐵匠鋪 (武器) | 鐵刃工坊 | Border / Fire | Facility Hero | Medium | 鐵匠鋪設施介面背景 | Fire baseline audit | needs owner decision | 熊熊燃燒的鍛造爐，鐵砧，火花與武器架。 |
| `img_facility_border_armor_workshop` | `armor_workshop` | `display_names.py` | 鐵匠鋪 (防具) | 堅甲工坊 | Border / Fire | Facility Hero | Medium | 鐵匠鋪設施介面背景 | Fire baseline audit | needs owner decision | 鋼護面罩、胸甲護具與鎖子甲擺設。 |
| `img_facility_border_synthesis` | `synthesis` | `display_names.py` | 煉金工坊 | 米菈合成屋 | Border / Fire | Facility Hero | Medium | 煉金設施介面背景 | Fire baseline audit | needs owner decision | 咕嘟冒泡的坩堝，藥草與試管架。 |
| `img_facility_border_magic_shop` | `magic_shop` | `display_names.py` | 魔導書屋 | 星燈魔法商店 | Border / Fire | Facility Hero | Medium | 魔導書屋設施介面背景 | Fire baseline audit | needs owner decision | 浮空的古籍，水晶球，溫暖燭光環繞。 |
| `img_facility_border_temple` | `temple` | `display_names.py` | 神殿 | 轉職神殿 | Border / Fire | Facility Hero | Low | 神殿設施介面背景 | Fire baseline audit | needs owner decision | 寂靜的禮拜堂，石拱門，陽光灑在祭壇。 |
| `img_facility_border_storage` | `storage` | `display_names.py` | 倉庫 | 倉庫 | Border / Fire | Facility Hero | Low | 倉庫設施介面背景 | Fire baseline audit | needs owner decision | 堅固的保險庫，排列整齊的鐵皮箱與木箱。 |
| `img_facility_border_relic` | `relic` | `display_names.py` | 神器台 | 聖物調查 | Border / Fire | Facility Hero | High | 神器祭壇介面背景 | Fire baseline audit | needs owner decision | 古老石質底座，浮空環繞的元素封印槽。 |
| `img_facility_ice_guild` | `guild` | `display_names.py` | 冒險者公會 | 霜潮工會聯絡所 | Ice | Facility Hero | Medium | 公會設施介面背景 | Ice production target | ready | 霜潮港工會分部。鋪設海圖、指南針，有防風海報，帶有白鹽痕跡的粗木樑。 |
| `img_facility_ice_inn` | `inn` | `display_names.py` | 旅店 | 霜潮旅店 | Ice | Facility Hero | Low | 旅店設施介面背景 | Ice production target | ready | 港口旅店客房，窗外隱約可見雪景與桅杆，爐火上燉著熱湯。 |
| `img_facility_ice_shop` | `shop` | `display_names.py` | 道具屋 | 寒港補給鋪 | Ice | Facility Hero | Medium | 商店設施介面背景 | Ice production target | ready | 沿海雜貨舖，掛著乾魚網、油燈，陳列海鹽防潮罐與抗寒物資。 |
| `img_facility_ice_weapon_workshop` | `weapon_workshop` | `display_names.py` | 鐵匠鋪 (武器) | 霜鐵工坊 | Ice | Facility Hero | Medium | 鐵匠鋪設施介面背景 | Ice production target | ready | 霜鐵鍛造坊，淬火池冒出滾滾白蒸汽，提煉霜鐵礦石。 |
| `img_facility_ice_armor_workshop` | `armor_workshop` | `display_names.py` | 鐵匠鋪 (防具) | 鹽霧護具鋪 | Ice | Facility Hero | Medium | 鐵匠鋪設施介面背景 | Ice production target | ready | 鹽霧護具鋪掛滿防寒皮甲、絕緣襯料與護盾。 |
| `img_facility_ice_synthesis` | `synthesis` | `display_names.py` | 煉金工坊 | 霜潮合成台 | Ice | Facility Hero | Medium | 煉金設施介面背景 | Ice production target | ready | 臨海研究室，懸掛著乾燥海草，玻璃瓶內裝有發光冰晶溶液。 |
| `img_facility_ice_magic_shop` | `magic_shop` | `display_names.py` | 魔導書屋 | 冰燈魔法商店 | Ice | Facility Hero | Medium | 魔導書屋設施介面背景 | Ice production target | ready | 潮濕的書庫，防潮皮革卷軸架，淡藍色冰魔力水晶。 |
| `img_facility_ice_temple` | `temple` | `display_names.py` | 神殿 | 霜碑神殿 | Ice | Facility Hero | Low | 神殿設施介面背景 | Ice production target | ready | 面向大海的冰晶聖堂，彩繪玻璃描繪怒濤，有寒霜花裝飾。 |
| `img_facility_ice_storage` | `storage` | `display_names.py` | 倉庫 | 港口倉庫 | Ice | Facility Hero | Low | 倉庫設施介面背景 | Ice production target | ready | 港口乾燥倉庫，高掛防潮布，堆放防水木桶與綁著纜繩的鐵箱。 |
| `img_facility_ice_relic` | `relic` | `display_names.py` | 神器台 | 冰印調查台 | Ice | Facility Hero | High | 神器祭壇介面背景 | Ice production target | ready | 幽藍冰窟石台，雕刻有水與冰的古老文字，用以共鳴冰之印。 |
| **地城探索場景與戰鬥背景** | | | | | | | | | | | |
| `img_dungeon_moss_cave_exp` | `dungeon_moss_cave` | `dungeons.py` | 青苔洞窟-探索 | 青苔洞窟-探索 | Border / Fire | Dungeon Exploration Scene | Medium | 地城探索畫面背景 | Fire baseline audit | needs owner decision | 潮濕陰暗的石穴，發光青苔。 |
| `img_dungeon_moss_cave_cbt` | `dungeon_moss_cave` | `dungeons.py` | 青苔洞窟-戰鬥 | 青苔洞窟-戰鬥 | Border / Fire | Combat Background | Medium | 戰鬥畫面背景 | Fire baseline audit | needs owner decision | 石窟平地，背景為苔蘚岩壁。 |
| `img_dungeon_scorched_mine_exp` | `dungeon_scorched_mine` | `dungeons.py` | 焦石礦坑-探索 | 焦石礦坑-探索 | Border / Fire | Dungeon Exploration Scene | Medium | 地城探索畫面背景 | Fire baseline audit | needs owner decision | 廢棄礦道，焦黑石壁，餘燼與軌道。 |
| `img_dungeon_scorched_mine_cbt` | `dungeon_scorched_mine` | `dungeons.py` | 焦石礦坑-戰鬥 | 焦石礦坑-戰鬥 | Border / Fire | Combat Background | Medium | 戰鬥畫面背景 | Fire baseline audit | needs owner decision | 礦坑空地，兩旁有崩落礦石與支撐木。 |
| `img_dungeon_ash_ravine_exp` | `dungeon_ash_ravine` | `dungeons.py` | 灰燼裂谷-探索 | 灰燼裂谷-探索 | Border / Fire | Dungeon Exploration Scene | Medium | 地城探索畫面背景 | Fire baseline audit | needs owner decision | 黑色大裂谷，空中飄散落灰，岩縫透出紅光。 |
| `img_dungeon_ash_ravine_cbt` | `dungeon_ash_ravine` | `dungeons.py` | 灰燼裂谷-戰鬥 | 灰燼裂谷-戰鬥 | Border / Fire | Combat Background | Medium | 戰鬥畫面背景 | Fire baseline audit | needs owner decision | 裂谷邊緣碎石地，背景為熔岩紅光與黑煙。 |
| `img_dungeon_cinder_seal_exp` | `dungeon_cinder_seal_depths` | `dungeons.py` | 燼印深窟-探索 | 燼印深窟-探索 | Border / Fire | Dungeon Exploration Scene | High | 地城探索畫面背景 | Fire baseline audit | needs owner decision | 地底古代神殿遺蹟，流動熔岩溝槽，巨大的熔鐵封印門。 |
| `img_dungeon_cinder_seal_cbt` | `dungeon_cinder_seal_depths` | `dungeons.py` | 燼印深窟-戰鬥 | 燼印深窟-戰鬥 | Border / Fire | Combat Background | High | 戰鬥畫面背景 | Fire baseline audit | needs owner decision | 神殿祭壇前平台，背景為流動的橙紅色岩漿與發光符文。 |
| `img_dungeon_ice_minor_a_exp` | `dungeon_ice_minor_a` | `dungeons.py` | 幽帆沉船-探索 | 幽帆沉船-探索 | Ice | Dungeon Exploration Scene | High | 地城探索畫面背景 | Ice production target | ready | 觸礁觸冰擱淺的古老帆船內部，結滿寒霜的腐木船艙。 |
| `img_dungeon_ice_minor_a_cbt` | `dungeon_ice_minor_a` | `dungeons.py` | 幽帆沉船-戰鬥 | 幽帆沉船-戰鬥 | Ice | Combat Background | Medium | 戰鬥畫面背景 | Ice production target | ready | 覆蓋薄冰傾斜的甲板，殘存桅杆，背景為咆哮的陰冷大海。 |
| `img_dungeon_ice_minor_b_exp` | `dungeon_ice_minor_b` | `dungeons.py` | 霜根岩窟-探索 | 霜根岩窟-探索 | Ice | Dungeon Exploration Scene | High | 地城探索畫面背景 | Ice production target | ready | 巨大老樹根編織而成的冰穴，幽藍發光植物與冰柱。 |
| `img_dungeon_ice_minor_b_cbt` | `dungeon_ice_minor_b` | `dungeons.py` | 霜根岩窟-戰鬥 | 霜根岩窟-戰鬥 | Ice | Combat Background | Medium | 戰鬥畫面背景 | Ice production target | ready | 結霜的岩石洞底，背景為爬滿冰藤的冰壁與晶瑩冰晶。 |
| `img_dungeon_ice_main_p1_exp` | `dungeon_ice_main_phase_1` | `dungeons.py` | 斷階外城-探索 | 霜鐵古城 - 斷階外城-探索 | Ice | Dungeon Exploration Scene | High | 地城探索畫面背景 | Ice production target | ready | 霜鐵古城斑駁的城牆，被風雪侵蝕的巨大石階與石拱門。 |
| `img_dungeon_ice_main_p1_cbt` | `dungeon_ice_main_phase_1` | `dungeons.py` | 斷階外城-戰鬥 | 霜鐵古城 - 斷階外城-戰鬥 | Ice | Combat Background | Medium | 戰鬥畫面背景 | Ice production target | ready | 城牆上的雪地平台，背景為遠處巍峨的風雪城堡主塔。 |
| `img_dungeon_ice_main_p2_exp` | `dungeon_ice_main_phase_2` | `dungeons.py` | 終印誓殿-探索 | 霜鐵古城 - 終印誓殿-探索 | Ice | Dungeon Exploration Scene | High | 地城探索畫面背景 | Ice production target | ready | 古城宮殿內部，大廳結滿玄冰與鐵鏈，盡頭有發光的冰之刻印。 |
| `img_dungeon_ice_main_p2_cbt` | `dungeon_ice_main_phase_2` | `dungeons.py` | 終印誓殿-戰鬥 | 霜鐵古城 - 終印誓殿-戰鬥 | Ice | Combat Background | High | 戰鬥畫面背景 | Ice production target | ready | 宮殿王座前發光的寒冰地板，背後有高聳冰封的巨大王座。 |
| **普通怪物頭像** | | | | | | | | | | | |
| `img_monster_moss_rat` | `mon_moss_rat` | `monsters.py` | 青苔鼠 | 青苔鼠 | Border / Fire | Monster Portrait | Low | 戰鬥介面怪物頭像 | Fire baseline audit | needs owner decision | 背部長著綠色青苔的灰毛老鼠。 |
| `img_monster_cave_slug` | `mon_cave_slug` | `monsters.py` | 洞窟黏蟲 | 洞窟黏蟲 | Border / Fire | Monster Portrait | Low | 戰鬥介面怪物頭像 | Fire baseline audit | needs owner decision | 帶有淡藍微光的半透明黏土軟體蟲。 |
| `img_monster_cracked_golem` | `mon_cracked_golem` | `monsters.py` | 裂石小魔像 | 裂石小魔像 | Border / Fire | Monster Portrait | Low | 戰鬥介面怪物頭像 | Fire baseline audit | needs owner decision | 碎石拼湊、能量縫隙散發微光的小魔像。 |
| `img_monster_cinder_bat` | `mon_cinder_bat` | `monsters.py` | 焦翼蝠 | 焦翼蝠 | Border / Fire | Monster Portrait | Low | 戰鬥介面怪物頭像 | Fire baseline audit | needs owner decision | 雙翼邊緣呈黑炭化、冒出小火花的蝙蝠。 |
| `img_monster_lava_imp` | `mon_lava_imp` | `monsters.py` | 熔岩小鬼 | 熔岩小鬼 | Border / Fire | Monster Portrait | Low | 戰鬥介面怪物頭像 | Fire baseline audit | needs owner decision | 全身由冷凝岩漿構成的赤紅小魔怪。 |
| `img_monster_scorched_guard` | `mon_scorched_guard` | `monsters.py` | 焦石斥候 | 焦石斥候 | Border / Fire | Monster Portrait | Low | 戰鬥介面怪物頭像 | Fire baseline audit | needs owner decision | 黑曜石外骨骼戰士，手握銹蝕兵刃，紅眼。 |
| `img_monster_ash_imp` | `mon_ash_imp` | `monsters.py` | 灰燼小鬼 | 灰燼小鬼 | Border / Fire | Monster Portrait | Low | 戰鬥介面怪物頭像 | Fire baseline audit | needs owner decision | 覆滿黑灰、尖耳、眼神狡黠的灰炭小惡魔。 |
| `img_monster_lava_bat` | `mon_lava_bat` | `monsters.py` | 熔岩蝙蝠 | 熔岩蝙蝠 | Border / Fire | Monster Portrait | Low | 戰鬥介面怪物頭像 | Fire baseline audit | needs owner decision | 翼膜流動著橙紅岩漿、體型較大的魔蝠。 |
| `img_monster_cinder_soldier` | `mon_cinder_soldier` | `monsters.py` | 燼火兵 | 燼火兵 | Border / Fire | Monster Portrait | Low | 戰鬥介面怪物頭像 | Fire baseline audit | needs owner decision | 破碎鎧甲內燃繞著烈火的元素士兵。 |
| `img_monster_ember_stalker` | `mon_ember_stalker` | `monsters.py` | 餘燼潛獵者 | 餘燼潛獵者 | Border / Fire | Monster Portrait | Low | 戰鬥介面怪物頭像 | Fire baseline audit | needs owner decision | 由黑煙與火炭構成的獵豹型魔獸。 |
| `img_monster_molten_shell` | `mon_molten_shell` | `monsters.py` | 熔殼岩獸 | 熔殼岩獸 | Border / Fire | Monster Portrait | Low | 戰鬥介面怪物頭像 | Fire baseline audit | needs owner decision | 覆蓋著冷凝火山岩甲殼的龜型怪獸，氣孔冒火。 |
| `img_monster_cinder_brand` | `mon_cinder_brand_wisp` | `monsters.py` | 燼印火靈 | 燼印火靈 | Border / Fire | Monster Portrait | Low | 戰鬥介面怪物頭像 | Fire baseline audit | needs owner decision | 浮空的烈焰精靈，核心處有赤紅的符文印記。 |
| `img_monster_ice_deckhand` | `mon_ice_drowned_deckhand` | `monsters.py` | 黑牙亡水手 | 黑牙亡水手 | Ice | Monster Portrait | Medium | 戰鬥介面怪物頭像 | Ice production target | ready | 身體浮腫呈深藍色、覆有冰晶與海草的亡靈水手。 |
| `img_monster_ice_crab` | `mon_ice_bilge_crab` | `monsters.py` | 鹽霧弩手 | 鹽霧弩手 | Ice | Monster Portrait | Medium | 戰鬥介面怪物頭像 | Ice production target | ready | 披掛白色結晶鹽岩鎧甲、手持強弩的骷髏弓手。 |
| `img_monster_ice_salt_wisp` | `mon_ice_salt_wisp` | `monsters.py` | 鐵鉤船員 | 鐵鉤船員 | Ice | Monster Portrait | Medium | 戰鬥介面怪物頭像 | Ice production target | ready | 獨眼，手部為沉重寒鐵船鉤的亡靈海盜。 |
| `img_monster_ice_ghost_sail` | `mon_ice_ghost_sail` | `monsters.py` | 幽帆瞭望手 | 幽帆瞭望手 | Ice | Monster Portrait | Medium | 戰鬥介面怪物頭像 | Ice production target | ready | 幽靈形態，漂浮並散發淡青色熒光，手持青銅望遠鏡。 |
| `img_monster_ice_root_lurker` | `mon_ice_frostroot_lurker` | `monsters.py` | 霜根獵蛛 | 霜根獵蛛 | Ice | Monster Portrait | Medium | 戰鬥介面怪物頭像 | Ice production target | ready | 體型巨大，足部硬化如結冰老樹根的白色毒蜘蛛。 |
| `img_monster_ice_cave_mite` | `mon_ice_cave_mite` | `monsters.py` | 凍爪穴熊 | 凍爪穴熊 | Ice | Monster Portrait | Medium | 戰鬥介面怪物頭像 | Ice production target | ready | 白色厚重毛皮，爪子凝聚為深藍色冰刀的巨熊。 |
| `img_monster_ice_rime_bloom` | `mon_ice_rime_bloom` | `monsters.py` | 冰刺蕈妖 | 冰刺蕈妖 | Ice | Monster Portrait | Medium | 戰鬥介面怪物頭像 | Ice production target | ready | 菌蓋完全由尖銳冰錐組成的怪異蕈類精靈。 |
| `img_monster_ice_stone_shell` | `mon_ice_stone_shell` | `monsters.py` | 藍光洞靈 | 藍光洞靈 | Ice | Monster Portrait | Medium | 戰鬥介面怪物頭像 | Ice production target | ready | 由冰藍寶石與洞穴岩石拼湊而成、大眼散發幽藍光芒的小精靈。 |
| `img_monster_ice_outer_guard` | `mon_ice_outer_guard` | `monsters.py` | 斷階石衛 | 斷階石衛 | Ice | Monster Portrait | Medium | 戰鬥介面怪物頭像 | Ice production target | ready | 破碎的石雕石衛，由冰魔力線條連接，手持厚重冰刃。 |
| `img_monster_ice_rime_hound` | `mon_ice_rime_hound` | `monsters.py` | 裂碑幽魂 | 裂碑幽魂 | Ice | Monster Portrait | Medium | 戰鬥介面怪物頭像 | Ice production target | ready | 怨魂形態，周身漂浮碎裂石碑殘片，呈冰白色。 |
| `img_monster_ice_frost_armor` | `mon_ice_frost_armor` | `monsters.py` | 殘塔弩手 | 殘塔弩手 | Ice | Monster Portrait | Medium | 戰鬥介面怪物頭像 | Ice production target | ready | 空心的重型鎧甲，頭盔與關節處塞滿冰霜與風雪。 |
| `img_monster_ice_seal_spark` | `mon_ice_seal_spark` | `monsters.py` | 迴廊石像兵 | 迴廊石像兵 | Ice | Monster Portrait | Medium | 戰鬥介面怪物頭像 | Ice production target | ready | 蹲踞狀的石翼鬼兵，胸口刻有發光藍色封印印記。 |
| `img_monster_ice_palace_wisp` | `mon_ice_palace_wisp` | `monsters.py` | 霜鐵禁衛 | 霜鐵禁衛 | Ice | Monster Portrait | Medium | 戰鬥介面怪物頭像 | Ice production target | ready | 穿戴精緻霜鐵板甲與藍色羽翎、手握重型戟矛的皇家幽靈。 |
| `img_monster_ice_throne_shade` | `mon_ice_throne_shade` | `monsters.py` | 鎖誓亡者 | 鎖誓亡者 | Ice | Monster Portrait | Medium | 戰鬥介面怪物頭像 | Ice production target | ready | 全身繞著發光冰鏈、穿戴華麗襤褸長袍的宮殿怨靈。 |
| `img_monster_ice_seal_knight` | `mon_ice_seal_knight` | `monsters.py` | 封印鏈奴 | 封印鏈奴 | Ice | Monster Portrait | Medium | 戰鬥介面怪物頭像 | Ice production target | ready | 拖著巨大寒鐵鏈條的冰石巨人，頭部貼著發光的深藍封印符紙。 |
| `img_monster_ice_core_sentry` | `mon_ice_core_sentry` | `monsters.py` | 碎印法師 | 碎印法師 | Ice | Monster Portrait | Medium | 戰鬥介面怪物頭像 | Ice production target | ready | 戴冰霜兜帽、面部陰影中只有亮藍雙眼的巫師，雙手懸浮碎裂魔力核心。 |
| **Boss 首領頭像** | | | | | | | | | | | |
| `img_boss_glen` | `boss_glen` | `monsters.py` | 山寨頭目葛倫 | 山寨頭目葛倫 | Border / Fire | Boss Portrait | High | 戰鬥介面 Boss 視覺 | Fire baseline audit | needs owner decision | 魁梧的盜賊首領，手持重劍，眼神通紅有怒氣。 |
| `img_boss_ash_guardian` | `boss_ash_guardian` | `monsters.py` | 灰燼守衛 | 灰燼守衛 | Border / Fire | Boss Portrait | High | 戰鬥介面 Boss 視覺 | Fire baseline audit | needs owner decision | 由黑曜石與飛灰熔煉而成的龐大元素傀儡。 |
| `img_boss_cinder_sentinel` | `boss_cinder_seal_sentinel` | `monsters.py` | 燼印鎮衛 | 燼印鎮衛 | Border / Fire | Boss Portrait | High | 戰鬥介面 Boss 視覺 | Fire baseline audit | needs owner decision | 身披焦黑板甲的古代守衛，肩甲有發光橙紅火印。 |
| `img_boss_ice_wreck_captain` | `boss_ice_wreck_captain` | `monsters.py` | 幽帆舵主 維爾洛 | 幽帆舵主 維爾洛 | Ice | Boss Portrait | High | 戰鬥介面 Boss 視覺 | Ice production target | ready | 亡靈船長維爾洛。戴三角海盜帽，身穿藤壺長袍，手持幽藍冰霜直刀，眼冒綠火。 |
| `img_boss_ice_root_keeper` | `boss_ice_frostroot_keeper` | `monsters.py` | 霜根母株 葛魯姆 | 霜根母株 葛魯姆 | Ice | Boss Portrait | High | 戰鬥介面 Boss 視覺 | Ice production target | ready | 龐大的冰霜樹妖，根鬚蔓延，樹幹中央跳動著散發冷光的藍色心臟。 |
| `img_boss_ice_outer_warden` | `boss_ice_outer_gatewarden` | `monsters.py` | 斷階守誓者 奧登 | 斷階守誓者 奧登 | Ice | Boss Portrait | High | 戰鬥介面 Boss 視覺 | Ice production target | ready | 高大魁梧的誓言守衛。身著發光藍色符文板甲，手持城牆塔盾與巨型石槌。 |
| `img_boss_ice_final_lord` | `boss_ice_final_seal_lord` | `monsters.py` | 霜冠誓王 亞爾溟 | 霜冠誓王 亞爾溟 | Ice | Boss Portrait | High | 戰鬥介面 Boss 視覺 | Ice production target | ready | 漂浮的冰冠幽靈王。頭頂冰雪皇冠，手持完全由水晶藍冰凝結的巨型重劍，周身環繞冰雪風暴。 |

---

## 冰區資產生成提示詞規格說明 (Ice Region Prompt Specifications)

此部分為面向生產的 **Ice Region** 核心資產設計的 Prompt 規格，旨在為生成工具提供精準且具備《元素迷宮》風格一致性的描述。

### 1. 城鎮中心背景: 霜潮港 (`img_town_ice_hub`)
- **美術風格**: 日系 3D 奇幻 RPG 風格（Stylized JRPG/Japanese-leaning 3D fantasy）。
- **畫面構圖**: 高視角（High-angle），俯瞰海港小鎮的廣場。保留畫面兩側作為半透明 UI 面板疊加的安全區域。畫面主體需有數個明確且寬大、比例清晰的建築入口，用以標示「工會聯絡所、旅店、補給鋪、工坊」等設施，防止建築過小。
- **視覺元素**: 潮濕、鋪有結霜石板的街道；積雪的木屋頂；海風吹拂的港灣，隱約能見風浪與桅杆影子；海霧籠罩；建築窗口和掛燈散發溫暖的橘黃色光芒，並在潮濕反光的地面留下倒影。
- **Prompt**:
  > *A stylized JRPG-style 3D fantasy scene of a frost-tide coastal town hub called Frost-tide Harbor. Cozy port town with wet stone docks and piers, rustic wooden buildings with snow-dusted roofs. Heavy sea fog rolls in from a cold dark sea. Windbreaks protect the buildings. Warm golden lights glow from building windows and lanterns, casting reflections on wet stone pavement. Clear, prominent entrances for a guild, inn, shop, and workshop. High-angle layout view with space for UI overlay panels on the sides. Atmospheric, high detail, JRPG aesthetic.*

### 2. 設施背景 (Facility Hero 範例)

#### A. 霜潮工會聯絡所 (`img_facility_ice_guild`)
- **視覺描述**: 溫暖舒適的公會大廳內部。屋頂由結了白色鹽霜的深色粗木樑支撐。一旁有用粗糙岩石堆砌的巨大壁爐，柴火噼啪燃燒。桌上鋪設著泛黃 of 沿海航海圖與黃銅指南針。牆上懸掛著魚網與木舵。
- **Prompt**:
  > *A JRPG-style facility interior of a cozy, rustic coastal guildhall in Frost-tide Harbor. A crackling stone fireplace keeps the room warm. The walls are decorated with old parchment maps of the coastline, ship steering wheels, and fishing nets. White salt crystals crust the dark wooden ceiling beams. Warm yellow light casts cozy shadows. Clean layout for UI overlay panels. Stylized 3D render.*

#### B. 霜鐵工坊 (`img_facility_ice_weapon_workshop`)
- **視覺描述**: 水蒸汽瀰漫的鐵匠工坊。一側是高溫燃燒的熔爐，散發熾熱的橙紅火光，正提煉著深色冰冷的霜鐵礦石。鐵砧上火花飛濺，淬火用的水池中正冒出滾滾白色蒸汽。後方陳列架上擺放著厚實沉重的冰結兵刃。
- **Prompt**:
  > *A JRPG-style blacksmith workshop. A hot forge glows with orange fire, melting chunks of dark frost-iron ore. An anvil sits in the center with sparks. Steam rises from a cold water quenching tank next to it. Racks of iron weapons stand in the background. High-detail 3D gaming concept art.*
