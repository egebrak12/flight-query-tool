
import argparse
import csv
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

from validator import load_airports
from csv_loader import parse_files
from query import run_queries


STUDENT_ID = "251ADB009"
FIRST_NAME = "EgeBurak"
LAST_NAME = "Ergun"


def read_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Flight query tool")

    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("-i", metavar="FILE")
    source.add_argument("-d", metavar="FOLDER")
    source.add_argument("-j", metavar="FILE")

    parser.add_argument("-a", metavar="FILE")
    parser.add_argument("-o", metavar="FILE")
    parser.add_argument("-q", metavar="FILE")
    parser.add_argument("-r", metavar="FOLDER", default=".")

    # Check command-line arguments.
    try:
        args = parser.parse_args(argv)

        if args.j is None and args.a is None:
            parser.error("-a is required with -i or -d")

        if args.j is not None and args.o is not None:
            parser.error("-o cannot be used with -j")

    except SystemExit as exc:
        return exc.code

    logger = logging.getLogger("flight_parser")
    handler = None

    try:
        if args.j is not None:
            db = read_json(args.j)

            if not isinstance(db, list) or not all(isinstance(row, dict) for row in db):
                raise ValueError("Database must be a JSON array of objects")

        else:
            output = Path(args.o if args.o is not None else "db.json")
            log_path = output.parent / "errors.log"

            # Set up the error log.
            logger.setLevel(logging.INFO)
            handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")

            handler.setFormatter(logging.Formatter(
                "%(asctime)s %(levelname)s %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            ))

            logger.addHandler(handler)

            airports = load_airports(args.a)

            if args.i is not None:
                paths = [args.i]

            else:
                paths = sorted(
                    str(path) for path in Path(args.d).iterdir()
                    if path.is_file() and path.name.endswith(".csv")
                )

                if not paths:
                    raise ValueError("No CSV files found")

            db, errors = parse_files(paths, airports)

            for error in errors:
                logger.warning(error)

            write_json(output, db)

        # Run queries if a query file is given.
        if args.q is not None:
            queries = read_json(args.q)

            if not isinstance(queries, dict):
                if not isinstance(queries, list) or not all(isinstance(q, dict) for q in queries):
                    raise ValueError("Queries must be a JSON object or an array of objects")

            results = run_queries(db, queries)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            filename = f"response_{STUDENT_ID}_{FIRST_NAME}_{LAST_NAME}_{timestamp}.json"

            write_json(Path(args.r) / filename, results)

        return 0

    except (OSError, ValueError, csv.Error) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    finally:
        if handler is not None:
            logger.removeHandler(handler)
            handler.close()


if __name__ == "__main__":
    sys.exit(main())
