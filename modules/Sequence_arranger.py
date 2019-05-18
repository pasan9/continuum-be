from deap import algorithms, base, creator, tools
from definitions.Guitar import Guitar
import copy
import numpy as np
import random

# Set Fitness and Individual Types
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

def get_seq_placements(guitar,segment,previous_segment):
    # Population size and tourn select size: TODO Make them depend on the segment size
    population_size = 300
    tournament_selection_size = 3

    # Initialize toolbox
    toolbox = base.Toolbox()
    # Define method to generate a Gene
    toolbox.register("gene", guitar.get_random_position)

    # Functions for creating and mutating individuals

    def create_individual(ind_segment=segment):
        #individual_segment = copy.deepcopy(ind_segment)
        # individual = []
        for note in ind_segment.notes:
            note.position = toolbox.gene(note.value)
        return segment.notes


    def evalInd(individual):
        no_strings_depressed = 0

        #Difference between last note played in previous segment, and first note in current segment
        difference_with_previous_segment = 0
        if(previous_segment):
            difference_with_previous_segment += abs(previous_segment[-1].position[1]-individual[0].position[1])


        min_fret = individual[0].position[1]
        max_fret = 0

        for note in individual:
            #Calculate string depressions
            if(note.position[1] != 0): #Fret val is not 0
                no_strings_depressed += 1

            #Calculate total fretspan
            if (note.position[1] > max_fret):
                max_fret = note.position[1]
            if (note.position[1] < min_fret):
                min_fret = note.position[1]

        total_fret_span = max_fret - min_fret

        total_fitness = total_fret_span + difference_with_previous_segment

        return (total_fitness),

    def mutate_ran_reset(individual):  # Does Random Resetting if possible
        # Get indexes and possible mutations of genes where mutation is possible to mutation dict
        # {Note_index:[possible position mutations array]}
        mutation_genes = dict()
        for i,note in enumerate(individual):
            positions = guitar.get_positions(note.value)
            if (len(positions) > 1):
                mutation_genes[i] = positions
        # If there are mutatable genes
        if (mutation_genes):  # Bool(dict) returns false for empty
            # Get a random Note index
            mut_index = random.choice(list(mutation_genes))  # list(dict) returns list of keys
            # Remove the current position from possible mutations
            possible_mutations = mutation_genes[mut_index]
            possible_mutations.remove(individual[mut_index].position)
            #Assign New position
            individual[mut_index].position = random.choice(possible_mutations)
        return individual,


    # Define how to generate individual and population
    toolbox.register("individual", tools.initIterate, creator.Individual, create_individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Define evolutionary functions
    toolbox.register("evaluate", evalInd)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", mutate_ran_reset)
    toolbox.register("select", tools.selTournament, tournsize=tournament_selection_size)

    #Evolution Starts
    NGEN = 50
    MU = population_size
    LAMBDA = 100
    CXPB = 0.7
    MUTPB = 0.2

    pop = toolbox.population(n=MU)
    hof = tools.ParetoFront()
    # stats = tools.Statistics(lambda ind: ind.fitness.values)
    # stats.register("avg", np.mean, axis=0)
    # stats.register("std", np.std, axis=0)
    # stats.register("min", np.min, axis=0)
    # stats.register("max", np.max, axis=0)

    algorithms.eaMuPlusLambda(pop, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN,
                                  halloffame=hof)

    #Get best individual : SelBest returns a list, get the first value
    best_ind = tools.selBest(pop, 1)[0]

    #print(best_ind)




    return best_ind