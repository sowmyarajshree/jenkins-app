pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/sowmyarajshree/jenkins-app.git'
            }
        }
        steps {
                dir('/path/to/your/frappe/bench') {
                    sh 'bench build'
                }
        }
        stage('Test') {
            steps {
                sh 'bench run-tests'
            }
        }
    }
}


  
