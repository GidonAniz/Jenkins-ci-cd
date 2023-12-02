# Jenkins-ci-cd
Jenkins-ci-cd - Devops course project

The project built with ...

  1. Python app that:
     1. Running every 5 minutes (configurable via environment variable)
     2. Checking with AWS (using boto) if there are machines up and running with the following tags: --filters "Name=tag:k8s.io/role/master,Values=1"  "Name=instance-state-code,Values=16”
     3.  If there is a response (IP’s) > the app Count them and output to stdout a log line

3. Jenkins pipeline that:
     1. Lint is set to not failing the code but only warning.
     2. Using DSL to build the first job that listens to jenkins pipelines that run in turn the container pipelines.
     3. Build docker image and push it to dockerhub.
     4. Run the docker image and create container on the local machine (continue to run).
     5. If dev branch change and  jenkins tests succeed dev merge to prod.
  
  

     
     
   




