from utils.Parameters import Parameters


class Configuration:
    def __init__(self,
                 type='blood',
                 geo='90degree',
                 velocity='15cms',
                 distance='5cm'):
        self.type = type
        self.alpha = 0.357 if self.type == 'blood' else 1
        self.geo = geo
        self.beta = 0 if self.geo == '90degree' else 0
        self.velocity_str = velocity
        self.distance_str = distance
        self.velocity = 15 * (10 ** (-2)) if '15cms' == velocity else 7.5 * (10 ** (-2))
        if distance == '5cm':
            self.distance = 5 * (10 ** (-2))
        elif distance == '10cm':
            self.distance = 10 * (10 ** (-2))
        elif distance == '15cm':
            self.distance = 15 * (10 ** (-2))
        else:
            self.distance = 20 * (10 ** (-2))

    def copy_config(self):
        config = Configuration()
        config.type = self.type
        config.alpha = self.alpha
        config.geo = self.geo
        config.beta = self.beta
        config.velocity = self.velocity
        config.distance = self.distance
        config.velocity_str = self.velocity_str
        config.distance_str = self.distance_str
        return config

    def set_parameters(self, p: Parameters):
        p.set_alpha(self.alpha)
        p.set_vmax(self.velocity * 2)
        p.set_z_rx(self.distance)
        p.recalc_parameters()

    def get_descriptor_str(self):
        return f'{self.type}_{self.geo}_{self.distance_str}_{self.velocity_str}'

