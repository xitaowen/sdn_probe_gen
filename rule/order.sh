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
rm -f ${FILE}_1.order
rm -f ${FILE}_2.order
rm -f ${FILE}_4.order
rm -f ${FILE}_8.order
rm -f ${FILE}_16.order
rm -f ${FILE}_32.order
#echo ${DB}db_generator -bc ${DB}parameter_files/fw4_seed ${SIZE} 2 -0.5 0.1 ${FILE}_0
python ${CUR}moutoforder.py ${FILE}_2 ${FILE}_3 ${FILE}_1.order 1
python ${CUR}moutoforder.py ${FILE}_2 ${FILE}_3 ${FILE}_2.order 2
python ${CUR}moutoforder.py ${FILE}_2 ${FILE}_3 ${FILE}_4.order 4
python ${CUR}moutoforder.py ${FILE}_2 ${FILE}_3 ${FILE}_8.order 8
python ${CUR}moutoforder.py ${FILE}_2 ${FILE}_3 ${FILE}_16.order 16
python ${CUR}moutoforder.py ${FILE}_2 ${FILE}_3 ${FILE}_32.order 32
cp -f ${FILE}_1.order ${TARGET}_1.order
cp -f ${FILE}_2.order ${TARGET}_2.order
cp -f ${FILE}_4.order ${TARGET}_4.order
cp -f ${FILE}_8.order ${TARGET}_8.order
cp -f ${FILE}_16.order ${TARGET}_16.order
cp -f ${FILE}_32.order ${TARGET}_32.order
