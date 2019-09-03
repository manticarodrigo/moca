properties([gitLabConnection('jenkins-gitlab')])

node {
  checkout scm

  sh 'ls -la'
  sh label: 'build db and service'  , script: 'docker-compose build --pull --force-rm --no-cache'
  sh label: 'Start db and service'  , script: 'docker-compose up -d'

  DB_CONNECTION = sh(
    returnStdout: true,
    script: 'docker-compose port moca_db 5432'
  )

  SERVICE_CONNECTION = sh(
    returnStdout: true,
    script: 'docker-compose port moca_service 8000'
  )

  sh label: 'Wait for db'           , script: """./integration/wait-for-it/wait-for-it.sh ${DB_CONNECTION}"""
  sh label: 'Wait for moca service' , script: """./integration/wait-for-it/wait-for-it.sh ${SERVICE_CONNECTION}"""
}
