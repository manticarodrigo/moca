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
            sh label: 'Run all tests', script: "bash -x './integration/run_tests.sh'"
            sh label: 'Check that swagger file is not changed', script: "git diff --exit-code"
            sh label: 'Compile the client with the generated bindings', script: "bash -c '(cd moca-client; yarn && yarn start & sleep 5; kill %1)'"
          }
        }
      }
    }
  }

  post {
    always {
      sh label: 'Tear down everything', script: """${composeCommand} rm -s"""
      sh label: 'Prune networks', script: "docker network prune -f"
    }

    unsuccessful {
      sh label: 'Service logs', script: """${composeCommand} logs moca_service"""
      sh label: 'DB logs', script: """${composeCommand} logs moca_db"""
    }
  }
}
