import numpy as np
from bokeh.models import LinearColorMapper, ColorBar
from bokeh.plotting import ColumnDataSource, curdoc, Figure
from bokeh.driving import count
from bokeh.layouts import column, row

from environment import Environment

from organisms import Organisms
from foodage import Foodage
from quad_tree import QuadTree, Rectangle

# Position: (x,y) \in [0,1]^2
# Velocity: [dx/dt, dy/dt]
# Energy: fraction of full energy 1


e = Environment()
print(e.current_time)

# --------------------------------------------------------------------------------#
#                                  DATA SOURCES                                  #
# --------------------------------------------------------------------------------#

blobs_source = ColumnDataSource(data=dict(x=[],
                                          y=[],
                                          radius=[],
                                          alpha=[]
                                          )
                                )

food_source = ColumnDataSource(data=dict(x=[],
                                         y=[],
                                         radius=[]
                                         )
                               )

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

reachable_org = ColumnDataSource(data=dict(x=[],
                                           y=[]
                                           )
                                 )
tracker = ColumnDataSource(data=dict(x=[],
                                     y=[]
                                     )
                           )

# --------------------------------------------------------------------------------#
#                                  FIGURE INIT                                   #
# --------------------------------------------------------------------------------#

scatter_plot = Figure(plot_width=400, plot_height=400)

env_plot = Figure(plot_width=600, plot_height=600, x_range=(0, 1), y_range=(0, 1))

stat_plot = Figure(plot_width=600, plot_height=200)

# --------------------------------------------------------------------------------#
#                                  SIM INIT                                      #
# --------------------------------------------------------------------------------#

organisms = Organisms()
organisms.add_random_blobs(10)

foodage = Foodage()
foodage.add_random_foods(30)

Organism_Tree = QuadTree(0, Rectangle(0, 0, 1, 1))

for org in organisms.organism_list:
    Organism_Tree.insert(org)


# --------------------------------------------------------------------------------#
#                                  UPDATE                                        #
# --------------------------------------------------------------------------------#

def make_org_data(organisms_class):
    return {
        'x': [organism.get_x_coordinate() for organism in organisms_class.organism_list],
        'y': [organism.get_y_coordinate() for organism in organisms_class.organism_list],
        'radius': [organism.radius for organism in organisms_class.organism_list],
        'alpha': [max(0, min(organism.energy, 1)) for organism in organisms_class.organism_list]
    }


def make_food_data(foodage_class):
    return {
        'x': [food.get_x_coordinate() for food in foodage_class.food_list],
        'y': [food.get_y_coordinate() for food in foodage_class.food_list],
        'radius': [food.radius for food in foodage_class.food_list]
    }


def consume_food(organism_quad_tree, foodage_class):
    for food in foodage_class.food_list:
        close_organisms = organism_quad_tree.retrieve([], food.bounding_box)
        for organism in close_organisms:
            if organism.radius > food.radius and \
                    np.linalg.norm(food.position - organism.position) < organism.radius + food.radius:
                organism.eat_food(food)
                foodage_class.delete_food(food)
                break


def kill_reproduce(organisms_class, t):
    for organism in organisms_class.organism_list:
        if organism.energy > 1:
            organisms_class.organism_list.append(organism.reproduce(birth_time=t))
            organism.update_energy(-0.5)
        if organism.energy < 0:
            organisms_class.kill_organism(organism)


blobs_source.stream(make_org_data(organisms))
food_source.stream(make_food_data(foodage))

env_plot.circle('x', 'y', radius='radius', alpha='alpha', source=blobs_source, fill_color='green', line_color='black')
env_plot.circle('x', 'y', radius='radius', alpha=1, source=food_source, fill_color='red', line_color='red')

env_plot.circle('x', 'y', alpha=1, radius=4, source=reachable_org, fill_color='yellow', line_color='black')
env_plot.circle('x', 'y', alpha=1, radius=4, source=tracker, fill_color='blue', line_color='blue')

stat_plot.line('time', 'nbr_of_orgs', source=stats, line_color='green')
stat_plot.line('time', 'nbr_of_food', source=stats, line_color='red')
stat_plot.x_range.follow = "end"
stat_plot.x_range.follow_interval = 100

color_mapper = LinearColorMapper(palette='Turbo256', low=0, high=1)
color_bar = ColorBar(color_mapper=color_mapper, location=(0, 0))

scatter_plot.circle('pop_radiuss', 'pop_speeds', color={'field': 'time_of_birth', 'transform': color_mapper},
                    source=scatter)
scatter_plot.add_layout(color_bar, 'right')

curdoc().add_root(row(column(env_plot, stat_plot), scatter_plot))


@count()
def update(t):
    organisms.update()
    blobs_source.data = make_org_data(organisms)
    food_source.data = make_food_data(foodage)

    organism_tree = QuadTree(0, Rectangle(0, 0, 1, 1))

    for organism in organisms.organism_list:
        organism_tree.insert(organism)

    scatter.data = {
        'pop_radiuss': [organism.radius for organism in organisms.organism_list],
        'pop_speeds': [organism.speed for organism in organisms.organism_list],
        'time_of_birth': [organism.time_of_birth / (t + 1) for organism in organisms.organism_list]
    }

    consume_food(organism_tree, foodage)
    kill_reproduce(organisms, t)

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
        foodage.add_random_foods(1)
        stats.stream({
            'time': [t / 100],
            'nbr_of_orgs': [len(organisms.organism_list)],
            'nbr_of_food': [len(foodage.food_list)]
        })

        foodage.add_random_foods(1)


curdoc().add_periodic_callback(update, 10)
