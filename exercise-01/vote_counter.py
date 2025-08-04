class VoteCounter:
    """
    Class that shows information about valid, blank and invalid votes by calculating the percentage of each type of vote.
    """

    def __init__(
        self,
        total_electors: int,
        valid_votes: int,
        blank_votes: int,
        invalid_votes: int,
    ):
        if total_electors < 1:
            raise ValueError("Total electors must be greater than zero.")
        if any(
            vote_type < 0 for vote_type in [valid_votes, blank_votes, invalid_votes]
        ):
            raise ValueError("All votes must be non-negative values.")

        self.total_electors: int = total_electors
        self.valid_votes: int = valid_votes
        self.blank_votes: int = blank_votes
        self.invalid_votes: int = invalid_votes

    @property
    def valid_vote_percentage(self) -> float:
        """
        Calculates the percentage of valid votes.

        Returns:
            The percentage of valid votes as a float.
        """
        return round((self.valid_votes / self.total_electors) * 100, 2)

    @property
    def blank_vote_percentage(self) -> float:
        """
        Calculates the percentage of blank votes.

        Returns:
            The percentage of blank votes as a float.
        """
        return round((self.blank_votes / self.total_electors) * 100, 2)

    @property
    def invalid_vote_percentage(self) -> float:
        """
        Calculates the percentage of invalid votes.

        Returns:
            The percentage of invalid votes as a float.
        """
        return round((self.invalid_votes / self.total_electors) * 100, 2)


if __name__ == "__main__":
    vote_counter = VoteCounter(
        total_electors=1000, valid_votes=800, blank_votes=150, invalid_votes=50
    )
    print(vote_counter.valid_vote_percentage)
    print(vote_counter.blank_vote_percentage)
    print(vote_counter.invalid_vote_percentage)
