properties([gitLabConnection('approdite-gitlab')])

pipeline {
  agent any

  stages {
    stage("Build") {
      steps {
        script {
          checkout scm

          composeCommand = """docker-compose -f ./integration/docker-compose.yml -p ${env.BRANCH_NAME}_${env.BUILD_ID}"""

          gitlabBuilds(builds: ["build"]) {
            stage("build") {
              gitlabCommitStatus("build") {
                sh label: 'build db and service', script: """${composeCommand} build --pull"""
                sh label: 'Start db and service', script: """${composeCommand} up -d"""
              }
            }

            DB_SERVICE = sh(
              returnStdout: true,
              script: """${composeCommand} port moca_db 5432"""
            )

            MOCA_SERVICE = sh(
              returnStdout: true,
              script: """${composeCommand} port moca_service 8000"""
            )

          }
        }
      }
    }

    stage("test") {
      agent {
        dockerfile {
          filename 'Dockerfile.tester'
          dir './integration'
        }
      }

      steps {
        script {
          sh label: 'Wait for db', script: """./integration/wait-for-it/wait-for-it.sh ${DB_SERVICE}"""
          sh label: 'Wait for moca service', script: """./integration/wait-for-it/wait-for-it.sh ${MOCA_SERVICE}"""

          withEnv(["""service=http://${MOCA_SERVICE}"""]) {
            sh label: 'Run all tests', script: "tavern-ci integration/tests/test_*.yaml"
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
