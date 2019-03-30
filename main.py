from analysis import *
from instance import run_optimization
import os

# make output folder
path_out = 'output/'
if not os.path.isdir(path_out):
    os.makedirs(path_out)
# Run optimization
run_optimization(path_out)
# Read timeseries from optimization
df_data = pd.read_csv('output/timeseries.csv')

# Read unit costs
df_chp_costs = pd.read_csv('input/cost_chp.csv', index_col=0)
df_heat_plant_costs = pd.read_csv('input/cost_heat_plant.csv', index_col=0)
# Read market costs
df_spot = pd.read_csv('input/timeseries_spot.csv', index_col=0)
df_gas = pd.read_csv('input/timeseries_gas.csv', index_col=0)
# Evaluate units
units = df_chp_costs.index.union(df_heat_plant_costs.index)
kpis = ['gas', 'power', 'heat', 'oh']
costs = ['gas', 'grid', 'oh', 'spot']

# Analysis
kpi_per_unit(df_data, units, kpis, path_out)
costs_per_unit(df_data, units, costs, df_chp_costs, df_heat_plant_costs,
               path_out)

# Plots
plot_timeseries(df_data, 'spot', 'Euro/MW', path_out)
plot_timeseries(df_data, 'demand', 'MW', path_out)
plot_timeseries(df_data, 'chp_old_heat', 'MW', path_out)

plot_heat_stack(df_data, path_out)
