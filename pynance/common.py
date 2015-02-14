"""
Functions needed by multiple submodules.

Copyright (c) 2014 Marshall Farrier
license http://opensource.org/licenses/MIT
"""

import pandas as pd

def featurize(equity_data, n_sessions, **kwargs):
    """
    featurize(equity_data, n_sessions, **kwargs)

    Generate a raw (unnormalized) feature set from the input data.
    The value at `column` on the given date is taken
    as a feature, and each row contains values for n_sessions

    Parameters
    ---
    equity_data : DataFrame
        data from which to generate features

    n_sessions : int
        number of sessions to use as features

    selection : str, default: 'Adj Close'
        column of `equity_data` from which to generate features.

    columns : list, default: map(str, range((-n_sessions + 1), 1))
        column names for output DataFrame. Default will look like:
        ['-5', '-4', '-3', '-2', '-1', '0']

    Returns
    --
    out : DataFrame
        Each row is a sequence of `n_sessions` session values where
        the last column matches the value on the date specified by
        the DataFrame index.

    Benchmarking
    ---
    >>> s = 'from __main__ import data\nimport datetime as dt\n'
    >>> timeit.timeit('data.featurize(data.get("ge", dt.date(1960, 1, 1), 
            dt.date(2014, 12, 31)), 256)', setup=s, number=1)
    1.6771750450134277
    """
    columns = kwargs.get('columns', map(str, range(-n_sessions + 1, 1)))
    selection = kwargs.get('selection', 'Adj Close')
    # empty DataFrame with desired index and column labels
    features = pd.DataFrame(index=equity_data.index[(n_sessions - 1):],
            columns=columns, dtype='float64')
    values = equity_data[selection].values
    for i in range(n_sessions - 1):
        features.iloc[:, i] = values[i:(-n_sessions + i + 1)]
    features.iloc[:, n_sessions - 1] = values[(n_sessions - 1):]
    return features

def decorate(fn, *args, **kwargs):
    """
    Return a new function that replicates the behavior of the input
    but also returns an additional value. Used for creating functions
    of the proper type to pass to `labeledfeatures()`.

    Parameters
    --
    fn : function

    *args : any
        Additional parameters that the returned function will return

    **kwargs : dict
        Each element in `kwargs` will become an attribute of the output
        function.

    Returns
    --
    wrapped : function
        New function that acts like `fn` except that it also returns
        an additional value.

    Examples
    --
    from functools import partial
    forecast_interval = 32
    features, labels = pn.data.labeledfeatures(eqdata, 256, featurefn
            decorate(partial(pn.data.lab.growth, forecast_interval, 'Adj Close'), forecast_interval))

    def f():
        return 0, 1 

    >>> pn.decorate(f, 3, 4, 5)()
    (0, 1, 3, 4, 5)
    >>> pn.decorate(lambda x: x * .5, 3, 4, 5)(1.)
    (1., 3, 4, 5)
    >>> pn.decorate(lambda x: x, 1 2)('foo')
    ('foo', 1, 2)
    >>> pn.decorate(f, 'foo'):
    (0, 1, 'foo')
    pn.decorate(f, 0, foo='bar').foo
    >>> 'bar'

    Notes
    --
    If `fn()` returns multiple values, these will be returned in sequence
    as the first values returned by `add_rets(fn, arg0, arg1, arg2)`. See example
    above.
    """
    def _wrapper(*_args, **kwargs):
        _ret = fn(*_args, **kwargs)
        if isinstance(_ret, tuple):
            return _ret + args
        return (_ret,) + args
    for key, value in kwargs.items():
        _wrapper.__dict__[key] = value
    return _wrapper
