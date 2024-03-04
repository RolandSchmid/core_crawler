import configparser
import os
from datetime import datetime
from pathlib import Path

# Main
default_name: str = 'buhurt_crawler'

# Paths
dir_root: Path = Path('..')
default_dir_out: Path = Path(dir_root, 'out')

# Files
default_file_json: Path = Path(default_dir_out, '{ts}-weapons.json')
default_file_xlsx: Path = Path(default_dir_out, '{ts}-weapons.xlsx')
file_ini: Path = Path(dir_root, 'config.ini')

# Json settings
default_json_indent: str | None = None

# Init timestamp
timestamp: str = datetime.now().strftime("%Y%m%d-%H%M%S")

# Init config
config: configparser.ConfigParser = configparser.ConfigParser()
config.read(file_ini)


class BaseConfig:

    @classmethod
    def get_name(cls) -> str:
        return cls.get_config_str('main', 'name', default_name)

    @classmethod
    def get_dir_out(cls) -> str:
        return cls.get_path_timestamp('paths', 'dir_out', default_dir_out, False)

    @classmethod
    def get_json_indent(cls) -> int or None:
        return cls.__get_config_int_or_none('json', 'indent', default_json_indent)

    @classmethod
    def get_config_str(cls, section: str, option: str, default: str) -> str:
        cls.__create_if_not_exists(section, option, default)
        return config[section].get(option, default)

    @classmethod
    def get_config_int(cls, section: str, option: str, default: int) -> int:
        cls.__create_if_not_exists(section, option, str(default))
        return config[section].getint(option, default)

    @classmethod
    def get_path_timestamp(cls, section: str, option: str, default: Path, is_file: bool) -> str:
        path: str = cls.get_config_str(section, option, str(default))
        path = path.replace('{ts}', timestamp)
        cls.__create_folder_structure(path, is_file)
        return path

    @classmethod
    def __get_config_int_or_none(cls, section: str, option: str, default: int | None) -> int | None:
        cls.__create_if_not_exists(section, option, str(default))
        result: str = config[section].get(option, default)
        if result == 'None':
            return None
        return int(result)

    @classmethod
    def __get_config_bool(cls, section, option, default) -> bool:
        cls.__create_if_not_exists(section, option, default)
        return config[section].getboolean(option, default)

    @classmethod
    def __create_if_not_exists(cls, section: str, option: str, default: str) -> None:
        if not config.has_section(section) or not config.has_option(section, option):
            if not config.has_section(section):
                config[section] = {option: default}
            if not config.has_option(section, option):
                config[section][option] = default
        with open(file_ini, 'w') as configfile:
            config.write(configfile)

    @classmethod
    def __create_folder_structure(cls, path: str, is_file: bool) -> None:
        if is_file:
            path: str = os.path.dirname(path)
        if not os.path.exists(path):
            os.makedirs(path)
