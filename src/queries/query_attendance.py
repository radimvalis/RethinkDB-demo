#!/usr/bin/env python3

from rethinkdb import r
from duration import get_query_duration

def main():

    print("=" * 30)
    print("Q1: Calculate attendance of event with id = 100.\n")

    r.connect( "localhost", 28015).repl()
    
    event_id = 100

    cursor = r.db(
            "booking_system"
        ).table(
            "ticket"
        ).filter(
            {"eventID": event_id} # filter tickets for event with id = 100
        ).count( # count them
        ).do(
            lambda tickets_count:
                r.db(
                    "booking_system"
                ).table(
                    "event"
                ).get(
                    event_id # match event with id = 100
                ).get_field(
                    "stadiumID" # match stadium where event takes place 
                ).do(
                    lambda stadium_id:
                        r.db(
                            "booking_system"
                        ).table(
                            "stadium"
                        ).get(
                            stadium_id
                        ).get_field(
                            "capacity" # match capacity of the stadium
                        ).do(
                            lambda capacity:
                                {
                                    "tickets_count": tickets_count,
                                    "capacity": capacity
                                }
                        )
                )
        ).run(
            profile=True
        )
    
    capacity = cursor['value']['capacity']
    tickets_count = cursor['value']['tickets_count']
    
    print(f"Stadium capacity: {capacity}, purchased tickets: {tickets_count}, attendance: {tickets_count / capacity * 100} %")

    print(f"\nQ1 duration: {get_query_duration(cursor['profile'])} ms")
    print("=" * 30)

if __name__ == "__main__":
    main()