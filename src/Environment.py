from src.Individual import Individual
import random


class Group:
    def __init__(self, population: list, limit):
        self._population = population
        self._limit = limit

    def get_ind(self, index):
        assert index < len(self._population), "Error"
        return self._population[index]

    def add_son(self, son:list):
        self._population  = self._population + son

    def sort(self):
            self._population.sort(key=lambda i: i._phenotype)

class Env:
    def __init__(self,group, filter_rate, mutation_rate, gates, env_mutate_rate):
        self._group = group
        self._filter = filter_rate
        self._mutation = mutation_rate
        self._gates = gates
        self._env_mutate_rate = env_mutate_rate
        self.sorted = False

    def get_population_size(self):
        return len(self._group._population)

    def get_ind_by_index(self, index):
        return self._group._population[index]

    def next_generation(self):
        number_fa_ma = len(self._group._population)
        son_list = []
        while len(son_list)+number_fa_ma < self._group._limit:
            a = random.randint(0, number_fa_ma-1)
            b = random.randint(0, number_fa_ma-1)
            while a == b:
                b = random.randint(0, number_fa_ma-1)
            ind1 = self._group.get_ind(a)
            ind2 = self._group.get_ind(b)
            new_ind = Individual.hybrid(ind1, ind2, self._mutation, self._gates, self._env_mutate_rate)
            if new_ind._genotype.validation():
                son_list.append(new_ind)
            else:
                continue
        self._group.add_son(son_list)
        self.sorted = False

    def sort(self):
        self._group.sort()
        self.sorted = True

    def filter(self):
        if not self.sorted:
            self.sort()
        n = len(self._group._population)
        m = int(n * self._filter)
        self._group._population = self._group._population[m:]
