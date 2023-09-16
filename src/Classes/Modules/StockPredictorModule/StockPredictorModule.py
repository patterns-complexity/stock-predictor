from torch import Tensor
from torch.nn import Module
from torch.nn import Sequential, Linear, Dropout, BatchNorm1d, LSTM, LeakyReLU


class StockPredictorModuleParams:
    def __init__(self, total_prices_per_time_unit: int, sequence_length: int, batch_size: int) -> None:
        self.total_prices_per_time_unit: int = total_prices_per_time_unit
        self.sequence_length: int = sequence_length
        self.batch_size: int = batch_size


class LSTMBlock(Module):
    def __init__(self, params: StockPredictorModuleParams) -> None:
        super(LSTMBlock, self).__init__()
        self.params: StockPredictorModuleParams = params
        self.lstm = LSTM(
            input_size=self.params.total_prices_per_time_unit,
            hidden_size=512,
            num_layers=1,
            batch_first=True,
            bidirectional=True
        )

    def forward(self, x: Tensor) -> Tensor:
        x = x.view(
            -1,
            self.params.sequence_length,
            self.params.total_prices_per_time_unit
        )
        x, _ = self.lstm(x)
        # Flatten the output for the subsequent linear layer
        x = x.contiguous().view(x.size(0), -1)
        return x


class StockPredictorModule(Module):
    def __init__(self, params: StockPredictorModuleParams) -> None:
        super(StockPredictorModule, self).__init__()
        self.params: StockPredictorModuleParams = params

        self.input = Sequential(
            LSTMBlock(self.params),
            # Input size is sequence_length * hidden_size * 2 (bidirectional)
            Linear(self.params.sequence_length * 512 * 2, 256),
            LeakyReLU(),
            BatchNorm1d(256),
            Dropout(0.1),

            Linear(256, 128),
            LeakyReLU(),
            BatchNorm1d(128),
            Dropout(0.1),

            Linear(128, 64),
            LeakyReLU(),
            BatchNorm1d(64),
            Dropout(0.1),

            Linear(64, 1)
        )

    def forward(self, x: Tensor) -> Tensor:
        x = self.input(x)
        return x
