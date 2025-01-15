class Auction:
    def __init__(self, id, name, description, price, ends_in):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.ends_in = ends_in

    @staticmethod
    def fromJson(json):
        return Auction(
            json["id"],
            json["name"],
            json["description"],
            json["price"],
            json["ends_in"],
        )

    def __str__(self):
        return f"{self.name} - {self.price}"
