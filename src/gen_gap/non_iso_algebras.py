#!/usr/bin/python3

"""
This script takes a list of model files, generate non-isomorphic models from each of them
by the splitModels utility.

 

"""

import os
import subprocess

def gen_non_iso(config, order, input_dir, input_files):
    """ 
    Args:
        config (dict): configurations from config file
        order (int):  order of the algebra
        input_dir (str): input directory
        input_files (List): list of input files, each file is of the format prefix_<x> where x is a number
    """
    isofilter = config['Filter']
    min_count = int(config['MinModelsInFile'])
    working_dir = config['WorkingDir']
    num_random = int(config['NumRandom'])
    max_random = int(config['MaxRandom'])
    sampling_freq = 100  # int(config['SamplingFreq'])
    
    prefix = input_files[0].replace(".out", "")
    params = f'-d{order} -f{isofilter} -m{min_count} -o{working_dir}/{prefix}_ -t{working_dir}/{prefix}_statistics.json -r{num_random} -l{max_random} -s{sampling_freq}'
    for in_model_file in input_files:
        in_model_filepath = os.path.join(input_dir, in_model_file)        
        # allow at most 5000 samples for random invariant screening
        cp = subprocess.run(f'./bin/splitModels {params} -u1000000 -x5000 -i{in_model_filepath}', capture_output=True, text=True, check=False, shell=True)
        with (open(os.path.join("logs", f"{prefix}.log" ), "a")) as fp:
            fp.write(cp.stdout)
            fp.write(cp.stderr)
            fp.write("\n===============================================================\n\n")

    
__all__ = ["gen_non_iso"]
