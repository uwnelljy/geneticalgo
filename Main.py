from src.utils.File_reader import Reader
from src.Gene import *
from src.Individual import Individual
from src.Environment import Group, Env
from numpy import random
import logging

logging.basicConfig(filename='./syslogging.log',
                    format='[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]',
                    filemode='a',
                    level=logging.DEBUG,
                    datefmt='%Y-%m-%d%I:%M:%S %p')


FILE_PUCKS = './data/Pucks.csv'
FILE_GATES = './data/Gates.csv'
FILE_TICKETS = './data/Tickets.csv'

INIT_POPULATION = 5000
LIMIT = 20000
FILTER_RATE = 0.4
MUTATION_RATE1 = 0.01
MUTATION_RATE2 = 0.05
MUTATION_RATE3 = 0.15
ENV_MUTATE_RATE = 0.4
ALPHA = 10
BETA = 1

EXIT = 30000



class Main:

    def __init__(self, filter_rate, mutation_rate1, mutation_rate2, mutation_rate3, env_mutate_rate):
        self._filter_rate = filter_rate
        self._mutation_rate1 = mutation_rate1
        self._mutation_rate2 = mutation_rate2
        self._mutation_rate3 = mutation_rate3
        self._env_mutate_rate = env_mutate_rate


    @staticmethod
    def get_object():
        df_bucks = Reader.read(FILE_PUCKS)
        flights = Reader.form_flights(df_bucks)
        df_gates = Reader.read(FILE_GATES)
        gates = Reader.form_gates(df_gates)
        df_tickets = Reader.read(FILE_TICKETS)
        tickets = Reader.form_ticket(df_tickets)
        Individual.set_tickets(tickets)
        return flights, gates, tickets

    @staticmethod
    def form_individual():
        flights, gates, tickets = Main.get_object()
        gene_list = []
        for f in flights:
            while True:
                random_index = random.randint(0, len(gates)-1)
                random_gate = gates[random_index]
                if f._type_arr not in random_gate._type_arr or \
                        f._type_dep not in  random_gate._type_dep or \
                        f._type_aircraft not in random_gate._type_flight:
                    continue
                else:
                    gene_list.append(Gene(f, random_gate))
                    break
        genotype = GenoType(gene_list)
        if genotype.validation() is False:
            return None
        else:
            return Individual(genotype)

    @staticmethod
    def form_pop():
        logging.debug("Create init population")
        ind_list = []
        while len(ind_list) < INIT_POPULATION:
            tempt = Main.form_individual()
            if tempt is None:
                continue
            else:
                ind_list.append(tempt)
        return Group(ind_list, LIMIT)

    def run(self):
        env = Env(group=Main.form_pop(),
                  filter_rate=self._filter_rate,
                  mutation_rate=self._mutation_rate3,
                  gates=Main.get_object()[1],
                  env_mutate_rate=self._env_mutate_rate)
        cur_mutation_rate = 3
        n = 0
        while True:
            logging.debug('=============================================================================')
            logging.debug('This is the {}th generation.'.format(n))

            env.next_generation()
            env.sort()
            pop_size = env.get_population_size()
            median_score = env.get_ind_by_index(int(pop_size/2)).get_pheno()
            highest_score = env.get_ind_by_index(-1).get_pheno()
            env.filter()

            logging.debug('Highest score is {}'.format(highest_score))
            logging.debug('Median score is {}'.format(median_score))
            if median_score > 0.01 and cur_mutation_rate == 3:
                logging.debug('Changing mutation rate to 0.05')
                env._mutation_rate = self._mutation_rate2
                cur_mutation_rate = 2
            if highest_score > 0.1 and cur_mutation_rate == 2:
                logging.debug('Changing mutation rate to 0.01')
                env._mutation_rate = self._mutation_rate1
                cur_mutation_rate = 1
            if n == EXIT:
                break
            if n%1000 == 0:
                file = open('./result/optimal{}.txt'.format(n), 'w+')
                file.write(env.get_ind_by_index(-1).tostring())
                file.close()
            n += 1



if __name__ == '__main__':
    Individual.set_al_be(ALPHA, BETA)
    main_func = Main(FILTER_RATE, MUTATION_RATE1, MUTATION_RATE2, MUTATION_RATE3, ENV_MUTATE_RATE)
    main_func.run()