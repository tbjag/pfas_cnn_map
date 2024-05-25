import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point
import argparse
from generate import GenerateShape

def main():
    parser = argparse.ArgumentParser('process map data')
    parser.add_argument('-length', type=int, default=7)
    parser.add_argument('-grain', type=float, default=0.1)
    parser.add_argument('-input', type=str, default='../stanford-sr396hp9621-shapefile.zip')
    parser.add_argument('-csv', type=str, default='../pfas_clean.csv')
    parser.add_argument('-output', type=str, default='data/generate')
    parser.add_argument('-interval', type=int, default=10)
    parser.add_argument('-checkpoint', type=int, default=0)
    
    args = parser.parse_args()
    print(args)
    # TODO check number is odd

    x = GenerateShape(args.grain, args.length, args.interval, args.checkpoint, args.output)
    x.setup(args.input, args.csv)
    x.base.dropna(subset=['PFAS_total'], inplace=True)
    print(len(x.base['PFAS_total']))


if __name__ == '__main__':
    main()