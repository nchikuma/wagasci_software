#!/bin/sh

inputfile=$1
outputfile=${inputfile//eps/png}
case "${inputfile}" in
*\.eps)
  GS="gs -dBATCH -dNOPAUSE -dEPSCrop -r${2}x${3} -sDEVICE=png16m -sOutputFile=${outputfile} -f ${inputfile}"
  $GS >> /dev/null
  ;;
*)
  echo "Not eps file"
  ;;
esac
