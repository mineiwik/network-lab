# Network-Lab - Create your own virtual networking lab

## Requirements
- Linux
- Python >= 3.9
  - PyYAML >= 6.0
- Docker
- Docker compose

## Getting Started
To configure a new or exisitng network configuration just enter:
``` bash
./configure.sh
```
You can find your configurations under `./configs/`

To create all necessary files and run the virtual network enter:
``` bash
./run.sh
```
**Warning:** The script will ask for sudo privileges (you can accept them in advance by adding the `-y` flag)

To stop all containers, enter:
``` bash
./stop.sh
```
or
``` bash
./stop.sh -v
```
to also delete all associated volumes

## Not implemented yet
- VLAN configurations need to be added manually to a config file (see default.yaml as an example)
