from environment import Environment
from bokeh.events import ButtonClick
from bokeh.layouts import row, column
from bokeh.models import Button, ColorBar, LinearColorMapper
from bokeh.plotting import ColumnDataSource, Figure
from statistics import Statistics
from controls import SpeedExtremeSlider, Controllers


class App:

    def __init__(self, environment: Environment):
        self.environment_view = EnvironmentView(environment)
        self.control_dashboard = ControlDashboard(environment)
        self.scatter_diagram = ScatterDiagram(environment)
        self.population_graph = PopulationGraph(environment, [Statistics.number_of_foods, Statistics.number_of_blobs])
        self.speed_extrema_slider = SpeedExtremeSlider(environment)
        self.controllers = Controllers(environment)

        self.app = row(
            column(
                self.environment_view.get_component(),
                self.control_dashboard.get_component(),
                self.population_graph.get_component()
            ),
            column(
                self.scatter_diagram.get_component(),
                self.speed_extrema_slider.get_component(),
                self.controllers.get_component()
            )
        )

    def get_app(self):
        return self.app

    def refresh(self):
        self.environment_view.refresh()
        self.scatter_diagram.refresh()


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
        self.environment.skip_forward(300)

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


class ScatterDiagram:

    def __init__(self, environment: Environment):
        self.environment = environment

        self.data_source = ColumnDataSource(data=dict(pop_radiuss=[],
                                                      pop_speeds=[],
                                                      time_of_birth=[]
                                                      )
                                            )
        self.diagram = Figure(plot_width=400, plot_height=400)

        self.color_mapper = LinearColorMapper(palette='Turbo256', low=0, high=1)
        self.color_bar = ColorBar(color_mapper=self.color_mapper, location=(0, 0))
        self.diagram.circle('pop_radiuss', 'pop_speeds',
                            color={'field': 'time_of_birth', 'transform': self.color_mapper},
                            source=self.data_source)
        self.diagram.add_layout(self.color_bar, 'right')

    def refresh(self):
        self.data_source.data = {
            'pop_radiuss': [organism.radius for organism in self.environment.organisms.organism_list],
            'pop_speeds': [organism.speed for organism in self.environment.organisms.organism_list],
            'time_of_birth': [organism.time_of_birth / (self.environment.current_time + 1) for organism in
                              self.environment.organisms.organism_list]
        }

    def get_component(self):
        return self.diagram


class PopulationGraph:

    def __init__(self, environment: Environment, statistics: [dict], snapshot_interval=100):
        self.environment = environment
        self.statistics = statistics
        self.number_of_statistics = len(statistics)

        self.data_sources = []
        self.graph = Figure(plot_width=600, plot_height=200)
        self.set_up_graph_lines()

        self.graph.x_range.follow = "end"
        self.graph.x_range.follow_interval = 50

        self.snapshot_interval = snapshot_interval

        self.environment.add_data_callback(self.upload_iteration)

    def set_up_graph_lines(self):
        for i in range(self.number_of_statistics):
            self.data_sources += [ColumnDataSource(data=dict(
                time=[],
                value=[]
            ))]
            self.graph.line('time', 'value', source=self.data_sources[i], line_color=self.statistics[i]['color'])

    def upload_iteration(self):
        if self.environment.current_time % self.snapshot_interval == 0:
            for i in range(self.number_of_statistics):
                self.data_sources[i].stream({
                    'time': [self.environment.current_time / self.snapshot_interval],
                    'value': [self.statistics[i]['function'](self.environment)]
                })

    def get_component(self):
        return self.graph
