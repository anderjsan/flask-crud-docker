pipeline {
    agent { 
        node {
            label 'docker-agent-python'
            }
    }
    triggers {
        pollSCM '* * * * *'
    }
    environment {
        COMPOSE_NAME = 'docker-compose.yml'  // Nome do arquivo docker-compose
        IMAGE_NAME = 'jenkins-101-jenkins-builder'
        IMAGE_TAG = 'latest'
    }
    stages {
        stage('Build') {
            steps {
                // echo "Building.."
                // sh '''
                // echo "doing build stuff.."
                // echo "vamos ver se se do jeito que está funciona?"
                // docker --version
                // '''
                docker.build("${IMAGE_NAME}:${IMAGE_TAG}")
            }
        }
        stage('Test') {
            steps {
                echo "Testing.."
                sh '''
                echo "doing test stuff.."
                docker --version
                '''
            }
        }
        stage('Deliver') {
            steps {
                echo 'Deliver....'
                sh '''
                echo "doing delivery stuff.."
                python --version
                '''
            }
        }
    }
}