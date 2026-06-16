class Plant:

    def __init__(self, name: str, height: int, age: int):
        self.name = name
        self.height = height
        self.age = age

    def show(self) -> str:
        return f"{self.name}: {self.height}cm, {self.age} days old"


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
                plants.append(Plant(name, height, age))
            except ValueError:
                print("Error type!")
        else:
            print("Error cmd!")
    print("=== Garden Plant Registry ===")
    for plant in plants:
        print(plant.show())
