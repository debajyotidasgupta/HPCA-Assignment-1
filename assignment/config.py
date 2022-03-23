"""
+-----------------------------------------------------+
|               HPCA Assignment - 1                   |
+-----------------------------------------------------+
|                    GROUP - 5                        |
+-----------------------------------------------------+
|   RollNo.   |          Name                         |
+-----------------------------------------------------+
|  18CS30051  |   Debajyoti Dasgupta                  |
|  18CS30050  |   Archisman Pathak                    |
|  18CS30047  |   Somnath Jena                        |
|  18CS30048  |   Rounak Patra                        |
|  18CS30044  |   Tushar Gupta                        |
|  18CS30045  |   Vaishnavi R. Munghate               |
|  18CS30046  |   Vattikuti Rahul Naga Sri Bharadhwaj |
|  18CS30049  |   Abhinav Bohra                       |
|  18CS30052  |   Chakka Venugopal                    |
|  18CS30053  |   Kothapalli Dileep                   |
|  18EC10047  |   Rudrajyoti Roy                      |
|  18EC10075  |   Ayan Chakraborty                    |
|  21CD91R10  |   Shubhi Shukla                       |
+-----------------------------------------------------+
|            Description of the program               |
+-----------------------------------------------------+
|       Custom script for running simulation          |
|       with different  parameters  for  the          |
|       assignment. This script will run the          |
|       simulation for the qsort4.c  program          |
|       provided in the assignment. This sim          |
|       script is written in python3 and uses         |
|       gem5 as the simulator.                        |
+-----------------------------------------------------+
|       Language:  Python3                            |
|       File name: config.py                          |
|       License:   MIT Open Source License            |
|       Year:      2021-2022 Spring Semester          |
|       Course:    High Performance Computer Arch.    |
+-----------------------------------------------------+
"""

from concurrent.futures import process
from multiprocessing.dummy import Process
import options
import argparse
import sys

# Import m5 (gem5) library created when gem5 is built
import m5

# Import all of the SimObjects
from m5.objects import *

# Import all the brach prediction objects
from m5.objects.BranchPredictor import *

# Import all the utility functions
from m5.util import addToPath, fatal, warn

# Add the current directory to the python path
addToPath('./')

# Create the parser
parser = argparse.ArgumentParser(description='Arguments for gem5 simulation')

# Add the gem5 simulation options to the parser
options.addSEOptions(parser)

# Add the gem5 common options to the parser
options.addCommonOptions(parser)

args = parser.parse_args()


"""
Class: L1Cache
Derived from: Cache
Purpose: To create a L1 cache

[*] Add the L1 cache to the system
[*] Add parameters to the L1 cache
    [*] The fixed parameters are:
        1. tag_latency      - Tag access latency       (value: 2)
        2. data_latency     - Data access latency      (value: 2)
        3. response_latency - Response latency         (value: 2)
        4. mshrs            - Number of MSHRs          (value: 4)
        5. tgts_per_mshr    - Targets per MSHR         (value: 20)
    [*] The variable parameters are:
        1. assoc            - Associativity
"""


class L1Cache(Cache):
    tag_latency = 2                                 # Tag access latency
    data_latency = 2                                # Data access latency
    response_latency = 2                            # Response latency
    mshrs = 4                                       # Number of MSHRs
    tgts_per_mshr = 20                              # Targets per MSHR

    assoc = args.l1_assoc                           # Associativity

    def connectBus(self, bus):
        """Connect this cache to a memory-side bus"""
        self.mem_side = bus.cpu_side_ports

    def connectCPU(self, cpu):
        """Connect this cache's port to a CPU-side port
           This must be defined in a subclass"""
        raise NotImplementedError


"""
Class: L1ICache
Derived from: L1Cache
Purpose: To create a L1 instruction cache

[*] Add the parameters for L1 instruction cache
    [*] The variable parameters are:
        1. size             - Size of the cache  
"""


