pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                sh '''
                python3 -m venv .venv
                . .venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Automation') {
            steps {
                sh '''
                . .venv/bin/activate
                python3 main.py --config config.yml
                '''
            }
        }
    }

    post {
        success {
            echo "Automation completed successfully"
        }
        failure {
            echo "Pipeline failed — Check logs"
        }
    }
}
