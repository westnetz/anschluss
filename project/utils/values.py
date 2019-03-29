from configurations.values import DictValue


class ListOfDictsValue(DictValue):
    """Parse an environment variable as list of dicts."""

    def __init__(self, *args, **kwargs):
        self.seq_separator = kwargs.pop("seq_separator", ";")
        super(DictValue, self).__init__(*args, **kwargs)
        if self.default is None:
            self.default = []
        else:
            self.default = list(self.default)

    def to_python(self, value):
        split_value = [v.strip() for v in value.strip().split(self.seq_separator)]
        return [super(ListOfDictsValue, self).to_python(v) for v in split_value if v]