class L1ICache(L1Cache):
    size = args.l1i_size                            # Size of the cache

    def connectCPU(self, cpu):
        """Connect this cache's port to a CPU icache port"""
        self.cpu_side = cpu.icache_port


"""
Class: L1DCache
Derived from: L1Cache
Purpose: To create a L1 data cache

[*] Add the parameters for L1 data cache
    [*] The variable parameters are:
        1. size             - Size of the cache
"""


class L1DCache(L1Cache):
    size = args.l1d_size                            # Size of the cache

    def connectCPU(self, cpu):
        """Connect this cache's port to a CPU dcache port"""
        self.cpu_side = cpu.dcache_port


class L2Cache(Cache):
    tag_latency = 20                                # Tag access latency
    data_latency = 20                               # Data access latency
    response_latency = 20                           # Response latency
    mshrs = 20                                      # Number of MSHRs
    tgts_per_mshr = 12                              # Targets per MSHR

    size = args.l2_size                             # Size of the cache
    assoc = args.l2_assoc                           # Associativity

    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.mem_side_ports

    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports


# Create the system we are going to simulate
system = System()

# Set the clock frequency of the system (and all of its children)
system.clk_domain = SrcClockDomain()                # Clock domain
system.clk_domain.clock = '2GHz'                    # Clock frequency
system.clk_domain.voltage_domain = VoltageDomain()  # Voltage domain

# Set the memory mode of the system
system.mem_mode = 'timing'                          # Use timing access mode

# Set the memory range of the system
# Add 1GB of memory (single memory range)
system.mem_ranges = [AddrRange('1GB')]

# Create a CPU for the system
system.cpu = DerivO3CPU()                           # Use the DerivO3CPU

system.cache_line_size = 64                         # Set the cache line size
system.cpu.icache = L1ICache()                      # Create the L1 instr cache
system.cpu.dcache = L1DCache()                      # Create the L1 data cache
system.cpu.l2cache = L2Cache()                      # Create the L2 cache

# Create a system bus for the system, a system crossbar in this case
system.membus = SystemXBar()

# Create a memory bus, a coherent crossbar, in this case
system.l2bus = L2XBar()

# Connect the instruction and data caches to the CPU
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

# Hook the CPU ports up to the l2bus
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

# Create an L2 cache and connect it to the l2bus
system.cpu.l2cache.connectCPUSideBus(system.l2bus)

# Connect the L2 cache to the membus
system.cpu.l2cache.connectMemSideBus(system.membus)

# Create the interrupt controller for the CPU and connect to the membus
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports

# Create a memory controller for the system
system.mem_ctrl = MemCtrl()                          # Use the MemCtrl
system.mem_ctrl.dram = DDR3_1600_8x8()               # Use the DDR3_1600_8x8 DRAM
system.mem_ctrl.dram.range = system.mem_ranges[0]    # Set the memory range
system.mem_ctrl.port = system.membus.mem_side_ports  # Set the memory port


system.cpu.numRobs = 1                              # Number of ROBs

if args.bp_type == 'TournamentBP':                  # Branch predictor type
    system.cpu.branchPred = TournamentBP()          # Use the TournamentBP
elif args.bp_type == 'BimodalBP':                   # Branch predictor type
    system.cpu.branchPred = BimodalBP()             # Use the BimodalBP
elif args.bp_type == 'LocalBP':                     # Branch predictor type
    system.cpu.branchPred = LocalBP()               # Use the LocalBP


binary = args.benchmark

system.workload = SEWorkload.init_compatible(binary)

# Create a process for a simple "Hello World" application
process = Process()

# Set the command
# cmd is a list which begins with the executable (like argv)
process.cmd = [binary]

# Set the cpu to use the process as its workload and create thread contexts
system.cpu.workload = process
system.cpu.createThreads()

# set up the root SimObject and start the simulation
root = Root(full_system=False, system=system)

# instantiate all of the objects we've created above
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()
print('Exiting @ tick %i because %s' % (m5.curTick(), exit_event.getCause()))
