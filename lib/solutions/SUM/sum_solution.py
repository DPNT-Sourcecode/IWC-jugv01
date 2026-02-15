
class SumSolution:
    
    def compute(self, x: int, y: int) -> int:
        """Returns the sum of two provided integers"""
        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError("Inputs must be integers")
        return x + y



