class Auction:
    def __init__(self, id, name, description, price, ends_in, image, last_bidder):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.ends_in = ends_in
        self.image = image
        self.last_bidder = last_bidder

    @staticmethod
    def fromJson(json):
        return Auction(
            json["id"],
            json["name"],
            json["description"],
            json["price"],
            json["ends_in"],
            json["image"],
            json["last_bid"]
        )

    def __str__(self):
        return f"{self.name} - {self.price}"
