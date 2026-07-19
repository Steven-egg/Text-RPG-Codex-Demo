from __future__ import annotations

import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "04_data"
if str(DATA_ROOT) not in sys.path:
    sys.path.insert(0, str(DATA_ROOT))

try:
    from data import (
        CORE_FACILITY_KEYS,
        CORE_NPC_KEYS,
        DUNGEONS,
        EQUIPMENT,
        EVENT_WEIGHTS,
        FACILITY_DISPLAY_NAMES,
        FACILITY_GREETINGS,
        FACILITY_SHORT_DESCRIPTIONS,
        ITEMS,
        JOB_SPECIALIZATIONS,
        JOBS,
        MAGIC_BOOKS,
        MATERIALS,
        MONSTERS,
        NPC_DISPLAY_NAMES,
        PROMOTIONS,
        QUESTS,
        RECIPES,
        REGIONS,
        RELICS,
        SHOP_INVENTORY,
        SKILLS,
    )
    from data.registry import (
        ENGINE_EVENT_UNLOCK_KEYS,
        INITIAL_UNLOCK_KEYS,
        KNOWN_FLAG_KEYS,
        STORY_UNLOCK_KEYS,
        SYSTEM_UNLOCK_KEYS,
        all_item_like_ids,
        all_material_ids,
        all_sellable_ids,
        all_unlock_producers,
    )
except Exception as exc:  # pragma: no cover - protects CLI diagnostics.
    print(f"[ERROR] failed to import data modules: {exc}")
    raise SystemExit(1)


VALID_SLOTS = {"weapon", "head", "body", "accessory", "special"}
VALID_ITEM_KINDS = {"consumable", "special", "battle"}
VALID_SKILL_KINDS = {"damage", "heal", "buff", "debuff", "dot", "regen", "passive"}
VALID_DAMAGE_STATS = {"attack", "magic"}
VALID_BUFF_STAT_KEYS = {"crit"}
VALID_EQUIPMENT_STATS = {
    "attack",
    "magic_attack",
    "defense",
    "magic_defense",
    "agility",
    "effect_accuracy",
    "crit",
    "fire_resist",
    "ice_resist",
    "earth_resist",
    "thunder_resist",
    "trap_evasion",
    "rare_drop",
}
VALID_EFFECT_KEYS = {"defense_up", "defense_down", "quickstep", "cinder_mark", "burn", "bleed", "poison", "regeneration"}
VALID_PASSIVE_EVENTS = {"physical_charge_reaches", "physical_status_applied"}
VALID_PASSIVE_EFFECT_KINDS = {"charge_skill_bonus", "extra_normal_followup"}
VALID_DAMAGE_SCOPES = {"elemental_magic"}
VALID_PROMOTION_STATUSES = {"preview"}
VALID_PROMOTION_REQUIREMENT_KINDS = {"level", "unlock", "quest", "flag", "item"}
VALID_JOB_SPECIALIZATION_STATUSES = {"preview"}
VALID_RELIC_STATUSES = {"preview"}
VALID_RELIC_UNLOCK_KINDS = {"level", "unlock", "quest", "flag", "item"}
VALID_RELIC_ELEMENT_IDS = {"fire", "ice", "earth", "thunder"}
VALID_RELIC_PASSIVE_EFFECTS = {
    "direct_damage_percent",
    "physical_lifesteal_percent",
    "crit_damage_percent",
    "all_element_resist",
    "direct_magic_damage_percent",
    "max_mp_percent",
    "magic_defense_percent",
    "max_hp_percent",
    "healing_regen_percent",
    "dot_damage_percent",
    "direct_physical_damage_percent",
    "crit",
    "effect_accuracy",
}
VALID_REGIONS = {"border_fire", "ice", "earth", "thunder", "final"}
VALID_MONSTER_RACES = {"beast", "humanoid", "plant", "construct", "spirit", "aberration"}
VALID_FOLLOWUP_DAMAGE_TYPES = {"physical"}
VALID_BATTLE_DAMAGE_TYPES = {"physical", "elemental", "fixed"}
VALID_BATTLE_ELEMENTS = {"fire", "ice", "earth", "thunder"}


def error(errors: list[str], path: str, message: str) -> None:
    errors.append(f"[ERROR] {path} {message}")


def require_keys(errors: list[str], path: str, data: dict[str, Any], keys: set[str]) -> None:
    for key in sorted(keys):
        if key not in data:
            error(errors, path, f"is missing required field: {key}")


def is_non_negative_int(value: Any) -> bool:
    return isinstance(value, int) and value >= 0


def check_jobs(errors: list[str]) -> None:
    required_base = {"max_hp", "max_mp", "attack", "magic_attack", "defense", "magic_defense", "agility", "effect_accuracy", "crit"}
    required_growth = {"max_hp", "max_mp", "attack", "magic_attack", "defense", "magic_defense", "agility"}
    for job_id, job in JOBS.items():
        require_keys(errors, f"JOBS.{job_id}", job, {"base", "growth", "extra_every_3", "base_skills"})
        base = job.get("base", {})
        growth = job.get("growth", {})
        require_keys(errors, f"JOBS.{job_id}.base", base, required_base)
        require_keys(errors, f"JOBS.{job_id}.growth", growth, required_growth)
        for skill_id in job.get("base_skills", []):
            if skill_id not in SKILLS:
                error(errors, f"JOBS.{job_id}.base_skills", f"references missing skill_id: {skill_id}")


