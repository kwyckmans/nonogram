from typing import List, Set
import sys
from enum import Enum

# def settle():
#     pass


# def full_settle(p: List) -> Set:
#     """Returns set of unknown pixels"""
#     return set()


# def convert_image_to_nonogram(source_image) -> List:
#     """Converts an image to a [0,1] nonogram

#     A [0,1] nonogram basically means that we return a pixalated black and
#     white version of the image.
#     """
#     return []


# def adapt(p, U, P, L) -> List:
#     return []


# def vary(p, P, L, depth) -> List:
#     return []


# def generate_nonogram(p: List) -> Set:
#     """Generates a set of nonograms from a grayscale image.

#     Each nonogram in the set has a different difficulty and is unique. They are
#     guaruanteed to be simply (but not necessarily easily) solvable.
#     """
#     return set()

def flatten(t):
    return [item for sublist in t for item in sublist]

description = "121"
width = 7
height = 1
start_string = "xxxxxx"


# Sigma = {0, 1}
# Gamma = {0, 1, x}
# Sigma_l = {all strings of length l over Sigma}
# Gamma_l = {all strings of length l over Gamma}
# Description d, of length k > 0 = (d1, d2, .., dk) with dj = sigma_j{aj, bj}.
#  with sigma_j in Sigma and aj, bj in {0, 1, 2, ..}, with aj <= bj
#  So each dj will correspond with between aj and bj characters sigma_j.

# d = (d1, d2, ..., dk) with length k > 0. d_j = oj{aj, bj}. So, d2 is description of length 2.
# d2 = o2{a2, b2}
# dj will correspond with between aj and bj characters σj:

# description of length 2: 2 3, width 6
# Solutions: 1 1 0 1 1 1
# sigma_1^c1 * sigma+2^c2 ... * sigma+k^ck with a_j <= c_j <= b_j for j = 1 .. k
# => 1 ^ 2, 0 ^ 1, 1 ^ 3

# d = 0{0, inf}, 1{a1, a1}, 0{1, inf}, 1{a2, a2}, 0{1, inf}, ..., 1{ar, ar}, 0{0, inf}
# A0 = B0 = 0, in example: 0{0}, 1{2}, 0{1}, 1{3}
# So, if length of s < 2 + 3 => not fixable
# .., if length of s > 2 + 3 => not fixable
#
# Fix("x x x x x x", "2 3") = True
# Fix("x x x x x", "2") = True
# Fix(0, j) can only be true when Aj = 0 (so, we no longer expect any black squares)
# Fix(i, 0) is false since there can no longer be can any black squares
# Fix(i, j) is false if i < Aj or i > Bj (for 0 <= i <= l, 0 <= j <= j)
#     So: if we len(s) < number of required black squares left, or len(s) > number of required black squares left

# Descriptor:
# The description indicates the lengths of the consecutive segments of black pixels
#  along the corresponding line, in order. For example, the description “1 1” in the first row
# indicates that when traversing the pixels in that row from left to right, there should
# first be zero or more white pixels, followed by one black pixel. Then, at least
# one white pixel must occur, followed by exactly one black pixel. There may
# be additional white pixels at the end of the line. T


class State(Enum):
    Unknown = 1
    Black = 2
    White = 3


def find_last_idx_not_equal_to(
    s: str,
    state: State,
    # limit: int
) -> int:
    # Might not need limit, I will be calling is_fixable with a shorter and shorter sting.
    # The length of the string should match what I pass in in limit.
    index = 0
    for i, s in enumerate(s):
        if s != state and s != State.Unknown:
            index = i

    return index


