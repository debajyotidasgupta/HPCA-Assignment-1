from importlib.resources import contents
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import os
import re
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("-d", help= "directory path containing stats file for different runs", required= True)
stats = {
    'cpi': 178,
    'mispred_exec': 562,
    'pred_NT_incorrect': 561,
    'pred_T_incorrect': 560,
    'ipc': 180,
    'btb_hit_ratio': 211,
    'rob_read': 808,
    'rob_write': 809,
    'lsq_full_stall': 558,
    'ld_st_data_fwd': 733,
    'cache_blocked_mem_fail': 739
}

options = ['l1d_size', 'l1i_size', 'l2_size', 'l1_assoc', 'l2_assoc', 'bp_type', 'ROBEntries', 'numIQEntries']

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
    for key in stats:
        l = re.split('\s+', contents[stats[key]-1], maxsplit= 2)
        needs.append(l[1])

    return dict(zip(stats.keys(), needs))





if __name__ == "__main__":

    # initialize configs list
    config_list = []

    # initialize to contain list for every stats
    stats_lists = {}
    for key in stats.keys():
        stats_lists[key] = list()

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

    print(stats_lists)                
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
        print(i, item)

    top_10_stats = {}
    for key in stats_lists.keys():
        top_10_stats[key] = []
        for i in range(10):
            top_10_stats[key].append(stats_lists[key][sort_idx_cpi[i]])
    print(top_10_stats)