def check_promotions(errors: list[str]) -> None:
    promotion_ids = list(PROMOTIONS)
    if len(promotion_ids) != len(set(promotion_ids)):
        error(errors, "PROMOTIONS", "contains duplicate promotion ids")

    for promotion_id, promotion in PROMOTIONS.items():
        require_keys(errors, f"PROMOTIONS.{promotion_id}", promotion, {"source_job", "name", "summary", "requirements", "status"})

        source_job = promotion.get("source_job")
        if source_job not in JOBS:
            error(errors, f"PROMOTIONS.{promotion_id}.source_job", f"references missing job_id: {source_job}")

        for field in ("name", "summary"):
            if not isinstance(promotion.get(field), str) or not promotion.get(field).strip():
                error(errors, f"PROMOTIONS.{promotion_id}.{field}", "must be a non-empty string")

        status = promotion.get("status")
        if status not in VALID_PROMOTION_STATUSES:
            error(errors, f"PROMOTIONS.{promotion_id}.status", f"uses unsupported status: {status}")

        requirements = promotion.get("requirements")
        if not isinstance(requirements, list):
            error(errors, f"PROMOTIONS.{promotion_id}.requirements", "must be a list")
            continue

        for idx, requirement in enumerate(requirements):
            path = f"PROMOTIONS.{promotion_id}.requirements[{idx}]"
            if not isinstance(requirement, dict):
                error(errors, path, f"must be a dict: {requirement}")
                continue
            require_keys(errors, path, requirement, {"kind", "label"})
            kind = requirement.get("kind")
            if kind not in VALID_PROMOTION_REQUIREMENT_KINDS:
                error(errors, f"{path}.kind", f"uses unsupported requirement kind: {kind}")
                continue
            if not isinstance(requirement.get("label"), str) or not requirement.get("label").strip():
                error(errors, f"{path}.label", "must be a non-empty string")

            if kind == "level":
                if not isinstance(requirement.get("value"), int) or requirement.get("value") <= 0:
                    error(errors, f"{path}.value", "must be a positive int")
            else:
                if "key" not in requirement:
                    error(errors, path, "is missing required field: key")
                    continue
                key = requirement.get("key")
                if kind == "unlock" and key not in all_unlock_producers():
                    error(errors, f"{path}.key", f"has no known unlock producer: {key}")
                elif kind == "quest" and key not in QUESTS:
                    error(errors, f"{path}.key", f"references missing quest_id: {key}")
                elif kind == "flag" and key not in KNOWN_FLAG_KEYS:
                    error(errors, f"{path}.key", f"references unknown flag: {key}")
                elif kind == "item" and key not in all_item_like_ids():
                    error(errors, f"{path}.key", f"references missing item/material id: {key}")


def check_job_specializations(errors: list[str]) -> None:
    for specialization_id, specialization in JOB_SPECIALIZATIONS.items():
        require_keys(
            errors,
            f"JOB_SPECIALIZATIONS.{specialization_id}",
            specialization,
            {"source_job", "name", "summary", "identity", "effect_preview", "status"},
        )

        source_job = specialization.get("source_job")
        if source_job not in JOBS:
            error(
                errors,
                f"JOB_SPECIALIZATIONS.{specialization_id}.source_job",
                f"references missing job_id: {source_job}",
            )

        for field in ("name", "summary", "identity", "effect_preview"):
            if not isinstance(specialization.get(field), str) or not specialization.get(field).strip():
                error(errors, f"JOB_SPECIALIZATIONS.{specialization_id}.{field}", "must be a non-empty string")

        status = specialization.get("status")
        if status not in VALID_JOB_SPECIALIZATION_STATUSES:
            error(errors, f"JOB_SPECIALIZATIONS.{specialization_id}.status", f"uses unsupported status: {status}")


def check_relic_unlock(errors: list[str], path: str, unlock_data: Any) -> None:
    if not isinstance(unlock_data, dict):
        error(errors, path, "must be a dict")
        return

    require_keys(errors, path, unlock_data, {"kind", "label"})
    kind = unlock_data.get("kind")
    if kind not in VALID_RELIC_UNLOCK_KINDS:
        error(errors, f"{path}.kind", f"uses unsupported unlock kind: {kind}")
        return
    if not isinstance(unlock_data.get("label"), str) or not unlock_data.get("label").strip():
        error(errors, f"{path}.label", "must be a non-empty string")

    if kind == "level":
        if not isinstance(unlock_data.get("value"), int) or unlock_data.get("value") <= 0:
            error(errors, f"{path}.value", "must be a positive int")
        return

    if "key" not in unlock_data:
        error(errors, path, "is missing required field: key")
        return
    key = unlock_data.get("key")
    if kind == "unlock" and key not in all_unlock_producers():
        error(errors, f"{path}.key", f"has no known unlock producer: {key}")
    elif kind == "quest" and key not in QUESTS:
        error(errors, f"{path}.key", f"references missing quest_id: {key}")
    elif kind == "flag" and key not in KNOWN_FLAG_KEYS:
        error(errors, f"{path}.key", f"references unknown flag: {key}")
    elif kind == "item" and key not in all_item_like_ids():
        error(errors, f"{path}.key", f"references missing item/material id: {key}")


