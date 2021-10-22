#!/usr/bin/env bash

# reading files
swl_names=$(ls *.swl)
swl=($swl_names)
bag_names=$(ls *.bag)

#ask which folder to move data in terminal
# read -p "Please Enter Path: " path
path=/automount_home_students/snagulavancha/Desktop/data_directory

# creating folders
for i in "${swl[@]}";do
  echo "$i"
  current_folder=${i%.*}
  DIR="$path""/"$current_folder
  if [ -d "$DIR" ]; then
    #Do not Take action if $DIR exists ###
    continue
    echo "${DIR} already exists, so skipping it"
  else
    ###  Control will jump here if $DIR does NOT exists ###
    mkdir -p "$path""/"$current_folder
    mkdir -p "$path""/"$current_folder/laser
    mkdir -p "$path""/"$current_folder/realsense
    mkdir -p "$path""/"$current_folder/tf

    #coping files
    cp -n ${swl[0]} "$path""/"$current_folder/laser/
    cp -n intrinsic.json "$path""/"$current_folder/realsense/
    cp -n config.json "$path""/"$current_folder/realsense/
    cp -n tsdf_pipeline.json "$path""/"$current_folder/realsense/
    cp -n dataset.json "$path""/"$current_folder/
    cp -n p.json "$path""/"$current_folder/realsense/
    mv "$path""/"$current_folder/realsense/p.json "$path""/"$current_folder/realsense/"$current_folder".json

    #finding corresponding bag file
    bag=$current_folder.bag

    #check if bag exisits and copying it
    if echo "$bag_names" | grep -q "$bag"; then
      cp -n $bag "$path""/"$current_folder/realsense
   
    else
      echo "no matching bag file found for $currentfolder";
    fi
    echo "$current_folder succesfull"
  fi
done






