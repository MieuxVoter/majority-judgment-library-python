from typing import Dict, List, TypeVar, Protocol, Iterator
from abc import abstractmethod
from itertools import accumulate, groupby
from operator import itemgetter


class Comparable(Protocol):
    """Protocol for annotating comparable types."""

    @abstractmethod
    def __lt__(self, other) -> bool:
        pass


Vote = TypeVar("Vote", bound=Comparable)
Candidate = TypeVar("Candidate")


def majority_judgment(
    votes_by_candidate: Dict[Candidate, List[Vote]], reverse: bool = False
) -> Dict[Candidate, int]:
    """
    Rank a tally using majority judgment

    Parameters
    ----------
    votes_by_candidate: Dict[Candidate, List[Vote]]
        Results of the votes
        Candidate correspond to the names of candidates,
        List of int is the votes for each candidates.
        The higher the vote, the better.

    reverse: bool
        If true, a lower vote value indicates a better vote.

    Returns
    -------
        Rank order for each candidates in a Dictionary Dict[Candidate, rank: int]


    >>> A = [0,0,0, 1,1, 2,2, 3,3,3]
    >>> B = [0,0, 1,1,2,2,2,2,3,3]
    >>> majority_judgment({'A': A, 'B': B}, reverse=False)
    {'B': 0, 'A': 1}
    >>> majority_judgment({'A': A, 'B': B}, reverse=True)
    {'A': 0, 'B': 1}
    """
    set_num_votes = {len(votes) for votes in votes_by_candidate.values()}
    if not len(set_num_votes) == 1:
        raise NotImplementedError("Unbalanced grades have not been implemented yet.")

    majority_values = {
        candidate: list(compute_majority_values(votes))
        for candidate, votes in votes_by_candidate.items()
    }
    ranked_scores = sorted(
        majority_values.items(), key=itemgetter(1), reverse=not reverse
    )

    ranking = {
        candidate: ranking for ranking, (candidate, _) in enumerate(ranked_scores)
    }

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


def compute_majority_values(votes: List[Vote]) -> Iterator[Vote]:
    """
    Compute iteratively the median grades.

    Parameters
    ----------
    votes: list of all grade values obtained for a given candidate.

    Returns
    -------
    Iterator of the next majority value

    Examples from MJ book (1.5):

    >>> list(compute_majority_values([7, 11, 9, 9, 11]))
    [9, 9, 11, 7, 11]
    >>> list(compute_majority_values([8, 11, 9, 9, 10]))
    [9, 9, 10, 8, 11]
    """
    grades = convert_votes_to_tally(votes)
    keys = list(grades.keys())
    num_votes = len(votes)

    for _ in range(num_votes):
        total = sum(grades.values())
        cumsum = list(accumulate(grades.values()))
        cumsum = [v / total for v in cumsum]

        idx = median_grade(cumsum)
        key = keys[idx]
        yield key

        # remove median grade
        grades[key] -= 1
        assert grades[key] > -1


def convert_votes_to_tally(votes: List[Vote]) -> Dict[Vote, int]:
    """
    Convert the frequency of each grade as a sorted dictionary.

    >>> convert_votes_to_tally([7, 11, 9, 9, 11])
    {7: 1, 9: 2, 11: 2}
    """
    return {key: len(list(group)) for key, group in groupby(sorted(votes))}
