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
            withCredentials([string(credentialsId: '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', variable: 'TOKEN')]) {
                // Checkout 'master' branch
                sh 'git checkout master'
                
                // Merge 'origin/dev' into 'master'
                sh 'git merge origin/dev'

                // Push changes to 'master' with token credentials
                sh "git push https://${TOKEN}@github.com/GidonAniz/Jenkins-ci-cd.git master"
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