def check_relics(errors: list[str]) -> None:
    relic_ids = list(RELICS)
    if len(relic_ids) != len(set(relic_ids)):
        error(errors, "RELICS", "contains duplicate relic ids")

    for relic_id, relic in RELICS.items():
        require_keys(
            errors,
            f"RELICS.{relic_id}",
            relic,
            {
                "action_label",
                "complete_flag",
                "complete_text",
                "effect_preview",
                "element_id",
                "label",
                "locked_text",
                "name",
                "ready_text",
                "seal_item_id",
                "source",
                "source_item_id",
                "source_required",
                "status",
                "summary",
            },
        )

        for field in (
            "action_label",
            "complete_text",
            "effect_preview",
            "label",
            "locked_text",
            "name",
            "ready_text",
            "source",
            "summary",
        ):
            if not isinstance(relic.get(field), str) or not relic.get(field).strip():
                error(errors, f"RELICS.{relic_id}.{field}", "must be a non-empty string")

        element_id = relic.get("element_id")
        if element_id not in VALID_RELIC_ELEMENT_IDS:
            error(errors, f"RELICS.{relic_id}.element_id", f"uses unsupported element id: {element_id}")

        source_required = relic.get("source_required")
        if not isinstance(source_required, int) or source_required <= 0:
            error(errors, f"RELICS.{relic_id}.source_required", "must be a positive int")

        for field in ("source_item_id", "seal_item_id"):
            item_id = relic.get(field)
            if item_id not in all_item_like_ids():
                error(errors, f"RELICS.{relic_id}.{field}", f"references missing item/material id: {item_id}")

        complete_flag = relic.get("complete_flag")
        if complete_flag not in KNOWN_FLAG_KEYS:
            error(errors, f"RELICS.{relic_id}.complete_flag", f"references unknown flag: {complete_flag}")

        status = relic.get("status")
        if status not in VALID_RELIC_STATUSES:
            error(errors, f"RELICS.{relic_id}.status", f"uses unsupported status: {status}")

        if "unlock" in relic:
            check_relic_unlock(errors, f"RELICS.{relic_id}.unlock", relic["unlock"])

        choices = relic.get("passive_choices")
        if not isinstance(choices, list) or len(choices) != 4:
            error(errors, f"RELICS.{relic_id}.passive_choices", "must contain exactly four choices")
            continue
        choice_ids = set()
        for index, choice in enumerate(choices):
            path = f"RELICS.{relic_id}.passive_choices[{index}]"
            if not isinstance(choice, dict):
                error(errors, path, "must be a dict")
                continue
            require_keys(errors, path, choice, {"id", "label", "summary", "effect"})
            choice_id = choice.get("id")
            if not isinstance(choice_id, str) or not choice_id:
                error(errors, f"{path}.id", "must be a non-empty string")
            elif choice_id in choice_ids:
                error(errors, f"{path}.id", "must be unique per relic")
            else:
                choice_ids.add(choice_id)
            for field in ("label", "summary"):
                if not isinstance(choice.get(field), str) or not choice[field].strip():
                    error(errors, f"{path}.{field}", "must be a non-empty string")
            effect = choice.get("effect")
            if not isinstance(effect, dict) or len(effect) != 1:
                error(errors, f"{path}.effect", "must contain exactly one effect")
                continue
            effect_id, value = next(iter(effect.items()))
            if effect_id not in VALID_RELIC_PASSIVE_EFFECTS:
                error(errors, f"{path}.effect", f"uses unsupported effect: {effect_id}")
            if not isinstance(value, int) or value <= 0:
                error(errors, f"{path}.effect.{effect_id}", "must be a positive int")


