import json
from typing import Text, List, Dict, Tuple, Any
from dataclasses import dataclass

import numpy as np


@dataclass
class Ranking:
    relate_matrix: np.ndarray
    rank_list: List[Tuple[int, int]]
    num_of_elems: int = 0

def unnest_list(input_list: List) -> List:
    out_list = []
    position = 0
    for elem in input_list:
        if isinstance(elem, list):
            for sub_elem in elem:
                out_list.append((sub_elem, position))

        else:
            out_list.append((elem, position))

        position += 1
        
    return out_list

def parse_json(json_str: Text) -> Ranking:
    parsed = json.loads(json_str)
    rank_set = unnest_list(parsed)

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
    print(f"Joined summed matrices: \n{joined}")

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
    """Column id is within 0 to 9 range."""

    column_sum = np.sum(ranking.relate_matrix[:10, column_id])
    other_sums = set()
    other_sums.add(column_sum)

    for i in range(column_id, 10):
        if i == column_id:
            continue

        new_sum = np.sum(ranking.relate_matrix[:10, i])

        if new_sum != column_sum:
            other_sums.add(new_sum)
        else:
            return -1, False

    return column_id, True


def get_ranking_elem(ind: int, ranking: Ranking) -> int:
    print(ranking.rank_list)
    flat = np.array(ranking.rank_list).flat

    print(f"Returning {flat[ind]}")

    return 1



def guess_position(column_id, ranking1, ranking2) -> tuple[int, bool]:
    """Column id is within 0 to 9 range."""
    pos_in_rank = 0
    
    # edge case: last element 
    # example: [1, [2, 4], 3], [1, [2, 3,] 4 ], contradiction: [[3, 4]]
    # 
    if column_id == 9:
        if ranking1.rank_list[column_id][1] != ranking1.rank_list[column_id - 1][1]:
            # position is guessable from 1
            return ranking1.rank_list[column_id][0]
        elif ranking2.rank_list[column_id][1] != ranking2.rank_list[column_id - 1][1]:
            # position is guessable from 2
            return ranking2.rank_list[column_id][0]
        else:
            return None
    else:
        if ranking1.rank_list[column_id][1] != ranking1.rank_list[column_id + 1][1]:
            # position is guessable from 1
            return ranking1.rank_list[column_id][0]
        elif ranking2.rank_list[column_id][1] != ranking2.rank_list[column_id + 1][1]:
            # position is guessable from 2
            return ranking2.rank_list[column_id][0]
        else:
            # unguessable. The point is in contradiction matrix...
            
            return None


def in_contradictions(value, contradictions):
    for contr_value, shadow_position in contradictions:
        if value == contr_value:
            return True
    return False


def rank_with_contradictions(
        contradictions: List[List[int]],
        joined: np.ndarray,
        ranking1: Ranking,
        ranking2: Ranking
) -> List:
    print("--------------------------------------------------")
    non_contradicting = [0 for _ in range(10)]
    unnested_contradictions = unnest_list(contradictions)

    for i in range(10):
        element = guess_position(i, ranking1, ranking2)

        if element and not in_contradictions(element, unnested_contradictions):
            non_contradicting[i] = element
        else:
            pass

    print(f"Non contradicting elements order: {non_contradicting}")
    out_ranking = []
    contr_id_to_insert = 0
    i = 0
    while i < len(non_contradicting):
        if non_contradicting[i]:
            out_ranking.append([non_contradicting[i]])
            i += 1
        else:
            out_ranking.append(contradictions[contr_id_to_insert])
            i += len(contradictions[contr_id_to_insert])
            contr_id_to_insert += 1

    print(f"Final answer: {out_ranking}")
    return out_ranking



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
    task("[1,[2,3],4,[5,6,7],8,9,10]", "[[1,2],[3,4,5],6,7,9,[8,10]]")
