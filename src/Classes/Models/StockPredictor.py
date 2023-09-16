from enum import Enum
from typing import Optional

from torch import Tensor, tensor
from torch.optim.adam import Adam
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch import \
    abs as tabs, \
    median as tmedian, \
    mul as tmul, \
    divide as tdiv, \
    pow as tpow
from torch.utils.tensorboard.writer import SummaryWriter
from pytorch_lightning import LightningModule as LM
from pytorch_lightning.loggers.tensorboard import TensorBoardLogger

from src.Classes.Modules.StockPredictorModule.StockPredictorModule import StockPredictorModule


class CurrentProcess(Enum):
    LR_FIND = 0
    TRAINING = 1


class StockPredictor(LM):
    def __init__(
        self,
        module: StockPredictorModule,
        custom_logger: TensorBoardLogger,
        learning_rate: float = 0.00
    ) -> None:
        super(StockPredictor, self).__init__()
        self.learning_rate: float = learning_rate
        self.module: StockPredictorModule = module
        self.custom_logger: TensorBoardLogger = custom_logger

        self._experiment: SummaryWriter = self.custom_logger.experiment

        self._current_process: Optional[CurrentProcess] = None

    def forward(self, x):
        return self.module(x)

    def configure_optimizers(self) -> dict:
        optimizer: Adam = Adam(
            self.parameters(),
            lr=self.learning_rate
        )
        scheduler: ReduceLROnPlateau = ReduceLROnPlateau(
            optimizer,
            'min'
        )
        return {
            'optimizer': optimizer,
            'lr_scheduler': scheduler,
            'monitor': 'train_mse_loss',
            'interval': 'step',
            'frequency': 50,
            'strict': True,
        }

    def calculate_loss(self, y_hat, y) -> list[Tensor, dict[str, Tensor]]:
        percentage_diff = tmul(
            tdiv(tabs(y_hat - y), y),
            tensor(100)
        )

        median_percentage_diff = tmedian(percentage_diff)

        min_percentage_diff = percentage_diff.min()
        max_percentage_diff = percentage_diff.max()

        max_vs_min_percentage_diff = tabs(
            max_percentage_diff - min_percentage_diff
        )

        loss = max_vs_min_percentage_diff + tpow(max_percentage_diff, 2)

        return loss, {
            "Median percentage diff": median_percentage_diff,
            "Min percentage diff": min_percentage_diff,
            "Max percentage diff": max_percentage_diff,
            "Min vs max percentage diff": max_vs_min_percentage_diff,
            "Learning rate": self.learning_rate,
        }

    def training_step(self, batch, batch_idx):
        x, y, _ = batch
        y_hat = self(x)
        y_hat_squeezed = y_hat.squeeze()

        loss, plots = self.calculate_loss(y_hat_squeezed, y)

        self.log_dict({
            "train_mse_loss": loss,
        },
            prog_bar=True,
            logger=True,
            on_step=True,
            on_epoch=True,
        )

        self._experiment.add_scalars(
            "training" if self._current_process == CurrentProcess.TRAINING else "lr_find_train",
            plots,
            global_step=self.global_step,
        )

        return loss

    def validation_step(self, batch, batch_idx):
        x, y, _ = batch
        y_hat = self(x)
        squeezed_y_hat = y_hat.squeeze()

        loss, plots = self.calculate_loss(squeezed_y_hat, y)

        self.log_dict({
            "train_mse_loss": loss,
        },
            prog_bar=True,
            logger=True,
            on_step=True,
            on_epoch=True,
        )

        self._experiment.add_scalars(
            "validation" if self._current_process == CurrentProcess.TRAINING else "lr_find_val",
            plots,
            global_step=self.global_step,
        )

        self._experiment.add_graph(self, x)

        return loss

    def set_current_process(self, current_process: CurrentProcess):
        self._current_process = current_process
