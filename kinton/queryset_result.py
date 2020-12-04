
class QuerySetResult:

    __slots__ = ('_model', '_records', '_index', '_iterated', '_result')

    def __init__(self, model, records):
        self._model = model
        self._records = records
        self._index = 0
        self._iterated = False
        self._result = []

    def __iter__(self):
        return self

    def __next__(self):
        try:
            if self._iterated is True:
                instance = self._result[self._index]
            else:
                instance = self._model(**self._records[self._index])
                self._result.append(instance)
        except IndexError:
            self._index = 0
            self._iterated = True
            raise StopIteration
        else:
            self._index += 1
            return instance

    def __len__(self):
        return len(self._records)

    def __getitem__(self, index):
        assert isinstance(index, int), 'index must be an integer'
        if self._iterated is True:
            return self._result[index]
        return self._model(**self._records[index])
