import numpy as np

from csver.reader import CSVReader


class GraphData(CSVReader):

    def __init__(self, csv_str: str):
        super().__init__(csv_str)
        self.sums = self.csv.sum(axis=1)
        self.n, self.m = self.csv.shape
        self.total_entropy = 0

    def calculate_entropy(self):
        self.total_entropy = 0

        for i in range(self.n):
            row_entropy = 0

            for j in range(self.m):
                if not self.csv.loc[i, j]:
                    continue

                row_entropy += self.csv.loc[i, j] / self.n * np.log2(self.csv.loc[i, j] / self.n)

            self.total_entropy += -row_entropy

        return self.total_entropy


def task(csv_string: str) -> int:
    gD = GraphData(csv_string)
    result = gD.calculate_entropy()

    return result


if __name__ == "__main__":
    task("0,1\n3,1\n1,0\n1,0\n1,0")
