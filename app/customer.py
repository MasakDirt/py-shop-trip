from app.car import Car
from app.shop import Shop
from math import sqrt


class Customer:
    def __init__(self, name: str,
                 product_cart: dict,
                 location: list,
                 money: int,
                 car: Car) -> None:
        self.name = name
        self.product_cart = product_cart
        self.location = location
        self.money = money
        self.car = car

    def __repr__(self) -> str:
        return (f"Customer(name={self.name}, products={self.product_cart}, "
                f"location={self.location}, "
                f"money={self.money}, car={self.car})")

    def buy_products(self, current_shop: Shop) -> float:
        total_cost = 0
        for key, value in self.product_cart.items():
            for _ in range(3):
                cost = current_shop.products[key] * value
                if ".0" in str(cost):
                    print(f"{value} {key}s for {round(cost)} dollars")
                else:
                    print(f"{value} {key}s for {cost} dollars")
                total_cost += cost
                break

        return total_cost

    def get_all_trip_costs(self, shops: list[Shop], fuel_price: float) -> dict:
        result_costs = {}
        print(f"{self.name} has {self.money} dollars")
        for shop in shops:
            trip_cost = self.calculate_trip_cost(shop, fuel_price)
            print(f"{self.name}'s trip to the {shop.name} costs {trip_cost}")
            result_costs[shop] = trip_cost

        return result_costs

    def calculate_trip_cost(self, shop: Shop, fuel_price: float) -> float:
        distance_to_shop_and_home = sqrt(
            (shop.location[0] - self.location[0]) ** 2
            + (shop.location[1] - self.location[1]) ** 2)

        fuel_cost_to_shop_and_home = (distance_to_shop_and_home
                                      * (self.car.fuel_consumption / 100)
                                      * fuel_price)

        product_cost_total = sum(shop.products[key] * value
                                 for key, value in self.product_cart.items())
        # multiply means fuel costs to home and shop
        total_trip_cost = (product_cost_total
                           + (fuel_cost_to_shop_and_home * 2))

        return round(total_trip_cost, 2)
