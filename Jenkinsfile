pipeline {
    agent any

    stages {
        stage('Start') {
            steps {
                script {
                    echo 'Starting Jenkins Pipeline'
                }
            }            
        }
        stage('Check Docker and Docker Compose and Python Installation ') {
            steps {
                script {
                    try {
                        echo 'Checking Docker'
                        sh 'docker --version'
                        echo 'Docker is installed.'
                    } catch (Exception e) {
                        error 'Docker is not installed. Please install Docker.'
                    }
                    try {
                        echo 'Checking Docker-compose'
                        sh 'docker-compose --version'
                        echo 'Docker Compose is installed.'
                    } catch (Exception e) {
                        error 'Docker Compose is not installed. Please install Docker Compose.'
                    }
                    try {
                        echo 'Checking Python'
                        sh 'python3 --version'
                        echo 'Python is installed.'
                    } catch (Exception e) {
                        error 'Python is not installed. Please install Python.'
                    }
                    try {
                        echo 'Checking Docker Containers'
                        sh 'docker ps'
                        echo 'Docker Containers Listed.'
                    } catch (Exception e) {
                        error 'No Docker Containers found. Please check DinD'
                    }
                }
                script {
                    sleep 3
                }
            }
        }
        stage('Execute New Version Tag') {
            steps {
                script {
                    echo 'Executing New Version Tag Commands'
                    sh 'export PROJECT=$JOB_NAME'
                    sh 'curl -X POST http://version-control:4005/$JOB_NAME/tag'
                    def tag = sh(script: 'cat /var/jenkins_home/.version/$JOB_NAME/.version', returnStdout: true).trim()
                    withEnv(["PROJECT=$JOB_NAME", "TAG=$tag"]) {
                        echo "Project: ${env.PROJECT}; Version: ${env.TAG}"
                    }
                }
            }
        }
        stage('Stop Current Containers'){
            steps {
                script {
                    echo 'docker-compose down'
                    withEnv(["TAG=${env.TAG}"]) {
                        sh 'docker-compose down'
                    }
                }
                script {
                    sleep 10 // Espera um tempo para os contêineres serem Parados completamente
                }
                script {
                    echo 'Stopping Current Containers'
                }
            }
        }

        stage('Build Docker Compose') {
            steps {
                script {
                    echo 'docker-compose build'
                    withEnv(["TAG=${env.TAG}"]) {
                        sh 'docker-compose build'
                    }
                }
                script {
                    sleep 10 // Espera um tempo para os contêineres serem iniciados completamente
                }
            }
        }

        stage('Run Docker Compose') {
            steps {
                script {
                    echo 'docker-compose up -d'
                    withEnv(["TAG=${env.TAG}"]) {
                        sh 'docker-compose up -d'
                    }
                }
                script {
                    sleep 10 // Espera um tempo para os contêineres serem iniciados completamente
                }
            }
        }
        stage('Finish') {
            steps {
                script {
                    echo 'Starting Jenkins Pipeline'
                }
            }            
        }
    }
}