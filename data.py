import pandas as pd


class Data:
    _id = '1zaxjdu9ESYy2MCNuDow0_5PnZpwEsyrdTQ_kk0PMZbw'
    _gid = '1175120296'

    def __init__(self):
        self.URL = f'https://docs.google.com/spreadsheets/d/{self._id}/export?format=csv&id={self._id}&gid={self._gid}'
        self.dataframe = pd.read_csv(self.URL)

    def __call__(self, item):
        value = self.dataframe[item]
        return value
