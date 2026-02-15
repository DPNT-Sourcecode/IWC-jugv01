
class SumSolution:
    
    def compute(self, x: int, y: int) -> int:
        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError("Inputs must be integers")
        return x + y


