# CCBDA-Project

## Directories
* lambdaScripts -> Contain the code and zip files for each lambda function used in the
project, zip file provides an easy way to deploy a given function.
  
* scripts -> scripts used in EC2 instances for creating the service that will run
4 workers instance at system startup

* simulation -> Contain the base py files used for instantiating the simulation. There is a
`Test.py` that allows us to run the simulation in local, used for debugging before doing the cloud
  deployment.