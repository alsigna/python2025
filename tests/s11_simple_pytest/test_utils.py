import string
from random import choices, randint

from c18_pytest.src.s11_simple_pytest.utils import concat


def test_concat_string() -> None:
    def _get_random_string(length: int = 4) -> str:
        return "".join(choices(string.ascii_letters + string.digits, k=length))

    str_a = _get_random_string()
    str_b = _get_random_string()
    expected = str_a + str_b
    result = concat(str_a, str_b)
    assert result == expected


def test_concat_int() -> None:
    num_a = randint(1, 10)
    num_b = randint(1, 10)
    expected = num_a + num_b
    result = concat(num_a, num_b)
    assert result == expected
