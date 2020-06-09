from bokeh.plotting import curdoc
from environment import Environment
from gui_components import App


environment = Environment(number_of_blobs=15, starting_food_items=30)
app = App(environment)


def update():
    environment.iterate()
    app.refresh()


curdoc().add_root(app.get_app())
curdoc().add_periodic_callback(update, 10)
