import pandas

from task1.reader import Reader


class JsonReader(Reader):

    def __init__(self, filepath):
        self.json = pandas.read_json(filepath)


    # def get_at(self, ):