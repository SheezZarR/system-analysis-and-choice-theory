from io import StringIO

import pandas

from reader import Reader


class CSVReader(Reader):

    def __init__(self, filepath_or_str):
        try:
            self.csv = pandas.read_csv(filepath_or_str, header=None)
        except FileNotFoundError:
            self.csv = pandas.read_csv(StringIO(filepath_or_str), sep=",", header=None)

    def get_at(self, x: int, y: int) -> str:
        return self.csv.loc[x][y]
