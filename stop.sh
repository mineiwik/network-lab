#!/bin/bash
delete_volumes=$1

set -e

if ! command -v docker &> /dev/null
then
    echo "Docker is not available on this system!"
    exit
fi

if command -v docker-compose &> /dev/null
then
    echo "Stopping and removing old containers"
    docker-compose rm -sf &> /dev/null
elif command -v docker compose &> /dev/null
then
    echo "Stopping and removing old containers"
    docker compose rm -sf &> /dev/null
else
    echo "Docker compose is not installed!"
fi

if [ "$delete_volumes" == "-v" ]
then
    echo "Deleting volumes"
    docker volume prune -f &> /dev/null
fi

exit