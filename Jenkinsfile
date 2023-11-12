pipeline {
    agent any

    environment {
        PATH = "$PATH:/usr/local/bin/helm" // Adjust to the actual Helm binary path
    }

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
                    sh '. venv/bin/activate && pip install -r python/requirements.txt --target ./pip_cache'
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
                    withCredentials([usernamePassword(credentialsId: 'c92d3aa8-67ab-4cf2-b3c6-a5e67285ed2d', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        // Log in to Docker securely
                        sh """
                        echo \${DOCKER_PASSWORD} | docker login -u \${DOCKER_USERNAME} --password-stdin
                        """
                        // Build the Docker image
                        sh "docker build -t gidonan/cicd:${BUILD_NUMBER} -f python/Dockerfile ."
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    // Use Docker Hub credentials
                    withCredentials([usernamePassword(credentialsId: 'c92d3aa8-67ab-4cf2-b3c6-a5e67285ed2d', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
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

      stage('Merge and Push Changes') {
            steps {
                script {
                    try {
                        // Merge 'dev' into 'master'
                        sh 'git checkout master'
                        sh 'git merge origin/dev'

                        // Push changes to 'master' with credentials
                        withCredentials([usernamePassword(credentialsId: 'c9a05144-5c1c-49b0-9786-ea924eeee2dd', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                            sh "git config --global credential.helper store"
                            sh "git push https://$USERNAME:$TOKEN@github.com/GidonAniz/Jenkins-ci-cd.git master"
                        }
                    } catch (Exception e) {
                        error "Error occurred while merging branches: ${e.message}"
                    }
                }
            }
        }
    }
        
    post {
        always {
            script {
                catchError {
                    // Ensure cleanup even on failure
                    sh 'git reset --hard HEAD' // Reset in case of failed merge
                }
            }
        }
        success {
            script {
                echo 'Merging and push successful'
            }
        }
        failure {
            echo 'Merging or push failed'
        }
    }
}
