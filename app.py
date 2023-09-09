# Bootstrap

# Imports
from environs import Env

from src.Services.YFinanceService import YFinanceService

env = Env()
env.read_env()

yfinance_service = YFinanceService()
