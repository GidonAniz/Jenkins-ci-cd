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
                    // Use Docker Hub credentials
                    withCredentials([usernamePassword(credentialsId: '1496238a-5997-4eeb-a124-459a08a17217', usernameVariable: 'gidonan', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh "docker login -u ${DOCKER_USERNAME} -p ${DOCKER_PASSWORD}"
                        sh "docker build -t your-docker-username/my-python-app:${BUILD_NUMBER} -f Jenkins-ci-cd/python/Dockerfile ."
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    // Use Docker Hub credentials
                    withCredentials([usernamePassword(credentialsId: '1496238a-5997-4eeb-a124-459a08a17217', usernameVariable: 'gidonan', passwordVariable: 'DOCKER_PASSWORD')]) {
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
