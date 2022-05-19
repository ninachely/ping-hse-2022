from sqlite3 import connect
from connector import *
from data import read_main_config, read_master_config
import argparse
import logging as log

from processor import DataProcessor


def main():
    log.basicConfig(format='[%(levelname)s %(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
                        level=log.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('config', type=Path)
    args = parser.parse_args()

    config = read_main_config(args.config)
    data_processor = DataProcessor(config)
    session = Session(config)

    try:
        session.run()
    finally:
        data_processor.on_terminate()