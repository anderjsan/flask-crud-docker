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
                    def dockerHome = tool 'docker' // assuming you have 'docker' configured in Jenkins as a tool
                    
                    withEnv(["PATH+DOCKER=${dockerHome}/bin"]) {
                        sh 'docker-compose build'
                    }
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