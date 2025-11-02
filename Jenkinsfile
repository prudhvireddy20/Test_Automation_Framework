pipeline {
  agent {
    docker {
      image 'python:3.11-slim'
    }
  }

  environment {
    VENV_DIR = 'venv'
    PIP_CACHE_DIR = "${WORKSPACE}/.pip_cache"
  }

  options {
    timestamps()
    buildDiscarder(logRotator(numToKeepStr: '10'))
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Setup Environment') {
    steps {
        sh '''
            echo "Creating virtual environment..."
            python -m venv venv

            echo "Activating venv and installing dependencies..."
            . venv/bin/activate

            # Ensure pip cache is in a writable location
            mkdir -p ${WORKSPACE}/.cache
            export XDG_CACHE_HOME=${WORKSPACE}/.cache

            # Upgrade pip *inside* venv
            python -m pip install --upgrade pip setuptools wheel --no-cache-dir

            # Install project requirements
            pip install --no-cache-dir -r requirements.txt

            # Verify environment
            python --version
            pip list
        '''
    }
}


    stage('Run Automation') {
      steps {
        sh '''
          . ${VENV_DIR}/bin/activate
          python main.py --config config.yml
        '''
      }
    }
  }

  post {
    success {
      echo "Pipeline succeeded"
      archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
    }
    failure {
      echo "Pipeline failed — see console for details"
      archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
    }
  }
}
