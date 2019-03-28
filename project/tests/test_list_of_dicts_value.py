from ..utils.values import ListOfDictsValue


def test_empty_default():
    value = ListOfDictsValue()
    assert value.default == []  # nosec


def test_nonempty_default():
    value = ListOfDictsValue([1, 2, 3, 4])
    assert value.default == [1, 2, 3, 4]  # nosec


def test_to_python_simple():
    value = ListOfDictsValue()

    python = value.to_python('{"foo":"bar"}')
    assert python == [{"foo": "bar"}]  # nosec


def test_to_python_complex():
    value = ListOfDictsValue()

    python = value.to_python(
        '{"foo":"bar"};{"foo":"bar","baz":{"qux":"quux", "aleph":[1,2,3,4]}}'
    )
    assert python == [  # nosec
        {"foo": "bar"},
        {"foo": "bar", "baz": {"qux": "quux", "aleph": [1, 2, 3, 4]}},
    ]
