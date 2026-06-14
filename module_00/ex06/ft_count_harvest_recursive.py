def ft_count_harvest_recursive(day=1, days=None):
    if days is None:
        days = int(input("Days until harvest: "))
    if day > days:
        print("Harvest time!")
        return
    print(f"Day {day}")
    ft_count_harvest_recursive(day + 1, days)
