import random


class ItineraryBuilder:
    def __init__(self, ships, destinations):
        self.ships = ships
        self.destinations = destinations
        self.ports = [
            "PORT CANAVERAL, FLORIDA",
            "Fort Lauderdale, Florida",
            "Miami, Florida",
        ]
        self.itinerary_names = ["Perfect", "Blissful", "Escape", "Experience"]
        self.days = [
            {"days": 5, "destinations": 1, "price": [500, 900]},
            {"days": 7, "destinations": 2, "price": [800, 1100]},
            {"days": 7, "destinations": 2, "price": [1000, 1500]},
        ]
        self.rooms = [
            {"name": "Inside View", "multiplier": 0.8},
            {"name": "Outside View", "multiplier": 0.9},
            {"name": "Balcony", "multiplier": 1},
            {"name": "Suite", "multiplier": 1.2},
        ]

    def build(self, itinerary_count: int):
        itinerary = []
        print("--build itinerary--")
        for i in range(itinerary_count):
            d = random.choice(self.days)
            prt = random.choice(self.ports)
            sp = random.choice(self.ships)
            it_nm = random.choice(self.itinerary_names)
            dest = [
                x.get("name")
                for x in random.sample(self.destinations, k=d.get("destinations"))
            ]
            price = random.randrange(d.get("price")[0], d.get("price")[1])
            it = [{"Day": 1, "type": "port", "location": prt}]
            cnt = 2
            for e in dest:
                it.append({"Day": cnt, "type": "sea", "location": "Cruise"})
                it.append({"Day": cnt + 1, "type": "destination", "location": e})
                cnt += 2
            it.append({"Day": cnt, "type": "sea", "location": "Cruise"})
            it.append({"Day": cnt + 1, "type": "port", "location": prt})
            rms = []
            for r in self.rooms:
                rms.append(
                    {
                        "name": r.get("name"),
                        "price": round(r.get("multiplier") * price, 2),
                    }
                )

            itinerary.append(
                {
                    "name": f"{d.get('days')} Day {it_nm} Mediterranean Sea",
                    "ship": {
                        "ship_id": sp.get("ship_id"),
                        "name": sp.get("name"),
                        "description": sp.get("description"),
                    },
                    "prices": rms,
                    "itinerary": it,
                }
            )

        return itinerary
