from abc import ABC, abstractmethod
from typing import Any

import numpy as np


class TheoreticalCIR(ABC):

    name = 'TheoreticalCIR'

    @abstractmethod
    def __init__(self, name, p):
        self.name = name
        self.parameters = p

    @abstractmethod
    def get_cir_value(self,
                      t: float                     # time t [s]
                      ) -> float:                  # reception probability according to cir
        pass

    def get_cir_values_interval(self,
                                t_start: float,    # start time [s]
                                t_end: float,      # end time [s]
                                t_step: float      # length of step [s]
                                ) -> dict[float | Any, float]:  # cir
        if t_start < 0 or t_end < 0 or t_step < 0:  # return empty dict in case of wrong t values
            return {}
        if t_end < t_start:  # return first value in case of wrong interval
            cir_value = self.get_cir_value(t_start)
            return {t_start: cir_value}
        n_entries = int((t_end - t_start) / t_step)
        cir_entries = {}
        for i in range(n_entries):
            t = t_start + i * t_step
            cir_value = self.get_cir_value(t)
            cir_entries[t] = cir_value
        cir_value = self.get_cir_value(t_end)
        cir_entries[t_end] = cir_value
        return cir_entries

    def get_name(self):
        return self.name

    def get_parameters(self):
        return self.parameters


