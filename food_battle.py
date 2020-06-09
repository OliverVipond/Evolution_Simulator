from bokeh.plotting import curdoc
from bokeh.driving import count
from bokeh.layouts import column, row

from environment import Environment

from gui_components import ControlDashboard, EnvironmentView, ScatterDiagram, PopulationGraph, Statistics

# reachable_org = ColumnDataSource(data=dict(x=[],
#                                            y=[]
#                                            )
#                                  )
# tracker = ColumnDataSource(data=dict(x=[],
#                                      y=[]
#                                      )
#                            )

environment = Environment(number_of_blobs=15, starting_food_items=1)

# env_plot.circle('x', 'y', alpha=1, radius=4, source=reachable_org, fill_color='yellow', line_color='black')
# env_plot.circle('x', 'y', alpha=1, radius=4, source=tracker, fill_color='blue', line_color='blue')

environment_view = EnvironmentView(environment)
control_dashboard = ControlDashboard(environment)
scatter_diagram = ScatterDiagram(environment)
population_graph = PopulationGraph(environment, [Statistics.number_of_foods, Statistics.number_of_blobs])

curdoc().add_root(row(column(environment_view.get_component(),
                             control_dashboard.get_component(),
                             population_graph.get_component()),
                      column(scatter_diagram.get_component())))


@count()
def update(t):
    environment.iterate()
    environment_view.refresh()
    scatter_diagram.refresh()
    population_graph.upload_iteration()

    # tracked_food_item = foodage.food_list[0]
    #
    # tracker.data = {
    #     'x' : [tracked_food_item.get_x_coordinate()],
    #     'y' : [tracked_food_item.get_y_coordinate()],
    # }
    #
    #
    # reachable_org.data = {
    #     'x' : [org.get_x_coordinate() for org in Organism_Tree.retrieve([],tracked_food_item.bounding_box)],
    #     'y' : [org.get_y_coordinate() for org in Organism_Tree.retrieve([],tracked_food_item.bounding_box)],
    # }

    if t % 100 == 0:
        environment.add_some_food(1)


curdoc().add_periodic_callback(update, 10)
