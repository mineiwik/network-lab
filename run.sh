#!/bin/bash
allow_sudo=$1

set -e
clear

echo "##############################"
echo "# Network Lab - Starter 3000 #"
echo "#         by mineiwik        #"
echo "##############################"

echo "Which config file would you like to run?"
files=$(ls configs/*.yaml | sed -e 's/\.yaml$//')
i=1

for j in $files
do
    echo "$i: $(basename "$j")"
    file[i]=$(basename "$j")
    i=$(( i + 1 ))
done

echo "Enter number"
read input
while  [[ ! $input ]] || [ $input -ge $i ] || [[ $input -le 0 ]]
do
    echo "Invalid input, try again!"
    read input
done
echo "You select the configuration ${file[$input]}"

echo "------------------------------"
echo "----------- Step 1 -----------"
echo "------------------------------"

echo "Building all necessary files"
python3 gen.py  "${file[$input]}"

chmod +x 02-load-modules.sh
chmod +x 03-start-containers.sh
chmod +x 04-link-containers.sh
chmod +x 05-configure-switches.sh
chmod +x 06-configure-vlans.sh
chmod +x 07-configure-hosts.sh
chmod +x goto.sh

echo "------------------------------"
echo "----------- Step 2 -----------"
echo "------------------------------"

echo "Loading necessary OVS module into kernel (needs root priviledges)"
if [ "$allow_sudo" != "-y" ]
then
    echo "Would you like to continue? y/[n]"
    read answer
    if [ "$answer" != "y" ]
    then
        echo "Aborting. Bye"
        exit
    fi
fi
sudo sh ./02-load-modules.sh

echo "------------------------------"
echo "----------- Step 3 -----------"
echo "------------------------------"

echo "Docker containers"
sh ./03-start-containers.sh

echo "------------------------------"
echo "----------- Step 4 -----------"
echo "------------------------------"

echo "Linking containers (needs root priviledges)"
if [ "$allow_sudo" != "-y" ]
then
    echo "Would you like to continue? y/[n]"
    read answer
    if [ "$answer" != "y" ]
    then
        echo "Aborting. Bye"
        exit
    fi
fi
sudo sh ./04-link-containers.sh > /dev/null

echo "------------------------------"
echo "----------- Step 5 -----------"
echo "------------------------------"

echo "Configuring OVS switches"
sh ./05-configure-switches.sh &> /dev/null || true

echo "------------------------------"
echo "----------- Step 6 -----------"
echo "------------------------------"

echo "Configuring VLANs"
sh ./06-configure-vlans.sh

echo "------------------------------"
echo "----------- Step 7 -----------"
echo "------------------------------"

echo "Configuring hosts"
sh ./07-configure-hosts.sh &> /dev/null

echo "Network Lab has been started"
echo "Type ./goto.sh APLIANCE_NAME to enter the appliance's shell"