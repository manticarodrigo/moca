properties([gitLabConnection('jenkins-gitlab')])

node {
  checkout scm

  environment {
    PATH = './integration/wait-for-it:$PATH'
  }

  sh label: 'Start db and service'  , script: 'docker-compose up -d'
  sh label: 'Wait for db'           , script: 'wait-for-it.sh localhost:5432'
  sh label: 'Wait for moca service' , script: 'wait-for-it.sh localhost:8000'
}
