def is_even(x: int) -> bool:
    if x % 2 == 0:
        return True
    else:
        return False


if __name__ == "__main__":
    if is_even(2):
        print("even")
    else:
        print("odd")
