from asyncio.log import logger
import itertools
import logging
import os


if __name__ == '__main__':
    # log_file will contain all the configurations that have been simulated
    # so that they won't be simulated again for optimization
    log_file = "/home/ubuntu/gem5/configs/assignment/runs/logs.txt"
    simulated_configs = set()
    with open(log_file, "r") as f:
        simulated_configs = set([line.strip().split(':')[2]
                                for line in f.readlines()])

    open(log_file, "w").close()
    logging.basicConfig(filename=log_file, level=logging.INFO)

    # variable parameters
    l1d_size = ["32kB", "64kB"]
    l1i_size = ["32kB", "64kB"]
    l2_size = ["128kB", "256kB", "512kB"]
    l1_assoc = [2, 4, 8]
    l2_assoc = [4, 8]
    bp_type = ['TournamentBP', 'BiModeBP', 'LocalBP']
    ROBEntries = [128, 192]
    numIQEntries = [16, 64]

    # command to execute with different configurations

    command = """/home/ubuntu/gem5/build/X86/gem5.opt                   \
        -d /home/ubuntu/gem5/configs/assignment/runs/{}                 \
        /home/ubuntu/gem5/configs/assignment/config.py                  \
        -b /home/ubuntu/gem5/configs/assignment/qsort4                  \
        --l1d_size={} --l1i_size={} --l2_size={} --l1_assoc={}          \
        --l2_assoc={} --bp_type={} --numROBEntries={} --numIQEntries={}"""

    # param names
    param_names = ["l1d_size", "l1i_size", "l2_size", "l1_assoc",
                   "l2_assoc", "bp_type", "numROBEntries", "numIQEntries"]

    # for all combinations run the simulation
    simulations = list(itertools.product(
        l1d_size, l1i_size, l2_size, l1_assoc, l2_assoc, bp_type, ROBEntries, numIQEntries))
    print("Total number of simulations: {}".format(
        len(simulations)), flush=True)

    for config in simulations:

        out_folder = "_".join([str(x) for x in config])

        if out_folder in simulated_configs:
            continue

        params = [out_folder]
        params.extend(config)
        print("Starting simulation with parameters", flush=True)

        for i in range(len(param_names)):
            print(param_names[i]+" : "+str(config[i]), flush=True)
        ret = os.system(command.format(*params))

        print("Simulation finished with return code {}".format(ret), flush=True)

        if ret == 0:
            # if this run was successful, append it to the log_file
            logger.info(out_folder)
