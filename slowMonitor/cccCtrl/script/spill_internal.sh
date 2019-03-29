#!/bin/sh

source $(cd $(dirname $0) && pwd)/ccc_setup.sh

${RBCPexe} ${WRITE} ${ADDR} 1 ${DATA} 1
${RBCPexe} ${WRITE} ${ADDR} 1 ${DATA} 1
${RBCPexe} ${WRITE} ${ADDR} 1 ${DATA} 1
