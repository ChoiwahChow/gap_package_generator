#!/usr/bin/python3

"""
"""
import os
import gzip
import stat
import shutil
from string import Template
import subprocess

author_lines = """
  <Author>AuthorN
    <Email>EmailN</Email>
    <Homepage>HomepageN</Homepage>
  </Author>
"""
person_lines ="""
  rec(
    LastName      := "LastNameN",
    FirstNames    := "FirstNameN",
    IsAuthor      := true,
    IsMaintainer  := true,
    Email         := "EmailN",
    WWWHome       := "HomepageN"
  ),
"""


def cp_doc(template_file, out_file):  
    with open(template_file, 'r') as f:
        contents = f.read()
    with open(out_file, "w") as f:
        f.write(contents)


def write_doc(d, template_file, out_file):    
    with open(template_file, 'r') as f:
        src = Template(f.read())
        contents = src.substitute(d)
    with open(out_file, "w") as f:
        f.write(contents)
    

def gen_main_doc(AllPersonsLines, OtherAuthorsLines, OtherAuthorNamesLines, AllAuthorsListString, func_names, gap_doc_templates_dir,
                 gap_top_dir, algebra_names, base_names, display_name_lc, domain_range, prefixes, config):
    """
    Args:
        func_names (List[str]): list of function names (*, v, ^ etc in the Mace4 algebrar definition).
        algebra_names (List[str]): list of algebra names
        base_names (List[str]): list of base names, one for each algebra
        display_name_lc (List[str]):  list of lower case display names
        domain_range (List[List[int])):  list of domain ranges (min, max)
    """
    root_config = config['ROOT']
    input_dir = config['MACE']['InputDir']
    def_files = config['GAP_PACKAGE']['AlgebraDefinitionFiles'].split(":")
    algebra_def = list()
    message = list()
    for x in range(0, len(def_files)):
        with open(os.path.join(input_dir, def_files[x])) as fp:
            algebra_def.append("<P/>".join(fp.read().splitlines()))
        if "," in func_names[x]:
            message.append(f"The output algebra is represented by a list of operation tables. The names of the operations are {func_names[x]} (in this order)")
        else:
            message.append(f"The output algebra is represented by its operation table for {func_names[x]}")
    algebraDisplayNames = root_config['AlgebraDisplayNames'].split(":")
    package_name = root_config['PackageName']
    d = {
        "Author1": root_config['Author1'],
        "Email1": root_config['Email1'],
        "Homepage1": root_config['Homepage1'],
        'MinDomainSize': domain_range[0][0],
        'MaxDomainSize': domain_range[0][1],
        "PackageName": package_name,
        "Version": root_config['Version'],
        "Status": root_config['Status'],
        "CopyrightYear": root_config['CopyrightYear'],
        "PackageWWWHome": root_config['PackageWWWHome'],
        "SourceRepository": root_config['SourceRepository'],
        "DateOfRelease": root_config['DateOfRelease'],
        "OtherAuthorsLines": OtherAuthorsLines,
        "AllPersonsLines": AllPersonsLines,
        "OtherAuthorNamesLines": OtherAuthorNamesLines,
        "AllAuthorsListString": AllAuthorsListString,
        "Prefix": prefixes[0],
        "AlgebraName": algebra_names[0],
        "AlgebraDisplayName": algebraDisplayNames[0],
        "AlgebraDisplayNameLowerCase": display_name_lc[0],
        "FunctionName": f"AllSmall{base_names[0]}",
        "OperationNames": message[0],
        "AlgebraDefinition": algebra_def[0],
        "ALGEBRA_RELATIONSHIP": config['GAP_PACKAGE']['AlgebraRelationship']
    }    
    d['ADDITIONAL_LIBS'] = ""
    d['ADDITIONAL_GD'] = ""
    d['ADDITIONAL_ALGEBRA'] = ""
    d['ADDITIONAL_ALGEBRA_DEFINITION'] = ""
    d['ADDITIONAL_FUNCTIONS'] = ""
    d['ADDITIONAL_ACCESSORS'] = ""
    for pos in range(1, len(prefixes)):
        d['ADDITIONAL_LIBS'] = f'{d["ADDITIONAL_LIBS"]}\nReadPackage( "{package_name}", "lib/{prefixes[pos]}_utils.gi" );\nReadPackage( "{package_name}", "lib/{prefixes[pos]}_small.gi" );\n'
        d['ADDITIONAL_GD'] = f'{d["ADDITIONAL_GD"]}, "../lib/{prefixes[pos]}_small.gd"'
        d['ADDITIONAL_ALGEBRA'] = f'{d["ADDITIONAL_ALGEBRA"]}{algebraDisplayNames[pos]} of orders {domain_range[pos][0]} to {domain_range[pos][1]}.<P/>\n'
        d['ADDITIONAL_ALGEBRA_DEFINITION'] = f'{d["ADDITIONAL_ALGEBRA_DEFINITION"]}\n<Subsection Label = "AlgebraDefinition{pos}">\n  <Heading>Definition of {algebraDisplayNames[pos]}</Heading>\n{algebra_def[pos]}\n</Subsection>\n'
        d['ADDITIONAL_FUNCTIONS'] = f'{d["ADDITIONAL_FUNCTIONS"]}\nAllSmall{base_names[pos]} is an accessor function for accessing the complete list of non-isomorphic {display_name_lc[pos]} models from order {domain_range[pos][0]} to {domain_range[pos][1]}.<P/>\n'
        d['ADDITIONAL_ACCESSORS'] = f'{d["ADDITIONAL_ACCESSORS"]}\n\n<Section Label = "Algebra Functions{pos}"><Heading>Accessing Small {algebraDisplayNames[pos]}</Heading>\nAllSmall{base_names[pos]} is an accessor function for accessing the complete list of non-isomorphic {display_name_lc[pos]} of orders {domain_range[pos][0]} to {domain_range[pos][1]}.\n\n<#Include Label = "AllSmall{base_names[pos]}">\n\n{message[pos]}, as given in Section <Ref Sect="AlgebraDefinition{pos}"/>.</Section>'
    
    doc_files = ['main.xml', 'z-chap01.xml', 'z-chap02.xml', 'title.xml']
    for x in doc_files:
        write_doc(d, os.path.join(gap_doc_templates_dir, 'doc', x),
                  os.path.join(gap_top_dir, 'doc', x))
    
    top_files = ['LICENSE', 'makedoc.g', 'makedocrel.g', 'Makefile.in', 'PackageInfo.g', 'read.g', 'init.g']
    for x in top_files:
        write_doc(d, os.path.join(gap_doc_templates_dir, x),
                  os.path.join(gap_top_dir, x))
    configure_file = os.path.join(gap_top_dir, 'configure')
    cp_doc(os.path.join(gap_doc_templates_dir, 'configure'), configure_file)
    bio_file = os.path.join(gap_top_dir, 'doc', 'bibliography.xml')
    cp_doc(os.path.join(gap_doc_templates_dir, 'doc', 'bibliography.xml'), bio_file)
    st = os.stat(configure_file)
    os.chmod(configure_file, st.st_mode | stat.S_IEXEC)
    
   
