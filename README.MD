<link href="https://fonts.googleapis.com/css?family=Lato" rel="stylesheet">
<style>
@keyframes ellipsis {
  0% {
    width: 0.2em;
    overflow: hidden;
    white-space: nowrap;
  }
  50% {
    width: 1em;
    overflow: hidden;
    white-space: nowrap;
  }
  100% {
    width: 1em;
    overflow: hidden;
    white-space: nowrap;
  }
}
@keyframes glow {
    0% {
        text-shadow: 0 0 2px #cb2431;
    }
    25% {
        text-shadow: 0 0 4px #cb2431;
    }
    50% {
        text-shadow: 0 0 4px #cb2431;
    }
    '75%' {
        text-shadow: 0 0 2px #cb2431;
    }
}
</style>
<style>
.ellipsis {
  overflow: hidden;
  display: inline-block;
  vertical-align: bottom;
  animation: ellipsis steps(3) 2.6s infinite;
}
.error-red {
    color: #cb2431;
    font-weight: 600;
}
.content {
    font-family: 'Lato', sans-serif;
    padding: 10px 40px;
    /* github style */
    background-color: #24292e;
    /* gray border */
    border: 1px solid #2c343b;
}
h1 {
    font-size: 1.5em;
    font-weight: 600;
    margin-top: 0.5em;
    margin-bottom: 0.5em;
    display: inline-block;
}
h2 {    
    font-size: 1.1em;
    font-weight: 600;
    margin-top: 0.5em;
    margin-bottom: 0.5em;
}
h3 {
    font-size: 1em;
    font-weight: 600;
    margin-top: 0.5em;
    margin-bottom: 0.5em;
}
/* github table */
table {
    border-collapse: collapse;
    border-spacing: 0;
    width: 100%;
}
table tr {
    border-top: 1px solid #dfe2e5;
    width: 100%;
}
table tr:nth-child(2n) {
    background-color: #1e262b;
}
table tr td:nth-child(2) {
    vertical-align: middle;
    width: 100%;
}
.note {
    color: #74808c;
}
</style>

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

<span class="error-red">work in progress</span><span class="error-red">...</span>

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

### Below is a list of all the available configuration options and their descriptions.

| Option | Description | Default Value |
| ------ | ----------- | ------------- |
| `LANGUAGE` | Program's language <span class="error-red">(not implemented yet)</span> | `en` |
| `DATA_PERIOD` | The amount of past data points to download from Yahoo Finance | `7d` |
| `DATA_INTERVAL` | Time interval between each data point <span class="note">(granularity)</span> | `1h` |
| `DATA_SAMPLES` | Number of training samples the dataset will generate <span class="note">(sampled from the downloaded data)</span> | `100000` |
| `TICKERS` | A comma-separated list of tickers to fetch data for <span class="note">(min 2)</span>. <br /> The model takes all of those tickers into consideration when training and predicting. <br /> **Always predict with the same value you trained the model on!** | <span class="note">N/A</span> |
| `TICKER_TO_PREDICT` | Ticker to predict <span class="note">(must be in the `TICKERS` list)</span> <br /> **Currently it has to be set to the same value between training and predicting, but this is intended to change!** | <span class="note">N/A</span> |
| `PRICE_TYPE` | Type of price to predict <span class="note">(Open, High, Low, Close)</span> | `Close` |
| `HISTORY_TIME_RANGE` | Number of time units to look back into the past | `24` |
| `FUTURE_OFFSET_POINT` | Number of time units into the future to predict for. <span class="note">(NOT A RANGE! It's a single point in time!)</span> | `8` |
| `PRICES_PER_TICKER_COUNT` | **DO NOT CHANGE** <br />UNLESS YOU ARE USING A DIFFERENT DATA PROVIDER!<br /> Number of prices to fetch per ticker <span class="note">(used to calculate the number of features)</span> | `5` |
| `BATCH_SIZE` | Batch size for training | `256` |
| `NUM_WORKERS` | Number of workers for the DataLoader (basically the number of threads to use for data loading) | `4` |
| `NUM_EPOCHS` | Number of epochs to train for | `100` |
| `HIDDEN_DIM` | Hidden dimension of LSTM layers and all additional layers connected to them | `256` |
| `LEARNING_RATE` | My IQ <span class="note">(jk, it's the learning rate, duh)</span> | `0.001` |

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


## Dependencies
```markdown
environs==9.5.0
pandas==2.1.0
pytorch_lightning==2.0.8
torch==2.1.0.dev20230901+cu121
yfinance==0.2.28
```

## License
This project is licensed under the MIT License - see the [LICENSE](https://opensource.org/licenses/MIT) file for details.

</div>