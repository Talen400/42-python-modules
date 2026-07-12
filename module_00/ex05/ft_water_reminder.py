def ft_water_reminder() -> None:
    last = int(input("Days since last watering: "))
    if (last > 2):
        print("Water the plants!")
    else:
        print("Plants are fine")
