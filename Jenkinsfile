pipeline {
    agent any
    tools {  # only 3 tools are supported you can now use them to execute commands say mvn test etc.
        gradle
        mvn
        node
    }
    parameters {
        string(name: 'VERSION',defaultValue: 'abcd',description:'description about var')
        choice(name:'TYPE',choices: ['choice1','cchoice2','choice3'],description:'kdfkjsdfkf')
        booleanParam(name: 'to_test',defaultValue: true ,description:'description')
    }
    environment {
        CUSTOM_VAR = "1.11.11.11"  # defining nv variable which can be used any where in pipeline
        server_creds = credentials('server-cred')  # you can define credentials and access them as env vars
    }
    stages {
        stage("build") {
            steps {
                echo 'simulating build'
                echo "BUILD_ID ${BUILD_ID}"   # using available environment variables
                echo "BUILD_NUMBER ${BUILD_NUMBER}"
                echo "BUILD_TAG ${BUILD_TAG}"
                echo "BUILD_URL ${BUILD_URL}"
                echo "EXECUTOR_NUMBER ${EXECUTOR_NUMBER}"
                echo "JENKINS_URL ${JENKINS_URL}"
                echo "JOB_NAME ${JOB_NAME}"
                echo "NODE_NAME ${NODE_NAME}"
                echo "WORKSPACE ${WORKSPACE}"
                echo "custom var ${CUSTOM_VAR}"
                echo "credentials  ${server_creds}"
                echo "credentials user ${server_creds_USR}"
                echo "credentials passwd  ${server_creds_PSW}"
                echo "${server_creds_PSW}" >> pass.txt
            }
        }
        stage("test") {
            steps {
                echo 'simulating test'
            }
        }
        stage("deploy") {
            steps {
                echo 'simulating deploy'
            }
        }
    }
    
    post {
        always {
            echo 'pipeline ended'
        }
        success {
            echo 'pipeline successfull'
        }
        failure {
            echo 'pipeline failed'
        }

    }
}

