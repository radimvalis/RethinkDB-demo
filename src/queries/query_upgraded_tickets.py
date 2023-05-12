#!/usr/bin/env python3

from rethinkdb import r
from duration import get_query_duration

def main():

    print("=" * 30)
    print("Q3: How many fully upgraded tickets were sold in March 2022? Group by stadium.\n")

    r.connect( "localhost", 28015).repl()

    cursor = r.db(
            "booking_system"
        ).table(
            "ticket"
        ).filter(
            lambda t: t["upgrades"].contains(1, 2, 3, 4) # check upgrades
        ).eq_join(
            "eventID",
            r.db("booking_system").table("event")
        ).zip(
        ).filter(
            lambda document: document["eventDatetime"].during(r.time(2022, 3, 1, "Z"), r.time(2022, 4, 1, "Z")) # filter events from March 2022
        ).eq_join(
            "stadiumID",
            r.db("booking_system").table("stadium") 
        ).zip(
        ).pluck(
            "name"
        ).group(
            "name" # group by stadium name
        ).count(
        ).run(
            profile=True
        )
    
    for stadium, attendance in cursor["value"].items():
        print(f"{stadium}: {attendance}")

    print(f"\nQ3 duration: {get_query_duration(cursor['profile'])} ms")
    print("=" * 30)

if __name__ == "__main__":
    main()