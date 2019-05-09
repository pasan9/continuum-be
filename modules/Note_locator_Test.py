import numpy as np
import random
import time
from deap import algorithms, base, creator, tools
from definitions.Guitar import Guitar


def arrange(guitar, note_seq, style):
    start_time = time.time()
    no_segments = 0
    no_notes = 0
    complete_arrangement = []

    # Set Fitness and Individual Types
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    for segment in note_seq:
        no_segments += 1
        no_notes += len(segment)
        # Previous result : If first segment then set to None
        previous_result = complete_arrangement and complete_arrangement[-1] or None
        complete_arrangement.append(get_placements(guitar,segment, previous_result, style))

    print('No. of Segments :',no_segments)
    print('No. of Notes :', no_notes)
    print('Time Elapsed :', time.time() - start_time)
    return complete_arrangement


def get_placements(guitar,segment, previous_result, style):
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

        if(style == 'fin'):
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
    toolbox.register("individual", tools.initIterate, creator.Individual, create_individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Define evolutionary functions
    toolbox.register("evaluate", evalInd)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", mutate_ran_reset)
    if(type=="cho"):
        toolbox.register("select", tools.selNSGA2)
    else:
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

#Testing
guitar = Guitar(6,24)
style = 'fin'
note_seq = [[64, 45, 60, 64],
 [57, 60, 62, 64, 57, 60, 62],
 [64, 45, 60, 64],
 [57, 60, 62, 64, 57, 60, 62],
 [64, 45, 60, 64],
 [57, 61, 62, 64, 57, 61, 62],
 [64, 45, 60, 64],
 [57, 61, 62, 64, 57, 61, 62],
 [64, 45, 60, 64],
 [60, 45, 60, 64, 57],
 [62, 64, 57, 60, 62],
 [59, 40, 59, 64],
 [52, 55, 57, 59, 52, 55, 57],
 [59, 40, 59, 64],
 [52, 55, 57, 59, 52, 55, 57],
 [62, 43, 59, 67],
 [60, 43, 59, 67, 55],
 [59, 62, 55, 60, 59],
 [57, 50, 62, 65],
 [62, 53, 55, 57, 62, 53, 55],
 [57, 50, 62, 65],
 [62, 53, 55, 57, 62, 53, 55],
 [64, 45, 60, 64],
 [60, 45, 60, 64, 57],
 [62, 64, 57, 60, 62],
 [59, 40, 59, 64],
 [52, 55, 57, 59, 52, 55, 57],
 [59, 40, 59, 64],
 [52, 55, 57, 59, 52, 55, 57],
 [62, 43, 59, 67],
 [60, 43, 59, 67, 55],
 [59, 62, 55, 60, 59],
 [57, 45, 60, 64],
 [52, 53, 55, 57, 52, 53, 55],
 [57, 45, 60, 64],
 [52, 53, 55, 57, 52, 53, 55],
 [64, 45, 60, 64],
 [60, 45, 60, 64, 57],
 [62, 64, 57, 60, 62],
 [59, 43, 59, 67],
 [55, 57, 59, 55, 57],
 [59, 43, 57, 59],
 [55, 57, 59, 55, 57],
 [62, 50, 62, 65],
 [59, 43, 59, 67, 55],
 [60, 59, 55],
 [57, 45, 60, 64],
 [52, 53, 55, 57, 52, 53, 55],
 [57, 45, 60, 64],
 [52, 53, 55, 57, 52, 53, 55],
 [57, 41, 60, 65],
 [60, 53, 55, 57, 60, 53, 57],
 [55, 43, 59, 67],
 [60, 52, 53, 55, 60, 52, 55],
 [53, 45, 62, 65],
 [57, 62, 52, 53, 57, 62, 53],
 [52, 45, 60, 64],
 [57, 60, 62, 52, 57, 60, 62],
 [60, 41, 60, 65],
 [53, 57, 59, 60, 53, 57, 59],
 [60, 40, 62, 64],
 [57, 60, 62, 59, 62],
 [57, 40, 60, 64],
 [52, 53, 55, 57, 52, 53, 55],
 [57, 40, 60, 64],
 [52, 53, 55, 57, 52, 53, 55],
 [57, 41, 60, 65],
 [60, 53, 55, 57, 60, 53, 57],
 [55, 48, 60, 64],
 [60, 52, 53, 55, 60, 52, 55],
 [53, 45, 62, 65],
 [57, 62, 52, 53, 57, 62, 53],
 [52, 45, 60, 64],
 [57, 60, 62, 52, 57, 60, 62],
 [60, 41, 60, 65],
 [53, 57, 59, 60, 53, 57, 59],
 [60, 43, 62, 65],
 [57, 60, 59, 55, 59],
 [57, 40, 60, 64],
 [52, 53, 55, 57, 52, 53, 55],
 [57, 45, 60, 64],[52, 53, 55, 57, 52, 53, 55],
 [57, 40, 60, 64],
 [52, 53, 55, 57, 52, 53, 55],
 [57, 41, 60, 65],
 [60, 53, 55, 57, 60, 53, 57],
 [55, 48, 60, 64],
 [60, 52, 53, 55, 60, 52, 55],
 [53, 45, 62, 65],
 [57, 62, 52, 53, 57, 62, 53],
 [52, 45, 60, 64],
 [57, 60, 62, 52, 57, 60, 62],
 [60, 41, 60, 65],
 [53, 57, 59, 60, 53, 57, 59],
 [60, 43, 62, 65],
 [57, 60, 59, 55, 59],
 [57, 40, 60, 64],
 [52, 53, 55, 57, 52, 53, 55],
 [57, 45, 60, 64]]

comp = arrange(guitar,note_seq,style)


# note_seq = [[64, 45, 60, 64],
#  [57, 60, 62, 64, 57, 60, 62],
#  [64, 45, 60, 64],
#  [57, 60, 62, 64, 57, 60, 62],
#  [64, 45, 60, 64],
#  [57, 61, 62, 64, 57, 61, 62],
#  [64, 45, 60, 64],
#  [57, 61, 62, 64, 57, 61, 62],
#  [64, 45, 60, 64],
#  [60, 45, 60, 64, 57],
#  [62, 64, 57, 60, 62],
#  [59, 40, 59, 64],
#  [52, 55, 57, 59, 52, 55, 57],
#  [59, 40, 59, 64],
#  [52, 55, 57, 59, 52, 55, 57],
#  [62, 43, 59, 67],
#  [60, 43, 59, 67, 55],
#  [59, 62, 55, 60, 59],
#  [57, 50, 62, 65],
#  [62, 53, 55, 57, 62, 53, 55],
#  [57, 50, 62, 65],
#  [62, 53, 55, 57, 62, 53, 55],
#  [64, 45, 60, 64],
#  [60, 45, 60, 64, 57],
#  [62, 64, 57, 60, 62],
#  [59, 40, 59, 64],
#  [52, 55, 57, 59, 52, 55, 57],
#  [59, 40, 59, 64],
#  [52, 55, 57, 59, 52, 55, 57],
#  [62, 43, 59, 67],
#  [60, 43, 59, 67, 55],
#  [59, 62, 55, 60, 59],
#  [57, 45, 60, 64],
#  [52, 53, 55, 57, 52, 53, 55],
#  [57, 45, 60, 64],
#  [52, 53, 55, 57, 52, 53, 55],
#  [64, 45, 60, 64],
#  [60, 45, 60, 64, 57],
#  [62, 64, 57, 60, 62],
#  [59, 43, 59, 67],
#  [55, 57, 59, 55, 57],
#  [59, 43, 57, 59],
#  [55, 57, 59, 55, 57],
#  [62, 50, 62, 65],
#  [59, 43, 59, 67, 55],
#  [60, 59, 55],
#  [57, 45, 60, 64],
#  [52, 53, 55, 57, 52, 53, 55],
#  [57, 45, 60, 64],
#  [52, 53, 55, 57, 52, 53, 55],
#  [57, 41, 60, 65],
#  [60, 53, 55, 57, 60, 53, 57],
#  [55, 43, 59, 67],
#  [60, 52, 53, 55, 60, 52, 55],
#  [53, 45, 62, 65],
#  [57, 62, 52, 53, 57, 62, 53],
#  [52, 45, 60, 64],
#  [57, 60, 62, 52, 57, 60, 62],
#  [60, 41, 60, 65],
#  [53, 57, 59, 60, 53, 57, 59],
#  [60, 40, 62, 64],
#  [57, 60, 62, 59, 62],
#  [57, 40, 60, 64],
#  [52, 53, 55, 57, 52, 53, 55],
#  [57, 40, 60, 64],
#  [52, 53, 55, 57, 52, 53, 55],
#  [57, 41, 60, 65],
#  [60, 53, 55, 57, 60, 53, 57],
#  [55, 48, 60, 64],
#  [60, 52, 53, 55, 60, 52, 55],
#  [53, 45, 62, 65],
#  [57, 62, 52, 53, 57, 62, 53],
#  [52, 45, 60, 64],
#  [57, 60, 62, 52, 57, 60, 62],
#  [60, 41, 60, 65],
#  [53, 57, 59, 60, 53, 57, 59],
#  [60, 43, 62, 65],
#  [57, 60, 59, 55, 59],
#  [57, 40, 60, 64],
#  [52, 53, 55, 57, 52, 53, 55],
#  [57, 45, 60, 64],
#  [52, 53, 55, 57, 52, 53, 55],
#  [57, 45, 60, 64],
#  [64, 65, 67, 69, 64, 65, 67],
#  [69, 45, 60, 64]]


print(comp)
