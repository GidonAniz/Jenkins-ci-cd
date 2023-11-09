pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    sh 'pip install -r Jenkins-ci-cd/python/requirements.txt --target ./pip_cache'
                }
            }
        }

        stage('Linting') {
            steps {
                script {
                    sh 'pylint Jenkins-ci-cd/python/app.py'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t my-python-app:${BUILD_NUMBER} -f Dockerfile ."
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    sh "docker push my-python-app:${BUILD_NUMBER}"
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
