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
                echo "Building.."
                sh '''
                echo "doing build stuff.."
                docker --version
                python3 -m venv py_env
                source py_env/bin/activate
                pip install -r requirements.txt
                #
                sudo service docker status
                #docker build -t anderjsan/flask_crud_app:latest .
                #
                '''
            }
        }
        stage('Test') {
            steps {
                echo "Testing.."
                sh '''
                echo "doing test stuff.."
                docker-compose --version
                '''
            }
        }
        stage('Deliver') {
            steps {
                echo 'Deliver....'
                sh '''
                echo "doing delivery stuff.."
                python3 --version
                '''
            }
        }
    }
}