from bokeh.models import LinearColorMapper, ColorBar
from bokeh.plotting import ColumnDataSource, curdoc, Figure
from bokeh.driving import count
from bokeh.layouts import column, row

from environment import Environment

from gui_components import ControlDashboard, EnvironmentView


# --------------------------------------------------------------------------------#
#                                  DATA SOURCES                                  #
# --------------------------------------------------------------------------------#


stats = ColumnDataSource(data=dict(time=[],
                                   nbr_of_orgs=[],
                                   nbr_of_food=[]
                                   )
                         )

scatter = ColumnDataSource(data=dict(pop_radiuss=[],
                                     pop_speeds=[],
                                     time_of_birth=[]
                                     )
                           )

# reachable_org = ColumnDataSource(data=dict(x=[],
#                                            y=[]
#                                            )
#                                  )
# tracker = ColumnDataSource(data=dict(x=[],
#                                      y=[]
#                                      )
#                            )

# --------------------------------------------------------------------------------#
#                                  FIGURE INIT                                   #
# --------------------------------------------------------------------------------#

scatter_plot = Figure(plot_width=400, plot_height=400)

stat_plot = Figure(plot_width=600, plot_height=200)

# --------------------------------------------------------------------------------#
#                                  SIM INIT                                      #
# --------------------------------------------------------------------------------#


environment = Environment(number_of_blobs=15, starting_food_items=1)

# env_plot.circle('x', 'y', alpha=1, radius=4, source=reachable_org, fill_color='yellow', line_color='black')
# env_plot.circle('x', 'y', alpha=1, radius=4, source=tracker, fill_color='blue', line_color='blue')

stat_plot.line('time', 'nbr_of_orgs', source=stats, line_color='green')
stat_plot.line('time', 'nbr_of_food', source=stats, line_color='red')
stat_plot.x_range.follow = "end"
stat_plot.x_range.follow_interval = 100

color_mapper = LinearColorMapper(palette='Turbo256', low=0, high=1)
color_bar = ColorBar(color_mapper=color_mapper, location=(0, 0))

scatter_plot.circle('pop_radiuss', 'pop_speeds', color={'field': 'time_of_birth', 'transform': color_mapper},
                    source=scatter)
scatter_plot.add_layout(color_bar, 'right')

environment_view = EnvironmentView(environment)
control_dashboard = ControlDashboard(environment)

curdoc().add_root(row(column(environment_view.get_component(), control_dashboard.get_component(), stat_plot), column(scatter_plot)))


@count()
def update(t):
    environment.iterate()
    environment_view.refresh()

    scatter.data = {
        'pop_radiuss': [organism.radius for organism in environment.organisms.organism_list],
        'pop_speeds': [organism.speed for organism in environment.organisms.organism_list],
        'time_of_birth': [organism.time_of_birth / (t + 1) for organism in environment.organisms.organism_list]
    }

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
        stats.stream({
            'time': [t / 100],
            'nbr_of_orgs': [len(environment.organisms.organism_list)],
            'nbr_of_food': [len(environment.foodage.food_list)]
        })


curdoc().add_periodic_callback(update, 10)
