pipeline {
    agent { 
        node {
            label 'docker-agent-python'
            }
    }
    triggers {
        pollSCM '* * * * *'
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
                def imageName = 'jenkins-101-jenkins-builder'
                def imageTag = 'latest'
                docker.build("${imageName}:${imageTag}")
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