class Shop:
    def __init__(self, name: str, location: list, products: dict) -> None:
        self.name = name
        self.location = location
        self.products = products

    def __repr__(self) -> str:
        return (f"Shop(name={self.name}, location={self.location}, "
                f"product={self.products})")
