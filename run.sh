#!/bin/bash

while true; do
	now=$(date +"%T")
	echo "Trenutno vreme : $now"
	echo "-----------"
	python3 main.py
	sleep 15
	echo "-----------"
done
