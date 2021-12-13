"""
This script has all mace-related processing.
It generates the models post-processed with interformat, so that the models
are ready to be filtered for isomorphism.

The only entry point is gen_mace_models.
"""
import os

import shutil
import subprocess


def run_mace(mace4exec, skipOrders, partition_id, input_dir, input_files, min_domain_size, max_domain_size, output_dir, output_file_base):
    """ This function runs the Mace 4 with the given input_files
    
        assign(domain_size, min_domain_size).
    Args:
        mace4exec (str): the Mace4 exec
        skipOrders (List[int]): domain size not to run mace4
        partition_id (int): id (starting from 0) for this set of input run. Different sets are assumed to be non-overlapping
        input_dir (str):  input directory
        input_files (List[str]): input files in the input directory
        min_domain_size (int): start generating models of this order
        max_domain_size (int): end generating models of this order
    Returns:
        List[List[str], List[str]]: [list of [output for each order, a log file for all runs]
                                    e.g. for orders 2 to 4 of partition_id = 1:
                                    [[of_2_1.out, of_3_1.out, of_4_1.out], log]
    """
    # print(f"input_dir: {input_dir}, input_files: {input_files}, partition_id: {partition_id}\n")
    
    all_inputs = [os.path.join(input_dir, x) for x in input_files]
    all_logs = list()
    all_out_files = list()
    for domain_size in range(min_domain_size, max_domain_size+1):
        output_file = output_file_base + "_" + str(domain_size) + "_" + str(partition_id) + ".out"        
        all_out_files.append(output_file)
        if domain_size in skipOrders:
            continue
        output_file_path = os.path.join(output_dir, output_file)
        # cp = subprocess.run(f'mace4 -n {domain_size} -N {domain_size} -f  {" ".join(all_inputs)} | interpformat > {output_file_path}',
        #                     capture_output=True, text=True, check=False, shell=True)  

        cp = subprocess.run(f'{mace4exec} -n {domain_size} -N {domain_size} -m-1 -A1 -f  {" ".join(all_inputs)} 2>{output_file_path}',
                            capture_output=True, text=True, check=False, shell=True)
        
        all_logs.append([cp.returncode, cp.stdout, cp.stderr])
        shutil.move('mace4_models.txt', os.path.join(output_file_path))
    return all_out_files, all_logs


def gen_mace_models(file_basename, mace_config, prebuilt_dir):
    """ Generate all mace models. When multiple input files are used, they are assumed to generate the models
        in non-isomorphic partitions (no models across partitions can be isomorphic).  For example, one input
        file may specify that the models have one or more idempotents, and the other specify that the models
        have no idempotent at all.
    Args:
        mace_config (dict): config settings
        prebuilt_dir (str): directory holding all prebuilt files
    Returns:
        All models from Mace in files grouped by model_size, for each model_size, each partition_id will give one output file.
        e.g. ['outputs/outdir' [['of_0_1.out', 'of_0_2.out'], ['of_1_1.out', 'of_1_2.out']]]
    """    
    input_dir = mace_config["InputDir"]
    input_sets = mace_config["InputFiles"].split(";")
    min_domain_size = int(mace_config['MinDomainSize'])
    max_domain_size = int(mace_config['MaxDomainSize'])
    output_dir = mace_config.get("OutputDir")
    mace4exec = mace_config.get('Mace4exe')
    
    if mace_config.get('SkipMace4'):
        skipOrders = [int(x) for x in mace_config.get('SkipMace4').split(",")]
    else:
        skipOrders = list()
    prebuilts = mace_config.get('Mace4Prebuilt')
    if prebuilts:
        for x in prebuilts.split(","):
            shutil.copy(os.path.join(prebuilt_dir, x), output_dir)
        
    # run Mace inputs
    all_outfiles = list()
    for partition_id in range(0, len(input_sets)):
        outfiles, logs = run_mace(mace4exec, skipOrders, partition_id, input_dir, input_sets[partition_id].split(","), min_domain_size, max_domain_size, output_dir, file_basename)
        all_outfiles.append(outfiles)
        with (open(os.path.join("logs", f"{file_basename}_{partition_id}.log" ), "a")) as fp:
            for y in logs:
                fp.write(f"return_code = {y[0]}\n")
                fp.write("".join(y[1:len(logs)+1]))
    
    # Re-group the output file by order size and partition_id
    # e.g original  [[of_2_0.out, of_3_0.out, of_4_0.out], [of_2_1.out, of_3_1.out, of_4_1.out]]
    # e.g. [[of_2_0.out, of_2_1.out], [of_3_0.out, of_3_1.out], [of_4_0.out, of_4_1.out]]
    all_outputfiles = list()
    for order in range(0, len(all_outfiles[0])):
        all_outputfiles.append([all_outfiles[partition_id][order] for partition_id in range(0, len(input_sets))])

    return output_dir, all_outputfiles

__all__ = ["gen_mace_models"]

