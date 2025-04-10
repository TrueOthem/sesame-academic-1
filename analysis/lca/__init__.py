import pandas as pd
import copy

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 02:05:43 2019

@author: SESAME-MITEI

LCA File for pathway analysis performs LCA based on units of emission factors in database.
Units accounted for include "kg/kWh", "kg/MJmile", "kg/MJ", "MJ/MJmile", "MJ/kWh", "MJ/MJ"

"""


def compute_activity_flows(df, flow_output, flow_info):
    flow_dict = {}
    flows = pd.unique(df['flows'].dropna())

    for i in flows:
        row = df[df['flows'] == i].groupby('flows').agg({'value': 'sum', 'unit': 'first'}).reset_index().iloc[0]
        row['value'] = float(row['value'])
        flow = {"name": i.lower()}
        upper_unit, lower_unit = row['unit'].split('/')
        flow["unit"] = upper_unit
#Tony changed rounding from 4 to 9 because nuclear and hydro power csv numbers are very small
        if lower_unit == "MJmile":
            assert flow_output['unit'] == "MJ"
            flow["value"] = round(row['value'] * flow_output['value'] * flow_info["distance"], 9)
        elif lower_unit == "kgmile":
            assert flow_output['unit'] == "kg"
            flow["value"] = round(row['value'] * flow_output['value'] * flow_info["distance"], 9)
        else:
            assert flow_output['unit'] == lower_unit
            flow["value"] = round(row['value'] * flow_output['value'], 9)

        flow_dict[i.lower()] = flow

    return flow_dict


def compute_flows(df, flow_output, flow_info):
    final_dict = {}
    if "activity" in list(df.columns):
        activities = list(df["activity"].unique())
        for activity in activities:
            activity_df = df[df["activity"] == activity]
            final_dict[activity] = compute_activity_flows(activity_df, flow_output, flow_info)
    else:
        final_dict["aggregate"] = compute_activity_flows(df, flow_output, flow_info)

    return final_dict


def compute_input_flows(df, flow_output=None, flow_info=None):
    df = df[df["direction"] == "input"]

    combined = {}
    all_input_flows = compute_flows(df, flow_output, flow_info)
    for _, flow_dict in all_input_flows.items():
        for name, flow in flow_dict.items():
            if name in combined:
                combined[name]["value"] += flow["value"]
            else:
                combined[name] = flow
    return combined

# Adding H2/Electrical emissions contribution calculator


def compute_elec_output_flows(df, flow_output=None, flow_info=None):
    df = df[df["direction"] == "output"]
    if "flow_source" in list(df.columns):
        df_elec = df[df["flow_source"] == "electricity"]
        if df_elec.empty:
            df_elec = df.copy()
            df_elec['value'] = 0
    else:
        df_elec = df.copy()
        df_elec['value'] = 0
    elec_emission_flows = compute_flows(df_elec, flow_output, flow_info)
    return elec_emission_flows

def compute_elec_input_flows(df, flow_output=None, flow_info=None):
    df = df[df["direction"] == "input"]
    df_elec = df[df["flows"] == "electricity"]
    if df_elec.empty:
        df_elec = df.copy()
        df_elec['value'] = 0
    elec_emission_flows = compute_flows(df_elec, flow_output, flow_info)
    return elec_emission_flows

def adjust_emissions_electricity(df, new_val, type_adj = 'ci',flow_output=None, flow_info=None):
    ci = {}
    elec_input = compute_elec_input_flows(df, flow_output, flow_info)
    elec_output = compute_elec_output_flows(df, flow_output, flow_info)
    elec_output_new = copy.deepcopy(elec_output)
    if "activity" in list(df.columns):
        activities = list(elec_input.keys())
        for activity in activities:
             input_val = elec_input[activity]['electricity']['value']
             flows = elec_output[activity]
             ci[activity] = {}
             for flow in flows.keys():
                if type_adj == 'ci':
                    if flow in new_val.keys():
                        elec_output_new[activity][flow]['value'] = new_val[flow] * input_val
                elif type_adj == 'elec_amt':
                     ci[activity][flow] = {}
                     output_val = elec_output[activity][flow]['value']
                     ci[activity][flow]['value']= output_val/input_val
                     ci[activity][flow]['unit'] = elec_output[activity][flow]['unit'] + '/' + elec_input[activity]['electricity']['unit']
                     ci[activity][flow]['name'] = flow + ' grid intensity'
                     elec_output_new[activity][flow]['value'] = new_val * (output_val/input_val)

    return ci, elec_output, elec_output_new

def compute_grid_intensity(df, flow_output=None, flow_info=None):
    ci = {}
    elec_input = compute_elec_input_flows(df, flow_output, flow_info)
    elec_output = compute_elec_output_flows(df, flow_output, flow_info)
    if "activity" in list(df.columns):
        activities = list(elec_input.keys())
        for activity in activities:
             input_val = elec_input[activity]['electricity']['value']
             flows = elec_output[activity]
             ci[activity] = {}
             for flow in flows.keys():
                ci[activity][flow] = {}
                output_val = elec_output[activity][flow]['value']
                ci[activity][flow]['value']= output_val/input_val
                ci[activity][flow]['unit'] = elec_output[activity][flow]['unit'] + '/' + elec_input[activity]['electricity']['unit']
                ci[activity][flow]['name'] = flow + ' grid intensity'

    return ci





#
# def compute_h2_flows(df, flow_output=None, flow_info=None):
#     df = df[df["direction"] == "output"]
#     if "flow_source" in list(df.columns):
#         df_h2 = df[df["flow_source"] == "h2"]
#     else:
#         df_h2 = df.copy()
#         df_h2['value'] = 0
#     h2_emission_flows = compute_flows(df_h2, flow_output, flow_info)
#     return h2_emission_flows


def compute_emission_flows(df, flow_output=None, flow_info=None):
    df = df[df["direction"] == "output"]
    if "flow_source" in list(df.columns):
        df = df[df["flow_source"] == "total"]
    all_emission_flows = compute_flows(df, flow_output, flow_info)
    return all_emission_flows


def calculate_emissions(results):
    data = []

    for stage in results:
        if stage == 'other_info':
            continue

        emissions = results[stage]['flow_emissions']

        if len(emissions) == 0:
            emissions = {"aggregate": {'co2': {'name': 'co2', 'value': 0, 'unit': 'kg'}}}

        for sub_stage, emission in emissions.items():
            for flow in emission:
                data.append({
                    'stage': stage,
                    'sub_stage': sub_stage,
                    'flows': emission[flow]['name'],
                    'value': emission[flow]['value'],
                    'unit': emission[flow]['unit']
                })

    return pd.DataFrame(data, columns=['stage', 'sub_stage', 'flows', 'value', 'unit'])


def calculate_co2_emissions(results):
    df = calculate_emissions(results)
    return df[df['flows'] == 'co2']


def perform_lcia(results, indicator='GWP'):
    emissions_df = calculate_emissions(results)

    lcia_df = pd.read_csv('analysis/lca/lciadata.csv')
    lcia_df = lcia_df[lcia_df['indicator'] == indicator]

    merged_df = pd.merge(emissions_df, lcia_df, on='flows', how='right')
    merged_df['value'] = merged_df['value_x'] * merged_df['value_y']
    merged_df = merged_df.rename(columns={'unit_x': 'unit'})
    merged_df.drop(columns=['value_x', 'value_y', 'flows', 'unit_y'], inplace=True)
    merged_df = merged_df.groupby(['stage', 'sub_stage']).agg({
        'value': 'sum',
        'unit': 'first',
        'indicator': 'first',
        'name': 'first',
    }).reset_index()

    return merged_df


def indicators():
    df = pd.read_csv('analysis/lca/lciadata.csv')
    return [
        {'value': value, 'label': label} for label, value in df[['name', 'indicator']].drop_duplicates().to_numpy()
    ]


def run(pathways, indicator='GWP'):
    data = pd.DataFrame()
    name = None

    for pathway in pathways:
        pathway_results = pathway.perform()
        # elec = total = 0
        # for stage in pathway_results.items():
        #     elec = elec + stage["elec_emissions"]['aggregate']['co2']['value']
        #     total = total + stage['flow_emissions']['aggregate']['co2']['value']
        # if elec > 0.1 * total:
        #     x= input('Enter grid intensity')
        #     for stage in pathway_results.items():
        #         stage['flow_emissions']['aggregate']['co2']['value'] = stage['flow_emissions']['aggregate']['co2']['value']*x*pathway_results["Enduse"]["flow_output"]["value"]/elec
        value = pathway_results["Enduse"]["flow_output"]["unit"]
        df = perform_lcia(pathway_results, indicator=indicator)
        df.value = df.value*1000
        df.unit = "g"
        df['pathway'] = pathway.name

        # sort by stage
        df['stage'] = pd.Categorical(df['stage'], categories=['Enduse', 'GateToEnduse', 'Process', 'Midstream', 'Upstream'], ordered=True)
        df = df.sort_values('stage')

        name = df['name'].iloc[0]
        # Use pd.concat instead of append (which is deprecated in newer pandas versions)
        data = pd.concat([data, df[['value', 'stage', 'sub_stage', 'pathway']]], ignore_index=True)

    return dict(
        title=f'Lifecycle GHG Emissions',
        unit=f'gCO\u2082e/{value}',
        value=value,
        columns=['value', 'stage', 'sub_stage', 'pathway'],
        params={'indicator': indicator},
        data=data
    )
