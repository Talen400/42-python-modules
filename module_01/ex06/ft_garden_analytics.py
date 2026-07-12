class Plant:
    # Class Stats (Encapsulated)

    class _Stats:
        def __init__(self) -> None:
            self.grow_count: int = 0
            self.age_count: int = 0
            self.show_count: int = 0

        def display(self) -> str:
            return (f"Stats: {self.grow_count} grow, "
                    f"{self.age_count} age, "
                    f"{self.show_count} show"
                    )

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

        self._stats = self._Stats()

        self.set_height(height)
        self.set_ages(ages)
        self.set_growth(growth)

    @staticmethod
    def is_older_than_year(days: int) -> bool:
        return days > 365

    @classmethod
    def create_anonymous(cls) -> "Plant":
        return cls(name="Unknown plant", height=0.0, ages=0, growth=1.0)

    def get_stats_display(self) -> str:
        return self._stats.display()

    # settres and getters
    def set_name(self, name: str) -> None:
        self._name = name

    def get_name(self) -> str:
        return self._name

    def set_height(self, height: float) -> None:
        if height < 0:
            print(f"{self.get_name()}: Error, height can't be negative")
            return
        self._height = height

    def get_height(self) -> float:
        return self._height

    def set_ages(self, ages: int) -> None:
        if ages < 0:
            print(f"{self.get_name()}: Error, age can't be negative")
            return
        self._ages = ages

    def get_ages(self) -> int:
        return self._ages

    def set_growth(self, growth: float) -> None:
        if growth < 0.0:
            print(f"{self.get_name()}: Error, growth can't be negative")
            return
        self._growth = growth

    def get_growth(self) -> float:
        return self._growth

    def grow(self) -> None:
        self._stats.grow_count += 1
        self._height += self._growth

    def age(self) -> None:
        self._stats.age_count += 1
        self._ages += 1

    def show(self) -> str:
        self._stats.show_count += 1
        return (
            f"{self.get_name()}: "
            f"{round(self.get_height(), 1)}cm, "
            f"{self.get_ages()} days old"
        )


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
        self._color: str = ""
        self.set_color(color)

        self._has_bloomed: bool = False

    def set_color(self, color: str) -> None:
        self._color = color

    def get_color(self) -> str:
        return self._color

    def bloom(self) -> None:
        self._has_bloomed = True
        print(f"{super().get_name()} is bloom beautifully")

    def show(self) -> str:
        self._stats.show_count += 1

        bloom_status = (
                f"{super().get_name()} is blooming beautifully!"
                if self._has_bloomed
                else f"{super().get_name()} has not bloomed yet"
                )

        return (
            f"{super().get_name()} ({self.get_color()}): "
            f"{round(super().get_height(), 1)}cm, "
            f"{super().get_ages()} days old\n"
            f"{bloom_status}"
        )


class Tree(Plant):
    class _TreeStats(Plant._Stats):
        def __init__(self) -> None:
            super().__init__()
            self.shade_count: int = 0

        def display(self) -> str:
            base_stats = super().display()
            return f"{base_stats}\n{self.shade_count} shade"

    def __init__(
            self,
            name: str = "tree",
            height: float = 0,
            ages: int = 0,
            growth: float = 1.0,
            trunk_diameter: float = 1.0
            ) -> None:
        super().__init__(name, height, ages, growth)
        self._trunk_diameter: float = 0.0
        self.set_trunk_diameter(trunk_diameter)

        self._stats: "Tree._TreeStats" = self._TreeStats()

    def set_trunk_diameter(self, trunk_diameter: float) -> None:
        if (trunk_diameter < 0):
            print(
                f"{self.get_name()}: "
                f"Error, trunk_diameter can't be negative")
            return
        self._trunk_diameter = trunk_diameter

    def get_trunk_diameter(self) -> float:
        return self._trunk_diameter

    def produce_shade(self) -> None:
        self._stats.shade_count += 1
        print(
            f"{super().get_name()} provides "
            f"{self._trunk_diameter * 8} "
            f"square meters of shade")

    def show(self) -> str:
        return (
            f"{super().get_name()} ({self.get_trunk_diameter()}cm): "
            f"{round(super().get_height(), 1)}cm, "
            f"{super().get_ages()} days old"
        )


class Seed(Flower):
    def __init__(
            self,
            name: str = "seed",
            height: float = 0,
            ages: int = 0,
            growth: float = 1.0,
            color: str = "Yellow"
            ) -> None:
        super().__init__(name, height, ages, growth, color)
        self._seeds_count: int = 0

    def bloom(self) -> None:
        super().bloom()
        self._seeds_count = 42

    def show(self) -> str:
        base_flower_show = super().show()
        return f"{base_flower_show}\nSeeds: {self._seeds_count}"


def display_plant_stats(plant: Plant) -> None:
    print(f"[Stats for {plant.get_name()}]")
    print(plant.get_stats_display())


if __name__ == "__main__":
    print("=== Garden statistics ===")
    print("=== Check year-old")
    print(f"Is 30 days more than a year? -> {Plant.is_older_than_year(30)}")
    print(f"Is 400 days more than a year? -> {Plant.is_older_than_year(400)}")

    print("=== Flower")
    rose = Flower("Rose", 15.0, 10, 8.0, "red")
    print(rose.show())
    display_plant_stats(rose)
    print("[asking the rose to grow and bloom]")
    rose.grow()
    rose.bloom()
    print(rose.show())
    display_plant_stats(rose)

    print("=== Tree")
    oak = Tree("Oak", 200.0, 365, 10.0, 5.0)
    print(oak.show())
    display_plant_stats(oak)
    print("[asking the oak to produce shade]")
    oak.produce_shade()
    display_plant_stats(oak)

    print("=== Seed")
    sunflower = Seed("Sunflower", 80.0, 45, 30.0, "yellow")
    print(sunflower.show())
    print("[make sunflower grow, age and bloom]")
    for _ in range(20):
        sunflower.grow()
        sunflower.age()
    sunflower.bloom()
    print(sunflower.show())
    display_plant_stats(sunflower)

    print("=== Anonymous")
    anonymous_plant = Plant.create_anonymous()
    print(anonymous_plant.show())
    display_plant_stats(anonymous_plant)
