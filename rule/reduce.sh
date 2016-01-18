#!/bin/bash
CUR=./
DB=./../classbench/

if [ "$#" -ne 2 ]; then
    echo $#
    exit
fi
FILE=$1
SIZE=$2
FOLD=./data
TARGET=./../data
TARGET=${TARGET}/${FILE}
FILE=${FOLD}/${FILE}
python ${CUR}reduce.py ${FILE}_2 ${FILE}.9_2
python ${CUR}reduce.py ${FILE}.9_2 ${FILE}.8_2
python ${CUR}reduce.py ${FILE}.8_2 ${FILE}.7_2
python ${CUR}reduce.py ${FILE}.7_2 ${FILE}.6_2
python ${CUR}reduce.py ${FILE}.6_2 ${FILE}.5_2
python ${CUR}reduce.py ${FILE}.5_2 ${FILE}.4_2
python ${CUR}reduce.py ${FILE}.4_2 ${FILE}.3_2
python ${CUR}reduce.py ${FILE}.3_2 ${FILE}.2_2
python ${CUR}reduce.py ${FILE}.2_2 ${FILE}.1_2
python ${CUR}reduce.py ${FILE}.1_2 ${FILE}.0_2
