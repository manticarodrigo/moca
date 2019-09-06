properties([gitLabConnection('approdite-gitlab')])

pipeline {
  agent any

  stages {
    stage("Minding my own business here...") {

      steps {
        script {
          checkout scm

          composeCommand = """docker-compose -f ./integration/docker-compose.yml -p ${env.BRANCH_NAME}_${env.BUILD_ID}"""

          gitlabBuilds(builds: ["build", "test"]) {
            stage("build") {
              gitlabCommitStatus("build") {
                sh label: 'build db and service', script: """${composeCommand} build --pull"""
                sh label: 'Start db and service', script: """${composeCommand} up -d"""
              }
            }

            DB_PORT = sh(
              returnStdout: true,
              script: """${composeCommand} port moca_db 5432 | cut -d: -f2"""
            )

            SERVICE_PORT = sh(
              returnStdout: true,
              script: """${composeCommand} port moca_service 8000 | cut -d: -f2"""
            )

            stage("test") {
              gitlabCommitStatus("test") {

                sh label: 'Wait for db', script: """./integration/wait-for-it/wait-for-it.sh localhost:${DB_PORT}"""
                sh label: 'Wait for moca service', script: """./integration/wait-for-it/wait-for-it.sh localhost:${SERVICE_PORT}"""

                sh label: 'Run all tests', script: 'exit 1'
              }
            }
          }
        }
      }
    }
  }

  post {
    always {
      sh label: 'Tear down everything', script: """${composeCommand} rm -s"""
    }
  }
}
