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
          # ensure a writable pip cache in workspace
          mkdir -p "${PIP_CACHE_DIR}"
          export XDG_CACHE_HOME="${PIP_CACHE_DIR}"

          # create venv first (this will be owned by the current user)
          python -m venv ${VENV_DIR}

          # activate venv and upgrade pip inside the venv, then install requirements
          . ${VENV_DIR}/bin/activate
          python -m pip install --upgrade pip setuptools wheel --no-cache-dir
          pip install --no-cache-dir -r requirements.txt

          # sanity: print python & pip locations and versions
          which python
          python --version
          which pip
          pip --version
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
