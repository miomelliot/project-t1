# main Python V 3.13.0

def sum_range(start, end):

    if start > end:
        start, end = end, start

    sum_integers = 0

    if start % 2 != 0:
        start += 1

    while start <= end:
        sum_integers += start
        start += 2

    return sum_integers


def three_args(*, var1=None, var2=None, var3=None):
    args = {
        "var1": var1,
        "var2": var2,
        "var3": var3
    }

    filtered_args = {key: value for key,
                     value in args.items() if value is not None}

    if filtered_args:
        result = ", ".join(f"{key} = {value}" for key,
                           value in filtered_args.items())
        print(f"Переданы аргументы: {result}")


def middle_letter(word):
    length = len(word)

    if length % 2 == 1:
        return word[length // 2]
    else:
        return word[length // 2 - 1: length // 2 + 1]


def calculate(a: int, b: int) -> int:
    if a * b >= 1000:
        return a * b
    else:
        return a + b


def process_number(n):
    if n % 2 == 0:
        return sum(range(n + 1))
    else:
        product = 1
        for i in range(1, n + 1):
            product *= i
        return product


if __name__ == "__main__":
    print(sum_range(1, 8))
    print(sum_range(8, 1))
    three_args(var1=21)
    three_args(var1='Python', var3=3)
    three_args(var1='Python', var2=3, var3=9)
    print(middle_letter('test'))
    print(middle_letter('testing'))
    print(calculate(20, 50))
    print(calculate(10, 30))
    print(process_number(6))
    print(process_number(5))