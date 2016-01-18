#!/bin/bash
CUR=./
DB=./../classbench/

if [ "$#" -ne 4 ]; then
    exit
fi
METHOD=$1
FILE=$2
NUM=$3
APPEND=$4
FOLD=./data
TARGET=./../data
TARGET=${TARGET}/${FILE}
FILE=${FOLD}/${FILE}
rm -f ${FILE}_${NUM}.${APPEND}
#echo ${DB}db_generator -bc ${DB}parameter_files/fw4_seed ${SIZE} 2 -0.5 0.1 ${FILE}_0
python ${CUR}${METHOD}.py ${FILE}_2 ${FILE}_3 ${FILE}_${NUM}.${APPEND} ${NUM}
cp -f ${FILE}_${NUM}.${APPEND} ${TARGET}_${NUM}.${APPEND}
