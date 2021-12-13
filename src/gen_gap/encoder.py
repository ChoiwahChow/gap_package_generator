"""
This script encodes the models to save space
"""
import os
from ast import literal_eval

conversion = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%&'()*+,-./:;<=>?@[]^_`{|}~"


def encode_a_row(row):
    z = [conversion[x-1] for x in row]
    return ''.join(z)
    
    
def encode_an_algebra(algebra):
    """ encode an algebra which is represented by a list of binary and unary functions. Binary functions are
        represented by a list of lists, and unary function, by a list.
        The encoded string uses the space char, " ", to separate binary/unary operations
    """
    line = []
    for x in algebra:
        if isinstance(x[0], (list, tuple)):
            final = []
            for y in x:
                final.append(encode_a_row(y))
            z = ''.join(final)
        else:
            z = encode_a_row(x)
        line.append(z)
    return '"' + " ".join(line) + '"'


def encode_data(algebraName, non_iso_dir, min_domain_size, max_domain_size):
    """ encode data
    Args:
        algebraName (str): name of algebra
        non_iso_dir (str): directory holding the non-isomorphic models
        min_domain_size (int): starting order
        max_domain_size (int): ending order
    Returns:
    """
    # get all Mace input files

    number_in_orders = []
    for order in range(min_domain_size, max_domain_size+1):
        algebra_count = 0
        source_file = os.path.join(non_iso_dir, f"{algebraName}_{order}.g")
        target_file = os.path.join(non_iso_dir, f"{algebraName}_{order}.txt")
        out_str = []
        with open(source_file) as fp:
            for line in fp:
                algebra_count += 1
                out_str.append(encode_an_algebra(literal_eval(line)))
        algebra_str = ",\n".join(out_str)
        out_str = [f"# order {order}", "[", algebra_str, "]"]
        with open(target_file, "w") as ofp:
            ofp.write("\n".join(out_str))
        
        number_in_orders.append(algebra_count)
            
    return number_in_orders

__all__ = ["encode_data", "conversion"]
