import pandas

class GraphData:

    def __init__(self, csv_str: str):
        self.csv = pandas.read_csv(csv_str)

    def calculate_row_entropy(self):
        pass

    def calculate_entropy(self):
        pass


def task(csv_string: str) -> int:
    pass


if __name__ == "__main__":
    task()
