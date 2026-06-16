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
    plants: list[Plant] = []

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
    for plant in plants:
        print(plant.show())
        for days in range(7):
            print(f"=== Day {days} ===")
            plant.age()
            plant.grow()
            print(plant.show())
