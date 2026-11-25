
import math
from validator import valid_datetime


RECORD_KEYS = ("flight_id", "origin", "destination", "departure_datetime",
               "arrival_datetime", "price")


def valid_query(query: dict) -> bool:
    if not isinstance(query, dict):
        return False

    for key, value in query.items():
        if key in ("flight_id", "origin", "destination"):
            if not isinstance(value, str):
                return False

        elif key in ("departure_datetime", "arrival_datetime"):
            if not isinstance(value, str) or not valid_datetime(value):
                return False

        elif key in ("price", "min_price"):
            if type(value) not in (int, float):
                return False
            if isinstance(value, float) and not math.isfinite(value):
                return False

        elif key == "sort_by":
            if value not in RECORD_KEYS:
                return False

        elif key == "order":
            if value not in ("asc", "desc") or "sort_by" not in query:
                return False

        elif key == "limit":
            if type(value) is not int or value < 0:
                return False

        else:
            return False

    return True


def run_query(db: list[dict], query: dict) -> dict:
    if not valid_query(query):
        return {"query": query, "error": "INVALID_QUERY", "matches": []}

    matches = []

    # Check all search conditions for each flight.
    for flight in db:
        found = True

        for key, value in query.items():
            if key in ("flight_id", "origin", "destination"):
                if flight[key] != value:
                    found = False

            elif key == "departure_datetime":
                if flight[key] < value:
                    found = False

            elif key == "arrival_datetime":
                if flight[key] > value:
                    found = False

            elif key == "price":
                if flight["price"] > value:
                    found = False

            elif key == "min_price":
                if flight["price"] < value:
                    found = False

            if not found:
                break

        if found:
            matches.append(flight)

    # Sort first, then apply the limit.
    if "sort_by" in query:
        sort_key = query["sort_by"]
        descending = query.get("order", "asc") == "desc"
        matches.sort(key=lambda flight: flight[sort_key], reverse=descending)

    if "limit" in query:
        matches = matches[:query["limit"]]

    return {"query": query, "matches": matches}


def run_queries(db: list[dict], queries: dict | list) -> list[dict]:
    if isinstance(queries, dict):
        queries = [queries]

    results = []

    for query in queries:
        results.append(run_query(db, query))

    return results
