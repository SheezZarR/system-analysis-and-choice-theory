import pandas

from reader import Reader


class JSONReader(Reader):

    def __init__(self, filepath):
        self.dataframe = pandas.read_json(filepath)
        print(self.dataframe)

    # ./ child::*[1] / child::[1]
    def get_at(self, xpath: str, *args, **kwargs) -> str:
        return self.dataframe.xpath(xpath)
