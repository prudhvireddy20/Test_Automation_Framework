pipeline {
  agent {
    docker {
      image 'python:3.11-slim'
    }
  }

  environment {
    VENV_DIR = 'venv'
  }

  options {
    buildDiscarder(logRotator(numToKeepStr: '10'))
    timestamps()
  }

  stages {
    stage('Checkout') {
      steps {
        echo 'Checking out source...'
        checkout scm
      }
    }

    stage('Setup Environment') {
      steps {
        echo 'Setting up Python venv and installing dependencies...'
        sh """
          python -m pip install --upgrade pip setuptools wheel
          python -m venv ${VENV_DIR}
          . ${VENV_DIR}/bin/activate
          pip install -r requirements.txt
        """
      }
    }

    stage('Run Automation') {
      steps {
        echo 'Running automation...'
        sh """
          . ${VENV_DIR}/bin/activate
          python main.py --config config.yml
        """
      }
    }
  }

  post {
    success {
      echo 'Pipeline completed successfully'
    }
    failure {
      echo 'Pipeline failed — check console logs'
    }
  }
}
