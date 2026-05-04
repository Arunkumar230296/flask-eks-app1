pipeline {
    agent any

    environment {
        AWS_REGION = "us-east-1"
        AWS_ACCOUNT_ID = "283904064946"
        ECR_REPO = "flask-eks-app1"
        IMAGE_TAG = "${BUILD_NUMBER}"

        GITHUB_CREDS = credentials('github-creds')
        ECR_URL = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}"
    }

    stages {
        stage('Docker Build') {
            steps {
                sh "docker build -t ${ECR_REPO}:${IMAGE_TAG} ."
                sh "docker tag ${ECR_REPO}:${IMAGE_TAG} ${ECR_URL}:${IMAGE_TAG}"
            }
        }

        stage('Login to ECR') {
            steps {
                sh "aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
            }
        }

        stage('Push Image to ECR') {
            steps {
                sh "docker push ${ECR_URL}:${IMAGE_TAG}"
            }
        }

        stage('Update GitOps Repo') {
            steps {
                sh """
                rm -rf gitops-helm-app1
                git clone https://${GITHUB_CREDS_USR}:${GITHUB_CREDS_PSW}@github.com/Arunkumar230296/gitops-helm-app1.git

                cd gitops-helm-app1/flask-app
                sed -i 's/tag: .*/tag: "${IMAGE_TAG}"/' values.yaml

                git config user.email "jenkins@example.com"
                git config user.name "jenkins"

                git add values.yaml
                git commit -m "Update image tag to ${IMAGE_TAG}"
                git push origin main
                """
            }
        }
    }
}
