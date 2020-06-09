from environment import Environment


def number_of_foods_function(environment: Environment):
    return len(environment.foodage.food_list)


def number_of_blobs_function(environment: Environment):
    return len(environment.organisms.organism_list)


class Statistics:

    number_of_blobs = {
        'color': 'green',
        'function': number_of_blobs_function
    }

    number_of_foods = {
        'color': 'red',
        'function': number_of_foods_function
    }
