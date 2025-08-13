pipeline {
  agent any
  environment {
    DOCKERHUB_USER = 'kanavgoyal781'
    IMAGE = "${DOCKERHUB_USER}/cicd-image-privacy-guard"
    VERSION = "${env.BUILD_NUMBER}"
  }
  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
stage('Tests') {
  steps {
    sh '''
      docker run --rm -v ${WORKSPACE}:/src -w /src \
        -e PYTHONPATH=/src \
        python:3.11-slim bash -lc "
          pip install --no-cache-dir -r requirements.txt pytest pillow python-multipart &&
          python -m pytest -q
        "
    '''
  }
}
    stage('Build') {
      steps { sh 'docker build -t $IMAGE:$VERSION -t $IMAGE:latest .' }
    }
    stage('Push') {
      steps {
        withCredentials([usernamePassword(
          credentialsId: 'dockerhub-creds',
          usernameVariable: 'USER', passwordVariable: 'PASS')]) {
          sh 'echo "$PASS" | docker login -u "$USER" --password-stdin'
          sh 'docker push $IMAGE:$VERSION && docker push $IMAGE:latest'
        }
      }
    }
    stage('Deploy') {
      steps {
        sh '''
          docker rm -f privacy-guard || true
          docker run -d --name privacy-guard \
            --restart unless-stopped \
            -p 80:8000 \
            -e APP_VERSION=$VERSION \
            $IMAGE:$VERSION
        '''
      }
    }
  }
}
