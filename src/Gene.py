import random

W = ['332', '333', '33E', '33H', '33L', '773']


class Flight:
    def __init__(self,
                 record_number,
                 date_arr,
                 time_arr,
                 aircraft_arr,
                 type_arr,
                 type_aircraft,
                 date_dep,
                 time_dep,
                 aircraft_dep,
                 type_dep):
        self._record_number = record_number
        self._date_arr = date_arr
        self._type_arr = type_arr
        self._date_dep = date_dep
        self._aircraft_arr = aircraft_arr
        self._aircraft_dep = aircraft_dep

        self._type_dep = type_dep

        if type_aircraft in W:
            self._type_aircraft = 'W'
        else:
            self._type_aircraft = 'N'

        if date_arr == '19-Jan-18':
            self._time_arr = 0
        else:
            time_arr_list = time_arr.split(':')
            self._time_arr = int(time_arr_list[0])*60 + int(time_arr_list[1])

        if date_dep == '21-Jan-18':
            self._time_dep = 24*60
        else:
            time_dep_list = time_dep.split(':')
            self._time_dep = int(time_dep_list[0])*60 + int(time_dep_list[1])

    def tostring(self):
        return 'FLIGHT: {},{},{},{},{},{},{},{},{},{}'.format(
            self._record_number,
            self._date_arr,
            self._time_arr,
            self._aircraft_arr,
            self._type_arr,
            self._type_aircraft,
            self._date_dep,
            self._time_dep,
            self._aircraft_dep,
            self._type_dep)

class Gate:
    def __init__(self,
                 gate_number,
                 terminal,
                 area,
                 type_arr,
                 type_dep,
                 type_flight):
        self._gate_number = gate_number
        self._terminal = terminal
        self._area = area
        self._type_arr = type_arr
        self._type_dep = type_dep
        self._type_flight = type_flight

    def tostring(self):
        return 'GATE: {},{},{},{},{},{}'.format(
            self._gate_number,
            self._terminal,
            self._area,
            self._type_arr,
            self._type_dep,
            self._type_flight)


class Ticket:
    def __init__(self,
                 pass_id,
                 pass_num,
                 aircraft_arr,
                 date_arr,
                 aircraft_dep,
                 date_dep):
        self._pass_id = pass_id
        self._pass_num = pass_num
        self._aircraft_arr = aircraft_arr
        self._date_arr = date_arr
        self._aircraft_dep = aircraft_dep
        self._date_dep = date_dep


class Gene:
    def __init__(self, flight: Flight, gate: Gate):
        self._flight = flight
        self._gate = gate

    def mutation(self, mutation_rate, gates):
        a = random.randint(0,999)
        if a in range(0, int(1000*mutation_rate)):
            b = random.randint(0, len(gates)-1)
            self._gate = gates[b]

    def replicate(self):
        return Gene(self._flight, self._gate)

    @staticmethod
    def time_for_walk_t_t(area1, area2):
        if (area1 == 'North' and area2 == 'North') or \
                (area1 == 'Center' and area2 == 'Center') or \
                (area1 == 'South' and area2 == 'South'):
            walk_time = 10
        elif (area1 == 'North' and area2 == 'Center') or \
                (area1 == 'South' and area2 == 'Center') or \
                (area1 == 'Center' and area2 == 'North') or \
                (area1 == 'Center' and area2 == 'South'):
            walk_time = 15
        else:
            walk_time = 20
        return walk_time

    @staticmethod
    def time_for_walk_s_s(area1, area2):
        if (area1 == 'North' and area2 == 'North') or \
                (area1 == 'Center' and area2 == 'Center') or \
                (area1 == 'South' and area2 == 'South') or \
                (area1 == 'East' and area2 == 'East'):
            walk_time = 10
        elif (area1 == 'North' and area2 == 'Center') or \
                (area1 == 'South' and area2 == 'Center') or \
                (area1 == 'Center' and area2 == 'North') or \
                (area1 == 'Center' and area2 == 'South') or \
                (area1 == 'Center' and area2 == 'East') or \
                (area1 == 'East' and area2 == 'Center'):
            walk_time = 15
        else:
            walk_time = 20
        return walk_time

    @staticmethod
    def time_for_walk_s_t(area1, area2):
        if area1 == 'Center' and area2 == 'Center':
            walk_time = 15
        elif (area1 == 'Center' and area2 == 'North') or \
                (area1 == 'North' and area2 == 'Center') or \
                (area1 == 'Center' and area2 == 'South') or \
                (area1 == 'South' and area2 == 'Center') or \
                (area1 == 'Center' and area2 == 'East') or \
                (area1 == 'East' and area2 == 'Center'):
            walk_time = 20
        else:
            walk_time = 25
        return walk_time


    @staticmethod
    def time_transfer(gene_arr,gene_dep):
        tt_arr = gene_arr._flight._type_arr
        tt_dep = gene_dep._flight._type_dep
        ter_arr = gene_arr._gate._terminal
        ter_dep = gene_dep._gate._terminal
        area_arr = gene_arr._gate._area
        area_dep = gene_dep._gate._area
        walk_t_t = Gene.time_for_walk_t_t(area_arr,area_dep)
        walk_s_s = Gene.time_for_walk_s_s(area_arr,area_dep)
        walk_s_t = Gene.time_for_walk_s_t(area_arr,area_dep)
        if tt_arr == 'D' and tt_dep == 'D':
            if ter_arr == 'T' and ter_dep == 'T':
                # including time for walk
                time = 15 + walk_t_t
            elif ter_arr == 'S' and ter_dep == 'S':
                time = 15 + walk_s_s
            else:
                time = 20 + 1*8 + walk_s_t
        elif tt_arr == 'D' and tt_dep == 'I':
            if ter_arr == 'T' and ter_dep == 'T':
                time = 35 + walk_t_t
            elif ter_arr == 'S' and ter_dep == 'S':
                time = 35 + walk_s_s
            else:
                time = 40 + 1*8 + walk_s_t
        elif tt_arr == 'I' and tt_dep == 'D':
            if ter_arr == 'T' and ter_dep == 'T':
                time = 35 + walk_t_t
            elif ter_arr == 'S' and ter_dep == 'S':
                time = 45 + 2*8 + walk_s_s
            else:
                time = 40 + 1*8 + walk_s_t
        else:
            if ter_arr == 'T' and ter_dep == 'T':
                time = 20 + walk_t_t
            elif ter_arr == 'S' and ter_dep == 'S':
                time = 20 + walk_s_s
            else:
                time = 30 + 1*8 + walk_s_t
        return time

