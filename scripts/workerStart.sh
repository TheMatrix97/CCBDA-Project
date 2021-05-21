#!/bin/bash

cd /home/ec2-user
rm -rf CCBDA-Project
git clone git@github.com:TheMatrix97/CCBDA-Project.git
cd CCBDA-Project/simulation/
python3 Worker.py & python3 Worker.py & python3 Worker.py & python3 Worker.py
