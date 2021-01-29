from src.Gene import GenoType,Gene
import random


class Individual:
    tickets = None
    alpha = 0
    beta = 0
    def __init__(self, genotype: GenoType):
        self._genotype = genotype
        self._phenotype = self.express()

    def get_pheno(self):
        return self._phenotype

    @staticmethod
    def set_tickets(tickets):
        Individual.tickets = tickets

    @staticmethod
    def set_al_be(alpha,beta):
        Individual.alpha = alpha
        Individual.beta = beta

    def express(self):
        """

        :return: the number of flights boarding at temporary gate AND the time of transferring flights
        """
        if self._genotype.is_valid():
            number_temp = 0
            total_time = 0
            for gene in self._genotype._gene_list:
                if gene._gate._gate_number == 'L':
                    number_temp += 1

            for t in Individual.tickets:
                t_aircraft_arr = t._aircraft_arr
                t_aircraft_dep = t._aircraft_dep
                gene_arr = None
                gene_dep = None
                for gene in self._genotype._gene_list:
                    if gene._flight._aircraft_arr == t_aircraft_arr and gene._gate._gate_number != 'L':
                        gene_arr = gene
                    if gene._flight._aircraft_dep == t_aircraft_dep and gene._gate._gate_number != 'L':
                        gene_dep = gene
                    if gene_arr is not None and gene_dep is not None:
                        break
                if gene_arr is None or gene_dep is None:
                    # ignore passengers of flights boarding at temporary gates.
                    continue
                else:
                    total_time += t._pass_num * Gene.time_transfer(gene_arr, gene_dep)
            print('1/number_temp:{}, 1/total_time:{}'.format(1/number_temp, 1/total_time))
            return Individual.alpha/number_temp + Individual.beta/total_time
        else:
            validation_score = self._genotype.validation_score()
            return -validation_score

    @staticmethod
    def hybrid(father, mother, mutation_rate, gates, env_mutation_rate):
        """

        :param father: object of Individual, father of the new born
        :param mother: object of Individual, mother of the new born
        :param mutation_rate: every single gene of the new born will have this possibility to mutate
        :param gates: the list of gates
        :param env_mutation_rate: the possibility that the new born will mutate
        :return:
        """
        n = len(father._genotype._gene_list)
        son_list = []
        ind_mutate_rand_seed = random.randint(0,100)
        if ind_mutate_rand_seed < int(env_mutation_rate * 100):
            should_this_new_born_mutate = True
        else:
            should_this_new_born_mutate = False
        for i in range(n):
            a = random.randint(0,1)
            gene_fa = father._genotype._gene_list[i]
            gene_mo = mother._genotype._gene_list[i]
            if a == 0:
                new_gene = gene_fa.replicate()
            else:
                new_gene = gene_mo.replicate()
            if should_this_new_born_mutate:
                new_gene.mutation(mutation_rate, gates)
            son_list.append(new_gene)
        return Individual(GenoType(son_list))

    def tostring(self):
        s = ''
        for gene in self._genotype._gene_list:
            flight_info = gene._flight.tostring()
            gate_info = gene._gate.tostring()
            s = s + flight_info + gate_info + '\n'
        return s

