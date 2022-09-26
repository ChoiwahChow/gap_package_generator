# gap_package_generator

This python package generates gap libraries for a given input file in the Mace4 input FOL format.  The output is a gap package, with documentation.

## File structures

Under the top directory, there are `inputs` directory that holds all Mace4 input files.

## Run the script

In the following example, `semi.ini` is a configuration file containing all the input parameters and options for running the script.
The system will automatically generate the required working and outputs directories.

At the top directory, run the command:

```text
./src/gen_gap/gap_gen.py semi.ini
```