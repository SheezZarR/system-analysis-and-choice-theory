import pandas

from reader import Reader


class CSVReader(Reader):

    def __init__(self, filepath):
        self.csv = pandas.read_csv(filepath, header=None)

    def get_at(self, x: int, y: int) -> str:
        return self.csv.loc[x][y]
