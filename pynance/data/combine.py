"""
Functions for generating feature sets from equity data.

Copyright (c) 2014 Marshall Farrier
license http://opensource.org/licenses/MIT
"""

import pandas as pd

from . import feat

def labeledfeatures(eqdata, featurefunc, labelfunc):
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

    featurefunc : function
        Function for deriving features from `eqdata`. `featurefunc` must
        take a dataframe as sole argument.

        Parameters:

        -   df : DataFrame
            Data from which to construct features.

        Returns:

        -   features : DataFrame
            The desired set of features.
        -   skipatstart : int
            The row number of the first feature returned, measured by
            the index of `df`. This is used to synchronize the indices of
            labels with those of features.

    labelfunc : function
        function for deriving labels from `eqdata`. `labelfunc` must
        take a single argument: `df`, a dataframe to which `labelfunc` will be applied.
        `labelfunc` should return a dataframe of labels followed by an int
        specifying the number of feature rows to skip at the end of the feature
        dataframe. For example, if features are relative prices 64 days out,
        these features will only be known up until 64 days before the data
        runs out. In order to properly align features and labels, the features
        should not include the last 64 rows that would otherwise be possible.

        Usage:
        `labels, skipatend = labelfunc(eqdata)`

    Returns
    --
    out : tuple (DataFrame, DataFrame)
        features and labels derived from the given parameters.
    """
    _labels, _skipatend = labelfunc(eqdata)
    _features, _skipatstart = featurefunc(eqdata)
    _size = len(_features.index)
    return _features.iloc[:(_size - _skipatend), :], _labels.iloc[_skipatstart:, :]
