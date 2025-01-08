#!/usr/bin/env python3

"""
This script generates a GAP library of non-isomorphic models of an algebra, including data (non-isomorphic models up to order n),
function to access the models, and documentation.

The algebra is specified in a Mace input file(s).
"""

import os
import sys

from datetime import datetime
import configparser
import glob
import shutil

from gap_lib import gen_gap_package
from mace import gen_mace_models
from mace_to_gap import extract_mace_models
# from non_iso_algebras import gen_non_iso
from encoder import encode_data


default_config = "algebra.ini"


def gen_gaplib(argv):
    
    if len(argv) > 1:
        config_file = argv[1]
    else:
        config_file = default_config
    config = configparser.ConfigParser()
    config.read(config_file)
    root_config = config['ROOT']
    algebraName = root_config['AlgebraName']
    algebraDisplayName = root_config['AlgebraDisplayName']
    print(f"\n{datetime.now()}** Started generating GAP package for small {algebraDisplayName}\n")

    final_model_dir = root_config['NonIsoDir']
    # non_iso_out_dir = config['NONISO']['OutputDir']
    mace_output_dir = config['MACE']['OutputDir']
    gap_lib_dir = f"{config['ROOT']['PackageName']}-{config['ROOT']['Version']}"
    log_dir = "logs"
    all_dirs = [mace_output_dir, gap_lib_dir, log_dir, final_model_dir]  # non_iso_out_dir
    for x in all_dirs:
        shutil.rmtree(x, ignore_errors=True)
    for x in all_dirs:
        os.makedirs(x, exist_ok=True)
        
    shutil.copytree(config['MACE']['InputDir'], os.path.join(gap_lib_dir, 'doc', config['MACE']['InputDir']))
    prebuilt_dir = config['ROOT']['PrebuiltDir']
        
    # extract models from mace output files.  All in the same output_dir,
    # each "partition" of output files are in the same list.  partitions of models are assumed to be non-overlapping
    # e.g. outfiles = [['of_2_0.out', 'of_3_0.out'], ['of_2_1.out', 'of_3_1.out']]
    
    func_names = list()   # names of the operations in the model, such as *, v, -, and ^.
    mace_output_dir, outfiles = gen_mace_models(algebraName, config["MACE"], prebuilt_dir)

    from_order = int(config["MACE"]['MinDomainSize'])
    to_order = int(config["MACE"]['MaxDomainSize'])
    print(f"Debug {datetime.now()} Done generating mace outputs, order size from {from_order} to {to_order}")
    print(f"Debug Total number of files: {len(outfiles)*len(outfiles[0])}")

    # delete iso models, and write the non-iso models for each order calculated
    for order in range(from_order, to_order+1):
        order_n_files = outfiles[order-from_order]
        # gen_non_iso(config['NONISO'], order, mace_output_dir, order_n_files, prebuilt_dir)
        
        basename = order_n_files[0][:-6]           # remove ending "_0.out"
        all_non_iso_files = os.path.join(mace_output_dir, order_n_files[0])  # there is only 1 file
        print(f"******************* {all_non_iso_files}")
        read_files = glob.glob(all_non_iso_files)
        write_file = os.path.join(final_model_dir, basename + ".g")
        with open(write_file, "w") as outfile:
            extract_mace_models(read_files, outfile, func_names)
    print(func_names)
    print(f"{datetime.now()} Done removing isomorphic models, and writing non-iso models by model orders")
    num_in_orders = encode_data(algebraName, final_model_dir, from_order, to_order)

    prefix = config['GAP_PACKAGE']['Prefix']
    base_name = config['ROOT']['BaseName']
    display_name_lc = config['ROOT']['AlgebraDisplayNameLowerCase']
    singularAlgebraName = config['ROOT']['SingularAlgebraName']
    gen_gap_package(algebraName, base_name, display_name_lc, singularAlgebraName, [from_order, to_order], prefix, num_in_orders, func_names, config)

    print(f"{datetime.now()} Finished generating GAP package for small {algebraDisplayName}")
    

if __name__ == "__main__":
    gen_gaplib(sys.argv)

