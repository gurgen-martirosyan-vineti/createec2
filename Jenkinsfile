pipeline {
    agent {
        kubernetes {
            label 'jenkins-slave'
        }
    }

    stages {
        stage("Checkout") {
            steps {
                dir("application") {
                    checkout scm: [
                            $class: 'GitSCM',
                            userRemoteConfigs: [[
                                 credentialsId: 'GitHub-Credentials',
                                 url: 'https://github.com/gurgen-martirosyan-vineti/createec2.git'
                                 ]],
                            branches: [[name: "main"]]
                    ]
                }
                dir("application") {
                    sh label: "Building and pushing docker image", script: """
                    aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 160878852983.dkr.ecr.us-west-2.amazonaws.com
                    docker build -t createec2 .
                    docker tag createec2:latest 160878852983.dkr.ecr.us-west-2.amazonaws.com/python:latest
                    docker push 160878852983.dkr.ecr.us-west-2.amazonaws.com/python:latest
                    """
                }
            }
        }
        stage("Login to cluster") {

            steps {
                withCredentials([
                        string(credentialsId: 'kube', variable: 'api_token')
                ]) {
                    sh 'kubectl --token $api_token --server https://192.168.94.132:8443 '
                }
                sh "kubectl get secret"
            }
        }
        stage('Workflow') {
            steps {
                dir ("application") {
                    sh  label: "Run Argo Workflow", script: """
                    argo submit createec2-workflow.yaml
                    """
                }
            }

        }
    }
}