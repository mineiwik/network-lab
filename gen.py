import sys
import network_gen

if len(sys.argv) < 2:
    network_gen.start_wizard()
elif len(sys.argv) == 2:
    network = network_gen.load_network(sys.argv[1] + ".yaml")
    network_gen.run(network)
else:
    print("Too many arguments!")
