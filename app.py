from shutil import rmtree

from pytorch_lightning import Trainer
from torch import float32, set_float32_matmul_precision
from torch.utils.data import DataLoader

from src.Classes.Datasets.YFTrainDataset import YFTrainDataset
from src.Classes.Models.StockPredictor import OptimizedLSTMWithAttention as AdvancedStockPredictor

from pytorch_lightning.callbacks import ModelCheckpoint

from Environment import *

# %% Set precision
set_float32_matmul_precision('medium')

# %% Clear logs
if __name__ == "__main__":
    rmtree('lightning_logs', ignore_errors=True)

    checkpoint_callback = ModelCheckpoint(
        dirpath='./checkpoints',
        filename='OptimizedLSTMWithAttention-{epoch:02d}-{train_loss:.2f}',
    )

    yf_train_dataset = YFTrainDataset(
        tickers=TICKERS,
        max_size=DATA_SAMPLES,
        future_offset_point=FUTURE_OFFSET_POINT,
        history_time_range=HISTORY_TIME_RANGE,
        ticker_to_predict=TICKER_TO_PREDICT,
        price_type=PRICE_TYPE,
        dtype=float32,
    )

    yf_train_dataloader = DataLoader(
        yf_train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=NUM_WORKERS,
        drop_last=True
    )

    model: AdvancedStockPredictor = AdvancedStockPredictor(
        input_dim=PRICES_PER_TICKER_COUNT*len(TICKERS),
        sequence_length=HISTORY_TIME_RANGE,
        hidden_dim=HIDDEN_DIM,
        learning_rate=LEARNING_RATE,
        batch_size=BATCH_SIZE,
    ).to('cuda', dtype=float32)

    trainer = Trainer(
        max_epochs=NUM_EPOCHS,
        log_every_n_steps=15,
        callbacks=[checkpoint_callback],
    )

    trainer.fit(model, yf_train_dataloader)

# %% save model