def check_items(errors: list[str]) -> None:
    for item_id, item in ITEMS.items():
        require_keys(errors, f"ITEMS.{item_id}", item, {"name", "kind", "price", "desc"})
        if item.get("kind") not in VALID_ITEM_KINDS:
            error(errors, f"ITEMS.{item_id}.kind", f"uses unsupported kind: {item.get('kind')}")
        if not is_non_negative_int(item.get("price")):
            error(errors, f"ITEMS.{item_id}.price", "must be a non-negative int")
        unlock_key = item.get("unlock")
        if unlock_key and unlock_key not in all_unlock_producers():
            error(errors, f"ITEMS.{item_id}.unlock", f"has no known producer: {unlock_key}")
        region = item.get("region")
        if region and region not in VALID_REGIONS:
            error(errors, f"ITEMS.{item_id}.region", f"uses unsupported region: {region}")
        battle_effect = item.get("battle_effect")
        if item.get("kind") == "battle":
            if not isinstance(battle_effect, dict):
                error(errors, f"ITEMS.{item_id}.battle_effect", "battle item must define an effect object")
                continue
            damage_type = battle_effect.get("damage_type")
            if damage_type not in VALID_BATTLE_DAMAGE_TYPES:
                error(errors, f"ITEMS.{item_id}.battle_effect.damage_type", "uses unsupported damage type")
            if not isinstance(battle_effect.get("power"), int) or battle_effect["power"] <= 0:
                error(errors, f"ITEMS.{item_id}.battle_effect.power", "must be a positive int")
            if damage_type == "elemental" and battle_effect.get("element") not in VALID_BATTLE_ELEMENTS:
                error(errors, f"ITEMS.{item_id}.battle_effect.element", "must be a core element")
            if damage_type == "physical" and battle_effect.get("element") is not None:
                error(errors, f"ITEMS.{item_id}.battle_effect.element", "physical battle items cannot declare an element")
            if damage_type == "fixed" and battle_effect.get("element") is not None:
                error(errors, f"ITEMS.{item_id}.battle_effect.element", "fixed battle items cannot declare an element")
            turns = battle_effect.get("defense_down_turns", 0)
            if not isinstance(turns, int) or turns < 0:
                error(errors, f"ITEMS.{item_id}.battle_effect.defense_down_turns", "must be a non-negative int")
            jobs = item.get("jobs")
            if jobs is not None and (not isinstance(jobs, list) or not jobs or any(job_id not in JOBS for job_id in jobs)):
                error(errors, f"ITEMS.{item_id}.jobs", "must be a non-empty list of known job ids")
            dot = battle_effect.get("dot")
            if dot is not None:
                if not isinstance(dot, dict):
                    error(errors, f"ITEMS.{item_id}.battle_effect.dot", "must be an object")
                elif (
                    not isinstance(dot.get("status"), str) or not dot["status"].strip()
                    or not isinstance(dot.get("duration"), int) or dot["duration"] <= 0
                    or not isinstance(dot.get("power"), int) or dot["power"] <= 0
                    or dot.get("damage_type") != "fixed"
                ):
                    error(errors, f"ITEMS.{item_id}.battle_effect.dot", "must define a fixed status, positive duration, and positive power")
        elif battle_effect is not None:
            error(errors, f"ITEMS.{item_id}.battle_effect", "only battle items may define an effect")


def check_equipment(errors: list[str]) -> None:
    for eq_id, equipment in EQUIPMENT.items():
        require_keys(errors, f"EQUIPMENT.{eq_id}", equipment, {"name", "slot", "subtype", "price", "jobs", "stats", "desc"})
        if equipment.get("slot") not in VALID_SLOTS:
            error(errors, f"EQUIPMENT.{eq_id}.slot", f"uses unsupported slot: {equipment.get('slot')}")
        if not is_non_negative_int(equipment.get("price")):
            error(errors, f"EQUIPMENT.{eq_id}.price", "must be a non-negative int")
        for job_id in equipment.get("jobs", []):
            if job_id not in JOBS:
                error(errors, f"EQUIPMENT.{eq_id}.jobs", f"references missing job_id: {job_id}")
        for stat_key in equipment.get("stats", {}):
            if stat_key not in VALID_EQUIPMENT_STATS:
                error(errors, f"EQUIPMENT.{eq_id}.stats", f"uses unsupported stat key: {stat_key}")
        unlock_key = equipment.get("unlock")
        if unlock_key and unlock_key not in all_unlock_producers():
            error(errors, f"EQUIPMENT.{eq_id}.unlock", f"has no known producer: {unlock_key}")
        region = equipment.get("region")
        if region and region not in VALID_REGIONS:
            error(errors, f"EQUIPMENT.{eq_id}.region", f"uses unsupported region: {region}")
        followup = equipment.get("normal_attack_followup")
        if followup is not None:
            if equipment.get("slot") != "head":
                error(errors, f"EQUIPMENT.{eq_id}.normal_attack_followup", "is only supported on head-slot pseudo-offhands")
            if not isinstance(followup, dict):
                error(errors, f"EQUIPMENT.{eq_id}.normal_attack_followup", "must be an object")
                continue
            require_keys(errors, f"EQUIPMENT.{eq_id}.normal_attack_followup", followup, {"multiplier", "element"})
            multiplier = followup.get("multiplier")
            if not isinstance(multiplier, (int, float)) or isinstance(multiplier, bool) or multiplier <= 0:
                error(errors, f"EQUIPMENT.{eq_id}.normal_attack_followup.multiplier", "must be a positive number")
            if not isinstance(followup.get("element"), str) or not followup.get("element"):
                error(errors, f"EQUIPMENT.{eq_id}.normal_attack_followup.element", "must be a non-empty string")
            on_hit = followup.get("on_hit")
            if on_hit is not None:
                if not isinstance(on_hit, dict):
                    error(errors, f"EQUIPMENT.{eq_id}.normal_attack_followup.on_hit", "must be an object")
                    continue
                require_keys(errors, f"EQUIPMENT.{eq_id}.normal_attack_followup.on_hit", on_hit, {"status", "duration", "chance", "multiplier", "damage_type"})
                if on_hit.get("status") not in {"bleed", "poison"}:
                    error(errors, f"EQUIPMENT.{eq_id}.normal_attack_followup.on_hit.status", "must be bleed or poison")
                expected_duration = {"bleed": 3, "poison": 5}.get(on_hit.get("status"))
                if expected_duration is not None and on_hit.get("duration") != expected_duration:
                    error(errors, f"EQUIPMENT.{eq_id}.normal_attack_followup.on_hit.duration", f"must be {expected_duration} for {on_hit.get('status')}")
                if not is_non_negative_int(on_hit.get("chance")) or on_hit.get("chance") > 100:
                    error(errors, f"EQUIPMENT.{eq_id}.normal_attack_followup.on_hit.chance", "must be an integer from 0 to 100")
                if not isinstance(on_hit.get("multiplier"), (int, float)) or isinstance(on_hit.get("multiplier"), bool) or on_hit.get("multiplier") <= 0:
                    error(errors, f"EQUIPMENT.{eq_id}.normal_attack_followup.on_hit.multiplier", "must be a positive number")
                if on_hit.get("damage_type") not in VALID_FOLLOWUP_DAMAGE_TYPES:
                    error(errors, f"EQUIPMENT.{eq_id}.normal_attack_followup.on_hit.damage_type", "must be physical")


