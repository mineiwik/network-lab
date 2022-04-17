from .templates import *


def gen_router(name, hostname, version="v7.5.1"):
    service = SERVICE_ROUTER_TEMPLATE.format(
        name=name, version=version, hostname=hostname)
    volume = VOLUME_TEMPLATE.format(name=name)
    return (service, volume)


def gen_switch(name, hostname):
    service = SERVICE_SWITCH_TEMPLATE.format(name=name, hostname=hostname)
    volume = ""
    volume += VOLUME_TEMPLATE.format(name=name + "_modules")
    volume += VOLUME_TEMPLATE.format(name=name + "_log")
    volume += VOLUME_TEMPLATE.format(name=name + "_lib")
    volume += VOLUME_TEMPLATE.format(name=name + "_run")
    volume += VOLUME_TEMPLATE.format(name=name + "_etc")
    return (service, volume)


def gen_host(name, hostname, version="3.15"):
    service = SERVICE_HOST_TEMPLATE.format(name=name, hostname=hostname)
    volume = VOLUME_TEMPLATE.format(name=name + "_network")
    return (service, volume)


def gen_goto(appliances):
    content = '#!/bin/bash\n' \
        'appliance=$1\n\n'

    for appliance in appliances:
        content += 'if [ "${{appliance}}" == "{appliance_short}" ]; then\n' \
            '  docker exec -it network_lab_{appliance} sh\n' \
            '  exit\n' \
            'fi\n\n'.format(appliance_short=appliance.split(
                "__")[0], appliance=appliance)
    content += 'echo "invalid arguments"\n'
    with open("goto.sh", "w") as file:
        file.writelines(content)


def gen_switch_configs():
    content = "#!/bin/bash\n"

    content += 'docker exec network_lab_S1__bb50aaeb-4444-435f-814f-dacbfbbb8584 sh -c "ovs-vsctl add-br br0 ; ovs-vsctl add-port br0 port_ZURI ; ovs-vsctl add-port br0 port_Conrad"'

    with open("20-configure-switches.sh", "w") as file:
        file.writelines(content)


def gen_docker_file(all_devices):
    with open("docker-compose.yml", "w") as file:
        services = ""
        volumes = ""
        appliances = []
        for device_type, devices in all_devices.items():
            device_generator = None
            if device_type == "routers":
                device_generator = gen_router
            elif device_type == "switches":
                device_generator = gen_switch
            elif device_type == "hosts":
                device_generator = gen_host
            if not device_generator:
                print("Invalid device type")
                return

            for device in devices:
                (service, volume) = device_generator(
                    name=device, hostname=device.split("__")[0])
                services += service
                volumes += volume
                appliances.append(device)

        docker_file = DOCKER_COMPOSE_TEMPLATE.format(
            services=services, volumes=volumes)

        file.writelines(docker_file)

        gen_goto(list(appliances))


def gen_links(links):
    with open("04-link-containers.sh", "w") as file:
        commands = "#!/bin/bash\n"\
            "mkdir -p /var/run/netns\n"\
            "\n"
        i = 1
        for link in links:
            names = []
            ports = []
            for appliance, port in link.items():
                names.append(appliance)
                ports.append(port)
            commands += LINK_TEMPLATE.format(
                name_1=names[0], name_2=names[1], port_1=ports[0], port_2=ports[1], num_1=i, num_2=i+1)
            i += 2
        file.writelines(commands)
