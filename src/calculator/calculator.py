def add(first_number: float, second_number: float) -> float:
    return first_number + second_number


def subtract(first_number: float, second_number: float) -> float:
    return first_number - second_number


def multiply(first_number: float, second_number: float) -> float:
    return first_number * second_number


def divide(numerator: float, denominator: float) -> float:
    if denominator == 0:
        raise ValueError("Denominator can not be zero.")
    return numerator / denominator
