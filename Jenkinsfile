pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/sowmyarajshree/jenkins-app.git'
            }
        }
        stage('Build') {
            steps {
                sh 'bench build'
            }
        }
    }
}


  
