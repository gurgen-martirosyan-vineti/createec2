pipeline {
    agent any

    stages {
        stage("Checkout") {
            steps {
                dir("application") {
                    checkout scm: [
                            $class: 'GitSCM',
                            userRemoteConfigs: [[
                                                        credentialsId: 'GitHub-Credentials',
                                                        url: 'https://github.com/vinetiworks/devsecops-cicd.git'
                                                ]],
                            branches: [[name: "gmartirosyan_testings"]]
                    ]
                }
                dir("python") {
                    sh label: "Building and pushing docker image", script: """
                    aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 788197806324.dkr.ecr.us-west-2.amazonaws.com
                    pwd
                    ls -la
                    docker build -t createec2 .
                    docker tag createec2:latest 788197806324.dkr.ecr.us-west-2.amazonaws.com/gurgens-image:latest
                    docker push 788197806324.dkr.ecr.us-west-2.amazonaws.com/gurgens-image:latest
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
                dir ("python") {
                    sh  label: "Run Argo Workflow", script: """
                    argo submit createec2-workflow.yaml
                    """
                }
            }

        }
    }
}