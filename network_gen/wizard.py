import os
from network_gen.utils.constants import APPLIANCE_TYPES
from .utils import *
from .run import run


def clear() -> None:
    """
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')
    """


def display_cmds(cmds: dict) -> None:
    print("What would you like to do?")
    for cmd, desc in cmds.items():
        print("{cmd}: {desc}".format(cmd=cmd, desc=desc))


def display_welcome_text(menu: str, cmd: str = None, error: str = None, output: str = None) -> None:
    clear()
    print("Welcome to the {} menu!".format(menu))
    if cmd:
        display_cmds(cmd)
    if error:
        print(error)
    if output:
        print(output)


def list_appliances(network: NetworkConfig, appliance_type: str) -> str:
    if len(network.config[appliance_type]) == 0:
        return "No elements to display"
    appliances = ""
    for appliance in network.get_appliance_names(appliance_type):
        appliances += appliance + ", "
    return appliances[:-2]


def list_all_appliances(network: NetworkConfig) -> str:
    appliances = ""
    for appliance_type in APPLIANCE_TYPES:
        appliances += appliance_type + ": "
        appliances += list_appliances(network, appliance_type)
        appliances += "\n"
    return appliances[:-1]


def wait_for_valid_command(menu: str, cmd: str = None) -> str:
    user_input = input()
    while len(user_input) == 0 or user_input not in cmd:
        display_welcome_text(menu, cmd, "Unknown command! Please try again")
        user_input = input()
    return user_input


def wait_for_valid_new_name(network: NetworkConfig, menu: str, cmd: str) -> str:
    print("Specify a name for the new {}".format(menu))
    user_input = input()
    while len(user_input) == 0 or network.appliance_exists(user_input):
        display_welcome_text(
            menu, cmd, "Name is already in use! Please try again")
        user_input = input()
    if user_input == 'q':
        return None
    return user_input


def wait_for_valid_existing_name(network: NetworkConfig, menu: str, target: str) -> str:
    print("Select an existing appliance name for the {target} of the new {menu}".format(
        target=target, menu=menu))
    print("Available appliances")
    print(list_all_appliances(network))
    name = input()
    while not network.appliance_exists(name):
        print("This appliance does not exist please try again!")
        name = input()
    return name


def new_config() -> NetworkConfig:
    clear()
    print("Creating new config")
    print("Please enter the name for the new configuration:")
    config_file = input()
    while os.path.isfile("./configs/" + config_file + ".yaml"):
        print("This config already exists, please enter another name:")
        config_file = input()
    print("Creating " + config_file)
    network = NetworkConfig(config_file + ".yaml")
    return network


def load_config() -> NetworkConfig:
    clear()
    print("Which config file would you like to load?")
    i = 0
    files = []
    for file in os.listdir("./configs"):
        if file.endswith(".yaml"):
            files.append(file.rsplit(".", 1)[0])
            print(str(i) + ": " + file.rsplit(".", 1)[0])
            i += 1
    print("Choose a number")
    config_file = input()
    while not config_file.isnumeric() or int(config_file) < 0 or int(config_file) >= len(files):
        if config_file == "q":
            return None
        print("This config does not exist! Please try again")
        config_file = input()
    print("Loading " + files[int(config_file)])
    network = NetworkConfig(files[int(config_file)] + ".yaml")
    network.read_file()
    return network


def appliance_menu(network: NetworkConfig, menu: str, appliance_type: str, output: str = None) -> tuple[bool, str]:
    display_welcome_text(menu=menu, cmd=APPLIANCE_MENU, output=output)
    cmd = wait_for_valid_command(menu, APPLIANCE_MENU)
    output = None
    if cmd == "l":
        output = list_appliances(network, appliance_type)
    elif cmd == "n":
        appliance_name = wait_for_valid_new_name(
            network, menu, APPLIANCE_MENU)
        if appliance_name == None:
            return (True, None)
        network.add_appliance(
            appliance_type=appliance_type, name=appliance_name)
    elif cmd == "d":
        print("Specify the {} name you would like to delete".format(menu))
        appliance_name = input()
        while len(appliance_name) == 0 or appliance_name not in network.config[appliance_type]:
            print("This {} name is unknown! Please try again!".format(menu))
            appliance_name = input()
        network.remove_appliance(
            appliance_type=appliance_type, name=appliance_name)
    elif cmd == "q":
        return (False, None)
    return (True, output)


def link_menu(network: NetworkConfig, output: str = None) -> tuple[bool, str]:
    display_welcome_text(menu="link", cmd=LINK_MENU, output=output)
    cmd = wait_for_valid_command(menu="link", cmd=LINK_MENU)
    output = None
    if cmd == "l":
        output = list_appliances(network, appliance_type="links")
    elif cmd == "n":
        link_src = wait_for_valid_existing_name(
            network, menu="link",  target="source")
        link_dst = wait_for_valid_existing_name(
            network, menu="link",  target="destination")
        while link_src == link_dst:
            print("Source and destination cannot be the same appliance!")
            link_dst = wait_for_valid_existing_name(
                network, menu="link",  target="destination")
        if (link_src + "_" + link_dst in network.config['links'] or link_dst + "_" + link_src in network.config['links']):
            return (True, "This link already exists! Please try again!")
        network.config['links'][link_src + "_" + link_dst] = {'type': 'veth', 'connections': {
            link_src: 'port_'+link_dst, link_dst: 'port_'+link_src}}
    elif cmd == "d":
        if len(network.config['links']) <= 0:
            print("You have no links to delete!")
        else:
            print("The following link(s) exist(s), which one would you like to delete?")
            print(list_appliances(network, appliance_type="links"))
            answer = input()
            while answer not in network.config['links']:
                print("This link does not exist! Please try again!")
                answer = input()
            res = network.remove_link(name=answer)
            if not res[0]:
                print(res[1])
    elif cmd == "q":
        return (False, None)
    return (True, output)


def config_menu(network: NetworkConfig) -> bool:
    display_welcome_text(menu="configuration", cmd=CONFIG_MENU)
    cmd = wait_for_valid_command(menu="configuration", cmd=CONFIG_MENU)
    output = None
    stay = True
    if cmd == "r":
        while stay:
            stay, output = appliance_menu(network, "router", "routers", output)
    elif cmd == "s":
        while stay:
            stay, output = appliance_menu(
                network, "switch", "switches", output)
    elif cmd == "h":
        while stay:
            stay, output = appliance_menu(network, "host", "hosts", output)
    elif cmd == "l":
        while stay:
            stay, output = link_menu(network, output)
    elif cmd == "w":
        if network.write_file():
            print("File was written successfully!")
        else:
            print("There was an error writitng this file")
    elif cmd == "q":
        return False
    return True


def start_wizard():
    print("#################################")
    print("# Network-Lab Configurator 2000 #")
    print("#         Version: 0.1          #")
    print("#    Type q to exit any menu    #")
    print("#################################")
    display_cmds(ENTRY_MENU)
    cmd = input()
    if len(cmd) == 0:
        print("No command specified")
    elif cmd[0] == "n":
        network = new_config()
        while config_menu(network):
            pass
    elif cmd[0] == "e":
        network = load_config()
        if not network:
            exit()
        while config_menu(network):
            pass
    elif cmd[0] == "r":
        network = load_config()
        if not network:
            exit()
        run(network)
