pipeline {
    agent {
        kubernetes {
            yaml '''
        apiVersion: v1
        kind: Pod
        spec:
           containers:
           - name: docker
             image: docker:dind
             command:
             - sleep
             args:
             - 99d
             volumeMounts:
             - name: docker-socket
               mountPath: /var/run/docker.sock
             - name: docker-config
               mountPath: /root/.docker
             env:
               - name: AWS_ACCESS_KEY_ID
                 valueFrom:
                   secretKeyRef:
                      name: "aws-creds"
                      key: "id"
               - name: AWS_SECRET_ACCESS_KEY
                 valueFrom:
                   secretKeyRef:
                      name: "aws-creds"
                      key: "key"
           volumes:
             - name: docker-config
               configMap:
                   name: ecr-login
             - name: docker-socket
               hostPath:
                 path: /var/run/docker.sock
        '''
        }
    }
    stages {
        stage('Prepare') {
            steps {
                container('docker') {
                    sh 'apk add git'
                }
            }
        }
        stage("Checkout") {
            steps {
                container('docker') {
                    dir("createec2") {
                        checkout scm: [
                                $class: 'GitSCM',
                                userRemoteConfigs: [[
                                                            credentialsId: 'GitHub-Credentials',
                                                            url: 'https://github.com/gurgen-martirosyan-vineti/createec2.git'
                                                    ]],
                                branches: [[name: "main"]]
                        ]
                    }
                }
            }
        }

        stage("Build/Push image") {
            steps {
                container('docker') {
                    dir("createec2") {
                        sh label: "Building and pushing docker image", script: """             
                          wget https://amazon-ecr-credential-helper-releases.s3.us-east-2.amazonaws.com/0.3.1/linux-amd64/docker-credential-ecr-login
                          chmod +x docker-credential-ecr-login
                          mv docker-credential-ecr-login /usr/bin/docker-credential-ecr-login
                          docker build . -t 160878852983.dkr.ecr.us-west-2.amazonaws.com/python:latest
                          docker push 160878852983.dkr.ecr.us-west-2.amazonaws.com/python:latest
                          """
                    }
                }

            }
        }
        stage('Deploy') {
            when { tag "v1.*" }
            steps {
                echo 'Deploying only because this commit is tagged...'
                sh 'make deploy'
            }
        }
    }
}
