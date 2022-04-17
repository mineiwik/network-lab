import uuid
import yaml
from .constants import CONFIG_TYPES, APPLIANCE_TYPES


class NetworkConfig:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = {}
        for config_type in CONFIG_TYPES:
            self.config[config_type] = {}

    def appliance_exists(self, name: str) -> bool:
        for appliance_type in APPLIANCE_TYPES:
            if name in self.config[appliance_type]:
                return True
        return False

    def get_device_id(self, name: str) -> str:
        for appliance_type in APPLIANCE_TYPES:
            if name in self.config[appliance_type]:
                return self.config[appliance_type][name]
        return None

    def get_device_id_in_appliance_type(self, appliance_type: str, name: str) -> str:
        if appliance_type in self.config:
            if name in self.config[appliance_type]:
                return self.config[appliance_type][name]
        return None

    def get_appliance_names(self, appliance_type: str) -> list[str]:
        if not appliance_type in self.config:
            return []
        appliance_names = []
        if len(list(self.config[appliance_type])) > 0:
            for appliance_name in self.config[appliance_type]:
                appliance_names.append(appliance_name)
        return appliance_names

    def get_appliance_names_with_ids(self, appliance_type: str) -> list[(str, str)]:
        if not appliance_type in self.config:
            return (False, "Appliance type {} does not exist".format(appliance_type))
        appliance_names = []
        if len(list(self.config[appliance_type])) > 0:
            for appliance_name, appliance_id in self.config[appliance_type].items():
                appliance_names.append((appliance_name, appliance_id))
        return appliance_names

    def add_appliance(self, appliance_type: str, name: str) -> tuple[bool, str]:
        if self.appliance_exists(name):
            return (False, "The appliance {} does already exist!".format(name))
        if not appliance_type in self.config:
            return (False, "Appliance type {} does not exist".format(appliance_type))
        self.config[appliance_type][name] = str(uuid.uuid4())
        return (True, "")

    def remove_appliance(self, appliance_type: str, name: str) -> tuple[bool, str]:
        if not self.appliance_exists(name):
            return (False, "The appliance {} does not exist!".format(name))
        if not appliance_type in self.config:
            return (False, "Appliance type {} does not exist".format(appliance_type))
        del self.config[appliance_type][name]
        return (True, "")

    def remove_link(self, name: str) -> tuple[bool, str]:
        if not name in self.config['links']:
            return (False, "The link {} does not exist!".format(name))
        del self.config['links'][name]
        return (True, "")

    def read_file(self) -> bool:
        config = {}
        with open("./configs/" + self.config_file, "r") as stream:
            try:
                config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
                return False
        for appliance_type in APPLIANCE_TYPES:
            if not appliance_type in config:
                return False
        self.config = config
        return True

    def write_file(self) -> bool:
        with open("./configs/" + self.config_file, "w") as stream:
            try:
                yaml.dump(self.config, stream)
            except yaml.YAMLError as exc:
                print(exc)
                return False
        return True
