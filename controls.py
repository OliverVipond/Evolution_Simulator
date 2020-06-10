from environment import Environment
from bokeh.models import RangeSlider, Slider
from bokeh.layouts import row, column
from blob import Blob


class Controllers:

    def __init__(self, environment: Environment):
        self.environment = environment
        self.component = column(
            MutationParameterSlider(
                parameters=Blob.MUTATION_PARAMETERS,
                key="speed",
                min_value=0,
                max_value=0.01,
                step=0.0001,
                label="Speed mutation"
            ).get_component()
        )

    def get_component(self):
        return self.component


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


class MutationParameterSlider:

    def __init__(self, parameters, key, min_value, max_value, step, label):
        self.slider = Slider(
            start=min_value,
            end=max_value,
            value=parameters[key],
            step=step,
            title=label
        )
        self.parameters = parameters
        self.key = key
        self.slider.on_change("value", self.update_parameter_callback)

    def update_parameter_callback(self, _attr, _old, new):
        self.parameters[self.key] = new

    def get_component(self):
        return self.slider
