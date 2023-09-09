import argparse
from typing import List

from csver.reader import CSVReader
from xmler.reader import XMLReader
from jsoner.reader import JSONReader

argParser = argparse.ArgumentParser()
argParser.add_argument("-f", "--filepath", type=str, help="Enter an absolute path to the file.")
argParser.add_argument("-q", "--search-query", type=str, help="Enter a search query.")


def execute(*args, **kwargs):
    args = argParser.parse_args()

    filepath: str = args.filepath
    query: [str | List[str]] = args.search_query
    client = None

    match filepath.rsplit(".", maxsplit=1)[-1]:
        case "csv":
            client = CSVReader(filepath)
            query = query.split(",")

        case "xml":
            client = XMLReader(filepath)

        case "json":
            client = JSONReader(filepath)

    print(client.get_at(*query))


if __name__ == "__main__":
    execute()
