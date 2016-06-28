#! /bin/bash


ROOT=~/DirectoryClean_test
ROOT+="$1"
echo "$ROOT"



rm -fr "$ROOT"
mkdir -p "$ROOT"

for i in 1 2 ;do

    mkdir -p "$ROOT/$i"
    fallocate -l 100 "$ROOT/$i/${i}_${1}.a.torrent"
    fallocate -l 8M "$ROOT/$i/delete"
    for j in 'a' 'b' 'c' ;do
        mkdir -p "$ROOT/$i/$j"
        fallocate -l 4 "$ROOT/$i/$j/${i}${j}_${1}.avi"
        fallocate -l 101M "$ROOT/$i/$j/keep"

    done

done







