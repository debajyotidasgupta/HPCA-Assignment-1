from importlib.resources import contents
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import os
import re
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("-d", help= "directory path containing stats file for different runs", required= True)

stats_def = {
    'system.cpu.cpi': 'cpi',
    'system.cpu.iew.branchMispredicts': 'mispred_exec',
    'system.cpu.iew.predictedNotTakenIncorrect': 'pred_NT_incorrect',
    'system.cpu.iew.predictedTakenIncorrect': 'pred_T_incorrect',
    'system.cpu.ipc': 'ipc',
    'system.cpu.branchPred.BTBHitRatio': 'btb_hit_ratio',
    'system.cpu.rob.reads': 'rob_reads',
    'system.cpu.rob.writes': 'rob_writes',
    'system.cpu.iew.lsqFullEvents': 'lsqfull_stall',
    'system.cpu.lsq0.forwLoads': 'ld_st_data_fwd',
    'system.cpu.lsq0.blockedByCache': 'cache_blocked_memfail',
    'system.cpu.icache.overallMissRate::total': 'miss_rate_icache',
    'system.cpu.l2cache.overallMissRate::total': 'miss_rate_l2cache',
    'system.cpu.dcache.overallMissRate::total': 'miss_rate_dcache',
    'system.cpu.dcache.overallAvgMissLatency::total': 'avg_miss_lat_dcache',
    'system.cpu.icache.overallAvgMissLatency::total': 'avg_miss_lat_icache',
    'system.cpu.l2cache.overallAvgMissLatency::total': 'avg_miss_lat_l2cache'
}

options = ['l1d_size', 'l1i_size', 'l2_size', 'l1_assoc', 'l2_assoc', 'bp_type', 'ROBEntries', 'numIQEntries']
stats_needed = ['cpi', 'mispred_exec', 'pred_NT_incorrect', 'pred_T_incorrect', 'ipc', 'btb_hit_ratio', 'overall_miss_cy', 'overall_miss_rate', 'overall_miss_lat', 'rob_access', 'lsqfull_stall', 'ld_st_data_fwd', 'cache_blocked_memfail']

class Config:
    def __init__(self, config_dict):
        self.l1d_size = config_dict['l1d_size']
        self.l1i_size = config_dict['l1i_size']
        self.l2_size = config_dict['l2_size']
        self.l1_assoc = config_dict['l1_assoc']
        self.l2_assoc = config_dict['l2_assoc']
        self.bp_type = config_dict['bp_type']
        self.ROBEntries = config_dict['ROBEntries']
        self.numIQEntries = config_dict['numIQEntries']

    def __str__(self):
        s = "config:[l1d_size:{} | l1i_size:{} | l2_size:{} | l1_assoc:{} | l2_assoc:{} | bp:{} | ROBEntries:{} | numIQEntries:{}]".format(
                self.l1d_size, self.l1i_size, self.l2_size, self.l1_assoc, self.l2_assoc, self.bp_type, self.ROBEntries, self.numIQEntries)
        return s



# return needed stats given the file pointer
def stats_extractor(fp):
    contents = fp.readlines()
    needs = []
    for line in contents:
        line = re.sub('\s+',' ',line)
        args = line.split(" ")
        if args[0] in stats_def.keys():
            needs.append(args[1])

    info = dict(zip(stats_def.values(), needs))
    
    needed_info = dict()
    needed_info['cpi'] = info['cpi']
    needed_info['mispred_exec'] = info['mispred_exec']
    needed_info['pred_NT_incorrect'] = info['pred_NT_incorrect']
    needed_info['pred_T_incorrect'] = info['pred_T_incorrect']
    needed_info['ipc'] = info['ipc']
    needed_info['rob_access'] = info['rob_reads'] + info['rob_writes']
    needed_info['lsqfull_stall'] = info['lsqfull_stall']
    needed_info['ld_st_data_fwd'] = info['ld_st_data_fwd']
    needed_info['cache_blocked_memfail'] = info['cache_blocked_memfail']
    needed_info['btb_hit_ratio'] = info['btb_hit_ratio']

    return needed_info


if __name__ == "__main__":

    # initialize configs list
    config_list = []

    # initialize to contain list for every stats
    stats_lists = {}
    for item in stats_needed:
        stats_lists[item] = list()

    # get directory path
    dirpath = vars(parser.parse_args())['d']

    # iterate through files in directory
    for subdir in os.listdir(dirpath):
        if os.path.isdir(dirpath + "/" + subdir):
            # get config object from file name
            arg_list = subdir.split("_")
            config_dict = dict(zip(options, arg_list))
            config = Config(config_dict= config_dict)
            config_list.append(config)

            filename = dirpath +"/" + subdir + "/stats.txt"
            with open(filename, 'r') as fp:
                config_stats = stats_extractor(fp)
                for key in config_stats:
                    stats_lists[key].append(config_stats[key])

    # print(stats_lists)                
    # convert to numpy arrays
    for key in stats_lists.keys():
        stats_lists[key] = np.array(stats_lists[key])


    # best 10 according to cpi value
    sort_idx_cpi = np.argsort(stats_lists['cpi'])
    top_10_by_cpi = []
    for i in range(10):
        top_10_by_cpi.append(config_list[sort_idx_cpi[i]])

    print("Top 10 configs according to CPI values are as shown below:")
    for i, item in enumerate(top_10_by_cpi):
        print(i+1, item)

    top_10_stats = {}
    for key in stats_lists.keys():
        top_10_stats[key] = []
        for i in range(10):
            top_10_stats[key].append(stats_lists[key][sort_idx_cpi[i]])
    print(top_10_stats)
