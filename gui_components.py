from environment import Environment
from bokeh.events import ButtonClick
from bokeh.layouts import row
from bokeh.models import Button
from bokeh.plotting import ColumnDataSource, Figure


class ControlDashboard:
    def __init__(self, environment: Environment):
        self.environment = environment

        self.skip_forward_button = Button(label="Skip forward", button_type="default")
        self.skip_forward_button.on_click(self.skip_forward_callback)

        self.add_food_button = Button(label="Add food", button_type="primary")
        self.add_food_button.on_click(self.add_food_callback)

        self.restart_button = Button(label="Restart", button_type="danger")
        self.restart_button.on_click(self.restart_callback)

    def get_component(self):
        return row(self.skip_forward_button, self.add_food_button, self.restart_button)

    def skip_forward_callback(self, _event: ButtonClick):
        self.environment.skip_forward()

    def restart_callback(self, _event: ButtonClick):
        self.environment.restart()

    def add_food_callback(self, _event: ButtonClick):
        self.environment.add_some_food()


class EnvironmentView:
    def __init__(self, environment: Environment):
        self.environment = environment

        self.blobs_data_source = ColumnDataSource(data=dict(x=[],
                                                            y=[],
                                                            radius=[],
                                                            alpha=[]
                                                            )
                                                  )
        self.food_data_source = ColumnDataSource(data=dict(x=[],
                                                           y=[],
                                                           radius=[]
                                                           )
                                                 )

        self.view = Figure(plot_width=600, plot_height=600, x_range=(0, 1), y_range=(0, 1))
        self.view.circle('x', 'y',
                         radius='radius',
                         alpha='alpha',
                         source=self.blobs_data_source,
                         fill_color='green',
                         line_color='black'
                         )
        self.view.circle('x', 'y',
                         radius='radius',
                         alpha=1,
                         source=self.food_data_source,
                         fill_color='red',
                         line_color='red'
                         )

    def refresh(self):
        self.refresh_blobs_data()
        self.refresh_food_data()

    def get_component(self):
        return self.view

    def refresh_blobs_data(self):
        self.blobs_data_source.data = {
            'x': [organism.get_x_coordinate() for organism in self.environment.organisms.organism_list],
            'y': [organism.get_y_coordinate() for organism in self.environment.organisms.organism_list],
            'radius': [organism.radius for organism in self.environment.organisms.organism_list],
            'alpha': [max(0, min(organism.energy, 1)) for organism in self.environment.organisms.organism_list]
        }

    def refresh_food_data(self):
        self.food_data_source.data = {
            'x': [food.get_x_coordinate() for food in self.environment.foodage.food_list],
            'y': [food.get_y_coordinate() for food in self.environment.foodage.food_list],
            'radius': [food.radius for food in self.environment.foodage.food_list]
        }
