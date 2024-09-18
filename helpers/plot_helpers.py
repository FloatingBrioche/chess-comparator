import pandas as pd
import matplotlib.pyplot as plt


def plot_pie(df: pd.DataFrame, name: str, rows):


    axes = df[name].filter(items=rows, axis=0).plot.pie(
        explode=(0, 0.1, 0),
        autopct="%1.0f%%",
        pctdistance=0.4,
        labeldistance=0.8,
        shadow=True,
        startangle=120
    )

    return axes.get_figure()
