from mathematical_models.TheoreticalCIR import TheoreticalCIR
from utils.Parameters import Parameters


class Unterweger2018Experimental_General_Undelayed(TheoreticalCIR):

    D_e = 0                                                     # first arrival time

    def __init__(self, p: Parameters, beta = 0):
        super().__init__("U18, beta="+str(beta), p)
        self.beta = beta

    def get_cir_value(self,
                      t: float                                  # time t [s]
                      ) -> float:                               # cir value
        t = t + self.parameters.l / self.parameters.v_max
        t_1 = self.parameters.l / self.parameters.v_max
        t_2 = (self.parameters.l + self.parameters.rx_d) / self.parameters.v_max
        if t <= t_1:
            return 0
        elif t_1 < t < t_2:
            return 1 - (self.parameters.l / (self.parameters.v_max * t)) ** (self.beta + 1)
        else:
            return (((self.parameters.l + self.parameters.rx_d) ** (self.beta + 1) - (self.parameters.l ** (self.beta + 1)))
                    / (self.parameters.v_max * t) ** (self.beta + 1))

