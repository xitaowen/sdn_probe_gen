#!/bin/bash
CUR=./
DB=./../classbench/

if [ "$#" -ne 4 ]; then
    exit
fi
METHOD=$1
FILE=$2
CASE=$3
NUM=$4
APPEND=$5
FOLD=./data
TARGET=./../data
TARGET=${TARGET}/${FILE}
FILE=${FOLD}/${FILE}_${CASE}_${NUM}
rm -f ${FILE}.${APPEND}
#echo ${DB}db_generator -bc ${DB}parameter_files/fw4_seed ${SIZE} 2 -0.5 0.1 ${FILE}_0
${DB}db_generator -bc ${DB}parameter_files/fw4_seed ${SIZE} 2 -0.5 -1.0 ${FILE}_0
#echo ${DB}db_generator -bc ${DB}parameter_files/fw4_seed ${SIZE} 2 -0.5 0.1 ${FILE}_0
python ${CUR}change.py ${FILE}_0 ${FILE}_1
python ${CUR}sort.py ${FILE}_1 ${FILE}_2
while true; do
    python ${CUR}dag_generator.py ${FILE}_2 > ${FILE}_3
    python ${CUR}combine.py ${FILE}_2 ${FILE}_3 ${FILE}_4
    ret=`python preTest.py ${FILE}_4`
    
python ${CUR}dag_generator.py ${FILE}_2 > ${FILE}_3
python ${CUR}${METHOD}.py ${FILE}_2 ${FILE}_3 ${FILE}__${NUM}.${APPEND} ${NUM}
cp -f ${FILE}_${NUM}.${APPEND} ${TARGET}_${NUM}.${APPEND}
