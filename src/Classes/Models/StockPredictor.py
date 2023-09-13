import torch
import torch.nn as nn
import torch.nn.functional as F
from pytorch_lightning import LightningModule as LM


class OptimizedLSTMWithAttention(LM):
    def __init__(self, input_dim=45, sequence_length=30, hidden_dim=256, batch_size=256, learning_rate=0.001):
        super(OptimizedLSTMWithAttention, self).__init__()
        self.batch_size = batch_size
        self.hidden_dim = hidden_dim
        self.learning_rate = learning_rate
        self.sequence_length = sequence_length

        # Input Layer: Normalization
        self.layer_norm = nn.LayerNorm(input_dim)

        # LSTM Layer
        self.lstm = nn.LSTM(input_dim, hidden_dim, batch_first=True)

        # Attention Layer
        self.attention = nn.MultiheadAttention(hidden_dim, num_heads=1)

        # Dense Layer
        self.fc1 = nn.Linear(hidden_dim, hidden_dim // 2)

        # Output Layer
        self.fc2 = nn.Linear(
            hidden_dim // 2 * sequence_length,
            5
        )

        # Batch Normalization
        self.batch_norm = nn.BatchNorm1d(sequence_length)

        # Dropout
        self.dropout = nn.Dropout(0.2)

    def forward(self, x):
        # Input Layer
        x = self.layer_norm(x)

        # LSTM Layer
        lstm_out, _ = self.lstm(x)
        lstm_out = self.batch_norm(lstm_out)
        lstm_out = self.dropout(lstm_out)

        # Attention Layer
        attn_output, _ = self.attention(lstm_out, lstm_out, lstm_out)

        # Dense Layer
        dense_out = F.relu(self.fc1(attn_output))

        # Flatten
        dense_out = dense_out.reshape(self.batch_size, -1)

        # Output Layer
        output = self.fc2(dense_out)

        return output

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=self.learning_rate)
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, 'min')
        return {'optimizer': optimizer, 'lr_scheduler': scheduler, 'monitor': 'train_loss'}

    def training_step(self, batch, batch_idx):
        x, y, _ = batch
        y_hat = self(x)
        loss = F.mse_loss(y_hat, y)
        prediction_error = torch.abs(y_hat - y)
        self.log_dict({
            'train_loss': loss.item(),
            'train_mae_loss': torch.mean(prediction_error).item(),
        },
            logger=True,
            on_step=True,
            on_epoch=True,
            prog_bar=True,
            sync_dist=True,
            batch_size=self.batch_size,
            enable_graph=True,
        )

        return loss
