import pytest
from lib.solutions.SUM.sum_solution import SumSolution


class TestSum():
    def test_sum(self):
        assert SumSolution().compute(1, 2) == 3

    def test_invalid_sum(self):
        with pytest.raises(TypeError):
            SumSolution().compute(1, "2")

