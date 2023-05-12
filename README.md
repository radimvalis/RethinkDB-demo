# RethinkDB Demo

## Setup

* clone this repo:
```
git clone git@github.com:radimvalis/RethinkDB-demo.git
```

* download [RethinkDB](https://rethinkdb.com/docs/install/)

* start the server with following command:
```
rethinkdb
```

## Administrative UI

* to see administrative UI, visit [localhost:8080](http://localhost:8080)

## Install Python driver

```
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

## Init database and load data

```
python3 src/load_data.py
```


## Queries

* Q1: Attendance of selected event
```
python3 src/queries/query_attendance.py
```

* Q2: Stadiums near Prague
```
python3 src/queries/query_geospatial.py
```

* Q3: Fully upgraded tickets purchased in March 2022
```
python3 src/queries/query_upgraded_tickets.py
```
