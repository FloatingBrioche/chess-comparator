import logging

logging.basicConfig(
    filename="errors.log",
    filemode="a",
    level=logging.ERROR,
    format="%(asctime)s – %(name)s. %(message)s",
    datefmt="%d-%b-%Y %H:%M:%S",
)

data_logger = logging.getLogger("Data logger")

request_logger = logging.getLogger("Request logger")

plot_logger = logging.getLogger("Plot logger")
