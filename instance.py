""" instance of the unit commitment """

from model import *
from pyomo.opt import SolverFactory
from pyomo.environ import DataPortal
import numpy as np
import pandas as pd


def run_optimization(path_out):
    # Select Solver
    opt = SolverFactory('cbc')

    # Create DataPortal
    data = DataPortal()

    # Read timeseries
    data.load(filename='input/timeseries_gas.csv', index='t', param='gas')
    data.load(filename='input/timeseries_heat_demand.csv', index='t', param='dem')
    data.load(filename='input/timeseries_spot.csv', index='t', param='spot')

    # Create instanz
    instance = m.create_instance(data)

    # Solve the optimization problem
    results = opt.solve(instance, symbolic_solver_labels=True, tee=True,
                        load_solutions=True)

    # Write timeseries
    df_output = pd.DataFrame()
    for t in instance.t.value:
        for j in instance.j_chp.value:
            df_output.loc[t, '_'.join([str(j), 'gas'])] = instance.gen_chp_gas[j, t].value
            df_output.loc[t, '_'.join([str(j), 'power'])] = instance.gen_chp_power[j, t].value
            df_output.loc[t, '_'.join([str(j), 'heat'])] = instance.gen_chp_heat[j, t].value
            df_output.loc[t, '_'.join([str(j), 'oh'])] = instance.on_chp[j, t].value\
                * df_chp_costs.loc[j, 'oh']
            df_output.loc[t, '_'.join([str(j), 'grid'])] = instance.gen_chp_gas[j, t].value\
                * df_chp_costs.loc[j, 'grid']
        for j in instance.j_heat_plant.value:
            df_output.loc[t, '_'.join([str(j), 'gas'])] = instance.gen_heat_plant_gas[j, t].value
            df_output.loc[t, '_'.join([str(j), 'heat'])] = instance.gen_heat_plant_heat[j, t].value
            df_output.loc[t, '_'.join([str(j), 'oh'])] = instance.on_heat_plant[j, t].value\
                * df_heat_plant_costs.loc[j, 'oh']
            df_output.loc[t, '_'.join([str(j), 'grid'])] = instance.gen_heat_plant_gas[j, t].value\
                * df_heat_plant_costs.loc[j, 'grid']
        for j in instance.j_store.value:
            df_output.loc[t, '_'.join([str(j), 'charge'])] = instance.store_charge[j, t].value
            df_output.loc[t, '_'.join([str(j), 'capacity'])] = instance.store_capacity[j, t].value
            df_output.loc[t, '_'.join([str(j), 'discharge'])] = instance.store_discharge[j, t].value
        df_output.loc[t, 'demand'] = instance.dem[t]
        df_output.loc[t, 'spot'] = instance.spot[t]
        df_output.loc[t, 'gas'] = instance.gas[t]

    df_output.to_csv(path_out+'timeseries.csv')