def check_skills(errors: list[str]) -> None:
    for skill_id, skill in SKILLS.items():
        require_keys(errors, f"SKILLS.{skill_id}", skill, {"name", "mp", "kind", "desc"})
        kind = skill.get("kind")
        if kind not in VALID_SKILL_KINDS:
            error(errors, f"SKILLS.{skill_id}.kind", f"uses unsupported kind: {kind}")
            continue
        if not is_non_negative_int(skill.get("mp")):
            error(errors, f"SKILLS.{skill_id}.mp", "must be a non-negative int")
        if kind == "damage":
            require_keys(errors, f"SKILLS.{skill_id}", skill, {"stat", "element", "multiplier"})
            if skill.get("stat") not in VALID_DAMAGE_STATS:
                error(errors, f"SKILLS.{skill_id}.stat", f"uses unsupported damage stat: {skill.get('stat')}")
            charge_bonus = skill.get("charge_bonus_per_stack")
            if charge_bonus is not None and not (
                skill.get("stat") == "attack"
                and isinstance(charge_bonus, (int, float))
                and not isinstance(charge_bonus, bool)
                and charge_bonus > 0
            ):
                error(errors, f"SKILLS.{skill_id}.charge_bonus_per_stack", "must be a positive number on a physical damage skill")
            on_hit = skill.get("on_hit")
            if on_hit:
                require_keys(errors, f"SKILLS.{skill_id}.on_hit", on_hit, {"status", "duration", "chance", "multiplier", "damage_type"})
                if on_hit.get("status") not in VALID_EFFECT_KEYS:
                    error(errors, f"SKILLS.{skill_id}.on_hit.status", "uses unsupported effect key")
                expected_duration = {"bleed": 3, "poison": 5}.get(on_hit.get("status"))
                if expected_duration is not None and on_hit.get("duration") != expected_duration:
                    error(errors, f"SKILLS.{skill_id}.on_hit.duration", f"must be {expected_duration} for {on_hit.get('status')}")
        elif kind == "heal":
            require_keys(errors, f"SKILLS.{skill_id}", skill, {"amount"})
        elif kind == "buff":
            require_keys(errors, f"SKILLS.{skill_id}", skill, {"buff", "duration"})
            if skill.get("buff") not in VALID_EFFECT_KEYS:
                error(errors, f"SKILLS.{skill_id}.buff", f"uses unsupported effect key: {skill.get('buff')}")
            buff_stats = skill.get("buff_stats")
            if buff_stats is not None:
                if not isinstance(buff_stats, dict) or not buff_stats:
                    error(errors, f"SKILLS.{skill_id}.buff_stats", "must be a non-empty stat dict")
                else:
                    for stat_key, value in buff_stats.items():
                        if stat_key not in VALID_BUFF_STAT_KEYS or not is_non_negative_int(value):
                            error(errors, f"SKILLS.{skill_id}.buff_stats.{stat_key}", "must be a non-negative supported buff stat")
        elif kind == "debuff":
            require_keys(errors, f"SKILLS.{skill_id}", skill, {"debuff", "duration"})
            if skill.get("debuff") not in VALID_EFFECT_KEYS:
                error(errors, f"SKILLS.{skill_id}.debuff", f"uses unsupported effect key: {skill.get('debuff')}")
            damage_percent = skill.get("damage_percent")
            if damage_percent is not None and (not is_non_negative_int(damage_percent) or damage_percent <= 0 or damage_percent > 100):
                error(errors, f"SKILLS.{skill_id}.damage_percent", "must be an int from 1 to 100")
            if damage_percent is not None and skill.get("damage_scope") not in VALID_DAMAGE_SCOPES:
                error(errors, f"SKILLS.{skill_id}.damage_scope", "uses unsupported damage scope")
        elif kind == "dot":
            require_keys(errors, f"SKILLS.{skill_id}", skill, {"stat", "element", "duration", "multiplier"})
            if skill.get("stat") != "magic":
                error(errors, f"SKILLS.{skill_id}.stat", "magic dot must use magic stat")
        elif kind == "regen":
            require_keys(errors, f"SKILLS.{skill_id}", skill, {"duration", "amount", "multiplier"})
        elif kind == "passive":
            triggers = skill.get("passive_triggers")
            if skill.get("mp") != 0:
                error(errors, f"SKILLS.{skill_id}.mp", "passive skills must cost 0 MP")
            if not isinstance(triggers, list) or not triggers:
                error(errors, f"SKILLS.{skill_id}.passive_triggers", "must be a non-empty list")
                continue
            for index, trigger in enumerate(triggers):
                path = f"SKILLS.{skill_id}.passive_triggers[{index}]"
                if not isinstance(trigger, dict):
                    error(errors, path, "must be a mapping")
                    continue
                require_keys(errors, path, trigger, {"job", "event", "requires", "effect"})
                if trigger.get("job") not in JOBS:
                    error(errors, f"{path}.job", "references missing job_id")
                if trigger.get("event") not in VALID_PASSIVE_EVENTS:
                    error(errors, f"{path}.event", "uses unsupported passive event")
                requires = trigger.get("requires")
                if not isinstance(requires, dict):
                    error(errors, f"{path}.requires", "must be a mapping")
                elif trigger.get("event") == "physical_charge_reaches" and requires.get("stacks") != 3:
                    error(errors, f"{path}.requires.stacks", "must be 3 for physical_charge_reaches")
                elif trigger.get("event") == "physical_status_applied" and set(requires.get("statuses", [])) - {"bleed", "poison"}:
                    error(errors, f"{path}.requires.statuses", "supports only bleed and poison")
                effect = trigger.get("effect")
                if not isinstance(effect, dict) or effect.get("kind") not in VALID_PASSIVE_EFFECT_KINDS:
                    error(errors, f"{path}.effect", "uses unsupported passive effect")
                    continue
                if not isinstance(effect.get("state_key"), str) or not effect["state_key"]:
                    error(errors, f"{path}.effect.state_key", "must be a non-empty string")
                if effect["kind"] == "charge_skill_bonus" and (not is_non_negative_int(effect.get("damage_percent")) or effect.get("damage_percent") <= 0):
                    error(errors, f"{path}.effect.damage_percent", "must be a positive int")
                if effect["kind"] == "extra_normal_followup" and (effect.get("uses") != 1 or not isinstance(effect.get("followup_multiplier"), (int, float)) or effect.get("followup_multiplier") <= 0):
                    error(errors, f"{path}.effect", "requires uses=1 and a positive followup_multiplier")
                group = trigger.get("replacement_group")
                if group is not None and (not isinstance(group, str) or not group or not is_non_negative_int(trigger.get("priority"))):
                    error(errors, path, "replacement_group requires a non-negative priority")


