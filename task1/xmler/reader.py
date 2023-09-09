import pandas

from reader import Reader


class XMLReader(Reader):

    def __init__(self, filepath: str):
        self.dataframe = pandas.read_json(filepath)

    def get_at(self, x_path: str, *args, **kwargs) -> str:
        return ""
