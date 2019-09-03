properties([gitLabConnection('jenkins-gitlab')])

node {
  checkout scm

  environment {
    PATH = './integration/wait-for-it:$PATH'
  }

  sh 'ls -la'
  sh label: 'build db and service'  , script: 'docker-compose build --pull --force-rm --no-cache'
  sh label: 'Start db and service'  , script: 'docker-compose up --force-recreate'

  DB_CONNECTION = sh(
    returnStdout: true,
    script: 'docker-compose port moca_db 5432'
  )

  SERVICE_CONNECTION = sh(
    returnStdout: true,
    script: 'docker-compose port moca_service 8000'
  )

  sh label: 'Wait for db'           , script: 'wait-for-it.sh $DB_CONNECTION'
  sh label: 'Wait for moca service' , script: 'wait-for-it.sh $SERVICE_CONNECTION'
}
