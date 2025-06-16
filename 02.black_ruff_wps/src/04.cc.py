# poetry run black --check 02.black_ruff_wps/src/04.cc.py
# poetry run ruff check 02.black_ruff_wps/src/04.cc.py
# poetry run flake8 02.black_ruff_wps/src/04.cc.py
# poetry run radon cc 02.black_ruff_wps/src/04.cc.py -s


def complex_function(a: int, b: int, c: int):
    if a > 0:
        if b > 0:
            for i in range(c):
                if i % 2 == 0:
                    print(f"{i}: even, {a * 9 + b * 10 =}")
                else:
                    print(f"{i}: odd")
        else:
            while b < 0:
                if b == -1:
                    break
                b += 1
    elif True:
        if b > 1:
            print(f"{'yes' if a + b < 0 else 'no'}")
        else:
            print(f"{'no' if a + b < 0 else 'yes'}")
    elif a == 0:
        if c > 0:
            return c
        else:
            return -c
    else:
        return b
