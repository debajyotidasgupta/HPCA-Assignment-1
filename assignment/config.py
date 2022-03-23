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
|       File name: config.py.py                       |
|       License:   MIT Open Source License            |
|       Year:      2021-2022 Spring Semester          |
|       Course:    High Performance Computer Arch.    |
+-----------------------------------------------------+
"""

import argparse

import m5
from m5.objects import *
from m5.objects.BranchPredictor import *

"""
[*] Add Argument Parser for the script
[*] Add the arguments for the argument parser
    [*] The arguments are:
        1. l1d_size      - L1 data cache size         (type: str)
        2. l1i_size      - L1 instruction cache size  (type: str)
        3. l2_size       - L2 cache size              (type: str)
        4. l1_assoc      - L1 cache associativity     (type: int)
        5. l2_assoc      - L2 cache associativity     (type: int)
        6. bp_type       - Branch predictor type      (type: str)
        7. numROBEntries - Number of ROB entries      (type: int)
        8. numIQEntries  - Number of IQ entries       (type: int)
"""

args = argparse.ArgumentParser(description='Arguments for gem5 simulation')
args.add_argument('--l1d_size', default='64kB',
                  help='L1 data cache size', type=str)
args.add_argument('--l1i_size', default='32kB',
                  help='L1 instruction cache size', type=str)
args.add_argument('--l2_size', default='128kB', help='L2 cache size', type=str)
args.add_argument('--l1_assoc', default=2,
                  help='L1 cache associativity', type=int)
args.add_argument('--l2_assoc', default=2,
                  help='L2 cache associativity', type=int)
args.add_argument('--bp_type', default='TournamentBP')
args.add_argument('--numROBEntries', default=128,
                  help='Number of ROB entries', type=int)
args.add_argument('--numIQEntries', default=64,
                  help='Number of IQ entries', type=int)


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
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20

    assoc = args.l1_assoc


"""
Class: L1ICache
Derived from: L1Cache
Purpose: To create a L1 instruction cache

[*] Add the parameters for L1 instruction cache
    [*] The variable parameters are:
        1. size             - Size of the cache  
"""


class L1ICache(L1Cache):
    size = args.l1i_size


"""
Class: L1DCache
Derived from: L1Cache
Purpose: To create a L1 data cache

[*] Add the parameters for L1 data cache
    [*] The variable parameters are:
        1. size             - Size of the cache
"""


class L1DCache(L1Cache):
    size = args.l1d_size


class L2Cache(Cache):
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12

    size = args.l2_size
    assoc = args.l2_assoc


system = System()

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '2GHz'
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('1GB')]

system.cpu = DerivO3CPU()

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]

system.cache_line_size = '64kB'
system.cpu.icache = L1ICache()
system.cpu.dcache = L1DCache()
system.cpu.l2cache = L2Cache()

system.cpu.numRobs = 1

if args.bp_type == 'TournamentBP':
    system.cpu.branchPred = TournamentBP()
elif args.bp_type == 'BimodalBP':
    system.cpu.branchPred = BimodalBP()
elif args.bp_type == 'LocalBP':
    system.cpu.branchPred = LocalBP()
