from bokeh.plotting import curdoc
from environment import Environment
from gui_components import App

environment = Environment(number_of_blobs=8, starting_food_items=30)
app = App(environment)

curdoc().add_root(app.get_app())
app.play()
