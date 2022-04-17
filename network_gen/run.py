from network_gen.utils.constants import CONFIG_TYPES
from .utils import NetworkConfig, APPLIANCE_TYPES, gen_docker_file, gen_links


def load_network(config_file: str) -> NetworkConfig:
    network = NetworkConfig(config_file)
    network.read_file()
    return network


def run(network: NetworkConfig) -> None:
    devices = {}
    links = []
    vlans = []
    for appliance_type in APPLIANCE_TYPES:
        devices[appliance_type] = [device + "__" + device_id for device,
                                   device_id in network.config[appliance_type].items()]
    for link in network.config['links'].values():
        link_config = {}
        for appliance in link['connections']:
            link_config[appliance + "__" + network.get_device_id(
                appliance)] = link['connections'][appliance]
        links.append(link_config)
    gen_docker_file(devices)
    gen_links(links)
    switch_configs = "#!/bin/bash\n"
    for switch, switch_id in network.config['switches'].items():
        ports = ""
        for link_name, link in network.config['links'].items():
            if switch in link['connections']:
                ports += " ; ovs-vsctl add-port br0 " + \
                    link['connections'][switch]
        switch_configs += 'docker exec {name} sh -c "ovs-vsctl add-br br0{ports} ; ovs-vsctl set bridge br0 stp_enable=true"\n'.format(
            name="network_lab_" + switch + "__" + switch_id, ports=ports)
    with open("05-configure-switches.sh", "w") as file:
        file.writelines(switch_configs)
    vlan_configs = "#!/bin/bash\n"
    for vlan_router, vlans in network.config['vlans'].items():
        for vlan_port, vlan_ids in vlans.items():
            for vlan_id in vlan_ids:
                vlan_configs += 'docker exec {name} sh -c "ip link add link {vlan_port} name {vlan_port}.{vlan_id} type vlan id {vlan_id}"\n'.format(
                    name="network_lab_" + vlan_router + "__" + network.get_device_id(vlan_router), vlan_port=vlan_port, vlan_id=vlan_id)
    with open("06-configure-vlans.sh", "w") as file:
        file.writelines(vlan_configs)
    host_configs = "#!/bin/bash\n"
    for host, host_id in network.config['hosts'].items():
        host_configs += 'docker exec network_lab_{host}__{host_id} sh -c "rc-service networking restart"\n'.format(
            host=host, host_id=host_id)
    with open("07-configure-hosts.sh", "w") as file:
        file.writelines(host_configs)
