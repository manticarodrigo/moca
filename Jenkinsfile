properties([gitLabConnection('jenkins-gitlab')])

node {
  checkout scm

  environment {
    PATH = './integration/wait-for-it:$PATH'
  }

  sh label: 'build db and service'  , script: 'docker-compose build --no-cache'
  sh label: 'Start db and service'  , script: 'docker-compose up'

  DB_CONNECTION = sh(
    returnStdout: true,
    script: 'docker-compose port db 5432'
  )

  SERVICE_CONNECTION = sh(
    returnStdout: true,
    script: 'docker-compose port moca_service 8000'
  )

  sh label: 'Wait for db'           , script: 'wait-for-it.sh $DB_CONNECTION'
  sh label: 'Wait for moca service' , script: 'wait-for-it.sh $SERVICE_CONNECTION'
}
