from typing import Dict, List, TypeVar, Protocol, Iterator
from abc import abstractmethod
from itertools import accumulate, groupby
from operator import itemgetter
from functools import reduce
from math import gcd


class Comparable(Protocol):
    """Protocol for annotating comparable types."""

    @abstractmethod
    def __lt__(self, other) -> bool:
        pass


Vote = TypeVar("Vote", bound=Comparable)
Candidate = TypeVar("Candidate")


def majority_judgment(
    votes_by_candidate: Dict[Candidate, List[Vote]], reverse: bool = False, normalize: bool = False
) -> Dict[Candidate, int]:
    """
    Rank a tally using majority judgment

    Parameters
    ----------
    votes_by_candidate: Dict[Candidate, List[Vote]]
        Results of the votes
        Candidate correspond to the names of candidates,
        List of int is the votes for each candidate.
        The higher the vote, the better.

    reverse: bool
        If true, a lower vote value indicates a better vote.

    normalize: bool
        If true, candidates with different number of votes are normalized,
        it may slow down the computation with many candidates >1000.
        because 1000 * 999 = 999,000 votes are needed to compare 1000 and 999 votes.

    Returns
    -------
        Rank order for each candidate in a Dictionary Dict[Candidate, rank: int]

    Examples
    --------
    >>> A = [3, 3, 3, 0, 0, 0, 1, 1, 2, 2]
    >>> B = [0, 0, 1, 1, 2, 2, 2, 2, 3, 3]
    >>> majority_judgment({'A': A, 'B': B}, reverse=False)
    {'B': 0, 'A': 1}
    >>> majority_judgment({'A': A, 'B': B}, reverse=True)
    {'A': 0, 'B': 1}
    >>> A = [0, 4]
    >>> B = [1, 2]
    >>> majority_judgment({'A': A, 'B': B}, reverse=True)
    {'B': 0, 'A': 1}
    >>> majority_judgment({81: [0, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5], 82: [0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]})
    {82: 0, 81: 1}
    >>> C = [3, 3, 3, 0, 0, 0, 1, 1, 2, 1]
    >>> majority_judgment({'A': A, 'B': B, 'C': C}, reverse=False, normalize=True)
    """
    set_num_votes = {len(votes) for votes in votes_by_candidate.values()}
    if not len(set_num_votes) == 1 and not normalize:
        raise ValueError("All candidates must have the same number of votes, set normalize=True otherwise.")

    if normalize:
        votes_by_candidate = normalize(votes_by_candidate)

    majority_values = {
        candidate: list(compute_majority_values(votes, reverse)) for candidate, votes in votes_by_candidate.items()
    }

    ranked_scores = sorted(majority_values.items(), key=itemgetter(1), reverse=not reverse)

    ranking = {candidate: ranking for ranking, (candidate, _) in enumerate(ranked_scores)}

    return ranking


def median_grade(seq: List[float]) -> int:
    """
    Evaluates the best grades

    Parameters
    ----------
    seq: List[float]
        The list of the cumulative sum from 0 to 1

    Returns
    -------
    The index of the median grade

    >>> median_grade([0.1, 0.5, 0.7, 1.0])
    1
    >>> median_grade([0.1, 0.3, 1.0])
    2
    """
    assert all(s >= 0 for s in seq), seq
    assert seq[-1] == 1, "Normalize the sequence first"

    for i, x in enumerate(seq[:-1]):
        if x >= 0.5:
            return i
    return len(seq) - 1


def compute_majority_values(votes: List[Vote], reverse: bool) -> Iterator[Vote]:
    """
    Compute iteratively the median grades.

    Parameters
    ----------
    votes: list of all grade values obtained for a given candidate.

    Returns
    -------
    Iterator of the next majority value

    Examples from MJ book (1.5):

    >>> list(compute_majority_values([7, 11, 9, 9, 11], False))
    [9, 9, 11, 7, 11]
    >>> list(compute_majority_values([8, 11, 9, 9, 10], False))
    [9, 9, 10, 8, 11]
    """
    grades = convert_votes_to_tally(votes)
    keys = sorted(grades.keys(), reverse=reverse)
    values = [grades[key] for key in keys]
    num_votes = len(votes)

    for _ in range(num_votes):
        total = sum(values)
        cumsum = list(accumulate(values, initial=0.0))[1:]
        cumsum = [v / total for v in cumsum]

        idx = median_grade(cumsum)
        yield keys[idx]

        # remove median grade
        values[idx] -= 1
        assert values[idx] > -1


def convert_votes_to_tally(votes: List[Vote]) -> Dict[Vote, int]:
    """
    Convert the frequency of each grade as a sorted dictionary.

    >>> convert_votes_to_tally([7, 11, 9, 9, 11])
    {7: 1, 9: 2, 11: 2}
    """
    return {key: len(list(group)) for key, group in groupby(sorted(votes))}


def _lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b)


def normalize(votes_by_candidate: Dict[Candidate, List[Vote]]) -> Dict[Candidate, List[Vote]]:
    """
    Normalize the number of votes for each candidate by replicating votes.

    Parameters
    ----------
    votes_by_candidate: Dict[Candidate, List[Vote]]
        Results of the votes
        Candidate correspond to the names of candidates,
        List of int is the votes for each candidate.
        The higher the vote, the better.

    Raises
    ------
    ValueError
        If a candidate has zero votes.

    Examples
    --------
    >>> A = [3, 3, 3, 0, 0, 0, 1, 1, 2, 2]
    >>> B = [0, 0, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]
    >>> votes_by_candidate = {'A': A, 'B': B}
    >>> votes_by_candidate = normalize(votes_by_candidate)
    >>> len(votes_by_candidate['A'])
    12
    >>> len(votes_by_candidate['B'])
    12
    """
    lengths = [len(v) for v in votes_by_candidate.values()]
    if any(n == 0 for n in lengths):
        raise ValueError("Normalization impossible: a candidate has zero votes.")

    target = reduce(_lcm, lengths)

    return {candidate: votes * (target // len(votes)) for candidate, votes in votes_by_candidate.items()}