def is_fixable(s: str, d: List[int]) -> bool:
    """Determines if a string s is fixable in relation to a description d.

    i is len(s)
    j is len(d)
    A_j is sum(a_p) with p = range(1, j)
    B_j is sum(b_p) with p = range(1, j)
    A_0, B_0 = 0

    s with length l < A_k is definitely not fixable
    s with length l > B_k is definitely not fixable
    L_i(s) is the largest index h <= i so that s_h not in {sigma, x}
    """
    i = len(s)  # position in string
    j = len(d)
    print(f"length of s: {i}, length of d: {j}")

    # An example of a description d:
    # 0^* 1^a1 0^+ 1^a2 0^+ ... 1^ar 0^*
    # A single d1, has specification:
    # dj = σj{aj, bj}
    # meaning, between aj and bj characters σj.
    #
    # As such, an a_p <= c_p <= b_p is either: 0 or infinity for '0', or c_p for '1'
    # an exact number of 1s or a number of zeroes between 0 and infinity
    # A_j is then 0 + 1  * d[0] +  0 + 1 * d[1] + 0 + 1 * d[2] ... 1 * d[j]
    # B_j is then inf + 1  * d[0] +  inf + 1 * d[1] + inf + 1 * d[2] ... 1 * d[j] + inf

    # An example:
    # d = [2, 3] means
    # 0^{0, inf} 1^2 0^{1, inf} 1^3 0 ^ {0, inf}
    # A_j is then 0 + 2 + 1 + 3 + 0
    # B_j is then inf + 2 + inf + 3 + inf

    A_j = [0] + flatten([[item, 1] for item in d[:-1]]) + d[-1:] + [0]
    B_j = (
        [sys.maxsize]
        + flatten([[item, sys.maxsize] for item in d[:-1]])
        + d[-1:]
        + [sys.maxsize]
    )

    print(f"A_j: {A_j}, B_j: {B_j}")

    if i < sum(A_j):
        # The string we have left needs to be able to fit at least all the '1's.
        print(f"i {i} smaller than sum(A_j): {A_j}")
        return False

    if i > sum(B_j):
        # The string we have left has more spaces than we need to be able to fill with '1's and '0's.
        print(f"i {i} larger than sum(B_j): {B_j}")
        return False

    sigma_j = (
        [State.White]
        + flatten([[State.Black, State.White] for item in d[:-1]])
        + [State.Black, State.White]
    )

    # Let L^σ_i(s) denote the largest index h ≤ i such that s_h not in {σ, x},
    # if such an index exists, and 0 otherwise.
    # Simply put, the first index in s where it's not equal to a certain character, x
    # and otherwise, make it 0.

    k = len(A_j) - 1  # position in description
    print(f"sigma_j: {sigma_j}, k: {k}, sigma_j[k]: {sigma_j[k]}, i: {i}")
    L_j = find_last_idx_not_equal_to(s, sigma_j[k])
    print(f"Last index not equal to {sigma_j[k]} or State.Unknown is {L_j}")

    if i > 0 and j == 0:
        print(f"We'er out of clues, but we still have string left.")
        return False

    if i == 0:
        print(f"We have no more charactes left in the string to check. \
        If we have no more clues left, then we have a fix. Othewise we don't: {sum(A_j)}")
        return sum(A_j) == 0

    print(f"Computing the max of {i - B_j[k]}, {sum(A_j[: k - 1])} and {L_j}")
    start = max(i - B_j[k], sum(A_j[: k - 1]), L_j)

    e_1 = i - A_j[k]
    e_2 = sum(B_j[: k - 1])
    print(f"Computing the min of {e_1}, {e_2}")

    end = min(e_1, e_2)
    print(end)

    for i in range(start, end + 1):
        print(f"Should call the recursion with {i}")
        # Here I need to call the recursion

    return False

    # if i == 0 and k != 0:
    #     # If there are still descriptors, we still need black pixels
    #     print("No more pixels available")
    #     return False

    # s(i) between aj and bj characters sigma_j. We want sigma_j at positions p + 1, p + 2, ..., i
    # Then a_j <= i - p <= bj.
    # In example form:
    # i = 3, s(3): 0 1 0, aj = 1, bj = 1
    # 1 <= i - p <= 1
    # -> p has to be 2.
    # s_p+1 -> s_3 => x or sigma_j
    # L_3(s) <= 2
    # s_2 must adhere to d(2), so P must be between Aj-1 and Bj-1, so A2 and B2.
    # L = 0
    # p = max(i - d[-1], sum(d[0:-1]), L)

    # d = [ 1 ]
    # x x x

if __name__ == "__main__":
    s = "xxxxxxx"
    # # 1 1 0 1 1 1 0 is a solution
    # # 0 1 1 0 1 1 1 is another solution
    d = [2, 3]
    # a_1 = 1, a_2 = 2, a_3 = 1. A_3 = a_1 + a_2 + a_3 = 4
    # b_1 = 1, b_2 = 2, b_3 = 1. B_3 = b_1 + b_2 + b_3 = 4

    # A_j = [0] + [x for x in [[y, 1] for y in d]]

    result = is_fixable(s, d)
    print(f"{s} is {'fixable' if result else 'not fixable'} in regards to {d}")
    # 2 x 1, with desc 1 | e 1: [0, 1]
    # 2 x 1, with desc 1 | 1 e: [1, 0]
