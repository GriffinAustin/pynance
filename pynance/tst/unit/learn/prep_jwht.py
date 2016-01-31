"""
.. Copyright (c) 2016 Marshall Farrier
   license http://opensource.org/licenses/MIT

Preprocess data to provide clean test data.

The dataset used is the "Hitters" data used in
James, Witten, Hastie, Tibshirani, An Introduction to Statistical
Learning, 2013, pp. 251ff.

The source data is currently available at 
https://cran.r-project.org/web/packages/ISLR/index.html
"""

import csv
import os

import numpy as np
import pandas as pd

def read_src(infile):
    with open(infile, 'r') as f:
        reader = csv.reader(f)
        src_data = list(reader)
    return src_data

def convert_nonnum(src_data):
    for row in src_data:
        # League
        row[14] = (1 if row[14] == 'N' else 0)
        # Division
        row[15] = (1 if row[15] == 'W' else 0)
        # NewLeague
        row[20] = (1 if row[20] == 'N' else 0)

def get_labeledfeatures(src_data):
    df = pd.DataFrame(data=src_data[1:], dtype=np.float64)
    df.replace(r'\s*NA\s*', np.nan, regex=True, inplace=True)
    df.dropna(inplace=True)
    features = df.iloc[:, 1:-1].values
    features[:, -1] = df.iloc[:, -1].values
    labels = df.iloc[:, -2].values
    return features, labels

def save_data(features, labels, outfile):
    nrows = features.shape[0]
    nfeatcols = features.shape[1]
    alldata = np.ones((nrows, nfeatcols + 3), dtype=np.float64)
    alldata[:, 1:(nfeatcols + 1)] = features
    alldata[:, nfeatcols + 1] = labels
    np.random.seed(31)
    alldata[:, -1] = np.random.randint(2, size=nrows)
    print(alldata[:4, :])
    np.savetxt(outfile, alldata)

def prep():
    path = os.path.dirname(os.path.realpath(__file__))
    ifname = 'Hitters.csv'
    infile = os.path.join(path, ifname)
    src_data = read_src(infile)
    convert_nonnum(src_data)
    features, labels = get_labeledfeatures(src_data)
    ofname = 'hitters.data'
    outfile = os.path.join(path, ofname)
    save_data(features, labels, outfile)

if __name__ == '__main__':
    prep()
