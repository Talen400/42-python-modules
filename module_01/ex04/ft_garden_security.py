class Plant:

    def __init__(
            self,
            name: str = "plant",
            height: float = 0,
            ages: int = 0,
            growth: float = 1):
        self.__name: str = name
        self.__height: float = 0.0
        self.__ages: int = 0
        self.__growth: float = 0
        self.set_height(height)
        self.set_ages(ages)
        self.set_growth(growth)

    def set_height(self, height: float) -> None:
        if height < 0:
            print(f"{self.__name}: Error, height can't be negative")
            return
        self.__height = height

    def get_height(self) -> float:
        return self.__height

    def set_ages(self, ages: int) -> None:
        if ages < 0:
            print(f"{self.__name}: Error, age can't be negative")
            return
        self.__ages = ages

    def get_ages(self) -> int:
        return self.__ages

    def set_growth(self, growth: float) -> None:
        if growth < 0.0:
            print(f"{self.__name}: Error, age can't be negative")
            return
        self.__growth = growth

    def get_growth(self) -> float:
        return self.__growth

    def show(self) -> str:
        return (
            f"{self.__name}: {round(self.__height, 1)}cm, "
            f"{self.__ages} days old"
        )

    def grow(self) -> None:
        self.__height += self.__growth

    def age(self) -> None:
        self.__ages += 1


if __name__ == "__main__":
    print("=== Garden Security System ===")
    Rose: Plant = Plant("Rose", 25, 30)
    print(Rose.show())
    Rose.set_height(-5)
    Rose.set_height(5)
    print(Rose.show())
