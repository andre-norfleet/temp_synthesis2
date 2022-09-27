import sys
#import ruamel.yaml
import yaml
import numpy as np
import random
import csv
import pandas as pd

#yaml = ruamel.yaml.YAML()
# Base config file, determines which conditions we're creating for sims and subsequent classes
with open('iPSC_cluster2316.yaml') as fp:
    config = yaml.load(fp, Loader=yaml.FullLoader)

wb = pd.read_csv('BETSE Permeability intervals 33.csv')
wb2 = pd.read_csv('BETSE Permeability intervals 34.csv')

new_df = pd.DataFrame(wb)
new_df2 = pd.DataFrame(wb2)
d = new_df['Perm'].tolist()
dd = new_df2['Perm'].tolist()
d4 = random.choices(d, k=31)
d5 = random.choices(dd, k=31)
d6 = random.choices(dd, k=31)
d44 = [int(b) for b in d4]
print(d4)


for i in range(1,31,1):
    for jj in range(1,4,1):

        try:
          config['init file saving']['worldfile'] = 'world_'+str(i)+'.betse'
        except KeyError:
          config['init file saving'] = {'worldfile': 'world_'+str(i)+'.betse'}

        try:
          config['init file saving']['file'] = 'init_'+str(i)+'.betse'
        except KeyError:
          config['init file saving'] = {'file': 'init_'+str(i)+'.betse'}

        try:
          config['sim file saving']['file'] = 'sim_'+str(i)+'.betse.gz'
        except KeyError:
          config['sim file saving'] = {'file': 'sim_'+str(i)+'.betse.gz'}

        try:
          config['results file saving']['init directory'] = 'RESULTS/init_'+str(i)+'_'+str(jj)+''
        except KeyError:
          config['results file saving'] = {'init directory': 'RESULTS/init_'+str(i)+''}

        try:
          config['results file saving']['sim directory'] = 'RESULTS/sim_'+str(i)+'_'+str(jj)+''
        except KeyError:
          config['results file saving'] = {'sim directory': 'RESULTS/sim_'+str(i)+''}

        try:
            config['tissue profile definition']['tissue']['default']['diffusion constants']['Dm_K'] = d4[i]
        except KeyError:
            config['tissue profile definition']['tissue']['default']['diffusion constants'] = {'Dm_K': '2.74384e-17'}

        try:
            config['tissue profile definition']['tissue']['default']['diffusion constants']['Dm_Na'] = d5[i]
        except KeyError:
            config['tissue profile definition']['tissue']['default']['diffusion constants'] = {'Dm_Na': '4.478e-18'}

        try:
            config['tissue profile definition']['tissue']['default']['diffusion constants']['Dm_Cl'] = d6[i]
        except KeyError:
            config['tissue profile definition']['tissue']['default']['diffusion constants'] = {'Dm_Cl': '1.973e-19'}


        with open("avge_cluster"+str(i)+"_"+str(jj)+".yaml", "w") as f:
            yaml.dump(config, f, sort_keys=False)
