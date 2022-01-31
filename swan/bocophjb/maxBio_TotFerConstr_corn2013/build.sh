#!/bin/bash

## This is a shell script to automate building process.
OS=`uname -s`
if ! [ -d build ]
then
  mkdir build
fi
cd build
cmake -DPROBLEM_DIR=.. -DCMAKE_BUILD_TYPE=Release -DSEQUENTIAL=OFF /home/ahaddon/Programs/bocop/BocopHJB-1.1.0-Linux
make -j
cd -
