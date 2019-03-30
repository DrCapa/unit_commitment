""" short analysis and some plots """
import pandas as pd
import matplotlib.pyplot as plt
import os


def kpi_per_unit(df_data, units, kpis, path_out):
    """ calcluation of the key performance indicator for the units """
    s_data_sum = df_data.sum(axis=0)
    dic = {(unit, kpi): s_data_sum[unit + '_' + kpi]
           for unit in units
           for kpi in kpis
           if unit + '_' + kpi in s_data_sum.index}
    df_kpi = pd.Series(dic).unstack().fillna(0)
    export = pd.ExcelWriter(path_out+'kpi_per_unit.xlsx', engine='xlsxwriter')
    df_kpi.to_excel(export, 'output', startrow=0,
                    startcol=0, float_format='%0.2f')
    export.save()


def costs_per_unit(df_data, units, costs, df_chp_costs, df_heat_plant_costs,
                   path_out):
    """ calcluation of the costs for the units """
    df_costs = pd.DataFrame(index=units, columns=costs)
    df_temp = pd.DataFrame(index=df_data.index)
    # gas costs and spot revenues
    for column in df_data.columns:
        if(column.find('_gas') >= 0):
            df_temp[column] = df_data[column]*df_data['gas']
        if(column.find('_power') >= 0):
            df_temp[column] = -df_data[column]*df_data['spot']
    df_temp.columns = df_temp.columns.str.replace('_power', '_spot')
    df_temp_sum = df_temp.sum(axis=0)
    df_data_sum = df_data.sum(axis=0)
    for unit in units:
        for cost in costs:
            name = unit+'_'+cost
            if((cost == 'gas' or cost == 'spot') and name in df_temp_sum):
                df_costs.loc[unit, cost] = df_temp_sum[name]
            if((cost == 'oh' or cost == 'grid') and name in df_data_sum):
                df_costs.loc[unit, cost] = df_data_sum[name]
    df_costs = df_costs.fillna(0)
    # Export
    export = pd.ExcelWriter(path_out+'costs_per_unit.xlsx',
                            engine='xlsxwriter')
    df_costs.to_excel(export, 'output', startrow=0,
                      startcol=0, float_format='%0.2f')
    export.save()


def plot_timeseries(df_data, name, measure, path_out):
    """ plot single timeseries """
    for column in df_data.columns:
        if(column.find(name) >= 0):
            y = df_data[name]
    x = df_data.index
    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot(111)
    ax.plot(x, y, drawstyle='steps-post', linewidth=1.2, label=name)
    plt.title(name, loc='left')
    plt.xlabel('hour')
    plt.ylabel(measure)
    plt.grid()
    if not os.path.isdir(path_out+'plots/'):
        os.makedirs(path_out+'plots/')
    fig.savefig(path_out+'plots/'+name)


def plot_heat_stack(df_data, path_out):
    """ plot heat stack of the units """
    x = df_data.index
    df_y_pos = pd.DataFrame()
    df_y_neg = pd.DataFrame()

    for column in df_data.columns:
        if(column.find('_heat') >= 0):
            df_y_pos[column] = df_data[column]
        if(column.find('store_discharge') >= 0):
            df_y_pos[column] = df_data[column]
        if(column.find('store_charge') >= 0):
            df_y_neg[column] = -df_data[column]

    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot(111)
    a = 0
    b = 0
    for column in df_y_pos.columns:
        a = b
        b = b + df_y_pos[column]
        ax.fill_between(x, a, b, step='post', label=column, alpha=.7)
    a = 0
    b = 0
    for column in df_y_neg.columns:
        a = b
        b = b + df_y_neg[column]
        ax.fill_between(x, a, b, step='post', label=column, alpha=.7)

    ax.plot(x, df_data['demand'], drawstyle='steps-post', color='black',
            linewidth=1.0, label='demand')

    plt.title('heat_stack', loc='left')
    plt.xlabel('hour')
    plt.ylabel('MW')
    plt.legend(loc='upper center')
    plt.grid()
    lgd = plt.legend(loc=9, bbox_to_anchor=(0.5, -0.1), ncol=5)
    art = []
    art.append(lgd)
    if not os.path.isdir(path_out+'plots/'):
        os.makedirs(path_out+'plots/')
    fig.savefig(path_out+'/plots/heat_stack', additional_artists=art,
                bbox_inches="tight")
