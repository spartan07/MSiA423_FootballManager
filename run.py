"""Enables the command line execution of multiple modules within src/

This module combines the argparsing of each module within src/ and enables the execution of the corresponding scripts
so that all module imports can be absolute with respect to the main project directory.

Current commands enabled:

To create a database for Tracks with an initial song:

    `python run.py create --artist="Britney Spears" --title="Radar" --album="Circus"`

To add a song to an already created database:

    `python run.py ingest --artist="Britney Spears" --title="Radar" --album="Circus"`
"""
import argparse
import logging.config
logging.config.fileConfig("config/logging/local.conf")
logger = logging.getLogger("run-whos-the-boss")

from src.load_data import pre_process


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Process the data")
    subparsers = parser.add_subparsers()

    sub_process = subparsers.add_parser('process')
    sub_process.add_argument("--path", type=str, default="./data/", help="Path for the data")
    sub_process.set_defaults(func=pre_process)

    args = parser.parse_args()
    args.func(args.path)