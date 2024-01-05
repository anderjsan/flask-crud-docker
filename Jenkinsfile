pipeline{
    agent any

    stages {
        stage ('Inicial'){
            steps {
                echo 'Iniciando a pipeline'
            }
        }
        stage ('Limpeza'){
            steps {
                echo 'Limpando a Pasta Workspace. Vamos ver se funciona'
                deleteDir()
            }
        }

        stage('Build') {
            steps {
                echo 'Iniciando o Build'
                script {
                    dockerapp = docker.build("flask_crud_app:0.0.1", '-f ./Dockerfile ./app')
                }
            }
        }
        

        stage ('Final'){
            steps {
                echo 'Fechando a pipeline'
            }
        }
    }
}