import pandas as pd
import matplotlib.pyplot as plt
from helpers.loggers import plot_logger


def plot_pie(df: pd.DataFrame, name: str, rows: list):
    """
    Returns a Matplotlib Figure object of a pie chart.

    Filters the passed dataframe using the list of rows and
    uses the plot.pie method to create the axes object from which the
    figure is returned.

    The function catches and logs exceptions that arise in occasional cases
    of insufficient data but does not reraise them meaning the rest
    of the app will execute without the figures.

    Args:
        N/A

    Returns:
        Matplotlib Figure object of a pie chart.
    """
    try:
        axes = (
            df[name]
            .filter(items=rows, axis=0)
            .plot.pie(
                explode=(0, 0.1, 0),
                autopct="%1.0f%%",
                pctdistance=0.4,
                labeldistance=0.8,
                shadow=True,
                startangle=120,
            )
        )
        return axes.get_figure()

    except ValueError as e:
        plot_logger.error(f"Value error in plot_pie: {str(e)}, name = {name}")

    except RuntimeError as e:
        plot_logger.error(f"Runtime error in plot_pie: {str(e)}, name = {name}")

    except Exception as e:
        plot_logger.error(f"Unexpected error in plot_pie: {str(e)}, name = {name}")
