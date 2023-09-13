from torch.utils.data import DataLoader

from src.Classes.Datasets.YFTrainDataset import YFTrainDataset


class YFTrainDataLoader(DataLoader):
    def __init__(self, dataset: YFTrainDataset, batch_size: int = 1, num_workers: int = 1):
        """
        ### Yahoo Finance train dataloader

        #### Parameters
        - `dataset` : `YFTrainDataset`
            -   Dataset
        - `batch_size` : `int`
            -   Optional
            -   Batch size
            -   Default: `1`
        - `num_workers` : `int`
            -   Optional
            -   Number of workers
            -   Default: `1`
        """
        super(YFTrainDataLoader, self).__init__(
            dataset,
            batch_size=batch_size,
            shuffle=True,
            num_workers=num_workers,
            drop_last=True,
        )
