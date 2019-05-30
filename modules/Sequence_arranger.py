from deap import algorithms, base, creator, tools
from definitions.Guitar import Guitar
import copy
import numpy as np
import random

random.seed(64)

# Set Fitness and Individual Types
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("SeqIndividual", list, fitness=creator.FitnessMin)

def get_seq_placements(guitar,segment,previous_result):
    # Population size and tourn select size: TODO Make them depend on the segment size
    population_size = 300
    tournament_selection_size = 3

    # Initialize toolbox
    toolbox = base.Toolbox()
    # Define method to generate a Gene
    toolbox.register("gene", guitar.get_random_position)

    # Functions for creating and mutating individuals

    def create_individual(ind_segment=segment):
        individual = []
        for note_val in ind_segment:
            individual.append(toolbox.gene(note_val))
        return individual


    def evalInd(individual):
        no_strings_depressed = 0

        #Difference between last note played in previous segment, and first note in current segment
        difference_with_previous_segment = 0
        if(previous_result):
            difference_with_previous_segment += abs(previous_result[-1][1]-individual[0][1])

        min_fret = individual[0][1]
        max_fret = 0

        for position in individual:
            #Calculate string depressions
            if(position[1] != 0): #Fret val is not 0
                no_strings_depressed += 1

            #Calculate total fretspan
            if (position[1] > max_fret):
                max_fret = position[1]
            if (position[1] < min_fret):
                min_fret = position[1]

        total_fret_span = max_fret - min_fret

        total_fitness = total_fret_span + difference_with_previous_segment

        # if(style == 'fin'):
        total_fitness += no_strings_depressed

        return (total_fitness),

    def mutate_ran_reset(individual):  # Does Random Resetting if possible
        # Get indexes and possible mutations of genes where mutation is possible to mutation dict
        # {gene_index:[possible mutations array]}
        mutation_genes = dict()
        for i, gene in enumerate(individual):
            note_val = guitar.get_note_from_position(gene)
            positions = guitar.get_positions(note_val)
            if (len(positions) > 1):
                mutation_genes[i] = positions
        # If there are mutatable genes
        if (mutation_genes):  # Bool(dict) returns false for empty
            # Get a random gene index
            mut_index = random.choice(list(mutation_genes))  # list(dict) returns list of keys
            # Remove the current position from possible mutations
            possible_mutations = mutation_genes[mut_index]
            possible_mutations.remove(individual[mut_index])
            new_gene = random.choice(possible_mutations)
            individual[mut_index] = new_gene
        return individual,


    # Define how to generate individual and population
    toolbox.register("individual", tools.initIterate, creator.SeqIndividual, create_individual)
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
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean, axis=0)
    stats.register("std", np.std, axis=0)
    stats.register("min", np.min, axis=0)
    stats.register("max", np.max, axis=0)

    algorithms.eaMuPlusLambda(pop, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN, stats,
                                  halloffame=hof)

    #Get best individual : SelBest returns a list, get the first value
    best_ind = tools.selBest(pop, 1)[0]

    return best_ind