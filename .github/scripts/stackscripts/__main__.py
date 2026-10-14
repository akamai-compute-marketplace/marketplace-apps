import argparse
import logging
import sys

from stackscripts.commands import BaseCommand, UpdateCommand, ValidateCommand
from stackscripts.config import Config


COMMANDS: list[type[BaseCommand]] = [ValidateCommand, UpdateCommand]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="python -m stackscripts")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command_class in COMMANDS:
        subparser = subparsers.add_parser(command_class.name, help=command_class.help)
        command_class.add_arguments(subparser)
        subparser.set_defaults(command_class=command_class)

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    config = Config.from_env()
    command = args.command_class.from_args(config, args)
    return command.run()


if __name__ == "__main__":
    sys.exit(main())