def check_magic_books(errors: list[str]) -> None:
    taught_skills: dict[str, str] = {}
    for book_id, book in MAGIC_BOOKS.items():
        require_keys(errors, f"MAGIC_BOOKS.{book_id}", book, {"name", "jobs", "level", "price", "materials", "skill"})
        for job_id in book.get("jobs", []):
            if job_id not in JOBS:
                error(errors, f"MAGIC_BOOKS.{book_id}.jobs", f"references missing job_id: {job_id}")
        for material_id in book.get("materials", {}):
            if material_id not in MATERIALS:
                error(errors, f"MAGIC_BOOKS.{book_id}.materials", f"references missing material_id: {material_id}")
        skill_id = book.get("skill")
        if skill_id not in SKILLS:
            error(errors, f"MAGIC_BOOKS.{book_id}.skill", f"references missing skill_id: {skill_id}")
        elif skill_id in taught_skills:
            error(errors, f"MAGIC_BOOKS.{book_id}.skill", f"duplicates skill taught by {taught_skills[skill_id]}: {skill_id}")
        else:
            taught_skills[skill_id] = book_id
        region = book.get("region")
        if region and region not in VALID_REGIONS:
            error(errors, f"MAGIC_BOOKS.{book_id}.region", f"uses unsupported region: {region}")


def check_recipes(errors: list[str]) -> None:
    for recipe_id, recipe in RECIPES.items():
        require_keys(errors, f"RECIPES.{recipe_id}", recipe, {"name", "output", "materials", "gold", "unlock", "desc"})
        if not is_non_negative_int(recipe.get("gold")):
            error(errors, f"RECIPES.{recipe_id}.gold", "must be a non-negative int")
        for output_id in recipe.get("output", {}):
            if output_id not in all_sellable_ids():
                error(errors, f"RECIPES.{recipe_id}.output", f"references missing item/equipment id: {output_id}")
        for material_id in recipe.get("materials", {}):
            if material_id not in all_material_ids():
                error(errors, f"RECIPES.{recipe_id}.materials", f"references missing material_id: {material_id}")
        base_item = recipe.get("base_item")
        if base_item and base_item not in all_sellable_ids():
            error(errors, f"RECIPES.{recipe_id}.base_item", f"references missing item/equipment id: {base_item}")
        unlock_key = recipe.get("unlock")
        if unlock_key not in all_unlock_producers():
            error(errors, f"RECIPES.{recipe_id}.unlock", f"has no known producer: {unlock_key}")
        region = recipe.get("region")
        if region and region not in VALID_REGIONS:
            error(errors, f"RECIPES.{recipe_id}.region", f"uses unsupported region: {region}")


