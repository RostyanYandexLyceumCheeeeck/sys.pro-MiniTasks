#!/bin/bash

count=$1
echo "================ std::sort baseline ================"
g++ -std=c++17 -O3 -DNDEBUG -DSTDSORT lomuto.cpp
./a.out $count
echo "===================================================="
echo

echo "================ Use Hoare partition ==============="
g++ -std=c++17 -O3 -DNDEBUG lomuto.cpp
./a.out $count
echo "===================================================="
echo

echo "= Use Lomuto partition, traditional implementation ="
g++ -std=c++17 -O3 -DNDEBUG -DLOMUTO_BRANCHY lomuto.cpp
./a.out $count
echo "===================================================="
echo

echo "= Use Lomuto partition, branch-free implementation ="
g++ -std=c++17 -O3 -DNDEBUG -DLOMUTO lomuto.cpp
./a.out $count
echo "===================================================="
echo