#!/usr/bin/env bash
ssh snagulavancha@131.220.233.14 'cd /export/datasets/igg_fruit/processed/SweetPepper/;
for dir in */; do
    hostname
    scp -r -v "$dir"/laser/ snagulavancha@131.220.233.204:/automount_home_students/snagulavancha/test/"$dir"
done'