def check_monsters(errors: list[str]) -> None:
    required = {"name", "level", "hp", "attack", "defense", "agility", "crit", "element", "race", "exp", "gold", "drops"}
    for monster_id, monster in MONSTERS.items():
        require_keys(errors, f"MONSTERS.{monster_id}", monster, required)
        if monster.get("race") not in VALID_MONSTER_RACES:
            error(errors, f"MONSTERS.{monster_id}.race", f"uses unsupported race: {monster.get('race')}")
        gold = monster.get("gold")
        if not (isinstance(gold, tuple) and len(gold) == 2 and gold[0] <= gold[1]):
            error(errors, f"MONSTERS.{monster_id}.gold", "must be tuple(min, max)")
        for drop in monster.get("drops", []):
            if not (isinstance(drop, tuple) and len(drop) == 3):
                error(errors, f"MONSTERS.{monster_id}.drops", f"has invalid drop tuple: {drop}")
                continue
            drop_id, chance, qty = drop
            if drop_id not in all_item_like_ids():
                error(errors, f"MONSTERS.{monster_id}.drops", f"references missing item/material id: {drop_id}")
            if not (isinstance(chance, float) and 0 <= chance <= 1):
                error(errors, f"MONSTERS.{monster_id}.drops", f"has invalid chance for {drop_id}: {chance}")
            if not (isinstance(qty, int) and qty > 0):
                error(errors, f"MONSTERS.{monster_id}.drops", f"has invalid qty for {drop_id}: {qty}")


def check_dungeons(errors: list[str]) -> None:
    required = {"name", "recommended", "steps", "element", "unlock", "materials", "monsters", "gold_range", "clear_guild", "boss"}
    for dungeon_id, dungeon in DUNGEONS.items():
        require_keys(errors, f"DUNGEONS.{dungeon_id}", dungeon, required)
        if dungeon.get("unlock") not in all_unlock_producers():
            error(errors, f"DUNGEONS.{dungeon_id}.unlock", f"has no known producer: {dungeon.get('unlock')}")
        for material_id in dungeon.get("materials", []):
            if material_id not in MATERIALS:
                error(errors, f"DUNGEONS.{dungeon_id}.materials", f"references missing material_id: {material_id}")
        for monster_id in dungeon.get("monsters", []):
            if monster_id not in MONSTERS:
                error(errors, f"DUNGEONS.{dungeon_id}.monsters", f"references missing monster_id: {monster_id}")
        boss_id = dungeon.get("boss")
        if boss_id is not None and boss_id not in MONSTERS:
            error(errors, f"DUNGEONS.{dungeon_id}.boss", f"references missing monster_id: {boss_id}")
        gold_range = dungeon.get("gold_range")
        if not (isinstance(gold_range, tuple) and len(gold_range) == 2 and gold_range[0] <= gold_range[1]):
            error(errors, f"DUNGEONS.{dungeon_id}.gold_range", "must be tuple(min, max)")
    for event_key, weight in EVENT_WEIGHTS:
        if not isinstance(event_key, str) or not isinstance(weight, int) or weight <= 0:
            error(errors, "EVENT_WEIGHTS", f"has invalid entry: {(event_key, weight)}")


def check_quests(errors: list[str]) -> None:
    valid_unlock_targets = (
        set(DUNGEONS)
        | set(QUESTS)
        | set(RECIPES)
        | {item.get("unlock") for item in ITEMS.values() if item.get("unlock")}
        | {equipment.get("unlock") for equipment in EQUIPMENT.values() if equipment.get("unlock")}
        | INITIAL_UNLOCK_KEYS
        | ENGINE_EVENT_UNLOCK_KEYS
        | STORY_UNLOCK_KEYS
        | SYSTEM_UNLOCK_KEYS
    )
    for quest_id, quest in QUESTS.items():
        require_keys(errors, f"QUESTS.{quest_id}", quest, {"title", "giver", "turn_in", "reward", "unlocks", "desc"})
        for turn_in_id in quest.get("turn_in", {}):
            if turn_in_id.startswith("flag:"):
                flag_key = turn_in_id.split(":", 1)[1]
                if flag_key not in KNOWN_FLAG_KEYS:
                    error(errors, f"QUESTS.{quest_id}.turn_in", f"references unknown flag: {turn_in_id}")
            elif turn_in_id not in all_item_like_ids():
                error(errors, f"QUESTS.{quest_id}.turn_in", f"references missing item/material id: {turn_in_id}")
        reward = quest.get("reward", {})
        require_keys(errors, f"QUESTS.{quest_id}.reward", reward, {"gold", "items", "guild"})
        for item_id in reward.get("items", {}):
            if item_id not in all_item_like_ids():
                error(errors, f"QUESTS.{quest_id}.reward.items", f"references missing item/material id: {item_id}")
        for unlock_key in quest.get("unlocks", []):
            if unlock_key not in valid_unlock_targets:
                error(errors, f"QUESTS.{quest_id}.unlocks", f"uses unknown unlock key: {unlock_key}")


def check_shops(errors: list[str]) -> None:
    for inventory_key, item_ids in SHOP_INVENTORY.items():
        if not isinstance(item_ids, list):
            error(errors, f"SHOP_INVENTORY.{inventory_key}", "must be a list")
            continue
        for item_id in item_ids:
            if item_id not in all_sellable_ids():
                error(errors, f"SHOP_INVENTORY.{inventory_key}", f"references missing item/equipment id: {item_id}")


