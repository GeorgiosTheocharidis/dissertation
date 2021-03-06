"""Exposes a scaler class to use for data normalization.

See also:
https://scikit-learn.org/stable/auto_examples/preprocessing/plot_all_scaling.html
"""

import pandas as pd
import sklearn.preprocessing as pp


class Scaler:
    """Hides the details of a MinMaxScaler transformer."""

    _scaler = None

    _SCALERS = {
        'MinMaxScaler': pp.MinMaxScaler,
        'MaxAbsScaler': pp.MaxAbsScaler,
        'StandardScaler': pp.StandardScaler,
        'RobustScaler': pp.RobustScaler,
        'Normalizer': pp.Normalizer,
        'QuantileTransformer': pp.QuantileTransformer,
        'PowerTransformer': pp.PowerTransformer
    }

    def __init__(self, data, scaler='MinMaxScaler'):
        """Initializer.

        :param DataFrame data: The data to use for fitting.
        """
        assert scaler in self._SCALERS
        assert isinstance(data, pd.DataFrame)
        data = data.copy()
        self._scaler = self._SCALERS[scaler]().fit(data)

    def scale(self, data):
        """Scales the passed-in data.

        :param pd.DataFrame data: The data to scale.

        :return: A scaled DataFrame.
        """
        data = data.copy()
        return pd.DataFrame(self._scaler.transform(data))

    def inverse(self, data):
        """Inverses the passed-in data.

        :param DataFrame data: The data to inverse scaling.

        :return: A scaled DataFrame.
        """
        data = data.copy()
        return pd.DataFrame(self._scaler.inverse_transform(data))
