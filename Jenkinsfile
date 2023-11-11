pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                script {
                    sh 'apt-get update'
                    sh 'apt-get install -y python3-venv'
                    sh 'python3 -m venv venv'
                    sh '. venv/bin/activate && pip install pylint'
                }
            }
        }

        stage('Install Python Dependencies') {
            steps {
                script {
                    sh '. venv/bin/activate && pip install -r  python/requirements.txt --target ./pip_cache'
                    // Install boto3
                    sh '. venv/bin/activate && pip install boto3'
                }
            }
        }

          stage('Linting') {
            steps {
                script {
                    sh '. venv/bin/activate && pylint python/app.py || true'
                }
            }
        }

        stage('Build Docker Image') {
    steps {
        script {
            // Use Docker Hub credentials
            withCredentials([usernamePassword(credentialsId: 'b5aaf9cd-ea18-4141-a22f-59f07ed41b2c', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                // Log in to Docker securely
                sh """
                echo \${DOCKER_PASSWORD} | docker login -u \${DOCKER_USERNAME} --password-stdin
                """
                // Build the Docker image
                sh "docker build -t gidonan/cicd:${BUILD_NUMBER} -f Jenkins-ci-cd/python/Dockerfile ."
            }
        }
    }
}

       stage('Push Docker Image') {
    steps {
        script {
            // Use Docker Hub credentials
            withCredentials([usernamePassword(credentialsId: 'b5aaf9cd-ea18-4141-a22f-59f07ed41b2c', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                // Log in to Docker securely
                sh """
                echo \${DOCKER_PASSWORD} | docker login -u \${DOCKER_USERNAME} --password-stdin
                """
                // Push the Docker image
                sh "docker push gidonan/cicd:${BUILD_NUMBER}"
            }
        }
    }
}


        stage('Helm Deploy') {
            steps {
                script {
                    sh "helm upgrade my-python-app my-python-app/ --set image.tag=${BUILD_NUMBER}"
                }
            }
        }
    }

    post {
        success {
            script {
                sh 'git checkout master'
                sh 'git merge dev'
                sh 'git push origin master'
            }
        }
    }
}
