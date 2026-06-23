#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Name Candidate Generator Prototype
Usage:
  python 06_tools/name_candidate_generator.py --category weapon --count 12
  python 06_tools/name_candidate_generator.py --category armor --region ice --tier 3
"""

import os
import sys
import json
import random
import argparse

# Force stdout/stderr to use utf-8 to prevent encoding issues in Windows environments
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


# Ensure project root is in sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Load EQUIPMENT from 04_data/data/items.py
data_dir = os.path.join(project_root, "04_data", "data")
if data_dir not in sys.path:
    sys.path.insert(0, data_dir)

try:
    import items
    EQUIPMENT = items.EQUIPMENT
except ImportError:
    EQUIPMENT = {}


# Map job CLI arguments to runtime item jobs
JOB_MAPPING = {
    "warrior": "劍士",
    "rogue": "盜賊",
    "mage": "法師",
    "priest": "牧師",
    "cleric": "牧師"
}

# Sensitive words for overlap filtering
SENSITIVE_WORDS = set("皮鐵鋼木石骨銀金布銅鱗冰火雷風磐石青苔")

def load_lexicons():
    lexicon_path = os.path.join(script_dir, "name_generation_lexicons.json")
    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
        sys.exit(1)
    with open(lexicon_path, "r", encoding="utf-8") as f:
        return json.load(f)

def clean_word(word):
    """Remove common syntax markers to extract the core stem."""
    if not word:
        return ""
    return word.replace("的", "").replace("製", "").replace("・", "").strip()

def has_overlap(prefix, material, base, suffix):
    """Check if there is semantic or word-stem overlap between parts."""
    parts = [clean_word(prefix), clean_word(material), clean_word(base), clean_word(suffix)]
    clean_parts = [p for p in parts if p]

    for i in range(len(clean_parts)):
        for j in range(i + 1, len(clean_parts)):
            w1, w2 = clean_parts[i], clean_parts[j]
            if not w1 or not w2:
                continue

            # Substring check
            if w1 in w2 or w2 in w1:
                overlap_len = min(len(w1), len(w2))
                # For length 1, only filter if it is in the sensitive list (e.g. "皮" vs "皮革")
                if overlap_len == 1:
                    char = w1 if len(w1) == 1 else w2
                    if char in SENSITIVE_WORDS:
                        return True
                else:
                    # For length >= 2, always filter (e.g. "烈焰" vs "烈焰之刃")
                    return True
    return False

def get_existing_names():
    """Retrieve all existing equipment names from runtime data."""
    names = set()
    for item_id, item_data in EQUIPMENT.items():
        if "name" in item_data:
            names.add(item_data["name"])
    return names

def select_candidate_pool(lexicons, category, region_element, job, slot, tier):
    """Filter and build candidate pools for each part based on arguments."""
    pools = {
        "prefixes": [],
        "materials": [],
        "bases": [],
        "suffixes": []
    }

    # 1. Base pool
    if category == "weapon":
        if job and job in lexicons["weapon_bases"]:
            pools["bases"] = lexicons["weapon_bases"][job]
        else:
            # Flatten all weapon bases
            for job_bases in lexicons["weapon_bases"].values():
                pools["bases"].extend(job_bases)
    elif category == "armor":
        if slot and slot in lexicons["armor_bases"]:
            pools["bases"] = lexicons["armor_bases"][slot]
        else:
            # Flatten all armor bases
            for slot_bases in lexicons["armor_bases"].values():
                pools["bases"].extend(slot_bases)

    # 2. Material pool
    if tier:
        tier_key = f"tier{tier}"
        if tier_key in lexicons["materials"]:
            pools["materials"] = lexicons["materials"][tier_key]
    else:
        # Flatten all materials
        for tier_mats in lexicons["materials"].values():
            pools["materials"].extend(tier_mats)

    # 3. Suffix pool
    # Suffixes can be general or elemental
    pools["suffixes"].extend(lexicons["suffixes"]["general"])
    if region_element:
        # Normalize region/element
        el = region_element.replace("border_", "")
        if el in lexicons["suffixes"]["elemental"]:
            pools["suffixes"].extend(lexicons["suffixes"]["elemental"][el])
    else:
        # Add all elemental suffixes
        for el_suffixes in lexicons["suffixes"]["elemental"].values():
            pools["suffixes"].extend(el_suffixes)

    # 4. Prefix pool
    # Prefix includes quality, elemental, and traits
    # Filter by tier -> quality prefixes
    quality_prefixes = []
    if tier:
        tier_key = f"tier{tier}"
        if tier_key in lexicons["prefixes"]["quality"]:
            quality_prefixes = lexicons["prefixes"]["quality"][tier_key]
    else:
        for tier_pfxs in lexicons["prefixes"]["quality"].values():
            quality_prefixes.extend(tier_pfxs)
    pools["prefixes"].extend(quality_prefixes)

    # Filter by region/element -> elemental prefixes
    elemental_prefixes = []
    if region_element:
        el = region_element.replace("border_", "")
        if el in lexicons["prefixes"]["elemental"]:
            elemental_prefixes = lexicons["prefixes"]["elemental"][el]
    else:
        for el_pfxs in lexicons["prefixes"]["elemental"].values():
            elemental_prefixes.extend(el_pfxs)
    pools["prefixes"].extend(elemental_prefixes)

    # Filter by job -> trait prefixes
    trait_prefixes = []
    if job and job in lexicons["prefixes"]["traits"]:
        trait_prefixes = lexicons["prefixes"]["traits"][job]
    else:
        for job_pfxs in lexicons["prefixes"]["traits"].values():
            trait_prefixes.extend(job_pfxs)
    pools["prefixes"].extend(trait_prefixes)

    return pools

def calculate_stats_and_tags(prefix, material, base, suffix, use_suffix):
    """Aggregate stats and merge tags from all chosen component items."""
    stats = {}
    tags = set()

    parts = [prefix, material, base]
    if use_suffix and suffix:
        parts.append(suffix)

    for part in parts:
        if not part:
            continue
        # Accumulate stats
        part_stats = part.get("stats", {})
        for stat_key, stat_val in part_stats.items():
            stats[stat_key] = stats.get(stat_key, 0) + stat_val

        # Merge tags
        part_tags = part.get("tags", [])
        for tag in part_tags:
            tags.add(tag)

    return stats, sorted(list(tags))

def generate_candidates(category, count, region_element, job, slot, tier):
    lexicons = load_lexicons()
    pools = select_candidate_pool(lexicons, category, region_element, job, slot, tier)
    existing_names = get_existing_names()

    candidates = []
    attempts = 0
    max_attempts = count * 200  # Prevent infinite loops

    while len(candidates) < count and attempts < max_attempts:
        attempts += 1

        # Pick components
        # 1. Base (required)
        if not pools["bases"]:
            break
        base_item = random.choice(pools["bases"])
        base_word = base_item["word"]

        # 2. Material (usually required, but we can make it optional for accessories sometimes)
        material_item = None
        material_word = ""
        # 90% chance to have material, or 100% if tier is locked
        if pools["materials"] and (tier or random.random() < 0.9):
            material_item = random.choice(pools["materials"])
            material_word = material_item["word"]

        # 3. Prefix (optional, e.g., 75% chance)
        prefix_item = None
        prefix_word = ""
        # If region, element, or tier is specified, we elevate chance to 95%
        prefix_chance = 0.95 if (region_element or tier or job) else 0.75
        if pools["prefixes"] and random.random() < prefix_chance:
            prefix_item = random.choice(pools["prefixes"])
            prefix_word = prefix_item["word"]

        # 4. Suffix (optional, 35% chance)
        suffix_item = None
        suffix_word = ""
        use_suffix = False
        suffix_chance = 0.50 if region_element else 0.30
        if pools["suffixes"] and random.random() < suffix_chance:
            suffix_item = random.choice(pools["suffixes"])
            suffix_word = suffix_item["word"]
            use_suffix = True

        # Build Name
        name = f"{prefix_word}{material_word}{base_word}"
        if use_suffix and suffix_word:
            name += f"・{suffix_word}"

        # Filters
        if not name:
            continue
        if len(name) > 15:
            continue
        if name in existing_names:
            continue
        if any(c["name"] == name for c in candidates):
            continue
        if has_overlap(prefix_word, material_word, base_word, suffix_word):
            continue

        # Calculate stats and tags
        stats, tags = calculate_stats_and_tags(prefix_item, material_item, base_item, suffix_item, use_suffix)

        # Determine slot for metadata
        resolved_slot = "weapon" if category == "weapon" else (slot or "body")
        if category == "armor" and not slot:
            # Try to infer slot from base_word
            for s_key, s_list in lexicons["armor_bases"].items():
                if any(b["word"] == base_word for b in s_list):
                    resolved_slot = s_key
                    break

        # Determine job eligibility
        resolved_jobs = []
        if category == "weapon":
            if job:
                resolved_jobs = [JOB_MAPPING.get(job, job)]
            else:
                # Find which job this base belongs to
                for j_key, j_list in lexicons["weapon_bases"].items():
                    if any(b["word"] == base_word for b in j_list):
                        resolved_jobs.append(JOB_MAPPING.get(j_key, j_key))
        else:
            # Armor is generally usable by multiple jobs; resolve based on slot/type
            resolved_jobs = ["劍士", "法師", "盜賊", "牧師"]

        candidates.append({
            "name": name,
            "category": category,
            "slot": resolved_slot,
            "tier": tier or 2,  # Default to tier 2 if unspecified
            "jobs": resolved_jobs,
            "stats": stats,
            "tags": tags
        })

    return candidates

def print_markdown(candidates):
    print("# RPG 裝備命名候選清單 (Name Candidate Tools)")
    print(f"共產生 {len(candidates)} 個候選名稱，已過濾重複與同一詞段重複字詞，並對齊現有裝備。\n")
    print("| 序號 | 候選名稱 | 分類 | 部位 | 階級 | 適用職業 | 推薦屬性 (Stats) | 標籤 (Tags) |")
    print("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for i, c in enumerate(candidates, 1):
        stats_str = ", ".join([f"{k}: +{v}" if v > 0 else f"{k}: {v}" for k, v in c["stats"].items()]) if c["stats"] else "無"
        tags_str = ", ".join([f"`{t}`" for t in c["tags"]]) if c["tags"] else "無"
        jobs_str = "/".join(c["jobs"])
        cat_zh = "武器" if c["category"] == "weapon" else "防具"
        slot_zh = {"head": "頭部", "body": "身體", "hand": "手部", "accessory": "裝飾品", "weapon": "武器"}.get(c["slot"], c["slot"])
        print(f"| {i} | **{c['name']}** | {cat_zh} | {slot_zh} | T{c['tier']} | {jobs_str} | {stats_str} | {tags_str} |")

def main():
    parser = argparse.ArgumentParser(description="RPG 武器與防具命名候選產生器 (帶屬性與效果連動)")
    parser.add_argument("--category", choices=["weapon", "armor"], required=True, help="裝備大類 (武器或防具)")
    parser.add_argument("--count", type=int, default=12, help="產生數量 (預設 12)")
    parser.add_argument("--region", choices=["fire", "border_fire", "ice", "earth", "thunder", "final"], help="指定區域/元素環境")
    parser.add_argument("--element", choices=["fire", "ice", "earth", "thunder", "final"], help="指定元素 (與 region 互通)")
    parser.add_argument("--job", choices=["warrior", "rogue", "mage", "priest", "cleric"], help="指定適用職業 (主要影響武器)")
    parser.add_argument("--slot", choices=["head", "body", "hand", "accessory"], help="指定防具部位 (主要影響防具)")
    parser.add_argument("--tier", type=int, choices=[1, 2, 3, 4], help="指定強度階級 (Tier 1~4)")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="輸出格式 (預設 markdown)")

    args = parser.parse_args()

    region_element = args.element or args.region

    candidates = generate_candidates(
        category=args.category,
        count=args.count,
        region_element=region_element,
        job=args.job,
        slot=args.slot,
        tier=args.tier
    )

    if args.format == "json":
        print(json.dumps(candidates, ensure_ascii=False, indent=2))
    else:
        print_markdown(candidates)

if __name__ == "__main__":
    main()
