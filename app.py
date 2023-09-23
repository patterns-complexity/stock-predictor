# %% Imports
from os import getenv
from shutil import rmtree

from pytorch_lightning import Trainer
from pytorch_lightning.tuner.tuning import Tuner
from pytorch_lightning.callbacks import ModelCheckpoint as ModelCallback
from pytorch_lightning.loggers.tensorboard import TensorBoardLogger

from torch import float32, set_float32_matmul_precision
from torch.utils.data import DataLoader

from src.Classes.Datasets.YFValidationDataset import YFValidationDataset
from src.Classes.Datasets.YFTrainDataset import YFTrainDataset
from src.Classes.Models.StockPredictor import CurrentProcess, StockPredictor
from src.Classes.Modules.StockPredictorModule.StockPredictorModule import StockPredictorModuleParams, StockPredictorModule

from Environment import *

set_float32_matmul_precision(getenv('MATMUL_PRECISION'))

# %% Main
if __name__ == "__main__":
    TICKERS_ARRAY = getenv('TICKERS').split(',')
    TOTAL_PRICES_COUNT_PER_TIME_UNIT = int(getenv(
        'PRICES_PER_TICKER_COUNT')) * len(TICKERS_ARRAY)

    # %% Clear logs
    rmtree('lightning_logs', ignore_errors=True)

    # %% Set up the training dataset
    yf_train_dataset = YFTrainDataset(
        tickers=TICKERS_ARRAY,
        max_size=int(getenv('DATA_SAMPLES')),
        future_offset_point=int(getenv('FUTURE_OFFSET_POINT')),
        history_time_range=int(getenv('HISTORY_TIME_RANGE')),
        ticker_to_predict=getenv('TICKER_TO_PREDICT'),
        price_type=getenv('PRICE_TYPE'),
        dtype=float32,
    )

    # %% Set up the validation dataset
    yf_validation_dataset = YFValidationDataset(
        tickers=TICKERS_ARRAY,
        max_size=int(getenv('DATA_SAMPLES')),
        future_offset_point=int(getenv('FUTURE_OFFSET_POINT')),
        history_time_range=int(getenv('HISTORY_TIME_RANGE')),
        ticker_to_predict=getenv('TICKER_TO_PREDICT'),
        price_type=getenv('PRICE_TYPE'),
        dtype=float32,
    )

    # %% Set up the training and data loader
    yf_train_dataloader = DataLoader(
        yf_train_dataset,
        batch_size=int(getenv('BATCH_SIZE')),
        shuffle=True,
        num_workers=int(getenv('NUM_WORKERS')),
        drop_last=True
    )

    # %% Set up the validation data loader
    yf_validation_dataloader = DataLoader(
        yf_validation_dataset,
        batch_size=int(getenv('BATCH_SIZE')),
        shuffle=False,
        num_workers=int(getenv('NUM_WORKERS')),
        drop_last=True
    )

    # %% Set up checkpointing
    checkpoint_callback = ModelCallback(
        monitor='train_mse_loss',
        dirpath=getenv('CHECKPOINT_PATH'),
        filename='stock-predictor-{epoch:02d}-{val_loss:.2f}',
        save_top_k=3,
        mode='min',
    )

    # %% Set up logging
    logger = TensorBoardLogger(
        'lightning_logs',
        name='StockPredictor',
        version='0.0.1',
        log_graph=True,
    )

    # %% Set up parameters
    params: StockPredictorModuleParams = StockPredictorModuleParams(
        total_prices_per_time_unit=TOTAL_PRICES_COUNT_PER_TIME_UNIT,
        sequence_length=int(getenv('HISTORY_TIME_RANGE')),
        batch_size=int(getenv('BATCH_SIZE')),
    )

    # %% Set up the module
    module: StockPredictorModule = StockPredictorModule(
        params=params
    )

    # %% Set up the model
    model: StockPredictor = StockPredictor(
        module=module,
        custom_logger=logger,
        learning_rate=float(getenv('LEARNING_RATE')),
    ).to('cuda', dtype=float32)

    # %% Set up the trainer
    trainer = Trainer(
        max_epochs=int(getenv('NUM_EPOCHS')),
        log_every_n_steps=15,
        val_check_interval=0.5,
        check_val_every_n_epoch=1,
        enable_checkpointing=True,
        callbacks=[checkpoint_callback],
    )

    # %% Set up the tuner
    tuner = Tuner(
        trainer=trainer
    )

    # %% Find the learning rate
    # model.set_current_process(CurrentProcess.LR_FIND)
    # tuner.lr_find(
    #     model=model,
    #     train_dataloaders=yf_train_dataloader,
    #     val_dataloaders=yf_validation_dataloader,
    #     min_lr=1e-6,
    #     max_lr=1e-1,
    #     num_training=100,
    #     update_attr=True,
    #     attr_name='learning_rate',
    # )
    # model.set_current_process(CurrentProcess.TRAINING)

    # %% Train the model
    trainer.fit(
        model,
        yf_train_dataloader,
        yf_validation_dataloader
    )

    # %% save model

# %%
