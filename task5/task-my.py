import json
from typing import Text, List, Dict, Tuple, Any
from dataclasses import dataclass

import numpy as np


@dataclass
class Ranking:
    relate_matrix: np.ndarray
    rank_list: List[Tuple[int, int]]
    num_of_elems: int = 0


def parse_json(json_str: Text) -> Ranking:
    parsed = json.loads(json_str)

    num_of_elems = 0
    rank_set = []

    position = 0
    for elem in parsed:
        if isinstance(elem, list):
            for sub_elem in elem:
                rank_set.append((sub_elem, position))

        else:
            rank_set.append((elem, position))

        position += 1

    num_of_elems = len(rank_set)
    relate_matrix = np.zeros((num_of_elems, num_of_elems))

    # Go over columns and fill
    for i in range(num_of_elems):
        for j in range(num_of_elems):
            if rank_set[i][1] >= rank_set[j][1]:
                relate_matrix[rank_set[j][0] - 1, rank_set[i][0] - 1] = 1

    print(f"relate_matrix: \n{relate_matrix}")
    return Ranking(relate_matrix, rank_set, num_of_elems)


def get_contradiction_kernel(ranking1: Ranking, ranking2: Ranking) -> tuple[list[list[int | Any]], Any]:
    print("Transposed relate matrices:")
    relate_matrix_t1 = np.transpose(ranking1.relate_matrix)
    print(f"Ranking 1 transposed: \n{relate_matrix_t1}")
    relate_matrix_t2 = np.transpose(ranking2.relate_matrix)
    print(f"Ranking 2 transposed: \n{relate_matrix_t2}")

    print("--------------------------------------------------")
    print("Multiplied relate matricies:")
    multiplied_orig = np.multiply(ranking1.relate_matrix, ranking2.relate_matrix)
    print(f"Originals multiplied: \n{multiplied_orig}")
    multiplied_t = np.multiply(relate_matrix_t1, relate_matrix_t2)
    print(f"Transposed multiplied: \n{multiplied_t}")

    print("--------------------------------------------------")
    joined = np.add(multiplied_orig, multiplied_t)
    print(f"Joined multiplicated matricies: \n{joined}")

    print("--------------------------------------------------")
    culprits = np.argwhere(joined == 0)
    print(f"Contradiction kernel: {culprits}")
    to_remove = np.shape(culprits)[0]
    print(f"Pairs: {to_remove} with duplicates")

    buckets = []

    for i in range(to_remove):
        x_i, x_j = culprits[i, 0] + 1, culprits[i, 1] + 1

        spot_found = False
        for j in range(len(buckets)):
            if x_i in buckets[j] or x_j in buckets[j]:
                if x_i not in buckets[j]:
                    buckets[j].append(x_i)
                elif x_j not in buckets[j]:
                    buckets[j].append(x_j)
                else:
                    pass

                spot_found = True
                break

        if not spot_found:
            buckets.append([x_i, x_j])

    print(f"Combined contradictions: {buckets}")
    return buckets, joined


def check_column_uniqueness(column_id: int, ranking: Ranking):
    column_sum = np.sum(ranking.relate_matrix[:10, column_id - 1])
    other_sums = set()
    other_sums.add(column_sum)

    for i in range(10):
        if i == column_id - 1:
            continue

        new_sum = np.sum(ranking.relate_matrix[:10, i])

        if new_sum != column_sum:
            other_sums.add(new_sum)
        else:
            return -1, False

    return column_id, True


def guess_position(column_id, ranking1, ranking2) -> int:

    position, is_ok = check_column_uniqueness(column_id, ranking1)

    # known position in ranking 1
    if is_ok:
        return position

    position, is_ok = check_column_uniqueness(column_id, ranking2)

    # Known position in ranking 2
    if is_ok:
        return position - 1

    # Position is not known in rankings but known after joining
    return column_id - 1


def rank_with_contradictions(
        contr: List[List[int]],
        culprits: np.ndarray,
        ranking1: Ranking,
        ranking2: Ranking
) -> List:
    print("--------------------------------------------------")
    positions_of_ok_points = []
    not_conflicted_locations = []

    for i in range(10):
        if np.sum(culprits[:10, i]) == 11:
            not_conflicted_locations.append(i + 1)

    print(f"Not conflicted ranks: {not_conflicted_locations}")

    for rank in not_conflicted_locations:
        guess = guess_position(rank, ranking1, ranking2)
        print(f"Guessed position for: {rank} is {guess}")
        positions_of_ok_points.append((rank, guess ))

    print(f"Ok points: {positions_of_ok_points}")

    for point in positions_of_ok_points:
        insert_position = point[1]
        shadow_ind = 0
        accumulated_ind = 0

        for i in range(len(contr)):
            if isinstance(contr[i], int):
                accumulated_ind += 1
                shadow_ind += 1
                continue

            if insert_position - (accumulated_ind + len(contr[i])) <= 0:
                break

            shadow_ind += 1
            accumulated_ind += len(contr[i])

        contr.insert(shadow_ind + 1, [point[0]])

    print(f"Final answer: {contr}")
    return contr



class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def task(ranking_1_json: Text, ranking_2_json: Text) -> Text:
    ranking_1 = parse_json(ranking_1_json)
    ranking_2 = parse_json(ranking_2_json)

    contradictions, joined = get_contradiction_kernel(ranking_1, ranking_2)
    ans = rank_with_contradictions(
        contradictions,
        joined,
        ranking_1,
        ranking_2
    )
    return json.dumps(ans, cls=NpEncoder, separators=(',', ':'))


if __name__ == "__main__":
    task("[3,[1,4],2,6,[5,7,8],[9,10]]", "[[1,2],[3,4,5],6,7,9,[8,10]]")
