class Plant:

    def __init__(
            self,
            name: str = "plant",
            height: float = 0,
            ages: int = 0,
            growth: float = 1):
        self.name = name
        self.height = height
        self.ages = ages
        self.growth = growth

    def show(self) -> str:
        return f"{self.name}: {round(self.height, 1)}cm, {self.ages} days old"

    def grow(self) -> None:
        self.height += self.growth

    def age(self) -> None:
        self.ages += 1


if __name__ == "__main__":
    plants: list[Plant] = [
        Plant("Samambaia", 15.5, 10, 2.3),
        Plant("Cacto", 5.0, 42, 0.1),
        Plant("Girassol", 50.0, 5, 5.0),
        Plant("Espada de São Jorge", 30.0, 20, 1.2),
        Plant("Pilant Original", 10.0, 1, 1.5)
    ]

    print("5 plants have been pre-loaded into the garden!")
    print("Type 'exit' to run the 7-day simulation immediately.\n")
    while True:
        cmd: str = input("exit/add: ")
        if cmd == "exit":
            break
        if cmd == "add":
            try:
                name: str = input("name: ")
                height: int = int(input("height: "))
                age: int = int(input("age: "))
                growth: float = float(input("growth: "))
                plants.append(Plant(name, height, age, growth))
            except ValueError:
                print("Error type!")
        else:
            print("Error cmd!")
    print("=== Garden Plant Registry ===")
    total_plants: int = 0
    for plant in plants:
        print(plant.show())
        for days in range(7):
            print(f"=== Day {days} ===")
            plant.age()
            plant.grow()
            print(plant.show())
        total_plants += 1
    print(f"Total plants created: {total_plants}")
