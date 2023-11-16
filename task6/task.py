import math
from typing import List


def row_mean_difference_squared(row: List[int], mean: float):
    return (sum(v for v in row) - mean) ** 2


def calculate_Candlle_coefficient(rank_matrix: List[List[int]], num_of_ratings: int) -> float:
    variance = 0
    mean = (num_of_ratings + 1) / 2 * num_of_ratings

    variance_max = (
        sum(
            math.pow(num_of_ratings * rating - mean, 2) for rating in range(1, num_of_ratings + 1)
        ) / (num_of_ratings - 1)
    )

    for row in rank_matrix:
        variance += row_mean_difference_squared(row, mean)

    variance = variance / (num_of_ratings - 1)

    return variance / variance_max


def task(*args, **kwargs) -> float:
    if isinstance(args, str):
        raise RuntimeError("Incorrect arguments")

    num_of_experts, num_of_ratings = len(args), len(args[0]) if args else 0

    if num_of_ratings == 0:
        print("No ratings")
        return 0.0

    if num_of_ratings == 1:
        print("Only 1 rating!")
        return 1.0

    available_keys = [x for x in args[0]]
    available_keys.sort()

    # Rows - i'th key, Cols - j'th expert
    ranked_ratings = [
        [
            (args[j].index(available_keys[i]) + 1) for j in range(num_of_ratings)
        ]
        for i in range(num_of_experts)
    ]

    return calculate_Candlle_coefficient(ranked_ratings, num_of_ratings)


def print_array(arr: List, help_text: str = None) -> None:
    """For debugging purposes."""

    if help_text:
        print(help_text)

    for row in arr:
        print(row)


if __name__ == "__main__":
    task(["02", "01", "03"], ["01", "03", "02"], ["01", "03", "02"])
