from difflib import get_close_matches
CATEGORY_KEYWORDS = {
    "People":   ["Person", "Human", "Face", "Portrait","Headphone","Black_Hair","Boy","Girl"],
    "Food":     ["Food", "Bread", "Curry", "Meal", "Pizza", "Sandwich","Brunch"],
    "Nature":   ["Tree", "Mountain", "Water", "Sky", "Flower", "Beach","City", "Buildings","Ocean","grass"],
    "Animal":   ["Cat", "Dog", "Bird", "Animal", "Horse"],
    "Vehicle":  ["Car", "Bike", "Vehicle", "Truck"],
    "Document": ["Text", "Document", "Paper", "Book"],
}

_flat_map = {kw: cat for cat, kws in CATEGORY_KEYWORDS.items() for kw in kws}

def map_to_category(label: str, cutoff: float = 0.6) -> str:
    """
    Fuzzy-match `label` against all keywords.
     - If a close match is found (similarity ≥ cutoff), return its category.
     - Otherwise return 'Other'.
    """
    # find the single best keyword match
    matches = get_close_matches(label, _flat_map.keys(), n=1, cutoff=cutoff)
    if matches:
        return _flat_map[matches[0]]
    return "Other"