import math
import bisect
import pandas as pd

from typing import Iterable, Any, List, Dict, Tuple
from itertools import combinations

def powerset(iterable: Iterable[Any]) -> List[List[Any]]:
    s = list(iterable)
    return [list(j) for i in range(len(s)) for j in combinations(s, i+1)]

def shapley_values(players: List[str], characteristic_function: Dict[Tuple[Any], float]) -> Dict[str, float]:

    shapleys = {}
    coalitions = powerset(players)
    n = len(players)

    for player in players:
        shapley = 0
        for coalition in coalitions:
            if player not in coalition:
                coalition = list(sorted(coalition))
                cmod = len(coalition)
                Cui = coalition[:]
                bisect.insort_left(Cui, player)

                try:
                    temp = float(float(characteristic_function[tuple(Cui)]) - float(characteristic_function[tuple(coalition)])) *\
                                float(math.factorial(cmod) * math.factorial(n - cmod - 1)) / float(math.factorial(n))
                except:
                    temp = 0
                
                shapley += temp
        
        cmod = 0
        Cui = [player]
        temp = float(characteristic_function[tuple(Cui)]) * float(math.factorial(cmod) * math.factorial(n - cmod - 1)) / float(math.factorial(n))
        shapley += temp

        shapleys[player] = shapley

    return shapleys

def flatten_dict(nested_dict):
    res = {}
    if isinstance(nested_dict, dict):
        for k in nested_dict:
            flattened_dict = flatten_dict(nested_dict[k])
            for key, val in flattened_dict.items():
                key = list(key)
                key.insert(0, k)
                res[tuple(key)] = val
    else:
        res[()] = nested_dict
    return res


def nested_dict_to_df(values_dict):
    flat_dict = flatten_dict(values_dict)
    df = pd.DataFrame.from_dict(flat_dict, orient="index")
    df.index = pd.MultiIndex.from_tuples(df.index)
    df = df.unstack(level=-1)
    df.columns = df.columns.map("{0[1]}".format)
    return df