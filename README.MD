<div class="content">

<div style="display: flex; justify-content: left; align-items: center; margin-top: 30px;">
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="MIT License"></a>
  <span style="margin: 0 4px;"></span>
  <a href="https://www.python.org/downloads/release/python-311/"><img src="https://img.shields.io/badge/Python-3.11-blue.svg" alt="Python 3.11"></a>
  <span style="margin: 0 4px;"></span>
  <a href="https://www.python.org/dev/peps/pep-0008/"><img src="https://img.shields.io/badge/Code%20Style-pep8-green.svg" alt="Pep8"></a>
  <span style="margin: 0 4px;"></span>
  <a href="https://pytorch.org/"><img src="https://img.shields.io/badge/PyTorch-🔥-orange.svg" alt="PyTorch"></a>
  <span style="margin: 0 4px;"></span>
  <a href="https://www.pytorchlightning.ai/"><img src="https://img.shields.io/badge/PyTorch%20Lightning-⚡-red.svg" alt="PyTorch Lightning"></a>
</div>

# Stock Prerdictor

<span class="error-red">This project is in it's infancy (alpha stage). It's a work in progress, approach it with caution</span><span class="error-red">...</span>

## Description
This project is a stock predictor that uses an `LSTM` neural network with `Attention` to predict future stock prices. It uses `pytorch_lightning` to train the model. The data is fetched from Yahoo Finance using the `yfinance` library.

## Installation
```bash
git clone git@github.com:patterns-complexity/stock-predictor.git
cd stock_predictor
pip install -r requirements.txt
cp env.train.dist .env.train
cp env.predict.dist .env.predict # WARNING: PREDICTION ENVIRONMENT IS NOT PROPERLY IMPLEMENTED YET!
```

## Configuration
```bash
# WARNING: PREDICTION ENVIRONMENT IS NOT PROPERLY IMPLEMENTED YET!

# Edit the .env.train file to configure the training environment
nano ./.env.train
```

<!-- ENVIRONMENT VARIABLES -->



### Yahoo Finance API parameters
| Variable | Value | Description |
| --- | --- | --- |
| TICKERS |                 `"TSLA" `                 |  Tickers passed as training data to the model |
| DATA_INTERVAL |                 `"1h" `                 |  Granularity of the data (time unit) |
| FETCH_START_DATE |                 `"2023-01-01" `                 |  Date range beginning of the data |
| FETCH_END_DATE |                 `"2023-03-01" `                 |  Date range end of the data |
| FETCH_START_DATE_VALIDATION |                 `"2023-03-02" `                 |  Date range beginning of the validation data |
| FETCH_END_DATE_VALIDATION |                 `"2023-06-02" `                 |  Date range end of the validation data |
| MAX_THREADS |                 `32 `                 |  Maximum number of threads to use for fetching the data |

### Dataset parameters
| Variable | Value | Description |
| --- | --- | --- |
| DATA_SAMPLES |                 `100000 `                 |  Number of samples to generate |
| TICKER_TO_PREDICT |                 `"TSLA" `                 |  Ticker to predict |
| PRICE_TYPE |                 `"Close" `                 |  Price type to predict |
| HISTORY_TIME_RANGE |                 `24 `                 |  Number of time units to look back into the past |
| FUTURE_OFFSET_POINT |                 `4 `                 |  Number of time units to look into the future |

### Provider-specific (default: Yahoo Finance) price parameters
| Variable | Value | Description |
| --- | --- | --- |
| PRICES_PER_TICKER_COUNT |                 `5 `                 |  Number of prices the provider returns per ticker (DO NOT CHANGE UNLESS YOU WANT TO CHANGE THE DATA PROVIDER!) |

### Data loader parameters
| Variable | Value | Description |
| --- | --- | --- |
| BATCH_SIZE |                 `256 `                 |  Batch size |
| NUM_WORKERS |                 `4 `                 |  Number of workers to load the data |

### Model parameters
| Variable | Value | Description |
| --- | --- | --- |
| USE_CUDA |                 `True `                 |  Use CUDA? (DOES NOT WORK YET!) |
| DEVICE |                 `0 `                 |  GPU device ID (DOES NOT WORK YET!) |
| HIDDEN_DIM |                 `256 `                 |  Hidden dimension of the model (NOT IMPLEMENTED YET!) |
| LEARNING_RATE |                 `0.001 `                 |  Learning rate |
| CHECKPOINT_PATH |                 `"./checkpoints" `                 |  Path to save the model checkpoints to |

### Training parameters
| Variable | Value | Description |
| --- | --- | --- |
| NUM_EPOCHS |                 `200 `                 |  Number of epochs to train the model |
| MATMUL_PRECISION |                 `"medium" `                 |  Precision of the matrix multiplication (low, medium, high) |

### Predictor's language (not implemented yet)
| Variable | Value | Description |
| --- | --- | --- |
| LANGUAGE |                 `"en" `                 |  Predictor's language (NOT IMPLEMENTED YET!) |

<!-- /ENVIRONMENT VARIABLES -->


## Usage
```bash
# WARNING: PREDICTION ENVIRONMENT IS NOT PROPERLY IMPLEMENTED YET!

# Run the main.py script in the root directory of this project
python ./main.py -e <environment> # Where <environment> is either 'train' or 'predict'

# Examples:
python ./main.py -e train # Run the program in the 'train' environment when you want to train the model.
python ./main.py -e predict # Run the program in the 'predict' environment when you want the model to make predictions.
python ./main.py # Run the program in the 'train' environment (default)
```

## Tensorboard
You can use Tensorboard to visualize the training process. It is included in the `requirements.txt` file as a dependency.

## Dependencies
```markdown
colorama==0.4.6
environs==9.5.0
pandas==2.1.0
pytorch_lightning==2.0.8
tabulate==0.9.0
torch==2.1.0.dev20230901+cu121
yfinance==0.2.28
tensorboard==2.14.0
tensorboardX==2.6.2.2
```

## License
This project is licensed under the MIT License - see the [LICENSE](https://opensource.org/licenses/MIT) file for details.

</div>