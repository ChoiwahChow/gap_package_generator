#!/usr/bin/python3

"""

This script reads Mace4 outputs from a list of files and writes the multiplication tables out in 
the gap standard format, i.e start with 1 instead of 0.  Each line in the output is 
one multiplication table.  It looks for each "numfuncs" of function/relation outputs in the
mace outputs to form one model.

"""

import os

INTERP_HEADER = "interpretation"
ISOFILTER_SUMMARY = "% isofilter"

binop = "(_,_),"
unop = "(_),"
function = "function("
zeroop2 = ", ["


def find_function_name(line, funcs):
    pos_left = line.find("(")
    pos_right = line.find("(", pos_left+1)
    func_name = line[pos_left+1 : pos_right]
    funcs.append(func_name)


def is_function_line(line, find_functions, funcs):
    if not function in line:
        return 0 

    if binop in line:
        if find_functions:
            find_function_name(line, funcs)
        return 1
    elif unop in line:
        if find_functions:
            find_function_name(line, funcs)
        return -1
    elif zeroop2 in line:
        return -2
    
    return 0


def write_model(ofp, model):
    if model:
        ofp.write(f"{str(model).replace(' ', '')}\n")
    model.clear()
    

def extract_mace_models(input_files, ofp, func_names, ignore_constants=True):
    """ extracts all the models in mace output file given as "input_file", and write them out in gap format to 
        output file.
        Gap starts elements from 1, Mace starts with 0, so we add 1 to Mace outputs to give Gap outputs
        
        Args:
        input_files (iterator, list[str]): input file paths
        ofp (file pointer): output file pointer
        func_names (list): in/out param, if it is empty on input, it will be filled on output
        ignore_constants (bool): do not output constants if true
        
        Returns:
            (int): total number of models written.
    """
    model_count = 0

    if not func_names:
        find_functions = True
    else:
        find_functions = False
    for ifile in input_files:
        with open(ifile) as ipf:
            in_model = False
            model = list()
            complete_model = list()
            is_end = False
            
            for line in ipf:
                if ")." in line:
                    is_end = True
                    find_functions = False
                
                if line.startswith(ISOFILTER_SUMMARY):
                    continue
                # unary models has func_number < 0, binary, > 0, and 0 if not a model
                func_number = is_function_line(line, find_functions, func_names)
                if ignore_constants and func_number == -2:
                    if is_end:
                        write_model(ofp, complete_model)
                        is_end = False
                        model_count += 1
                    continue
                if func_number > 0:   # binary op, in 2-d arrays, multiple lines
                    in_model = True
                elif (in_model or func_number < 0 ) and "])" in line:  # unary op or constant, all in one line
                    in_model = False
                    line = line.split("])")[0]
                    if func_number < 0:
                        line = line.split("[")[1]
                        model = [int(x)+1 for x in line.strip().split(',')]
                    else:
                        model.append([int(x)+1 for x in line.strip().split(',')])
                    complete_model.append(model)
                    model = list()
                    if is_end:
                        write_model(ofp, complete_model)
                        is_end = False
                        model_count += 1
                elif in_model:
                    model.append([int(x)+1 for x in line.strip().rstrip(',').split(',')])

    ofp.close()
    
    return model_count

__all__ = ["extract_mace_models"]
