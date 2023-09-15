from environs import Env
from os import getenv, path
from enum import Enum
from argparse import ArgumentParser
from tabulate import tabulate
from colorama import Fore, Style


class Environment(Enum):
    TRAIN = 'train'
    PREDICT = 'predict'


parser = ArgumentParser()

parser.add_argument(
    '-e', '--environment',
    type=str,
    default=Environment.TRAIN.value,
    help='Environment to load',
    required=False
)

arguments = parser.parse_known_args()[0]

abspath = path.abspath(path.curdir)
strpath = f'{abspath}/.env.{arguments.environment}'
path = path.normpath(strpath)

env = Env()
env.read_env(path=path)

env_vars = [
    [Fore.BLACK +
        "\n# Yahoo Finance API parameters", "" + Style.RESET_ALL],
    [Fore.GREEN + "TICKERS", getenv("TICKERS") + Style.RESET_ALL],
    [Fore.GREEN + "DATA_INTERVAL", getenv("DATA_INTERVAL") + Style.RESET_ALL],
    [Fore.GREEN + "FETCH_START_DATE",
        getenv("FETCH_START_DATE") + Style.RESET_ALL],
    [Fore.GREEN + "FETCH_END_DATE",
        getenv("FETCH_END_DATE") + Style.RESET_ALL],
    [Fore.BLACK +
        "\n# Dataset parameters", "" + Style.RESET_ALL],
    [Fore.YELLOW + "DATA_SAMPLES", getenv("DATA_SAMPLES") + Style.RESET_ALL],
    [Fore.YELLOW + "TICKER_TO_PREDICT",
        getenv("TICKER_TO_PREDICT") + Style.RESET_ALL],
    [Fore.YELLOW + "PRICE_TYPE", getenv("PRICE_TYPE") + Style.RESET_ALL],
    [Fore.YELLOW + "HISTORY_TIME_RANGE",
        getenv("HISTORY_TIME_RANGE") + Style.RESET_ALL],
    [Fore.YELLOW + "FUTURE_OFFSET_POINT",
        getenv("FUTURE_OFFSET_POINT") + Style.RESET_ALL],
    [Fore.BLACK +
        "\n# Data loader parameters", "" + Style.RESET_ALL],
    [Fore.LIGHTGREEN_EX + "BATCH_SIZE",
        getenv("BATCH_SIZE") + Style.RESET_ALL],
    [Fore.LIGHTGREEN_EX + "NUM_WORKERS",
        getenv("NUM_WORKERS") + Style.RESET_ALL],
    [Fore.BLACK +
        "\n# Model parameters", "" + Style.RESET_ALL],
    [Fore.MAGENTA + "USE_CUDA", getenv("USE_CUDA") + Style.RESET_ALL],
    [Fore.MAGENTA + "DEVICE", getenv("DEVICE") + Style.RESET_ALL],
    [Fore.MAGENTA + "HIDDEN_DIM", getenv("HIDDEN_DIM") + Style.RESET_ALL],
    [Fore.MAGENTA + "LEARNING_RATE",
        getenv("LEARNING_RATE") + Style.RESET_ALL],
    [Fore.BLACK +
        "\n# Training parameters", "" + Style.RESET_ALL],
    [Fore.RED + "NUM_EPOCHS", getenv("NUM_EPOCHS") + Style.RESET_ALL],
    [Fore.RED + "MATMUL_PRERCISION",
        getenv("MATMUL_PRECISION") + Style.RESET_ALL],
    [Fore.BLACK +
        "\n# Provider-specific (default: Yahoo Finance) price parameters", "" + Style.RESET_ALL],
    [Fore.BLUE + "PRICES_PER_TICKER_COUNT",
        getenv("PRICES_PER_TICKER_COUNT") + Style.RESET_ALL],
    [Fore.BLACK +
        "\n", "" + Style.RESET_ALL],
    [Fore.BLACK +
        "# Predictor's language (not implemented yet)", "" + Style.RESET_ALL],
    [Fore.BLACK + Style.DIM + "LANGUAGE",
        getenv("LANGUAGE") + Style.RESET_ALL],

]
print("\n")
print(
    tabulate(
        env_vars,
        headers=[Fore.MAGENTA +
                 "Variable", "Value" + Style.RESET_ALL]
    )
)
print("\n")
