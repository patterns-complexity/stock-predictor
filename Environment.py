from environs import Env
from os import getenv, path
from enum import Enum
from argparse import ArgumentParser


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

TICKERS = str(getenv('TICKERS')).split(',')
HISTORY_DAYS_COUNT = int(getenv('HISTORY_DAYS_COUNT'))
FUTURE_DAYS_DELTA = int(getenv('FUTURE_DAYS_DELTA'))
PRICES_PER_TICKER_COUNT = int(getenv('PRICES_PER_TICKER_COUNT'))

BATCH_SIZE = int(getenv('BATCH_SIZE', 1))
NUM_WORKERS = int(getenv('NUM_WORKERS', 1))
NUM_EPOCHS = int(getenv('NUM_EPOCHS', 10))
HIDDEN_DIM = int(getenv('HIDDEN_DIM', 64))

LEARNING_RATE = float(getenv('LEARNING_RATE', 0.001))

DATA_SAMPLES = int(getenv('DATA_SAMPLES', 1000))

print(f"""
Environment variables loaded from {path}:
    TICKERS: {TICKERS}
    HISTORY_DAYS_COUNT: {HISTORY_DAYS_COUNT}
    FUTURE_DAYS_DELTA: {FUTURE_DAYS_DELTA}
    PRICES_PER_TICKER_COUNT: {PRICES_PER_TICKER_COUNT}
    BATCH_SIZE: {BATCH_SIZE}
    NUM_WORKERS: {NUM_WORKERS}
    NUM_EPOCHS: {NUM_EPOCHS}
    HIDDEN_DIM: {HIDDEN_DIM}
    LEARNING_RATE: {LEARNING_RATE}
    DATA_SAMPLES: {DATA_SAMPLES}
""")
