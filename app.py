# %% Imports
from shutil import rmtree

from pytorch_lightning import Trainer
from torch import float32, set_float32_matmul_precision
from torch.utils.data import DataLoader

from src.Classes.Datasets.YFTrainDataset import YFTrainDataset
from src.Classes.Models.StockPredictor import OptimizedLSTMWithAttention as AdvancedStockPredictor

from Environment import *

set_float32_matmul_precision(getenv('MATMUL_PRECISION'))

# %% Clear logs
if __name__ == "__main__":
    TICKERS_ARRAY = getenv('TICKERS').split(',')
    TOTAL_PRICES_COUNT_PER_TIME_UNIT = int(getenv(
        'PRICES_PER_TICKER_COUNT')) * len(TICKERS_ARRAY)

    rmtree('lightning_logs', ignore_errors=True)

    yf_train_dataset = YFTrainDataset(
        tickers=TICKERS_ARRAY,
        max_size=int(getenv('DATA_SAMPLES')),
        future_offset_point=int(getenv('FUTURE_OFFSET_POINT')),
        history_time_range=int(getenv('HISTORY_TIME_RANGE')),
        ticker_to_predict=getenv('TICKER_TO_PREDICT'),
        price_type=getenv('PRICE_TYPE'),
        dtype=float32,
    )

    yf_train_dataloader = DataLoader(
        yf_train_dataset,
        batch_size=int(getenv('BATCH_SIZE')),
        shuffle=True,
        num_workers=int(getenv('NUM_WORKERS')),
        drop_last=True
    )

    model: AdvancedStockPredictor = AdvancedStockPredictor(
        input_dim=(
            int(len(TICKERS_ARRAY) * int(getenv('PRICES_PER_TICKER_COUNT')))
        ),
        sequence_length=int(getenv('HISTORY_TIME_RANGE')),
        hidden_dim=int(getenv('HIDDEN_DIM')),
        learning_rate=float(getenv('LEARNING_RATE')),
        batch_size=int(getenv('BATCH_SIZE')),
    ).to('cuda', dtype=float32)

    trainer = Trainer(
        max_epochs=int(getenv('NUM_EPOCHS')),
        log_every_n_steps=15,
    )

    trainer.fit(model, yf_train_dataloader)

# %% save model
