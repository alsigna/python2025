from collections.abc import Generator

import pytest


# фикстура для каждого теста новая
@pytest.fixture(scope="function")
def f() -> Generator[str]:
    print("\n---- setup f()")
    yield "f"
    print("\n---- teardown f()")


@pytest.fixture(scope="module")
def m() -> Generator[str]:
    print("\n---- setup m()")
    yield "m"
    print("\n---- teardown m()")


@pytest.fixture(scope="class")
def c() -> Generator[str]:
    print("\n---- setup c()")
    yield "c"
    print("\n---- teardown c()")


def test_f_a(f: str) -> None:
    assert True


def test_f_b(f: str) -> None:
    assert True


def test_m_a(m: str) -> None:
    assert True


def test_m_b(m: str) -> None:
    assert True


class TestClass1:
    def test_method_1_1(self, c: str) -> None:
        assert True

    def test_method_1_2(self, c: str) -> None:
        assert True


class TestClass2:
    def test_method_2_1(self, c: str) -> None:
        assert True

    def test_method_2_2(self, c: str) -> None:
        assert True