def check_regions(errors: list[str]) -> None:
    dungeon_regions: dict[str, list[str]] = {dungeon_id: [] for dungeon_id in DUNGEONS}
    quest_regions: dict[str, list[str]] = {quest_id: [] for quest_id in QUESTS}

    for region_id, region in REGIONS.items():
        path = f"REGIONS.{region_id}"
        require_keys(errors, path, region, {"name", "town_name", "unlock_key", "dungeon_ids", "quest_ids"})

        for field in ("name", "town_name"):
            if not isinstance(region.get(field), str) or not region.get(field).strip():
                error(errors, f"{path}.{field}", "must be a non-empty string")

        unlock_key = region.get("unlock_key")
        if unlock_key is not None and unlock_key not in all_unlock_producers():
            error(errors, f"{path}.unlock_key", f"has no known unlock producer: {unlock_key}")

        dungeon_ids = region.get("dungeon_ids", [])
        if not isinstance(dungeon_ids, list):
            error(errors, f"{path}.dungeon_ids", "must be a list")
        else:
            seen_dungeons: set[str] = set()
            for dungeon_id in dungeon_ids:
                if dungeon_id in seen_dungeons:
                    error(errors, f"{path}.dungeon_ids", f"duplicates dungeon id: {dungeon_id}")
                    continue
                seen_dungeons.add(dungeon_id)
                if dungeon_id not in DUNGEONS:
                    error(errors, f"{path}.dungeon_ids", f"references missing dungeon_id: {dungeon_id}")
                    continue
                dungeon_regions[dungeon_id].append(region_id)

        quest_ids = region.get("quest_ids", [])
        if not isinstance(quest_ids, list):
            error(errors, f"{path}.quest_ids", "must be a list")
        else:
            seen_quests: set[str] = set()
            for quest_id in quest_ids:
                if quest_id in seen_quests:
                    error(errors, f"{path}.quest_ids", f"duplicates quest id: {quest_id}")
                    continue
                seen_quests.add(quest_id)
                if quest_id not in QUESTS:
                    error(errors, f"{path}.quest_ids", f"references missing quest_id: {quest_id}")
                    continue
                quest_regions[quest_id].append(region_id)

        for source_name, source, required_keys in (
            ("NPC_DISPLAY_NAMES", NPC_DISPLAY_NAMES, CORE_NPC_KEYS),
            ("FACILITY_DISPLAY_NAMES", FACILITY_DISPLAY_NAMES, CORE_FACILITY_KEYS),
            ("FACILITY_SHORT_DESCRIPTIONS", FACILITY_SHORT_DESCRIPTIONS, CORE_FACILITY_KEYS),
        ):
            entries = source.get(region_id)
            if not isinstance(entries, dict):
                error(errors, f"{source_name}.{region_id}", "must define a dict for every region")
                continue
            for key in required_keys:
                value = entries.get(key)
                if not isinstance(value, str) or not value.strip():
                    error(errors, f"{source_name}.{region_id}.{key}", "must be a non-empty string")

        # Check FACILITY_GREETINGS
        greetings = FACILITY_GREETINGS.get(region_id)
        if not isinstance(greetings, dict):
            error(errors, f"FACILITY_GREETINGS.{region_id}", "must define a dict for every region")
        else:
            required_greetings = {
                "guild": ["greeting", "welcome"],
                "weapon_workshop": ["ambiance", "quote"],
                "armor_workshop": ["ambiance", "quote"],
                "shop": ["welcome", "greeting"],
                "synthesis": ["welcome"],
                "magic_shop": ["welcome"],
                "temple": ["welcome"],
                "storage": ["locked", "unlocked"],
                "inn": ["welcome", "reject"],
            }
            for fac_key, subkeys in required_greetings.items():
                fac_entry = greetings.get(fac_key)
                if not isinstance(fac_entry, dict):
                    error(errors, f"FACILITY_GREETINGS.{region_id}.{fac_key}", "must be a dict")
                    continue
                for subkey in subkeys:
                    val = fac_entry.get(subkey)
                    if not isinstance(val, str) or not val.strip():
                        error(errors, f"FACILITY_GREETINGS.{region_id}.{fac_key}.{subkey}", "must be a non-empty string")

    for dungeon_id, region_ids in dungeon_regions.items():
        if len(region_ids) != 1:
            error(errors, f"DUNGEONS.{dungeon_id}", f"must map to exactly one region, found: {region_ids}")

    for quest_id, region_ids in quest_regions.items():
        if len(region_ids) != 1:
            error(errors, f"QUESTS.{quest_id}", f"must map to exactly one region, found: {region_ids}")


def validate() -> list[str]:
    errors: list[str] = []
    check_jobs(errors)
    check_job_specializations(errors)
    check_promotions(errors)
    check_relics(errors)
    check_items(errors)
    check_equipment(errors)
    check_skills(errors)
    check_magic_books(errors)
    check_recipes(errors)
    check_monsters(errors)
    check_dungeons(errors)
    check_quests(errors)
    check_shops(errors)
    check_regions(errors)
    return errors


def main() -> int:
    errors = validate()
    if errors:
        for message in errors:
            print(message)
        return 1
    print("data validation ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
