from math import log2
from typing import List, Tuple


def entropy(probabilities: List[float]) -> float:
    return -sum(p * log2(p) for p in probabilities if p > 0.0)


def get_probs(combinations: int) -> Tuple[List, List, List]:
    sm = {i: 0 for i in range(2, 13)}
    mult = {i: 0 for i in range(1, 37)}
    combined = {}

    for i in range(1, 7):
        for j in range(1, 7):
            sm[i + j] += 1
            mult[i * j] += 1
            combined[(i + j, i * j)] = combined.get((i + j, i * j), 0) + 1

    sm = [occurrences / combinations for occurrences in sm.values()]
    mult = [occurrences / combinations for occurrences in mult.values()]
    combined = [occurrences / combinations for occurrences in combined.values()]

    return sm, mult, combined


def task() -> list[float]:
    combinations = 36

    sum_probabilities, multi_probabilities, combined = get_probs(combinations)

    sum_entropy = entropy(sum_probabilities)
    mult_entropy = entropy(multi_probabilities)
    combined_entropy = entropy(combined)
    selected_entropy = combined_entropy - sum_entropy
    raw_mult_entropy = mult_entropy - selected_entropy

    return [sum_entropy, mult_entropy, combined_entropy, selected_entropy, raw_mult_entropy]


if __name__ == "__main__":
    print(task())