def gen_lib_code(author1, OtherAuthorNamesLines, num_in_orders, gap_doc_templates_dir,
                 gap_top_dir, algebra_name, base_name, display_name_lc, domain_range, prefix, config):
    lib_dir = os.path.join(gap_top_dir, 'lib')
    lib_template_dir = os.path.join(gap_doc_templates_dir, 'lib')
    
    d = {
        "FunctionName": f"AllSmall{base_name}",
        "PackageName": config['ROOT']['PackageName'],
        "AlgebraName": algebra_name,
        'MinDomainSize': domain_range[0],
        "MinAlgebraSize": num_in_orders[0],
        "AlgebraDisplayNameLowerCase": display_name_lc,
        "Author1": author1,
        "OtherAuthorNamesLines": OtherAuthorNamesLines,
        "xxx": "$",
        "Prefix": prefix,
        "CopyrightYear": config['ROOT']['CopyrightYear']
    }
    lib_files = ['small.gd', 'small.gi', 'utils.gd', 'utils.gi']
    for x in lib_files:
        write_doc(d, os.path.join(lib_template_dir, x), os.path.join(lib_dir, f"{prefix}_{x}"))


def gen_data_file(OtherAuthorNamesLines, AllAuthorsListString, gap_templates_dir, 
                  gap_top_dir, algebra_name, domain_range, num_in_orders, prefix, config):
    """
        algebra_name (str): name of the (sub)algebra
        domain_range (List[int]): min and max domain sizes
        num_in_orders (List[int]): number of models for each order in the algebra
        prefix (str): prefix to use in naming functions/files for this algebra
    """
    gap_data_dir = os.path.join(gap_top_dir, 'data')
    MinDomainSize = domain_range[0]
    MaxDomainSize = domain_range[1] + 1
    d = {
        "AlgebraName": algebra_name,
        "ImplementedOrders": ", ".join([str(x) for x in range(MinDomainSize, MaxDomainSize)]),
        "NumberInOrders": str(num_in_orders),   # TODO work on this one
        "Prefix": prefix,
        "Author1": config['ROOT']['Author1'],
        "CopyrightYear": config['ROOT']['CopyrightYear'],
        "OtherAuthorNamesLines": OtherAuthorNamesLines,
        "AllAuthorsListString": AllAuthorsListString
    }
    template_data_file = os.path.join(gap_templates_dir, 'data', f'small.tbl')
    data_file = os.path.join(gap_data_dir, f'{prefix}_small.tbl')
    write_doc(d, template_data_file, data_file)
    source_data_dir = config['ROOT']['NonIsoDir']
    with open(data_file, "a") as fp:
        for order in range(MinDomainSize, MaxDomainSize):
            with open(os.path.join(source_data_dir, f"{algebra_name}_{order}.txt")) as ifp:
                g = ifp.read()
            fp.write(g)
            if order < MaxDomainSize-1:
                fp.write(",\n")
        fp.write("\n]];")
        
    compress_file = data_file + ".gz"
    with open(data_file, 'rb') as f_in:
        with gzip.open(compress_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(data_file)


def gen_tst(AllAuthorsListString, algebra_names, base_names, num_in_orders, domain_range, gap_templates_dir, gap_top_dir, config):
    """
    Args:
        algebra_names (List[str]): list of algebra names
        base_names (List[str]): list of base names, one for each algebra
        num_in_orders (List[List[int]]): number of models for each order in the algebra, one list for each algebra
        domain_range (List[List[int]]): min and max domain sizes
    """
    tst_template_dir = os.path.join(gap_templates_dir, 'tst')
    tst_dir = os.path.join(gap_top_dir, 'tst')
    packageName = config['ROOT']['PackageName']
    d = {
        "FunctionName": f"AllSmall{base_names[0]}",
        "PackageName": packageName,
        "AlgebraName": algebra_names[0],
        'MinDomainSize': domain_range[0][0],
        "MinAlgebraSize": num_in_orders[0][0],
        "AllAuthorsListString": AllAuthorsListString
    }
    tst_files = ['quickcheck.g', 'testall.g']
    for x in tst_files:
        write_doc(d, os.path.join(tst_template_dir, x), os.path.join(tst_dir, x))
    write_doc(d, os.path.join(tst_template_dir, 'algebra.tst'), os.path.join(tst_dir, f'{packageName}.tst'))


def gen_package_doc(gap_top_dir, config):
    gap_path = config['ROOT']['GAPPATH']
    subprocess.run(f"cd {gap_top_dir}; ./configure {gap_path}; make > ../logs/configure.log 2>&1", 
                        capture_output=False, text=True, check=True, shell=True)


def authors(config):
    """ generates all the authors-related strings
    """
    OtherAuthorDetails = [x.split(";") for x in config['ROOT']['OtherAuthors'].split("|")]
    author1 = config['ROOT']['Author1']
    if OtherAuthorDetails:
        OtherAuthorNames = [x[0] for x in OtherAuthorDetails]
        OtherAuthorNamesLines = [f'#Y                                                 {x}' for x in OtherAuthorNames]
        OtherAuthorNamesLines = "\n".join(OtherAuthorNamesLines)
        if len(OtherAuthorNames) > 1:
            OtherAuthorNames[-1] = "and " + OtherAuthorNames[-1] # e.g. John doe, Jane Doe, and Sally Doe
        OtherAuthorNamesString = ", ".join(OtherAuthorNames)    # e.g. John Doe, Jane Doe
    else:
        OtherAuthorNamesLines = ""
        OtherAuthorNamesString = ""
        
    if ", " in OtherAuthorNamesString:
        AllAuthorsListString = f"{author1}, {OtherAuthorNamesString}"
    elif OtherAuthorNamesString:
        AllAuthorsListString = f"{author1} and {OtherAuthorNamesString}"
    else:
        AllAuthorsListString = author1
    
    new_authors = list()
    names = author1.split(" ")
    all_persons = [person_lines.replace("LastNameN", names[-1]).replace("FirstNameN", names[0]).\
                   replace("EmailN", config['ROOT']['Email1']).replace("HomepageN", config['ROOT']['Homepage1'])]
    for author in OtherAuthorDetails:
        new_authors.append(author_lines.replace("AuthorN", author[0]).replace("EmailN", author[1]).replace("HomepageN", author[2]))
        names = author[0].split(" ")
        all_persons.append(person_lines.replace("LastNameN", names[-1]).replace("FirstNameN", names[0]).\
                           replace("EmailN", author[1]).replace("HomepageN", author[2]))
    OtherAuthorsLines = "\n".join(new_authors)
    AllPersonsLines = "\n".join(all_persons)

    return author1, AllPersonsLines, AllAuthorsListString, OtherAuthorNamesLines, OtherAuthorsLines
    

def gen_gap_package(algebra_names, base_names, display_names_lc, domain_range, prefixes, num_in_orders, func_names, config):
    """
    Args:
        algebra_names (list): list algebrar names
        base_names (List[str]): list of base names, one for each sub-algebra
        display_names_lc (List[str]): display names of algebrar, in lowe case
        num_in_orders:
        func_names (List(str)):  list of comma-separated list of functions in the definition of the algebra
        config (dict): configurations
    """
    gap_config = config['GAP_PACKAGE']
    gap_top_dir = f"{config['ROOT']['PackageName']}-{config['ROOT']['Version']}"
    gap_templates_dir = gap_config['TemplatesDir']
    
    for x in ['data', 'doc', 'lib', 'tst']:
        os.makedirs(os.path.join(gap_top_dir, x), exist_ok=True)
    
    author1, AllPersonsLines, AllAuthorsListString, OtherAuthorNamesLines, OtherAuthorsLines = authors(config)
  
    gen_main_doc(AllPersonsLines, OtherAuthorsLines, OtherAuthorNamesLines, AllAuthorsListString, func_names, gap_templates_dir,
                 gap_top_dir, algebra_names, base_names, display_names_lc, domain_range, prefixes, config)

    for pos in range(0, len(algebra_names)):
        gen_lib_code(author1, OtherAuthorNamesLines, num_in_orders[pos], gap_templates_dir, gap_top_dir,
                     algebra_names[pos], base_names[pos], display_names_lc[pos], domain_range[pos], prefixes[pos], config)
        gen_data_file(OtherAuthorNamesLines, AllAuthorsListString, gap_templates_dir, gap_top_dir, 
                      algebra_names[pos], domain_range[pos], num_in_orders[pos], prefixes[pos], config)
        

    gen_tst(AllAuthorsListString, algebra_names, base_names, num_in_orders, domain_range, gap_templates_dir, gap_top_dir, config)
    gen_package_doc(gap_top_dir, config);
    

__all__ = ["gen_gap_package"]

