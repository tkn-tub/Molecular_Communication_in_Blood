import math


class Parameters:

    def __init__(self):
        # GEOMETRY #
        self.z_tx = 0  # position of plane Tx in z
        self.z_rx = 20 * (10 ** (-2))  # position of plane Rx in z
        self.l = abs(self.z_rx - self.z_tx)  # distance between Tx and Rx along z axis
        self.r = 1.5 * (10 ** (-3))  # radius of channel [m]
        self.rx_d = 29 * (10 ** (-3))  # depth of the Rx along z axis
        self.rx_V = math.pi * self.r * self.rx_d  # volume of Rx

        # FLUID #
        self.D = 1.0 * (10 ** (-6))  # diffusion coefficient [m2/s]
        # self.Q = 1.17 * (10 ** (-5))                           # volumetric flow rate
        # self.v = self.Q / (math.pi * self.r ** 2)                        # average flow velocity [m/s]
        self.v_max = 15 * (10 ** (-2))  # maximum flow velocity [m/s] constant
        self.alpha = 0.357  # form factor
        self.v_m_pl = self.v_max * (self.alpha + 1) / (3 * self.alpha + 1)  # average cross-sectional velocity - power law
        self.v_m_p = self.v_max / 2  # average cross-sectional velocity - poiseuille
        self.Q = self.v_max * (math.pi * self.r ** 2)  # volumetric flow rate [m3/s]
        self.peclet = self.l * self.v_m_pl / self.D  # peclet number
        self.peclet_substitute = self.r * self.v_m_pl / self.D  # peclet number substitute
        self.nu = 3.8 * (10 ** (-6))  # kinematic viscosity [m2/s]
        self.reynolds = self.v_m_pl * self.r / self.nu  # reynolds number

        # PARTICLES #
        self.c_b = 0  # reaction rate at boudary, 0 for reflective
        self.c_d = 0  # degredation rate
        self.c_r = 0  # reaction rate
        self.c_a = 0  # absoption rate

        # CALCULATION #
        self.t_start = 0  # start time [s], MUST ALWAYS BE 0!!!
        self.t_end = 3  # end time [s]
        self.t_step = 0.01  # length of single step [s]

    def set_alpha(self, alpha):
        self.alpha = alpha

    def set_vmax(self, vmax):
        self.v_max = vmax

    def set_z_rx(self, z_rx):
        self.z_rx = z_rx - self.rx_d / 2

    def recalc_parameters(self):
        self.l = abs(self.z_rx - self.z_tx)  # distance between Tx and Rx along z axis
        self.rx_V = math.pi * self.r * self.rx_d  # volume of Rx
        self.rx_V = math.pi * self.r * self.rx_d  # volume of Rx
        self.v_m_pl = self.v_max * (self.alpha + 1) / (3 * self.alpha + 1)  # average cross-sectional velocity - power law
        self.v_m_p = self.v_max / 2  # average cross-sectional velocity - poiseuille
        self.Q = self.v_max * (math.pi * self.r ** 2)  # volumetric flow rate [m3/s]
        self.peclet = self.l * self.v_m_pl / self.D  # peclet number
        self.peclet_substitute = self.r * self.v_m_pl / self.D  # peclet number substitute
        self.reynolds = self.v_m_pl * self.r / self.nu  # reynolds number


