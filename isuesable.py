# need to write main with input args as datasets
import os
import sys
import argparse
import json
import sys
from glob import glob


if __name__ == '__main__':
    #%% Parse arguments
    parser = argparse.ArgumentParser(description="Data preparation for all datasets")
    parser.add_argument("datasets_path", help=("Path under which to search for datasets. A json configuration file"
                      " it should be the path to search for completed Datsets"))
    args = parser.parse_args()
    print("Searching for datasets ...")
    config_files = glob(os.path.join(args.datasets_path,'**/dataset.json'), recursive=True)
    count=0
    total = 0
    failed = 0
    for config_filename in config_files:
        parent_folder = config_filename.split(os.path.sep)[-2] # if no backslashes at the end
        
        if os.stat(config_filename).st_size == 0:
            print("ERROR : config file is empty, exiting.... ", parent_folder)
            sys.exit()
        with open(config_filename) as json_file:
            config = json.load(json_file)
        if ('is_useable' in config) and config['is_useable']:
            count += 1
            # print("is useable found at:", parent_folder) #if you want to print all useable datasets enable this:
        elif('is_useable' in config):
            print("not useable found at: ", parent_folder)
            failed += 1
        else:
            print("dataset.json file is not as expected at: ", parent_folder)
            failed +=1
        
        total +=1
    
    
    
    print("Completed work\n")
    print("total number of datasets is:", total, "\n")
    print("total number of datasets is useable is:", count,"\n")
    print("total number of datasets is not useable is:", failed,"\n")