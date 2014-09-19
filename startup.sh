#!/bin/sh
echo "Starting Python NewHolland BeerFinder server"
workon newholland
nohup python ./BeerFinder.py &
echo "NewHolland BeerFinder application is running"