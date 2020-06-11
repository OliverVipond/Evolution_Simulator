from environment import Environment


def number_of_foods_function(environment: Environment):
    return len(environment.foodage.food_list)


def number_of_blobs_function(environment: Environment):
    return len(environment.organisms.organism_list)


def total_energy_of_blobs(environment: Environment):
    energy_sum = 0
    for organism in environment.organisms.organism_list:
        energy_sum += organism.get_energy()
    return energy_sum


def total_mass_of_blobs(environment: Environment):
    mass_sum = 0
    for organism in environment.organisms.organism_list:
        mass_sum += organism.get_mass()
    return mass_sum


class Statistics:

    number_of_blobs = {
        'color': 'green',
        'function': number_of_blobs_function
    }

    number_of_foods = {
        'color': 'red',
        'function': number_of_foods_function
    }

    total_energy_of_blobs = {
        'color': 'purple',
        'function': total_energy_of_blobs
    }

    total_mass_of_blobs = {
        'color': 'blue',
        'function': total_mass_of_blobs
    }
