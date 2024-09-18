import pandas as pd
import matplotlib.pyplot as plt


def plot_pie(df: pd.DataFrame, name: str, rows):

    explode = (0, 0.1, 0)

    pie = df[name].filter(items=rows, axis=0).plot.pie(
        explode=explode,
        autopct="%1.0f%%",
        pctdistance=0.4,
        labeldistance=0.8,
        shadow=True,
        startangle=120,
    )


    return pie