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
            }
        }
        stage('Execute New Version Tag') {
            steps {
                script {
                    echo 'Executing New Version Tag Commands'
                    sh 'export PROJECT=$JOB_NAME'
                    sh 'curl -X POST http://version-control:4005/$JOB_NAME/tag'
                    def tag = sh(script: 'cat /var/jenkins_home/.version/$JOB_NAME/.version', returnStdout: true).trim()
                    env.TAG = tag // Defina o valor da variável TAG globalmente
                    env.PROJECT = env.JOB_NAME
                    echo "Project: ${env.PROJECT}; Version: ${env.TAG}"
                }
            }
        }
        stage('Stop Current Containers'){
            steps {
                script {

                    echo 'Stopping Current Containers'
                    withEnv(["TAG=${env.TAG}"]) {
                        sh 'docker-compose down'
                    }
                }
                script {
                    echo 'Stopping Current Containers'
                }
            }
        }

        stage('Build Docker Compose') {
            steps {
                script {
                    echo 'Building new Containers with Docker Compose'
                    withEnv(["TAG=${env.TAG}"]) {
                        sh 'docker-compose build'
                    }
                }
            }
        }

        stage('Run Docker Compose') {
            steps {
                script {
                    echo 'Running Docker Compose'
                    withEnv(["TAG=${env.TAG}"]) {
                        sh 'echo TAG: ${TAG}' // Use echo para imprimir a variável TAG
                        sh 'docker-compose up -d'
                    }
                }
            }
        }
        stage('Prune') {
            steps{
                script{
                    echo 'Clean unused assets on docker'
                }
                script{
                    sh 'docker system prune -f'
                }
            }
        }
        stage('Finish') {
            steps {
                script {
                    echo 'Finishing Jenkins Pipeline'
                }
            }            
        }
    }
}