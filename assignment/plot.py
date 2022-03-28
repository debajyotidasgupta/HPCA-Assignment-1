from importlib.resources import contents
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import os
import re
import numpy as np
import pandas as pd
from pprint import pprint

parser = argparse.ArgumentParser()
parser.add_argument("-d", help= "directory path containing stats file for different runs", required= True)

stats_line_id = {
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
    'system.cpu.l2cache.overallAvgMissLatency::total': 'avg_miss_lat_l2cache',

    'system.cpu.dcache.overallMisses::total': 'miss_cycle_dcache',
    'system.cpu.icache.overallMisses::total': 'miss_cycle_icache',
    'system.cpu.l2cache.overallMisses::total': 'miss_cycle_l2cache',

    'system.cpu.dcache.overallAccesses::total': 'num_access_dcache',
    'system.cpu.icache.overallAccesses::total': 'num_access_icache',
    'system.cpu.l2cache.overallAccesses::total': 'num_access_l2cache',
    
    'system.mem_ctrl.dram.numReads::total': 'mem_read',
    'system.mem_ctrl.dram.numWrites::total': 'mem_write'
}

options = ['l1d_size', 'l1i_size', 'l2_size', 'l1_assoc', 'l2_assoc', 'bp_type', 'ROBEntries', 'numIQEntries']
stats_needed = ['cpi', 'mispred_exec', 'pred_NT_incorrect', 'pred_T_incorrect', 'ipc', 'btb_hit_ratio', 'overall_miss_cycle', 'overall_miss_rate', 'overall_miss_lat', 'rob_access', 'lsqfull_stall', 'ld_st_data_fwd', 'cache_blocked_memfail']

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
    info = {}

    #check through all lines
    for line in contents:
        line = re.sub('\s+',' ',line)
        args = line.split(" ")
        if args[0] in stats_line_id.keys():
            info[stats_line_id[args[0]]] = float(args[1])


    # info corresponding to lines in stats_line_id
    # pprint(info)
    
    # from extracted info to needed info
    needed_info = dict()
    needed_info['cpi'] = info['cpi']
    needed_info['mispred_exec'] = info['mispred_exec']
    needed_info['pred_NT_incorrect'] = info['pred_NT_incorrect']
    needed_info['pred_T_incorrect'] = info['pred_T_incorrect']
    needed_info['ipc'] = info['ipc']

    # total ROB access = read + write
    needed_info['rob_access'] = info['rob_reads'] + info['rob_writes']

    # total miss cycles = miss in all 3 caches
    needed_info['overall_miss_cycle'] = info['miss_cycle_dcache'] + info['miss_cycle_icache'] + info['miss_cycle_l2cache']

    # overall miss rate 
    # total_mem_access = info['mem_read'] + info['mem_write']
    icache_miss = info['miss_rate_icache']*info['num_access_icache']
    dcache_miss = info['miss_rate_dcache']*info['num_access_dcache']
    l2cache_miss = info['miss_rate_l2cache']*info['num_access_l2cache']

    total_mem_access = info['num_access_icache'] + info['num_access_dcache'] + info['num_access_l2cache']

    needed_info['overall_miss_rate'] = (icache_miss + dcache_miss + l2cache_miss)/total_mem_access

    # overall miss latency

    needed_info['overall_miss_lat'] = ( icache_miss*info['avg_miss_lat_icache'] +
                                        dcache_miss*info['avg_miss_lat_dcache'] +
                                        l2cache_miss*info['avg_miss_lat_l2cache'])/ (icache_miss + dcache_miss + l2cache_miss)


    needed_info['lsqfull_stall'] = info['lsqfull_stall']
    needed_info['ld_st_data_fwd'] = info['ld_st_data_fwd']
    needed_info['cache_blocked_memfail'] = info['cache_blocked_memfail']
    needed_info['btb_hit_ratio'] = info['btb_hit_ratio']

    return needed_info, info

def plotter(x, y, xlabel, ylabel):
    # data = pd.DataFrame({xlabel: x, ylabel: y})
    # sns.lineplot(data, x= xlabel, y= ylabel)
    plt.plot(x, y)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.show()



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

            # extract info from file
            filename = dirpath +"/" + subdir + "/stats.txt"
            with open(filename, 'r') as fp:
                config_stats, _ = stats_extractor(fp)
                for key in config_stats:
                    stats_lists[key].append(config_stats[key])

    # print(stats_lists)                
    # convert to numpy arrays
    for key in stats_lists.keys():
        stats_lists[key] = np.array(stats_lists[key])


    # best 10 according to cpi value
    sort_idx_cpi = np.argsort(stats_lists['cpi'])
    top_10_by_cpi = []
    for i in sort_idx_cpi[:10]:
        top_10_by_cpi.append(config_list[i])

    # show top 10 configs
    print("Top 10 configs according to CPI values are as shown below:")
    for i, item in enumerate(top_10_by_cpi):
        print(i+1, item)


    top_10_stats = {}
    for key in stats_lists.keys():
        top_10_stats[key] = []
        temp = stats_lists[key]
        for i in sort_idx_cpi[:10]:
            top_10_stats[key].append(temp[i])
        plotter(x= list(range(10)), y= top_10_stats[key], xlabel= "configs", ylabel= str(key))
    pprint(top_10_stats)