""" model of the unit commitment """

import pandas as pd
from pyomo.environ import *


# Define abstracte model
m = AbstractModel()

# Define sets
m.t = Set(ordered=True)

# Define parameters
m.gas = Param(m.t)
m.spot = Param(m.t)
m.dem = Param(m.t)

# Read unit capacities
df_chp_param = pd.read_csv('input/capacity_chp.csv', index_col=0)
df_heat_plant_param = pd.read_csv('input/capacity_heat_plant.csv', index_col=0)
df_store_param = pd.read_csv('input/capacity_store.csv', index_col=0)

# Read unit costs
df_chp_costs = pd.read_csv('input/cost_chp.csv', index_col=0)
df_heat_plant_costs = pd.read_csv('input/cost_heat_plant.csv', index_col=0)

# Define unit index
m.j_chp = Set(initialize=df_chp_param.index)
m.j_heat_plant = Set(initialize=df_heat_plant_param.index)
m.j_store = Set(initialize=df_store_param.index)

# CHP equations
m.on_chp = Var(m.j_chp, m.t, within=Binary)
m.gen_chp_gas = Var(m.j_chp, m.t, domain=NonNegativeReals)
m.gen_chp_power = Var(m.j_chp, m.t, domain=NonNegativeReals)
m.gen_chp_heat = Var(m.j_chp, m.t, domain=NonNegativeReals)


def heat_max_chp(m, j, t):
    return m.gen_chp_heat[j, t] <= df_chp_param.loc[j, 'heat_max']*m.on_chp[j, t]
m.heatmaxchp = Constraint(m.j_chp, m.t, rule=heat_max_chp)


def heat_min_chp(m, j, t):
    return df_chp_param.loc[j, 'heat_min']*m.on_chp[j, t] <= m.gen_chp_heat[j, t]
m.heatminchp = Constraint(m.j_chp, m.t, rule=heat_min_chp)


def heat_power_chp(m, j, t):
    """ power = a*heat + b*on """
    a = (df_chp_param.loc[j, 'power_max']-df_chp_param.loc[j, 'power_min'])\
        / (df_chp_param.loc[j, 'heat_max']-df_chp_param.loc[j, 'heat_min'])
    b = df_chp_param.loc[j, 'power_min']-a*df_chp_param.loc[j, 'heat_min']
    return m.gen_chp_power[j, t] == a*m.gen_chp_heat[j, t]+b*m.on_chp[j, t]
m.heatpowerchp = Constraint(m.j_chp, m.t, rule=heat_power_chp)


def heat_gas_chp(m, j, t):
    """ gas = a*heat + b*on """
    a = (df_chp_param.loc[j, 'gas_max']-df_chp_param.loc[j, 'gas_min'])\
        / (df_chp_param.loc[j, 'heat_max']-df_chp_param.loc[j, 'heat_min'])
    b = df_chp_param.loc[j, 'gas_min']-a*df_chp_param.loc[j, 'heat_min']
    return m.gen_chp_gas[j, t] == a*m.gen_chp_heat[j, t]+b*m.on_chp[j, t]
m.heatgasrchp = Constraint(m.j_chp, m.t, rule=heat_gas_chp)

# Heat plant equations
m.on_heat_plant = Var(m.j_heat_plant, m.t, within=Binary)
m.gen_heat_plant_gas = Var(m.j_heat_plant, m.t, domain=NonNegativeReals)
m.gen_heat_plant_heat = Var(m.j_heat_plant, m.t, domain=NonNegativeReals)


def heat_max_heat_plant(m, j, t):
    return (m.gen_heat_plant_heat[j, t] <=
            df_heat_plant_param.loc[j, 'heat_max']*m.on_heat_plant[j, t])
m.heatmaxheatplant = Constraint(m.j_heat_plant, m.t, rule=heat_max_heat_plant)


def heat_min_heat_plant(m, j, t):
    return (df_heat_plant_param.loc[j, 'heat_min']*m.on_heat_plant[j, t] <=
            m.gen_heat_plant_heat[j, t])
