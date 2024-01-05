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
                script {
                    sh 'docker-compose build -d'
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