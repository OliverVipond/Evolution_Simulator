from environment import Environment
from bokeh.models import RangeSlider, Slider, Tabs, Panel, Button
from bokeh.layouts import column, row
from blob import Blob


class Component:
    def __init__(self):
        self.component = None

    def get_component(self):
        return self.component


class ControlPanel(Component):

    def __init__(self, environment: Environment):
        super().__init__()
        self.component = Tabs(tabs=[
            ActionCentre(environment).get_component(),
            MutationParameterControls().get_component(),
            ExtremaControls(environment).get_component()
        ])


class ActionCentre(Component):
    def __init__(self, environment: Environment):
        super().__init__()
        self.environment = environment

        self.buttons = row(
            ActionCentre.make_button(
                label="Skip forward",
                button_type="default",
                callback=lambda: self.environment.skip_forward(300)
            ),
            ActionCentre.make_button(
                label="Add food",
                button_type="primary",
                callback=self.environment.add_some_food
            ),
            ActionCentre.make_button(
                label="Restart",
                button_type="danger",
                callback=self.environment.restart
            )
        )

        self.component = Panel(
            child=self.buttons,
            title="Action Centre"
        )

    @staticmethod
    def make_button(label: "", button_type: "", callback):
        button = Button(label=label, button_type=button_type)
        button.on_click(lambda _event: callback())
        return button


class MutationParameterControls(Component):

    def __init__(self):
        super().__init__()
        self.controls = column(
            MutationParameterControls.make_parameter_slider(
                parameters=Blob.MUTATION_PARAMETERS,
                key="speed",
                min_value=0,
                max_value=0.01,
                step=0.0001,
                label="Speed mutation"
            ),
            MutationParameterControls.make_parameter_slider(
                parameters=Blob.MUTATION_PARAMETERS,
                key="radius",
                min_value=0,
                max_value=0.03,
                step=0.0001,
                label="Radius mutation"
            )
        )
        self.component = Panel(
            child=self.controls,
            title="Mutation Parameters"
        )

    @staticmethod
    def make_parameter_slider(parameters, key, min_value, max_value, step, label):
        slider = Slider(
            start=min_value,
            end=max_value,
            value=parameters[key],
            step=step,
            title=label
        )

        def change_parameter_callback(new_value):
            parameters[key] = new_value

        slider.on_change("value", lambda _attr, _old, new: change_parameter_callback(new))
        return slider


class ExtremaControls(Component):

    def __init__(self, environment: Environment):
        super().__init__()
        self.environment = environment
        self.controls = column(
            ExtremaControls.make_extrema_slider(
                absolute_min=0,
                absolute_max=0.5,
                extrema_values=Blob.SPEED_EXTREMA,
                step=.0001,
                label="Blob speed",
                environment_callback=environment.organisms.update_extrema_of_organisms
            ),
            ExtremaControls.make_extrema_slider(
                absolute_min=0,
                absolute_max=0.5,
                extrema_values=Blob.RADIUS_EXTREMA,
                step=.0001,
                label="Blob radius",
                environment_callback=environment.organisms.update_extrema_of_organisms
            )
        )

        self.component = Panel(
            child=self.controls,
            title="Extrema"
        )

    @staticmethod
    def make_extrema_slider(absolute_min, absolute_max, extrema_values, step, label, environment_callback):
        slider = RangeSlider(
            start=absolute_min,
            end=absolute_max,
            value=(extrema_values["minimum"], extrema_values["maximum"]),
            step=step,
            title=label
        )

        def update_extrema_callback(new_min, new_max):
            extrema_values["minimum"] = new_min
            extrema_values["maximum"] = new_max
            environment_callback()

        slider.on_change("value", lambda _attr, _old, new_value: update_extrema_callback(new_value[0], new_value[1]))
        return slider
