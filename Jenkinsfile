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
          args '--network host -v /var/run/docker.sock:/var/run/docker.sock'
        }
      }

      steps {
        script {
          withEnv([
              """service=http://${MOCA_SERVICE}""",
              """service_container=${env.BRANCH_NAME}_${env.BUILD_ID}_moca_service_1""".toLowerCase()]) {

            sh label: 'Wait for db', script: """./integration/wait-for-it/wait-for-it.sh ${DB_SERVICE}"""
            sh label: 'Wait for moca service', script: """./integration/wait-for-it/wait-for-it.sh ${MOCA_SERVICE}"""
            sh label: 'Run all tests', script: "bash -c './integration/run_tests.sh'"
            sh label: 'Generate typescript client library', script: "bash -c 'openapi-generator generate -g typescript-axios -i swagger.yaml --skip-validate-spec -o moca-typescript'"
          }
        }
      }
    }
  }

  post {
    always {
      sh label: 'Tear down everything', script: """${composeCommand} rm -s"""
      sh label: 'Prune networks', script: "docker network prune"
    }

    unsuccessful {
      sh label: 'Service logs', script: """${composeCommand} logs moca_service"""
      sh label: 'DB logs', script: """${composeCommand} logs moca_db"""
    }
  }
}
