<link href="https://fonts.googleapis.com/css?family=Lato" rel="stylesheet">

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

### Yahoo Finance API parameters
| Option | Description | Default Value |
| ------ | ----------- | ------------- |
| `TICKERS` | A comma-separated list of tickers to fetch data for <span class="note">(min 2)</span>. <br /> The model takes all of those tickers into consideration when training and predicting. <br /> **Always predict with the same value you trained the model on!** | <span class="note">N/A</span> |
| `DATA_INTERVAL` | The granularity of the data fetched from Yahoo Finance. Later referenced as a `time unit` | `1h` |
| `FETCH_START_DATE` | The beginning date of the time span the model will be basing its predictions on. | `2022-01-01` |
| `FETCH_END_DATE` | The end date of the time span the model will be basing its predictions on. | `2022-01-07` |
| `MAX_THREADS` | Maximum number of threads to use for data fetching. <span class="note">(used by the `yfinance` library)</span> | `1` |

### Dataset parameters
| Option | Description | Default Value |
| ------ | ----------- | ------------- |
| `DATA_SAMPLES` | Number of training samples the dataset will generate <span class="note">(sampled from the downloaded data)</span> | `100000` |
| `TICKER_TO_PREDICT` | Ticker to predict <span class="note">(must be in the `TICKERS` list)</span> <br /> **Currently it has to be set to the same value between training and predicting, but this is intended to change!** | <span class="note">N/A</span> |
| `PRICE_TYPE` | Type of price to predict <span class="note">(`Open`, `High`, `Low`, `Close`)</span> | `Close` |
| `HISTORY_TIME_RANGE` | Number of time units to look back into the past during training | `24` |
| `FUTURE_OFFSET_POINT` | Number of time units into the future to predict for. <br /> <span class="note">**NOT A RANGE! It's a single point in time!**</span> | `8` |

### Provider-specific (default: Yahoo Finance) price parameters
| Option | Description | Default Value |
| ------ | ----------- | ------------- |
| `PRICES_PER_TICKER_COUNT` | **DO NOT CHANGE** <br />UNLESS YOU ARE USING A DIFFERENT DATA PROVIDER!<br /> Number of prices to fetch per ticker <span class="note">(used to calculate the number of features)</span> | `5` |

### Data loader parameters
| Option | Description | Default Value |
| ------ | ----------- | ------------- |
| `BATCH_SIZE` | Batch size for training | `256` |
| `NUM_WORKERS` | Number of workers for the DataLoader (basically the number of threads to use for data loading) | `4` |

### Model parameters
| Option | Description | Default Value |
| ------ | ----------- | ------------- |
| `USE_CUDA` | Whether to use `CUDA` or not. <br /> <span class="note">**This does not change anything yet. Pytorch Lightning should pick the best device by default for now. If you prefer to use a different device please modify the value in code for now. This is intended to change!**</span> | `True` |
| `DEVICE` | If `CUDA` is enabled, this is the `GPU` index that will be used. <br /> <span class="note">**This does not change anything yet. Pytorch Lightning should pick the best device by default for now. If you prefer to use a different device please modify the value in code for now. This is intended to change!**</span> | `0` |
| `HIDDEN_DIM` | Hidden dimension of LSTM layers and all additional layers connected to them | `256` |
| `LEARNING_RATE` | My IQ <span class="note">(jk, it's the learning rate, duh)</span> | `0.001` |

### Training parameters
| Option | Description | Default Value |
| ------ | ----------- | ------------- |
| `NUM_EPOCHS` | Number of epochs to train for | `200` |
| `MATMUL_PRECISION` | Precision of the matrix multiplication used in the attention layer. <br /> **Read up on it in the PyTorch documentation if you encounter any problems with it.** | `medium` |

### Logging parameters
| Option | Description | Default Value |
| ------ | ----------- | ------------- |
| `LANGUAGE` | Program's language. <br /> **Not implemented yet.** | `en` |

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