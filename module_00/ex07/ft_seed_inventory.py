def ft_seed_inventory(seed_type: str, quantity: int, unit: str) -> None:
    seed_format: str = seed_type.capitalize()

    if unit not in ["packets", "grams", "area"]:
        print("Unknown unit type")
        return
    if unit == "packets":
        print(f"{seed_format} seeds: {quantity} {unit} available")
    elif unit == "grams":
        print(f"{seed_format} seeds: {quantity} {unit} total")
    elif unit == "area":
        print(f"{seed_format} seeds: covers {quantity} square meters")
