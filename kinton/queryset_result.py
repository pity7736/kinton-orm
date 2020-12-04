
class QuerySetResult:

    __slots__ = ('_model', '_records', '_index')

    def __init__(self, model, records):
        self._model = model
        self._records = records
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            instance = self._model(**self._records[self._index])
            self._index += 1
            return instance
        except IndexError:
            raise StopIteration

    def __len__(self):
        return len(self._records)

    def __getitem__(self, index):
        assert isinstance(index, int), 'index must be an integer'
        return self._model(**self._records[index])
