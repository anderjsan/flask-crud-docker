pipeline{
    agent any

    stages {
        stage ('Inicial'){
            steps {
                echo 'iniciando a pipeline'
            }
        }
        stage ('Limpeza'){
            steps {
                echo 'Limpando a Pasta Workspace. Vamos ver se funciona'
                deleteDir()
            }
        }
    }
}