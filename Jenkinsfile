pipeline {
    agent any

 environment {
        GITHUB_APP_CREDENTIALS_ID = 'afe25623-3632-4320-ad34-89ce96429f58'
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
                        // Checkout the code using GitHub App credentials
                        checkout([$class: 'GitSCM', 
                                  branches: [[name: '*/master']], 
                                  doGenerateSubmoduleConfigurations: false, 
                                  extensions: [[$class: 'CloneOption', 
                                                depth: 1, 
                                                noTags: false, 
                                                shallow: true, 
                                                reference: '/path/to/git/reference']], 
                                  submoduleCfg: [], 
                                  userRemoteConfigs: [[credentialsId: GITHUB_APP_CREDENTIALS_ID, 
                                                      url: 'https://github.com/GidonAniz/Jenkins-ci-cd.git']]])

                        // Configure Git user identity
                        sh 'git config user.email "Gidon.Aniz@gmail.com"'
                        sh 'git config user.name "G.A"'

                        sh 'git merge --allow-unrelated-histories origin/dev'

                        // Merge 'origin/dev' into 'master'
                        sh 'git merge origin/dev'

                        // push changes to 'master'
                         sh "git push https://${GidonAniz}:${afe25623-3632-4320-ad34-89ce96429f58}@github.com/GidonAniz/Jenkins-ci-cd.git master"
                    } catch (Exception e) {
                        // Handle merge failure or check failures
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
