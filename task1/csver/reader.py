import pandas

from task1.reader import Reader


class CSVReader(Reader):

    def __init__(self, filepath):
        print(filepath)
        self.csv = pandas.read_csv(filepath)
        print(self.csv)


    def get_at(self, x: int, y: int) -> str:
        print("Retrieving")

        return ""