m.heatminheatplant = Constraint(m.j_heat_plant, m.t, rule=heat_min_heat_plant)


def heat_gas_heat_plant(m, j, t):
    """ gas = a*heat + b*on """
    a = (df_heat_plant_param.loc[j, 'gas_max']-df_heat_plant_param.loc[j, 'gas_min'])\
        / (df_heat_plant_param.loc[j, 'heat_max']-df_heat_plant_param.loc[j, 'heat_min'])
    b = df_heat_plant_param.loc[j, 'gas_min']-a*df_heat_plant_param.loc[j, 'heat_min']
    return (m.gen_heat_plant_gas[j, t] ==
            a*m.gen_heat_plant_heat[j, t]+b*m.on_heat_plant[j, t])
m.heatgasrheat_plant = Constraint(m.j_heat_plant, m.t, rule=heat_gas_heat_plant)

# Store equations
m.on_charge_store = Var(m.j_store, m.t, within=Binary)
m.on_discharge_store = Var(m.j_store, m.t, within=Binary)
m.store_charge = Var(m.j_store, m.t, domain=NonNegativeReals)
m.store_discharge = Var(m.j_store, m.t, domain=NonNegativeReals)
m.store_capacity = Var(m.j_store, m.t, domain=NonNegativeReals)


def charge_store(m, j, t):
    return (m.store_charge[j, t] <=
            df_store_param.loc[j, 'charge']*m.on_charge_store[j, t])
m.chargestorer = Constraint(m.j_store, m.t, rule=charge_store)


def discharge_store(m, j, t):
    if t == m.t.first():
        return m.store_discharge[j, t] == 0
    else:
        return (m.store_discharge[j, t] <=
                df_store_param.loc[j, 'discharge']*m.on_discharge_store[j, t])
m.dischargestore = Constraint(m.j_store, m.t, rule=discharge_store)


def capacity_max_store(m, j, t):
    return m.store_capacity[j, t] <= df_store_param.loc[j, 'capacity']
m.capacitymaxstore = Constraint(m.j_store, m.t, rule=capacity_max_store)


def capacity_store(m, j, t):
    if t == m.t.first():
        return m.store_capacity[j, t] == 0
    else:
        return (m.store_capacity[j, t] <=
                m.store_capacity[j, t-1]+m.store_charge[j, t]-m.store_discharge[j, t])
m.capacitystore = Constraint(m.j_store, m.t, rule=capacity_store)


def charge_or_discharge_store(m, j, t):
    return m.on_charge_store[j, t]+m.on_discharge_store[j, t] <= 1
m.chargeordischargestore = Constraint(m.j_store, m.t, rule=charge_or_discharge_store)


# Objective function
# oh - costs for operating hour, grid - gas grid fee 
def obj_expression(m):
    return sum((sum(m.gen_chp_gas[j, t] for j in m.j_chp) +
                sum(m.gen_heat_plant_gas[j, t] for j in m.j_heat_plant))*m.gas[t] -
               sum(m.gen_chp_power[j, t] for j in m.j_chp)*m.spot[t] +
               sum(m.on_chp[j, t]*df_chp_costs.loc[j, 'oh'] for j in m.j_chp) +
               sum(m.on_heat_plant[j, t]*df_heat_plant_costs.loc[j, 'oh']
                   for j in m.j_heat_plant) +
               sum(m.gen_chp_gas[j, t]*df_chp_costs.loc[j, 'grid'] for j in m.j_chp) +
               sum(m.gen_heat_plant_gas[j, t]*df_heat_plant_costs.loc[j, 'grid']
                   for j in m.j_heat_plant)
               for t in m.t)
m.obj = Objective(rule=obj_expression, sense=minimize)


# Heat-balance
def balance_rule(m, t):
    return (sum(m.gen_chp_heat[j, t] for j in m.j_chp) +
            sum(m.gen_heat_plant_heat[j, t] for j in m.j_heat_plant) +
            sum(m.store_discharge[j, t] for j in m.j_store) ==
            m.dem[t]+sum(m.store_charge[j, t] for j in m.j_store))
m.balance = Constraint(m.t, rule=balance_rule)
