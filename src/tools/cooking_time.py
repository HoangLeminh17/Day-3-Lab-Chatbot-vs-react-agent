from typing import Any, Dict, Iterable, Tuple


_TECHNIQUE_RANGES: Dict[str, Tuple[int, int]] = {
    "stir-fry": (10, 15),
    "saute": (10, 15),
    "fry": (12, 20),
    "pan-fry": (15, 25),
    "boil": (10, 20),
    "steam": (10, 20),
    "bake": (25, 40),
    "roast": (25, 45),
    "grill": (15, 30),
    "stew": (45, 90),
    "simmer": (30, 60),
    "braise": (60, 120),
    "salad": (5, 10),
    "no-cook": (3, 8),
}


_TECHNIQUE_ALIASES: Dict[str, str] = {
    "xao": "stir-fry",
    "xào": "stir-fry",
    "luoc": "boil",
    "luộc": "boil",
    "nuong": "bake",
    "nướng": "bake",
    "hap": "steam",
    "hấp": "steam",
    "chien": "fry",
    "chiên": "fry",
    "ham": "stew",
    "hầm": "stew",
    "salad": "salad",
    "khong nau": "no-cook",
    "no-cook": "no-cook",
}


def _normalize_text(value: str) -> str:
    return value.strip().lower()


def _resolve_technique(technique: str, dish_type: str) -> str:
    candidates: Iterable[str] = (
        technique,
        dish_type,
    )

    for candidate in candidates:
        normalized = _normalize_text(candidate)
        if normalized in _TECHNIQUE_RANGES:
            return normalized
        if normalized in _TECHNIQUE_ALIASES:
            return _TECHNIQUE_ALIASES[normalized]

    return "stir-fry"


def _complexity_multiplier(complexity: str) -> float:
    level = _normalize_text(complexity)
    if level in {"simple", "easy", "low"}:
        return 1.0
    if level in {"complex", "hard", "high"}:
        return 1.3
    return 1.15


def estimate_cooking_time(
    dish_type: str = "",
    ingredients_count: Any = 0,
    servings: Any = 1,
    technique: str = "",
    complexity: str = "medium",
    marinate_minutes: Any = 0,
    needs_thawing: Any = False,
    needs_preheat: Any = False,
) -> str:
    """Estimate prep/cook time using simple rules for cooking-related questions."""

    resolved_technique = _resolve_technique(technique, dish_type)
    base_min, base_max = _TECHNIQUE_RANGES[resolved_technique]
    estimated_min = (base_min + base_max) / 2

    try:
        ingredients_count_int = int(ingredients_count)
    except (TypeError, ValueError):
        ingredients_count_int = 0

    try:
        servings_int = max(1, int(servings))
    except (TypeError, ValueError):
        servings_int = 1

    try:
        marinate_minutes_int = max(0, int(marinate_minutes))
    except (TypeError, ValueError):
        marinate_minutes_int = 0

    estimated_min *= _complexity_multiplier(complexity)

    if ingredients_count_int > 5:
        estimated_min += (ingredients_count_int - 5) * 1.5

    if servings_int > 2:
        estimated_min += (servings_int - 2) * 2

    extra_notes = []
    total_additional = 0

    if marinate_minutes_int > 0:
        total_additional += marinate_minutes_int
        extra_notes.append(f"marinating adds about {marinate_minutes_int} minutes")

    if str(needs_thawing).strip().lower() in {"true", "1", "yes", "y"}:
        total_additional += 30
        extra_notes.append("thawing can add about 30 minutes")

    if str(needs_preheat).strip().lower() in {"true", "1", "yes", "y"}:
        total_additional += 10
        extra_notes.append("oven preheating can add about 10 minutes")

    cooking_min = max(3, round(estimated_min))
    cooking_max = max(cooking_min + 3, round(cooking_min * 1.25))
    total_min = cooking_min + total_additional
    total_max = cooking_max + total_additional

    note_text = "; ".join(extra_notes) if extra_notes else "no major extra prep time detected"

    return (
        f"Estimated time for {dish_type or resolved_technique}: {cooking_min}-{cooking_max} minutes "
        f"for cooking/prep. Estimated total time including extras: {total_min}-{total_max} minutes. "
        f"Technique used: {resolved_technique}. Notes: {note_text}."
    )