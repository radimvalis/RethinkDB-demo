#!/usr/bin/env python3

from rethinkdb import r
from duration import get_query_duration

def main():

    print("=" * 30)
    print("Q2: Find outdoor stadiums that are located within 300 kilometres of Prague. List their names and distances.\n")

    r.connect( "localhost", 28015).repl()

    coordinates_prague = r.point(14.418540, 50.073658)
    cursor = r.db(
            "booking_system"
        ).table(
            "stadium"
        ).get_nearest( # match stadiums near Prague
            coordinates_prague,
            unit="km",
            max_dist=300,
            index="coordinates"
        ).filter(
            {"doc": { "indoor": False } } # filter outdoor stadiums
        ).map(
            lambda document: { "distance": document["dist"], "stadium": document["doc"]["name"] }
        ).run(
            profile=True
        )

    for document in cursor["value"]:
        print(f"stadium: { document['stadium'] }, distance: { document['distance'] } km")

    print(f"\nQ2 duration: {get_query_duration(cursor['profile'])} ms")
    print("=" * 30)

if __name__ == "__main__":
    main()