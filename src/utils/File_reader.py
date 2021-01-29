import pandas as pd
from src.Gene import Flight,Gate,Ticket


class Reader:
    def __init__(self):
        pass

    @staticmethod
    def read(file):
        df = pd.read_csv(file)
        return df

    @staticmethod
    def form_flights(df: pd.DataFrame):
        n = df.shape[0]
        flights = []
        for i in range(n):
            tempt = df.iloc[i]
            if tempt['date_dep'] == '19-Jan-18' or \
                    tempt['date_arr'] == '21-Jan-18' or \
                    tempt['aircraft_arr'] == '*****':
                continue
            else:
                ff = Flight(record_number=tempt['ID'],
                            date_arr=tempt['date_arr'],
                            time_arr=tempt['time_arr'],
                            aircraft_arr=tempt['aircraft_arr'],
                            type_arr=tempt['type_arr'],
                            type_aircraft=tempt['type_aircraft'],
                            date_dep=tempt['date_dep'],
                            time_dep=tempt['time_dep'],
                            aircraft_dep=tempt['aircraft_dep'],
                            type_dep=tempt['type_dep'])
                flights.append(ff)
        return flights

    @staticmethod
    def form_gates(df: pd.DataFrame):
        n = df.shape[0]
        gates = []
        for i in range(n):
            tempt = df.iloc[i]
            gg = Gate(gate_number=tempt['ID'],
                      terminal=tempt['terminal'],
                      area=tempt['area'],
                      type_arr=tempt['type_arr'],
                      type_dep=tempt['type_dep'],
                      type_flight=tempt['type_flight'])
            gates.append(gg)
        return gates

    @staticmethod
    def form_ticket(df: pd.DataFrame):
        n = df.shape[0]
        tickets = []
        for i in range(n):
            tempt = df.iloc[i]
            if tempt['date_dep'] == '19-Jan-18' or tempt['date_arr'] == '21-Jan-18':
                continue
            else:
                tt = Ticket(pass_id=tempt['pass_id'],
                            pass_num=tempt['pass_num'],
                            aircraft_arr=tempt['aircraft_arr'],
                            date_arr=tempt['date_arr'],
                            aircraft_dep=tempt['aircraft_dep'],
                            date_dep=tempt['date_dep'])
                tickets.append(tt)
        return tickets
