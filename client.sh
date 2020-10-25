#!/bin/bash
for (( ; ; ))
do
   echo "Hitting url"
   curl http://localhost:5000/200
   sleep 5
   curl http://localhost:5000/503
   sleep 5
   curl http://localhost:5000/metrics
   sleep 10
done
