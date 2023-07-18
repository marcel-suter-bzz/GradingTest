from dataclasses import dataclass
from datetime import datetime


@dataclass
class Entry:
    """
    an accounting entry for the charging
    """
    start_time: str
    end_time: str
    release_time: str
    energy_amount: float

    @property
    def cost(self):
        """
        gets the total cost for the charging
        :return:
        """
        energy_cost = self.energy_amount * 0.35
        return energy_cost
    
