import datetime
from json import load
from os import path

from app.car import Car
from app.customer import Customer
from app.shop import Shop


def get_data_from_json() -> dict:
    file_path = path.abspath("config.json")
    with open(file_path) as file:
        return load(file)


def init_customers(data: list) -> list[Customer]:
    customers = []
    for customer in data:
        customer = Customer(
            name=customer["name"],
            product_cart=customer["product_cart"],
            location=customer["location"],
            money=customer["money"],
            car=get_instance_of_car(customer["car"]), )
        customers.append(customer)

    return customers


def get_instance_of_car(car: dict) -> Car:
    return Car(brand=car["brand"], fuel_consumption=car["fuel_consumption"])


def init_shops(data: list) -> list[Shop]:
    result_list = []
    for shop in data:
        shop = Shop(
            name=shop["name"],
            location=shop["location"],
            products=shop["products"], )
        result_list.append(shop)

    return result_list


def get_min_cost_and_current_shop(trip_costs: dict) -> list:
    min_cost = float("inf")
    current_shop = ""
    for key, value in trip_costs.items():
        if min_cost > value:
            min_cost = value
            current_shop = key

    return [min_cost, current_shop]


def shop_trip() -> None:
    data = get_data_from_json()
    fuel_price = data["FUEL_PRICE"]
    customers = init_customers(data["customers"])
    shops = init_shops(data["shops"])
    for customer in customers:
        trip_costs = customer.get_all_trip_costs(shops, fuel_price)

        min_cost_and_current_shop_list = (
            get_min_cost_and_current_shop(trip_costs))

        min_cost = min_cost_and_current_shop_list[0]
        current_shop = min_cost_and_current_shop_list[1]

        if customer.money < min_cost:
            print(f"{customer.name} doesn't have enough"
                  f" money to make a purchase in any shop")
            return

        print(f"{customer.name} rides to {current_shop.name}")
        print()
        today = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"Date: {today}")
        print(f"Thanks, {customer.name}, for your purchase!")
        print("You have bought:")

        total_cost = customer.buy_products(current_shop)

        print(f"Total cost is {total_cost} dollars")
        print("See you again!")
        print()

        print(f"{customer.name} rides home")
        print(f"{customer.name} now has {customer.money - min_cost} dollars")
        print()
