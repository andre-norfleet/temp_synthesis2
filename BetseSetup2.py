import sys, os, errno
import argparse
import yaml
import re
from shutil import copyfile
from shutil import copytree
from xml.dom import minidom

import numpy as np

# Base config file, determines which conditions we're creating for sims and subsequent classes
with open('iPSC_cluster2356.yaml') as fp:
    config = yaml.load(fp, Loader=yaml.FullLoader)

def main():
    args = read_args()
    diffusivityparams = configure_diffusivity_const()

    model_file = 'iPSC_cluster2356.yaml'

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
                        type=float)
    parser.add_argument("Dm_Na",
                        help="Diffusivity constant 1.{Dm_K,Dm_Na,Dm_Cl}",
                        type=str)
    parser.add_argument('value_2',
                        help='randomized value for Dm_Na[1e-19,1e-17]',
                        type=float)
#    parser.add_argument("Dm_Cl",
#                        help="Diffusivity constant 1.{Dm_K,Dm_Na,Dm_Cl}",
#                        type=str)
#    parser.add_argument('value_3',
#                        help='randomized value for Dm_Cl[1e-19,1e-17]',
#                        type=float)
#    parser.add_argument("gj_sa",
#                        help="Diffusivity constant 1.{Dm_K,Dm_Na,Dm_Cl}",
#                        type=str)
#    parser.add_argument('value_4',
#                        help='randomized value for gap junction surface area[1e-7,1e-9]',
#                        type=float)

    parser.add_argument('try_number',
                        help='try attempt number for averageScore [1-3]',
                        type=str)

    args = parser.parse_args()
    return args

def configure_diffusivity_const():

    C =  {}  

    C['Dm_Kr'] = config['tissue profile definition']['tissue']['default']['diffusion constants']['Dm_K']
    C['Dm_Nar'] = config['tissue profile definition']['tissue']['default']['diffusion constants']['Dm_Na']
    C['Dm_Clr'] = config['tissue profile definition']['tissue']['default']['diffusion constants']['Dm_Cl']
    C['gap junction surface area'] = config['variable settings']['gap junctions']['gap junction surface area'] #**** new

    return C

def configure_yaml_model(args, model_file, diffusivityparams):
#    with open('iPSC_cluster2356.yaml') as fp:
#        config = yaml.load(fp, Loader=yaml.FullLoader)

#    output_folder = "%s_%s_%s_%s_%s_%s_%s_%s_%s" % (args.Dm_K,args.value_1,args.Dm_Na,args.value_2,args.Dm_Cl,args.value_3,args.gap_junction_surface_area,args.value_4,args.try_number)
    output_folder = "%s_%s_%s_%s_%s" % (args.Dm_K,args.value_1,args.Dm_Na,args.value_2,args.try_number)
    output_folder_prefix = "simulations"
    output_folder = os.path.join(output_folder_prefix,output_folder) #prefix folder

    make_sure_path_exists(output_folder)
    #copyfile('/storage/scratch1/5/dnorfleet7/my_simdre2/Multicellular-Pattern-Synthesis/temp_synthesis/square1.png', os.path.join(output_folder,'square1.png'))
    copyfile(model_file, os.path.join(output_folder,model_file))
    copytree("/storage/scratch1/5/dnorfleet7/my_simdre2/Multicellular-Pattern-Synthesis/temp_synthesis/geo", os.path.join(output_folder,"geo"), dirs_exist_ok=True)
    os.chdir(output_folder)

    change_yaml(args,model_file,diffusivityparams)

def change_yaml(args,model_file,diffusivityparams):

    #testchange = int(args.value_1)
    #print(testchange)
    #print(testchange.type)
    config['tissue profile definition']['tissue']['default']['diffusion constants']['Dm_K'] = float(args.value_1)
    config['tissue profile definition']['tissue']['default']['diffusion constants']['Dm_Na'] = float(args.value_2)
    #config['tissue profile definition']['tissue']['default']['diffusion constants']['Dm_Cl'] = float(args.value_3)
    #config['variable settings']['gap junctions']['gap junction surface area'] = float(args.value_4) #*********new

    #config['tissue profile definition']['tissue']['default']['diffusion constants']['Dm_K'] = float(args.value_1)
    #config['tissue profile definition']['tissue']['default']['diffusion constants']['Dm_Na'] = int(args.value_2)
    #config['tissue profile definition']['tissue']['default']['diffusion constants']['Dm_Cl'] = int(args.value_3)
    #setattr(C['Dm_Cl'], 'Dm_K', args.value_3)

    with open("iPSC_cluster2356.yaml", "w") as f:
        yaml.dump(config, f, sort_keys=False)

def run_model(model_file):
    #os.system("module load anaconda3")
    #os.system("conda env list")
    #os.system("source activate dnorfleetbetse")
    os.system("betse seed iPSC_cluster2356.yaml")
    os.system("betse init iPSC_cluster2356.yaml")
    os.system("betse sim iPSC_cluster2356.yaml")
    os.system("betse plot sim iPSC_cluster2356.yaml")

if __name__ == "__main__":
    main()
