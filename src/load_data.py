#!/usr/bin/env python3

import random
from datetime import datetime, timedelta
from rethinkdb import r

def create_visitors():

    given_names = ["Joe", "Peter", "Jill", "John", "George", "Amy", "Jane", "Sam", "Emma", "Emily", "Lucy", "Rose", "Lilly", "Harry", "Kevin", "Bruce", "Lisa", "Brad", "Tyler", "Stephen", "Ahmed", "Alice", "Natalie", "Sophia", "Olivia", "Mia", "David", "Evelyn", "Henry", "Lucas", "Martin"]
    family_names = ["Doe", "Smith", "Jackson", "Thompson", "Simpson", "Felix", "Miller", "Bean", "Archer", "Burns", "White", "Black", "Brown", "McDavid", "Sanches", "Adams", "Price", "Peterson", "West", "Rose", "Rice", "Austin", "Walsh", "Cohen", "Prince", "Wall", "Yates", "Froome", "Lin"]

    visitors = []
    visitor_id = 1

    for given_name in given_names:
        for family_name in family_names:

            visitors.append({
                "id": visitor_id,
                "givenName": given_name,
                "familyName": family_name,
                "age": random.randint(15, 90)
            })

            visitor_id += 1

    return visitors

def create_stadiums():

    statiums_first_names = ["City", "Town", "Olympic", "National", "Royal", "Supreme", "World", "Vision"]
    stadiums_second_names = ["Arena", "Stadium", "Hall", "Park", "Centre"]

    stadiums = []
    stadium_id = 1

    for first in statiums_first_names:
        for second in stadiums_second_names:

            stadiums.append({
                "id": stadium_id,
                "name": first + " " + second,
                "capacity": random.randint(10, 90) * 10,
                "indoor": bool(random.getrandbits(1)),
                "coordinates": r.point(random.uniform(2, 22), random.uniform(42, 54))
            })

            stadium_id += 1

    return stadiums

def create_ticket_upgrades():

    ticket_upgrades = []

    ticket_upgrades.append({
        "id": 1,
        "name": "VIP",
        "description": "Customer can access private lounge area",
        "price": 200
    })

    ticket_upgrades.append({
        "id": 2,
        "name": "Fast pass",
        "description": "Customer can skip all regular lines",
        "price": 100
    })

    ticket_upgrades.append({
        "id": 3,
        "name": "Parking reservation",
        "description": "Customer has a reserved parking spot near the stadium",
        "price": 20
    })

    ticket_upgrades.append({
        "id": 4,
        "name": "Food and beverage discount",
        "description": "Customer has discount in all restaurants at the stadium",
        "price": 30
    })

    return ticket_upgrades

def create_events_and_tickets(stadiums: list[dict], visitors: list[dict], ticket_upgrades: list[dict]):

    events = []
    event_id = 1
    event_date = datetime(2022, 1, 1, tzinfo=r.make_timezone('00:00'))

    tickets = []
    ticket_id = 1

    for _ in range(100):

        random.shuffle(visitors)
        it_visitors = iter(visitors)

        stadiums_sample = random.sample(stadiums, random.randint(0, len(stadiums)))

        for stadium in stadiums_sample:

            event_datetime = event_date + timedelta(hours=random.randint(8, 22), minutes=random.choice([0, 15, 30, 45]))
            prices = list({random.randint(10, 1000) for _ in range(random.randint(1, 4))})

            events.append({
                "id": event_id,
                "name": "Event" + (str)(event_id),
                "eventDatetime": r.expr(event_datetime),
                "prices": prices,
                "stadiumID": stadium["id"],
            })

            tickets_count = random.randint(0, stadium["capacity"])

            for i in range(1, tickets_count + 1):
                
                visitor = next(it_visitors, None)

                if visitor == None:
                    break

                purchase_datetime = event_datetime - timedelta(days=random.randint(0, 100), minutes=random.randint(0, 59), seconds=random.randint(0, 59))

                tickets.append({
                    "id": ticket_id,
                    "price": random.choice(prices),
                    "seatNumber": i,
                    "purchaseDatetime": r.expr(purchase_datetime),
                    "upgrades": [ u["id"] for u in random.sample(ticket_upgrades, random.randint(0, len(ticket_upgrades))) ],
                    "visitorID": visitor["id"],
                    "eventID": event_id
                })

                ticket_id += 1
            
            event_id += 1

        event_date += timedelta(days=1)

    return (events, tickets)

def main():

    random.seed("RethinkDB")

    print("Creating data ...")

    visitors = create_visitors()
    stadiums = create_stadiums()
    ticket_upgrades = create_ticket_upgrades()
    events, tickets = create_events_and_tickets(stadiums, visitors, ticket_upgrades)

    print("Data created")
    print("Loading data to database ...")

    r.connect( "localhost", 28015).repl()

    r.db_create("booking_system").run()

    r.db("booking_system").table_create("visitor", primary_key = "id").run()
    r.db("booking_system").table_create("stadium", primary_key = "id").run()
    r.db("booking_system").table_create("event", primary_key = "id").run()
    r.db("booking_system").table_create("ticket", primary_key = "id").run()
    r.db("booking_system").table_create("ticket_upgrade", primary_key = "id").run()

    r.db("booking_system").table("ticket").index_create("eventID").run()
    r.db("booking_system").table("ticket").index_create("visitorID").run()
    r.db("booking_system").table("event").index_create("stadiumID").run()
    r.db("booking_system").table("stadium").index_create("coordinates", geo=True).run()

    r.db("booking_system").table("visitor").insert(visitors).run()
    r.db("booking_system").table("stadium").insert(stadiums).run()
    r.db("booking_system").table("event").insert(events).run()
    r.db("booking_system").table("ticket").insert(tickets).run()
    r.db("booking_system").table("ticket_upgrade").insert(ticket_upgrades).run()

    print("Data loaded")

if __name__ == "__main__":
    main()