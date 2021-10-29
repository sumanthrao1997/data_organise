#!/usr/bin/bash
#this file will change the dataset.josn as the given input in the selcted folders

#read all the foders
dir_names=$(ls -d */)
dir=($dir_names)


#ask for json input
echo "give your json text here"
touch custom_dataset.json
gedit custom_dataset.json

#building zenity list
count=1
zenity_list=()

for i in "${dir[@]}";
do
    zenity_list+=($count)
    zenity_list+=($i)
    let count++
    
done

echo ${zenity_list[@]}

# cat custom_dataset.json

#want to edit folder lists
folder_list=$(zenity --list --title="select the folders where you want to change the dataset.json file" --checklist --column="select"  --column="device" ${zenity_list[@]} 2>/dev/null)
folder=${folder_list//[|]/ }
folders=($folder)

for i in "${folders[@]}";
do
cp -f custom_dataset.json "$i"/dataset.json
done
rm -r custom_dataset.json
echo "finished changing the datset file in folders :"
echo $folder
