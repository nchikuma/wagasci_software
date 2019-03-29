#! /usr/bin/sh

str=$1
hex=$(for x in $(echo ${str} | grep -o '.');do printf "\\\\x%2X" \"$x; done) \
      && echo $hex
