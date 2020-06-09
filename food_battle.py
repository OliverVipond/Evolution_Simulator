from bokeh.plotting import curdoc
from bokeh.layouts import column, row

from environment import Environment

from gui_components import ControlDashboard, EnvironmentView, ScatterDiagram, PopulationGraph
from statistics import Statistics


environment = Environment(number_of_blobs=15, starting_food_items=30)

environment_view = EnvironmentView(environment)
control_dashboard = ControlDashboard(environment)
scatter_diagram = ScatterDiagram(environment)
population_graph = PopulationGraph(environment, [Statistics.number_of_foods, Statistics.number_of_blobs])

curdoc().add_root(row(column(environment_view.get_component(),
                             control_dashboard.get_component(),
                             population_graph.get_component()),
                      column(scatter_diagram.get_component())))


def update():
    environment.iterate()
    environment_view.refresh()
    scatter_diagram.refresh()


curdoc().add_periodic_callback(update, 10)
