# Set non-interactive backend to avoid macOS issues
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

import matplotlib.pyplot as plt
from analysis.lca import perform_lcia

def plot(analysis_result, x, y='value', group_by=None):
    # Fix for pandas FutureWarning: specify observed=False explicitly
    df = analysis_result['data'].pivot_table(index=x, values=y, columns=group_by, observed=False)
    df.plot(kind='bar', stacked=True, rot=0)

    plt.title(analysis_result['title'], fontweight='bold', fontsize=14)
    plt.xlabel(x, fontweight='bold', fontsize=14)

    unit = analysis_result['unit']
    value = analysis_result['value']
    plt.ylabel(unit, fontweight='bold', fontsize=14)
    plt.yticks(fontweight='bold', fontsize=14)
    plt.xticks(fontweight='bold', fontsize=14)
    # Save the figure to a file instead of showing it interactively
    plt.savefig('plot.png')
    print("Plot saved to plot.png")
    plt.close()


def plot_lcia_multiple_pathways(multiple_pathways, indicator="GWP"):
    stack_df = perform_lcia(multiple_pathways, indicator)
    #Greys
    stack_df.plot.bar(stacked=True, width=0.40, figsize=(12, 7))
    plt.title("LCIA - {}  for Multiple Pathways".format(indicator), fontweight="bold", fontsize=14)
    plt.ylabel("Emissions in kg", fontweight="bold", fontsize=14)
    plt.xticks(fontweight='bold', fontsize=14, rotation=0)
    plt.savefig("multiple_pathways/stacked_plot.png")
    # Save the figure to a file instead of showing it interactively
    print("Plot saved to multiple_pathways/stacked_plot.png")
    plt.close()

    return plt
