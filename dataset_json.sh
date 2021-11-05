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
echo "Existing folders in th current directory are as follows:"
echo ${dir[@]}
for i in "${dir[@]}";
do
    zenity_list+=($count)
    zenity_list+=($i)
    let count++
    
done



zenity --question --text "Do you want to make changes to all the folders" 2>/dev/null
		all_folder_check=$?
		if [ $all_folder_check -eq 0 ]
		then
            for i in "${dir[@]}";
                do
                cp -f custom_dataset.json "$i"/dataset.json
                done
                echo "Finished editing the datset.json file in folders :"
                echo ${dir[@]}      
		else
			folder_list=$(zenity --list --title="select the folders where you want to change the dataset.json file" --checklist --column="select"  --column="device" ${zenity_list[@]} 2>/dev/null)
                folder=${folder_list//[|]/ }
                folders=($folder)
				for i in "${folders[@]}";
                do
                cp -f custom_dataset.json "$i"/dataset.json
                done
                echo "Finished editing the datset file in folders :"
                echo ${folders[@]}
		fi
rm -r custom_dataset.json	