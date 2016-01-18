#!/bin/bash
CUR=./
DB=./../classbench/

if [ "$#" -ne 1 ]; then
    exit
fi
FILE=$1
FOLD=./data
TARGET=./../data
TARGET=${TARGET}/${FILE}
FILE=${FOLD}/${FILE}
rm -f ${FILE}_1.miss
rm -f ${FILE}_2.miss
rm -f ${FILE}_4.miss
rm -f ${FILE}_8.miss
rm -f ${FILE}_16.miss
rm -f ${FILE}_32.miss
#echo ${DB}db_generator -bc ${DB}parameter_files/fw4_seed ${SIZE} 2 -0.5 0.1 ${FILE}_0
python ${CUR}mrulemissing.py ${FILE}_2 ${FILE}_3 ${FILE}_1.miss 1
python ${CUR}mrulemissing.py ${FILE}_2 ${FILE}_3 ${FILE}_2.miss 2
python ${CUR}mrulemissing.py ${FILE}_2 ${FILE}_3 ${FILE}_4.miss 4
python ${CUR}mrulemissing.py ${FILE}_2 ${FILE}_3 ${FILE}_8.miss 8
python ${CUR}mrulemissing.py ${FILE}_2 ${FILE}_3 ${FILE}_16.miss 16
python ${CUR}mrulemissing.py ${FILE}_2 ${FILE}_3 ${FILE}_32.miss 32
cp -f ${FILE}_1.miss ${TARGET}_1.miss
cp -f ${FILE}_2.miss ${TARGET}_2.miss
cp -f ${FILE}_4.miss ${TARGET}_4.miss
cp -f ${FILE}_8.miss ${TARGET}_8.miss
cp -f ${FILE}_16.miss ${TARGET}_16.miss
cp -f ${FILE}_32.miss ${TARGET}_32.miss
