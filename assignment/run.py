import itertools
import os

# variable parameters

l1d_size    = ["32kB","64kB"]
l1i_size    = ["32kB","64kB"]
l2_size     = ["128kB","256kB","512kB"]
l1_assoc    = [2,4,8]
l2_assoc    = [4,8]
bp_type     = ['TournamentBP','BiModeBP','LocalBP']
ROBEntries  = [128,192]
numIQEntries= [16,64]

# command to execute with different configurations

command = """build/X86/gem5.opt -d configs/assignment/{} configs/assignment/config.py -b configs/assignment/qsort4 
            --l1d_size={} --l1i_size={} --l2_size={} --l1_assoc={} --l2_assoc={} --bp_type={} --ROBEntries={} --numIQEntries={}"""

# param names
param_names = ["l1d_size","l1i_size","l2_size","l1_assoc","l2_assoc","bp_type","ROBEntries","numIQEntries"]

# for all combinations run the simulation

for config in itertools.product(l1d_size,l1i_size,l2_size,l1_assoc,l2_assoc,bp_type,ROBEntries,numIQEntries):
    out_folder = "runs/"+"_".join([str(x) for x in config])
    out_path = os.path.join("configs/assignment/",out_folder)
    # to write each stats.txt into different folder
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    params = [out_folder]
    params.extend(config)
    print("Starting simulation with parameters")
    for i in range(len(param_names)):
        print(param_names[i]+" : "+str(config[i]))
    os.system(command.format(*params))
