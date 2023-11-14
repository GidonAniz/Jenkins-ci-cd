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

  stage('Run Docker Container') {
    steps {
        script {
            // Run the Docker container
            sh "docker run gidonan/cicd:${BUILD_NUMBER}"
        }
    }
}

  stage('Merge Dev to Master') {
    steps {
        script {
            try {
                // Checkout 'master' branch
                sh 'git checkout master'

                // Configure Git with personal access token
                sh 'git config credential.helper "!f() { echo password=${afe25623-3632-4320-ad34-89ce96429f58}; }; f"'

                // Merge 'origin/dev' into 'master'
                sh 'git merge origin/dev'

                // Push changes to 'master'
                sh 'git push origin master'
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
