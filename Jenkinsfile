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

        stage ('Build') {
            steps {
                                script {
                    // Define a tag para a imagem Docker
                    def dockerTag = "flask_crud_app:0.0.1"
                    
                    // Constrói a imagem Docker usando o Dockerfile no diretório atual
                    sh "echo ${dockerTag} ."
                    sh "ls -l"
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