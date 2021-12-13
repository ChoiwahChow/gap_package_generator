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
from non_iso_algebras import gen_non_iso
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
    algebraNames = root_config['AlgebraNames'].split(":")
    algebraDisplayNames = root_config['AlgebraDisplayNames'].split(":")
    print(f"\n{datetime.now()}** Started generating GAP package for small {algebraDisplayNames}\n")

    final_model_dir = root_config['NonIsoDir']
    non_iso_out_dir = config['NONISO']['OutputDir']
    mace_input_dir = config["MACE"]['InputDir']
    mace_output_dir = config["MACE"]['OutputDir']
    gap_lib_dir = f"{config['ROOT']['PackageName']}-{config['ROOT']['Version']}"
    log_dir = "logs"
    all_dirs = [mace_output_dir, gap_lib_dir, non_iso_out_dir, log_dir, final_model_dir]
    for x in all_dirs:
        shutil.rmtree(x, ignore_errors=True)
    for x in all_dirs:
        os.makedirs(x, exist_ok=True)
        
    shutil.copytree(config['MACE']['InputDir'], os.path.join(gap_lib_dir, 'doc', config['MACE']['InputDir']))
    
    range_pairs = [y.split(",") for y in config['MACE']['DomainSizeRange'].split(":")]
    domain_range = [(int(x[0]), int(x[1])) for x in range_pairs]
    
    # extract models from mace output files.  All in the same output_dir,
    # each "partition" of output files are in the same list.  partitions of models are assumed to be non-overlapping
    # e.g. outfiles = [['of_2_0.out', 'of_3_0.out'], ['of_2_1.out', 'of_3_1.out']]
    
    mace_input_files = config["MACE"]['InputFiles'].split(":")
    mace_config = {"InputDir": mace_input_dir, "OutputDir": mace_output_dir}
    func_names = list()   # names of the operations in the model, such as *, v, -, and ^.
    num_in_orders = list()
    for pos in range(0, len(algebraNames)):
        algebraName = algebraNames[pos]
        mace_config["algebraName"] = algebraNames[pos]
        mace_config["InputFiles"] = mace_input_files[pos]
        mace_config["DomainSizeRange"] = domain_range[pos]
        mace_output_dir, outfiles = gen_mace_models(algebraName, mace_config)
        
        from_order = domain_range[pos][0]
        to_order = domain_range[pos][1]
    
        print(f"Debug {datetime.now()} Done generating mace outputs, order size from {from_order} to {to_order}")
        print(f"Debug Total number of files: {len(outfiles)*len(outfiles[0])}")

        # delete iso models, and write the non-iso models for each order calculated
        alg_func_names = list()
        for order in range(from_order, to_order+1):
            order_n_files = outfiles[order-from_order]
            gen_non_iso(config['NONISO'], order, mace_output_dir, order_n_files)
            
            basename = order_n_files[0][:-6]           # remove ending "_0.out"
            all_non_iso_files = os.path.join(non_iso_out_dir, basename + "_*.out.f")
            read_files = glob.glob(all_non_iso_files)
            write_file = os.path.join(final_model_dir, basename + ".g")
            with open(write_file, "w") as outfile:
                extract_mace_models(read_files, outfile, alg_func_names)
        func_names.append(", ".join(alg_func_names))
        print(f"{datetime.now()} Done removing isomorphic models, and writing non-iso models by model orders")
        num_in_orders.append( encode_data(algebraName, final_model_dir, from_order, to_order) )

    prefixes = config['GAP_PACKAGE']['Prefixes'].split(":")
    base_names = config['ROOT']['BaseNames'].split(":")
    display_names_lc = config['ROOT']['AlgebraDisplayNamesLowerCase'].split(":")
    gen_gap_package(algebraNames, base_names, display_names_lc, domain_range, prefixes, num_in_orders, func_names, config)

    print(f"{datetime.now()} Finished generating GAP package for small {algebraDisplayNames[0]}")
    

if __name__ == "__main__":
    gen_gaplib(sys.argv)

