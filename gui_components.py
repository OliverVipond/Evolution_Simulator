from environment import Environment
from bokeh.events import ButtonClick
from bokeh.models import Button
from bokeh.layouts import row


class ControlDashboard:
    def __init__(self, environment_argument: Environment):
        self.environment = environment_argument

        self.skip_forward_button = Button(label="Skip forward", button_type="default")
        self.skip_forward_button.on_click(self.skip_forward_callback)

        self.add_food_button = Button(label="Add food", button_type="primary")
        self.add_food_button.on_click(self.add_food_callback)

        self.restart_button = Button(label="Restart", button_type="danger")
        self.restart_button.on_click(self.restart_callback)

    def get_buttons(self):
        return row(self.skip_forward_button, self.add_food_button, self.restart_button)

    def skip_forward_callback(self, _event: ButtonClick):
        self.environment.skip_forward()

    def restart_callback(self, _event: ButtonClick):
        self.environment.restart()

    def add_food_callback(self, _event: ButtonClick):
        self.environment.add_some_food()
