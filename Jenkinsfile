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
                }
            }
        }

        stage('Install Python Dependencies') {
            steps {
                script {
                    sh '. venv/bin/activate && pip install -r  python/requirements.txt --target ./pip_cache'
                }
            }
        }

       stage('Linting') {
            steps {
                script {
                    sh '. venv/bin/activate && pip install pylint && pylint python/app.py'
                    sh '. venv/bin/activate && pylint python/app.py'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Use Docker Hub credentials
                    withCredentials([usernamePassword(credentialsId: 'bed587c7-2800-453a-8e8c-4ba1b61611d8', usernameVariable: 'gidon.aniz@gmail.com', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh "docker login -u ${DOCKER_USERNAME} -p ${DOCKER_PASSWORD}"
                        sh "docker build -t gidonan/my-python-app:${BUILD_NUMBER} -f Jenkins-ci-cd/python/Dockerfile ."
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    // Use Docker Hub credentials
                    withCredentials([usernamePassword(credentialsId: 'bed587c7-2800-453a-8e8c-4ba1b61611d8', usernameVariable: 'gidon.aniz@gmail.com', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh "docker push gidonan/my-python-app:${BUILD_NUMBER}"
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
