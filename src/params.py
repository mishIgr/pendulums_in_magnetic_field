class Params(dict):
    def __init__(self, d):
        for key, value in d.items():
            self[key] = self._convert(value)

    def _convert(self, value):
        if isinstance(value, dict):
            return Params(value)
        elif isinstance(value, (list, tuple, set)):
            return type(value)(self._convert(v) for v in value)
        else:
            return value

    def __getattribute__(self, name):
        try:
            return self[name]
        except KeyError:
            return super().__getattribute__(name)
