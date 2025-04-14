import math
from mathematical_models.TheoreticalCIR import TheoreticalCIR
from utils.Parameters import Parameters


class Huang2024NonNewtonian_Uniform(TheoreticalCIR):

    D_e = 0                                                     # effective diffusion coefficient

    def __init__(self, p: Parameters):
        super().__init__("HUANG24U", p)
        factor = self.parameters.D
        numerator = self.parameters.alpha ** 2 * self.parameters.peclet_substitute ** 2
        denominator = 2 * (3 * self.parameters.alpha + 1) * (5 * self.parameters.alpha + 1)
        sum = 1 + numerator / denominator
        self.D_e = factor * sum
        # peak position
        # t_p = (math.sqrt(self.D_e ** 2 + self.parameters.v_m_pl ** 2 * self.parameters.l ** 2) - self.D_e) / (self.parameters.v_m_pl ** 2)
        # print(t_p)

    def get_rx_prob(self,
                      t: float                                  # time t [s]
                      ) -> float:                               # cir value
        if t <= 0:
            return 0
        factor = 0.5
        erfc_1 = (self.parameters.l - self.parameters.v_m_pl * t) / math.sqrt(4 * self.D_e * t)
        erfc_2 = (self.parameters.l + self.parameters.rx_d - self.parameters.v_m_pl * t) / math.sqrt(4 * self.D_e * t)
        return factor * (math.erfc(erfc_1) - math.erfc(erfc_2))


    def get_cir_value(self,
                      t: float                                  # time t [s]
                      ) -> float:
        return self.get_rx_prob(t)
