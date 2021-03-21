#!/usr/bin/env python3

__author__ = 'Hedius'
__version__ = '1.1.0'
__license__ = 'GPLv3'
__copyright__ = 'Copyright 2020 Hedius'

#  Copyright (C) 2020. Hedius gitlab.com/hedius
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
from pathlib import Path
from argparse import ArgumentParser
from dynaconf import Dynaconf, Validator, ValidationError

from BF4StatusBot import BF4StatusBot


def main():
    logging.basicConfig(level=logging.INFO)

    parser = ArgumentParser(description='Discord bot for showing the status '
                                        'of BF4 servers.')
    parser.add_argument('-c', '--config-folder',
                        dest='config_folder',
                        default='config',
                        help='Path to config folder.\nThe folder should '
                             'contain the default.toml and user.toml.\n'
                             'This option is optional.\nIt\'s also possible to'
                             ' configure the bot with environment variables.')

    args = parser.parse_args()

    if not Path(args.config_folder).exists():
        logging.warning(
            f'Config folder "{args.config_folder}" does not exist! '
            'You must configure the bot with environment variables!')

    settings = Dynaconf(
        settings_files=[f'{args.config_folder}/default.toml',
                        f'{args.config_folder}/user.toml'],
        envvar_prefix='BF4STATUSBOT',
        environments=['BF4StatusBot'],
        env='BF4StatusBot',
        default_env='BF4StatusBot'
    )

    try:
        settings.validators.register(Validator('BOT_TOKEN', must_exist=True))
        settings.validators.register(Validator('INTERVAL_PRESENCE_CHANGE',
                                               must_exist=True, lte=120,
                                               gte=4))
        settings.validators.register(
            Validator('INTERVAL_DATA_FETCH', must_exist=True, gte=15))
        settings.validators.register(
            Validator('CHECK_MAP', must_exist=True))
        settings.validators.register(
            Validator('SERVER_GUID', must_exist=True))
        settings.validators.validate()
    except ValidationError as e:
        logging.critical(f'Invalid config! {e}')
        exit(2)

    logging.debug('Starting the bot.')
    BF4StatusBot(settings).run(settings.BOT_TOKEN)


if __name__ == '__main__':
    main()