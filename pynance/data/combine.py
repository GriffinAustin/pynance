"""
Functions for generating feature sets from equity data.

Copyright (c) 2014 Marshall Farrier
license http://opensource.org/licenses/MIT
"""

import pandas as pd

from . import feat

def labeledfeatures(eqdata, n_sessions, labelfunc, **kwargs):
    """
    Return features and labels for the given equity data.

    Each row of the features returned contains `2 * n_sessions + 1` columns
    (or 1 less if the constant feature is excluded). After the constant feature,
    if present, there will be `n_sessions` columns derived from daily growth
    of the given price column, which defaults to 'Adj Close'. There will then
    follow another `n_sessions` columns representing current volume as
    a multiple of average volume over the previous 252 (or other value determined
    by the user) sessions. 
    
    The returned features are not centered or normalized because these
    adjustments need to be made after test or cross-validation data has
    been removed.

    The constant feature is prepended by default.

    The labels are derived from `eqdata` using `labelfunc`.

    Parameters
    --
    eqdata : DataFrame
        Expected is a dataframe as return by the `get()` function. A column
        labeled 'Volume' must be present.

    n_sessions : int
        number of sessions to use as features. This is the number
        of growth and relative volume datapoints to be used in each
        row of features

    labelfunc : function
        function for deriving labels from `eqdata`. `labelfunc` must
        take a single arguments: `df`, a dataframe to which `labelfunc` will be applied.
        `labelfunc` should return a dataframe of labels followed by an int
        specifying the number of feature rows to skip at the end of the feature
        dataframe. For example, if features are relative prices 64 days out,
        these features will only be known up until 64 days before the data
        runs out. In order to properly align features and labels, the features
        should not include the last 64 rows that would otherwise be possible.

        Usage:
        `labels, skipatend = labelfunc(eqdata)`

    pricecol : str, optional
        Column to use for price. Defaults to 'Adj Close'

    averaging_interval : int, optional
        Interval to use for generating the average volume, relative
        to which current volume will be expressed. Defaults to 252
        (1 year of sessions)

    constfeat : bool
        If true, returned dataframe will include as first column
        the constant feature 1. Defaults to True.

    Returns
    --
    out : tuple (DataFrame, DataFrame)
        features and labels derived from the given parameters.
    """
    pricecol = kwargs.get('pricecol', 'Adj Close')
    averaging_interval = kwargs.get('averaging_interval', 252)
    labels, skipatend = labelfunc(eqdata)
    growth = feat.growth(eqdata, selection=pricecol, 
            skipstartrows=(averaging_interval - 1), skipendrows=skipatend)
    volume = feat.ratio_to_ave(eqdata, averaging_interval, skipendrows=skipatend)
    features = feat._featurize_growth_vol(growth, volume, n_sessions)
    if kwargs.get('constfeat', True):
        features = feat.add_const(features)
    return features, labels.iloc[(n_sessions + averaging_interval - 1):, :]