class GenoType:
    def __init__(self, gene_list: list):
        self._gene_list = gene_list

    def validation(self) -> bool:
        return True

    def is_valid(self) -> bool:
        """
        Validation process is consist of two main step:
        1. Check the type of flights and gates
        2. Check the rationality of timetable at each gate
        """
        timetable = {}
        for gene in self._gene_list:
            if gene._flight._type_aircraft in gene._gate._type_flight and \
                    gene._flight._type_arr in gene._gate._type_arr and \
                    gene._flight._type_dep in gene._gate._type_dep:
                gate_id = gene._gate._gate_number
                if gate_id != 'L':
                    if gate_id in timetable.keys():
                        this_gate = timetable[gate_id]
                        for time_list in this_gate:
                            if gene._flight._time_dep <= time_list[0]-45 or gene._flight._time_arr >= time_list[1]+45:
                                continue
                            else:
                                return False
                        this_gate.append([gene._flight._time_arr, gene._flight._time_dep])
                    else:
                        timetable.update({gate_id:[]})
                        timetable[gate_id].append([gene._flight._time_arr, gene._flight._time_dep])
                else:
                    if gate_id in timetable.keys():
                        timetable[gate_id].append([gene._flight._time_arr, gene._flight._time_dep])
                    else:
                        timetable.update({gate_id:[]})
                        timetable[gate_id].append([gene._flight._time_arr, gene._flight._time_dep])

            else:
                return False
        return True

    def validation_score(self):
        """
        Validation process is consist of two main step:
        1. Check the type of flights and gates
        2. Check the rationality of timetable at each gate
        """
        invalid_num = 0
        timetable = {}
        for gene in self._gene_list:
            if gene._flight._type_aircraft in gene._gate._type_flight and \
                    gene._flight._type_arr in gene._gate._type_arr and \
                    gene._flight._type_dep in gene._gate._type_dep:
                gate_id = gene._gate._gate_number
                if gate_id != 'L':
                    if gate_id in timetable.keys():
                        this_gate = timetable[gate_id]
                        for time_list in this_gate:
                            if gene._flight._time_dep <= time_list[0] - 45 or gene._flight._time_arr >= time_list[1] + 45:
                                continue
                            else:
                                invalid_num += 1
                        this_gate.append([gene._flight._time_arr, gene._flight._time_dep])
                    else:
                        timetable.update({gate_id: []})
                        timetable[gate_id].append([gene._flight._time_arr, gene._flight._time_dep])
                else:
                    if gate_id in timetable.keys():
                        timetable[gate_id].append([gene._flight._time_arr, gene._flight._time_dep])
                    else:
                        timetable.update({gate_id: []})
                        timetable[gate_id].append([gene._flight._time_arr, gene._flight._time_dep])

            else:
                invalid_num += 1
        return invalid_num