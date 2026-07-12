class Plant:

    def __init__(
            self,
            name: str = "plant",
            height: float = 0,
            ages: int = 0,
            growth: float = 1):
        self._name: str = name
        self._height: float = 0.0
        self._ages: int = 0
        self._growth: float = 0
        self.set_height(height)
        self.set_ages(ages)
        self.set_growth(growth)

    def set_height(self, height: float) -> None:
        if height < 0:
            print(f"{self._name}: Error, height can't be negative")
            return
        self._height = height

    def get_height(self) -> float:
        return self._height

    def set_ages(self, ages: int) -> None:
        if ages < 0:
            print(f"{self._name}: Error, age can't be negative")
            return
        self._ages = ages

    def get_ages(self) -> int:
        return self._ages

    def set_growth(self, growth: float) -> None:
        if growth < 0.0:
            print(f"{self._name}: Error, age can't be negative")
            return
        self._growth = growth

    def get_growth(self) -> float:
        return self._growth

    def show(self) -> str:
        return (
            f"{self._name}: {round(self._height, 1)}cm, "
            f"{self._ages} days old"
        )

    def grow(self) -> None:
        self._height += self._growth

    def age(self) -> None:
        self._ages += 1


if __name__ == "__main__":
    print("=== Garden Security System ===")
    Rose: Plant = Plant("Rose", 25, 30)
    print(Rose.show())
    Rose.set_height(-5)
    Rose.set_height(5)
    print(Rose.show())
