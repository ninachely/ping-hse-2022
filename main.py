from connector import *
from data import SessionConfig, read_session_config
import argparse
import logging as log
from pathlib import Path
from processor import MasterDataProcessor
from session import Session


def main():
    log.basicConfig(format='[%(levelname)s %(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
                        level=log.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('config', type=Path)
    args = parser.parse_args()

    config = read_session_config(args.config)
    data_processor = MasterDataProcessor(config)
    session = Session(config, data_processor)

    try:
        session.run()
    finally:
        data_processor.on_terminate()

if __name__ == "__main__":
    main()
