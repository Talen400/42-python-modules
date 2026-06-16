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

    def set_name(self, name: str) -> None:
        self.__name = name

    def get_name(self) -> str:
        return self.__name

    def set_height(self, height: float) -> None:
        if height < 0:
            print(f"{self.get_name()}: Error, height can't be negative")
            return
        self.__height = height

    def get_height(self) -> float:
        return self.__height

    def set_ages(self, ages: int) -> None:
        if ages < 0:
            print(f"{self.get_name()}: Error, age can't be negative")
            return
        self.__ages = ages

    def get_ages(self) -> int:
        return self.__ages

    def set_growth(self, growth: float) -> None:
        if growth < 0.0:
            print(f"{self.get_name()}: Error, growth can't be negative")
            return
        self.__growth = growth

    def get_growth(self) -> float:
        return self.__growth

    def show(self) -> str:
        return (
            f"{self.get_name()}: "
            f"{round(self.get_height(), 1)}cm, "
            f"{self.get_ages()} days old"
        )

    def grow(self) -> None:
        self.__height += self.__growth

    def age(self) -> None:
        self.__ages += 1


class Flower(Plant):
    def __init__(
            self,
            name: str = "flower",
            height: float = 0,
            ages: int = 0,
            growth: float = 1.0,
            color: str = "Red"
            ) -> None:
        super().__init__(name, height, ages, growth)
        self.__color: str = ""
        self.set_color(color)

    def set_color(self, color: str) -> None:
        self.__color = color

    def get_color(self) -> str:
        return self.__color

    def bloom(self) -> None:
        print(f"{super().get_name()} is bloom beautifully")

    def show(self) -> str:
        return (
            f"{super().get_name()} ({self.get_color()}): "
            f"{round(super().get_height(), 1)}cm, "
            f"{super().get_ages()} days old"
        )


class Tree(Plant):
    def __init__(
            self,
            name: str = "flower",
            height: float = 0,
            ages: int = 0,
            growth: float = 1.0,
            trunk_diameter: float = 1.0
            ) -> None:
        super().__init__(name, height, ages, growth)
        self.__trunk_diameter: float = 0.0
        self.set_trunk_diameter(trunk_diameter)

    def set_trunk_diameter(self, trunk_diameter: float) -> None:
        if (trunk_diameter < 0):
            print(
                f"{self.get_name()}: "
                f"Error, trunk_diameter can't be negative")
            return
        self.__trunk_diameter = trunk_diameter

    def get_trunk_diameter(self) -> float:
        return self.__trunk_diameter

    def produce_shade(self) -> None:
        print(
            f"{super().get_name()} provides "
            f"{self.__trunk_diameter * 8} "
            f"square meters of shade")

    def show(self) -> str:
        return (
            f"{super().get_name()} ({self.get_trunk_diameter()}cm): "
            f"{round(super().get_height(), 1)}cm, "
            f"{super().get_ages()} days old"
        )


class Vegetable(Plant):
    def __init__(
            self,
            name: str = "flower",
            height: float = 0,
            ages: int = 0,
            growth: float = 1.0,
            nutritional_value: float = 1.0
            ) -> None:
        super().__init__(name, height, ages, growth)
        self.__nutritional_value: float = 0.0
        self.set_nutritional_value(nutritional_value)

    def set_nutritional_value(self, nutritional_value: float) -> None:
        if (nutritional_value < 0):
            print(
                f"{self.get_name()}: "
                f"Error, nutritional_value can't be negative")
            return
        self.__nutritional_value = nutritional_value

    def get_nutritional_value(self) -> float:
        return self.__nutritional_value

    def show(self) -> str:
        return (
            f"{super().get_name()} ({self.get_nutritional_value()} kcal): "
            f"{round(super().get_height(), 1)}cm, "
            f"{super().get_ages()} days old"
        )


if __name__ == "__main__":
    garden: list[Plant] = [
        Flower("Rose", 5.0, 2, 1.5, "Yellow"),
        Tree("Oak", 50.0, 365, 5.0),
        Plant("Plant Common", 10.0, 5, 2.0),
        Vegetable("Vegetable", 10.0, 5, 2.0)
    ]

    print("=== Garden ===")
    for plant in garden:
        print(plant.show())
        match plant:
            case Tree():
                plant.produce_shade()
            case Flower():
                plant.bloom()
            case _:
                pass
        plant.grow()
        print(f"-> Post grow: {plant.show()}")
