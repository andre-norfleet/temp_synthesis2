import sys, os, errno
import yaml
import re
from shutil import copyfile
from xml.dom import minidom

import numpy as np

# Base config file, determines which conditions we're creating for sims and subsequent classes
with open('iPSC_cluster2316.yaml') as fp:
    config = yaml.load(fp, Loader=yaml.FullLoader)

def main():
    args = read_args()
    diffusivityparams = configure_diffusivity_const()

    model_file = config

    configure_yaml_model(args, model_file, diffusivityparams)

    run_model(model_file)

def make_sure_path_exists(path):

    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def read_args():

    parser = argparse.ArgumentParser(description=\
    "This is an extended BETSE Model that captures bioelectric pattern emergence in hiPSCs.\n")

    parser.add_argument("Dm_K",
                        help="Diffusivity constant 1.{Dm_K,Dm_Na,Dm_Cl}",
                        type=str)
    parser.add_argument('value_1',
                        help='randomized value for Dm_K[1e-19,1e-16]',
                        type=str)
    parser.add_argument("Dm_Na",
                        help="Diffusivity constant 1.{Dm_K,Dm_Na,Dm_Cl}",
                        type=str)
    parser.add_argument('value_2',
                        help='randomized value for Dm_Na[1e-19,1e-17]',
                        type=str)
    parser.add_argument("Dm_Cl",
                        help="Diffusivity constant 1.{Dm_K,Dm_Na,Dm_Cl}",
                        type=str)
    parser.add_argument('value_3',
                        help='randomized value for Dm_Cl[1e-19,1e-17]',
                        type=str)

    args = parser.parse_args()
    return args

def configure_diffusivity_const():

    C = {}

    C['Dm_K'] = config['tissue profile definition']['tissue']['default']['diffusion constants']['Dm_K']
    C['Dm_Na'] = config['tissue profile definition']['tissue']['default']['diffusion constants']['Dm_Na']
    C['Dm_Cl'] = config['tissue profile definition']['tissue']['default']['diffusion constants']['Dm_Cl']

    return C

def configure_yaml_model(args, model_file, diffusivityparams):
    output_folder = "%s_%s_%s_%s_%s_%s" % (args.Dm_K,args.value_1,args.Dm_Na,args.value_2,args.Dm_Cl,args.value_3)

    output_folder_prefix = "simulations"
    output_folder = os.path.join(output_folder_prefix,output_folder) #prefix folder

    make_sure_path_exists(output_folder)
    copyfile(model_file, os.path.join(output_folder,model_file))
    os.chdir(output_folder)

    change_yaml(args,model_file,diffusivityparams)

def change_yaml(args,model_file,diffusivityparams):

    setattr(C['Dm_K'], 'Dm_K', args.value_1)
    setattr(C['Dm_Na'], 'Dm_K', args.value_2)
    setattr(C['Dm_Cl'], 'Dm_K', args.value_3)

    with open("iterativerun.yaml", "w") as f:
        yaml.dump(model_file, f, sort_keys=False)

def run_model(model_file):
    os.system("module load anaconda3")
    os.system("conda env list")
    os.system("source activate dnorfleetbetse")
    os.system("betse seed iterativerun.yaml")
    os.system("betse init iterativerun.yaml")
    os.system("betse sim iterativerun.yaml")
    os.system("betse plot sim iterativerun.yaml")

if __name__ == "__main__":
    main()



    
