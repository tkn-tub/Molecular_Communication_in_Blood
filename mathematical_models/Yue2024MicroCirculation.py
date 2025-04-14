import numpy as np
from mathematical_models.TheoreticalCIR import TheoreticalCIR
from utils.Parameters import Parameters


class Yue2024MicroCirculation(TheoreticalCIR):

    t_1 = 0                                                     # first arrival time

    def __init__(self, p: Parameters):
        super().__init__("YUE24", p)
        self.t_1 = self.parameters.l / self.parameters.v_max
        self.t_2 = (self.parameters.l+self.parameters.rx_d) / self.parameters.v_max

    def calc_h_value(self, t, t_min, dist):
        if t <= t_min or t <= 0:
            return 0
        else:
            return np.sqrt(1 - (dist / (2 * self.parameters.v_max * t)))

    def get_cir_value(self,
                      t: float                                  # time t [s]
                      ) -> float:

        return self.calc_h_value(t, self.t_1, self.parameters.l) - self.calc_h_value(t, self.t_2, self.parameters.l+self.parameters.rx_d)

