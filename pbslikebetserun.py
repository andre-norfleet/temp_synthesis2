import sys
import os
#import ruamel.yaml
import yaml
import numpy as np
import random


for i in range(1,31,1):
    for jj in range(1,4,1):

        os.system("betse seed avge_cluster"+str(i)+"_"+str(jj)+".yaml")
        os.system("betse init avge_cluster"+str(i)+"_"+str(jj)+".yaml")
        os.system("betse sim avge_cluster"+str(i)+"_"+str(jj)+".yaml")
        os.system("betse plot sim avge_cluster"+str(i)+"_"+str(jj)+".yaml")