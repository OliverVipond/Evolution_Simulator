from environment import Environment
from bokeh.models import RangeSlider


def callback(attr, old, new):
    print(attr, old, new)


class SpeedExtremeSlider:

    def __init__(self, environment: Environment):
        self.range_slider = RangeSlider(start=0, end=0.5, value=(0, 0.8), step=.0001, title="Blob speed")
        self.environment = environment
        self.range_slider.on_change("value", self.update_speed_extrema_callback)

    def get_component(self):
        return self.range_slider

    def update_speed_extrema_callback(self, _attr, _old, new):
        self.environment.organisms.update_bound_speed_of_organisms(
            minimum_speed=new[0],
            maximum_speed=new[1]
        )
