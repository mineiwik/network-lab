DOCKER_COMPOSE_TEMPLATE = \
    "version: '3'\n\n"\
    "services:\n"\
    "{services}"\
    "volumes:\n"\
    "{volumes}"

SERVICE_ROUTER_TEMPLATE = \
    "  {name}:\n"\
    "    image: frrouting/frr:{version}\n"\
    "    hostname: {hostname}\n"\
    "    container_name: network_lab_{name}\n"\
    "    restart: always\n"\
    "    privileged: true\n"\
    "    network_mode: 'none'\n"\
    "    volumes:\n"\
    "      - {name}:/etc/frr\n"\
    "\n"

SERVICE_HOST_TEMPLATE = \
    "  {name}:\n"\
    "    build: ./host\n"\
    "    image: host_alpine\n"\
    "    hostname: {hostname}\n"\
    "    container_name: network_lab_{name}\n"\
    "    restart: always\n"\
    "    privileged: true\n"\
    "    network_mode: 'none'\n"\
    "    volumes:\n"\
    "      - {name}_network:/etc/network\n"\
    "    tty: true\n"\
    "\n"

SERVICE_SWITCH_TEMPLATE = \
    "  {name}:\n"\
    "    build: ./ovs\n"\
    "    image: ovs_alpine\n"\
    "    hostname: {hostname}\n"\
    "    container_name: network_lab_{name}\n"\
    "    restart: always\n"\
    "    privileged: true\n"\
    "    network_mode: 'none'\n"\
    "    tty: true\n"\
    "    volumes:\n"\
    "      - {name}_modules:/lib/modules\n"\
    "      - {name}_log:/var/log/openvswitch\n"\
    "      - {name}_lib:/var/lib/openvswitch\n"\
    "      - {name}_run:/var/run/openvswitch\n"\
    "      - {name}_etc:/etc/openvswitch\n"\
    "\n"

VOLUME_TEMPLATE = "  {name}:\n"

LINK_TEMPLATE = \
    """PID1="$(docker inspect network_lab_{name_1} -f '{{{{.State.Pid}}}}')"\n"""\
    """PID2="$(docker inspect network_lab_{name_2} -f '{{{{.State.Pid}}}}')"\n"""\
    """ln -sf /proc/$PID1/ns/net /var/run/netns/network_lab_{name_1}\n"""\
    """ln -sf /proc/$PID2/ns/net /var/run/netns/network_lab_{name_2}\n"""\
    """ip link add nl_{num_1} type veth peer name nl_{num_2}\n"""\
    """ip link set nl_{num_1} netns network_lab_{name_1} name {port_1}\n"""\
    """ip link set nl_{num_2} netns network_lab_{name_2} name {port_2}\n"""\
    """ip netns exec network_lab_{name_1} ip link set {port_1} up\n"""\
    """ip netns exec network_lab_{name_2} ip link set {port_2} up\n"""\
    """\n"""
