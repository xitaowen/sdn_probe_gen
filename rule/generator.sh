#!/bin/bash
CUR=./
DB=./../classbench/

if [ "$#" -ne 2 ]; then
    exit
fi
FILE=$1
SIZE=$2
FOLD=./data
TARGET=./../data
TARGET=${TARGET}/${FILE}
FILE=${FOLD}/${FILE}
rm -f ${FILE}_0
rm -f ${FILE}_1
rm -f ${FILE}_2
rm -f ${FILE}_3
rm -f ${FILE}_4
rm -f ${FILE}_5
rm -f ${FILE}_6
${DB}db_generator -bc ${DB}parameter_files/fw4_seed ${SIZE} 2 -0.5 -1.0 ${FILE}_0
#echo ${DB}db_generator -bc ${DB}parameter_files/fw4_seed ${SIZE} 2 -0.5 0.1 ${FILE}_0
python ${CUR}change.py ${FILE}_0 ${FILE}_1
python ${CUR}sort.py ${FILE}_1 ${FILE}_2
python ${CUR}dag_generator.py ${FILE}_2 > ${FILE}_3
python ${CUR}combine.py ${FILE}_2 ${FILE}_3 ${FILE}_4
python ${CUR}rulemissing.py ${FILE}_2 ${FILE}_3 ${FILE}_5
python ${CUR}outOfOrder.py ${FILE}_2 ${FILE}_3 ${FILE}_6
cp -f ${FILE}_4 ${TARGET}
cp -f ${FILE}_5 ${TARGET}.miss
cp -f ${FILE}_6 ${TARGET}.order
