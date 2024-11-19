### 사용 도구  
- **이슈 관리**: Jira  
- **형상 관리**: GitLab  
- **커뮤니케이션**: Notion, MatterMost  
- **디자인**: Figma  
- **빌드 도구**: Jenkins  

### 개발 도구  
- **Visual Studio Code**: ver 1.90.2  
- **IntelliJ IDEA Ultimate**: 2024.1.4  
- **Pycharm**: 2024.1.6  
- **DataGrip**: 2024.1.4  

### 외부 서비스  
- **Open AI (chat gpt API)**  

### 개발 환경  

#### **Frontend**  
| Tool         | Version  |  
|--------------|----------|  
| React Native | 0.76.0   |  
| React        | 18.3.1   |  
| Firebase     | 21.4.0   |  
| TypeScript   | 0.20.0   |  

#### **Backend**  
| Tool           | Version                 |  
|----------------|-------------------------|  
| Java           | 17.0.11 2024-04-16 |  
| Spring Boot    | 3.3.5                   |  
| Python (LLM)   | 3.11.0                  |  
| Python (AI - ViT) | 3.8.0               |  
| Python (AI Speaker) | 3.7.0            |  
| Python library | requirements.txt 참조 |  
| Redis          | 7.4.0                   |  
| MySQL          | Ver 8.0.1               |  
| MongoDB        | 7.0.12                  |  
| Apache Kafka   | 2.12-2.5.0              |  
| FastAPI        | 1.11.0                  |  

#### **Server**  
| Tool   | Version  |  
|--------|----------|  
| AWS S3 | ---      |  
| AWS EC2 | ---     |  

#### **Infra**  
| Tool            | Version     |  
|-----------------|-------------|  
| Docker          | 27.1.1      |  
| Docker Compose  | 2.18.1      |  
| Ubuntu          | 20.04.6 LTS |  
| Jenkins         | 2.452.3     |  

### 포트 관련 정보  

#### **Backend**  
| Service      | Port  |  
|--------------|-------|  
| Spring Boot  | 8080  |  
| FastAPI      | 8000  |  
| Apache Kafka | 9092  |  
| Kafka UI     | 9093  |  
| Redis        | 6379  |  
| MySQL        | 3306  |  
| phpMyAdmin   | 3366  |  

#### **Infra**  
| Service    | Port   |  
|------------|--------|  
| Jenkins    | 9090   |  
| Portainer  | 55555  |  

### 환경 변수

.env (중요 정보 생략)
    
    REDIS_URL=k11a202.p.ssafy.io

    JWT_SECRET_KEY=
    JWT_SALT=
    JWT_ACCESS_TOKEN_EXPIRETIME=360000000
    JWT_REFRESH_TOKEN_EXPIRETIME=604800000

    AWS_S3_ACCESS_KEY=
    AWS_S3_SECRET_KEY=
    AWS_S3_BUCKET_REGION=ap-northeast-2
    AWS_S3_BUCKET_NAME=jungkkiri
    MYSQL_URL=jdbc:mysql://k11a202.p.ssafy.io:3306/ssafy
    MYSQL_USER=ssafy
    MYSQL_PASSWORD=
    REDIS_URL=k11a202.p.ssafy.io
    FIREBASE_JSON_PATH=firebase-service-account.json

    KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
    KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092,PLAINTEXT_HOST://0.0.0.0:9094
    KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://k11a202.p.ssafy.io:9092,PLAINTEXT_HOST://localhost:9094
    KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
    KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
    KAFKA_AUTO_CREATE_TOPICS_ENABLE: "true"

    

### CI/CD

**jenkins**

**기본 plugin 외에 추가 설치**

*   SSH Agent Plugin
*   Docker plugin
*   NodeJS
*   Mattermost Notification Plugin

**credentials 설정**


*   GitLab Token 등록
*   Docker hub 로그인 정보 등록
*   Docker image push를 위한 repo 정보 등록
*   SSH 접속을 위해 EC2 IP 정보와 .pem키 정보 등록
*   .env 파일 등록

**backend pipeline**

    pipeline {
    agent any
    
    parameters {
        string(name: 'JWT_SECRET_KEY', defaultValue: '', description: '')
        string(name: 'JWT_SALT', defaultValue: '', description: '')
        string(name: 'JWT_ACCESS_TOKEN_EXPIRETIME', defaultValue: '360000000', description: '')
        string(name: 'JWT_REFRESH_TOKEN_EXPIRETIME', defaultValue: '604800000', description: '')
        string(name: 'AWS_S3_ACCESS_KEY', defaultValue: '', description: '')
        string(name: 'AWS_S3_SECRET_KEY', defaultValue: '', description: '')
        
        // backendConfig와 관계 있는 내용
        string(name: 'AWS_S3_BUCKET_REGION', defaultValue: 'ap-northeast-2', description: '')
        string(name: 'AWS_S3_BUCKET_NAME', defaultValue:'jungkkiri', description: '')
        string(name: 'MYSQL_URL', defaultValue:'jdbc:mysql://k11a202.p.ssafy.io:3306/ssafy', description:'')
        string(name: 'MYSQL_USER', defaultValue:'', description: '')
        string(name: 'MYSQL_PASSWORD', defaultValue:'', description: '')
        string(name: 'REDIS_URL', defaultValue:'k11a202.p.ssafy.io', description: '')
        string(name: 'FIREBASE_JSON_PATH', defaultValue:'firebase-service-account.json', description: '')
    }
    
    tools {
        jdk 'jdk-17'
    }
    
    stages {
        
        stage('github clone (BE)') {
            steps {
                script {
                    dir("./spring") {
                        git branch: 'BE_DEVELOP', credentialsId: 'person456', 
                        url: 'https://lab.ssafy.com/s11-final/S11P31A202.git'
                    }
                }
            }
        }
        stage('Copy Firebase Config') {
            steps {
                sshagent(['ssafy-server-ssh']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no ubuntu@ip-172-26-10-34 \
                        "sudo cp /home/ubuntu/firebase-service-account.json /home/ubuntu/jenkins/workspace/jungkkiri/spring/BomBom/src/main/resources/"
                    '''
                }
            }
        }
        stage('build (BE)') {
            steps {
                dir("./spring/BomBom") {
                    
                    sh """
                    
                        chmod +x ./gradlew
                        
                        ./gradlew clean build -x test
                    
                    """
                }
            }
        }
        stage('docker hub push (BE)') {
            steps {
                script {
                    dir("./spring/BomBom") {
                        docker.withRegistry('https://index.docker.io/v1/', 'docker') {
                            sh """
                                docker build -t person456/jungkkiri:latest .
                                docker push person456/jungkkiri:latest
                            """
                        }
                    }
                }
            }
        }
        stage('Deploy') {
            steps {
                sshagent(['ssafy-server-ssh']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ubuntu@ip-172-26-10-34 \
                        'sudo -E bash -c "export JWT_SECRET_KEY=\\"${params.JWT_SECRET_KEY}\\" && \
                        export JWT_SALT=\\"${params.JWT_SALT}\\" && \
                        export JWT_ACCESS_TOKEN_EXPIRETIME=\\"${params.JWT_ACCESS_TOKEN_EXPIRETIME}\\" && \
                        export JWT_REFRESH_TOKEN_EXPIRETIME=\\"${params.JWT_REFRESH_TOKEN_EXPIRETIME}\\" && \
                        export AWS_S3_ACCESS_KEY=\\"${params.AWS_S3_ACCESS_KEY}\\" && \
                        export AWS_S3_SECRET_KEY=\\"${params.AWS_S3_SECRET_KEY}\\" && \
                        export AWS_S3_BUCKET_REGION=\\"${params.AWS_S3_BUCKET_REGION}\\" && \
                        export AWS_S3_BUCKET_NAME=\\"${params.AWS_S3_BUCKET_NAME}\\" && \
                        export MYSQL_URL=\\"${params.MYSQL_URL}\\" && \
                        export MYSQL_USER=\\"${params.MYSQL_USER}\\" && \
                        export MYSQL_PASSWORD=\\"${params.MYSQL_PASSWORD}\\" && \
                        export REDIS_URL=\\"${params.REDIS_URL}\\" && \
                        export FIREBASE_JSON_PATH=\\"${params.FIREBASE_JSON_PATH}\\" && \
                        cd /home/ubuntu && chmod +x ./deploy.sh && ./deploy.sh"'
                    """
                }
            }
        }
    }
}
    
    

### 빌드 및 실행
**deploy.sh**
    #!/bin/bash

    # 환경변수 출력으로 확인
    echo "Checking environment variables:"
    echo "JWT_SECRET_KEY: $JWT_SECRET_KEY"
    echo "JWT_SALT: $JWT_SALT"
    echo "JWT_ACCESS_TOKEN_EXPIRETIME: $JWT_ACCESS_TOKEN_EXPIRETIME"
    echo "JWT_REFRESH_TOKEN_EXPIRETIME: $JWT_REFRESH_TOKEN_EXPIRETIME"
    echo "AWS_S3_ACCESS_KEY: $AWS_S3_ACCESS_KEY"
    echo "AWS_S3_SECRET_KEY: $AWS_S3_SECRET_KEY"
    echo "AWS_S3_BUCKET_REGION: $AWS_S3_BUCKET_REGION"
    echo "AWS_S3_BUCKET_NAME: $AWS_S3_BUCKET_NAME"
    echo "MYSQL_URL: $MYSQL_URL"
    echo "MYSQL_USER: $MYSQL_USER"
    echo "MYSQL_PASSWORD: $MYSQL_PASSWORD"
    echo "REDIS_URL: $REDIS_URL"
    echo "FIREBASE_JSON_PATH: $FIREBASE_JSON_PATH"

    # 기존 컨테이너 중지
    echo "Stopping existing containers..."
    sudo docker compose -f backend-compose.yml down

    # 기존 이미지 제거
    echo "Removing old image..."
    sudo docker rmi person456/jungkkiri:latest || true

    # docker-compose 파일 생성
    echo "Creating docker-compose file..."
    cat > backend-compose.yml << EOF
    networks:
    jungkkiri_network:
        external: true
        driver: bridge


    services:
    mysql:
        image: mysql:8.0
        container_name: mysql
        environment:
        - TZ=Asia/Seoul
        - MYSQL_ROOT_PASSWORD=Hot&6Man!A606
        - MYSQL_DATABASE=ssafy
        - MYSQL_USER=ssafy
        - MYSQL_PASSWORD=ssafy
        volumes:
        - /home/ubuntu/yongsoo/deploy/0/mysql:/var/lib/mysql
        - ./mysql-init-files/:/docker-entrypoint-initdb.d
        ports:
        - '3306:3306'
        command:
        - --character-set-server=utf8mb4
        - --collation-server=utf8mb4_unicode_ci
        - --skip-character-set-client-handshake
        - --lower_case_table_names=0
        networks:
        - jungkkiri_network

    phpmyadmin:
        image: phpmyadmin/phpmyadmin:latest
        container_name: phpmyadmin
        environment:
        PMA_HOST: mysql
        MYSQL_ROOT_PASSWORD: Hot&6Man!A606
        ports:
        - '3366:80'
        restart: always
        networks:
        - jungkkiri_network

    spring:
        image: person456/jungkkiri:latest
        container_name: spring
        environment:
        - JWT_SECRET_KEY=${JWT_SECRET_KEY}
        - JWT_SALT=${JWT_SALT}
        - JWT_ACCESS_TOKEN_EXPIRETIME=${JWT_ACCESS_TOKEN_EXPIRETIME}
        - JWT_REFRESH_TOKEN_EXPIRETIME=${JWT_REFRESH_TOKEN_EXPIRETIME}
        - AWS_S3_ACCESS_KEY=${AWS_S3_ACCESS_KEY}
        - AWS_S3_SECRET_KEY=${AWS_S3_SECRET_KEY}
        - AWS_S3_BUCKET_REGION=${AWS_S3_BUCKET_REGION}
        - AWS_S3_BUCKET_NAME=${AWS_S3_BUCKET_NAME}
        - MYSQL_URL=${MYSQL_URL}
        - MYSQL_USER=${MYSQL_USER}
        - MYSQL_PASSWORD=${MYSQL_PASSWORD}
        - REDIS_URL=${REDIS_URL}
        - FIREBASE_JSON_PATH=${FIREBASE_JSON_PATH}
        ports:
        - '8080:8080'
        restart: always
        depends_on:
        - mysql
        networks:
        - jungkkiri_network

    llm:
        image: person456/llm:latest
        container_name: llm
        ports:
        - '8000:8000'
        depends_on:
        - mysql
        networks:
        - jungkkiri_network
    EOF

    # 컨테이너 시작
    echo "Starting containers..."
    sudo docker compose -f backend-compose.yml up -d

    echo "Deployment completed!"



**docker-compose.yml**

    networks:
        jungkkiri_network:
            external: true
            driver: bridge
        kafka_network:
            driver: bridge

    services:
        portainer:
            image: portainer/portainer-ce:latest
            container_name: portainer
            privileged: true
            ports:
            - "55555:9000"
            volumes:
            - "./portainer:/data"
            - "/var/run/docker.sock:/var/run/docker.sock"
            restart: always
            networks:
            - jungkkiri_network
        zookeeper:
            image: zookeeper:3.8.4
            container_name: zookeeper
            ports:
            - "2181:2181"
            networks:
            - jungkkiri_network
            - kafka_network

        kafka:
            image: wurstmeister/kafka:2.12-2.5.0
            container_name: kafka
            ports:
            - "9092:9092"
            - "9094:9094"
            environment:
            KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
            KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092,PLAINTEXT_HOST://0.0.0.0:9094
            KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://k11a202.p.ssafy.io:9092,PLAINTEXT_HOST://localhost:9094
            KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
            KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
            KAFKA_AUTO_CREATE_TOPICS_ENABLE: "true"
            volumes:
            - /var/run/docker.sock:/var/run/docker.sock
            depends_on:
            - zookeeper
            networks:
            - jungkkiri_network
            - kafka_network

        kafka-ui:
            image: provectuslabs/kafka-ui
            container_name: kafka-ui
            ports:
            - "9093:8080"
            environment:
            - KAFKA_CLUSTERS_0_NAME=local
            - KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=kafka:9092
            - KAFKA_CLUSTERS_0_ZOOKEEPER=zookeeper:2181
            depends_on:
            - kafka
            networks:
            - jungkkiri_network
            - kafka_network

        redis:
            image: redis:latest
            container_name: redis
            ports:
            - '6379:6379'
            networks:
            - jungkkiri_network

        jenkins:
            image: jenkins_docker:latest
            container_name: jenkins
            user: root
            volumes:
            - ./jenkins:/var/jenkins_home
            - /var/run/docker.sock:/var/run/docker.sock
            ports:
            - "9090:8080"
            networks:
            - jungkkiri_network

    

### 빌드 및 실행

**backend-compose.yml**

    networks:
        jungkkiri_network:
            external: true
            driver: bridge


    services:
        mysql:
            image: mysql:8.0
            container_name: mysql
            environment:
            - TZ=Asia/Seoul
            - MYSQL_ROOT_PASSWORD=Hot&6Man!A606
            - MYSQL_DATABASE=ssafy
            - MYSQL_USER=ssafy
            - MYSQL_PASSWORD=ssafy
            volumes:
            - /home/ubuntu/yongsoo/deploy/0/mysql:/var/lib/mysql
            - ./mysql-init-files/:/docker-entrypoint-initdb.d
            ports:
            - '3306:3306'
            command:
            - --character-set-server=utf8mb4
            - --collation-server=utf8mb4_unicode_ci
            - --skip-character-set-client-handshake
            - --lower_case_table_names=0
            networks:
            - jungkkiri_network

        phpmyadmin:
            image: phpmyadmin/phpmyadmin:latest
            container_name: phpmyadmin
            environment:
            PMA_HOST: mysql
            MYSQL_ROOT_PASSWORD: Hot&6Man!A606
            ports:
            - '3366:80'
            restart: always
            networks:
            - jungkkiri_network

        spring:
            image: person456/jungkkiri:latest
            container_name: spring
            environment:
            - JWT_SECRET_KEY=
            - JWT_SALT=
            - JWT_ACCESS_TOKEN_EXPIRETIME=360000000
            - JWT_REFRESH_TOKEN_EXPIRETIME=604800000
            - AWS_S3_ACCESS_KEY=
            - AWS_S3_SECRET_KEY=
            - AWS_S3_BUCKET_REGION=ap-northeast-2
            - AWS_S3_BUCKET_NAME=jungkkiri
            - MYSQL_URL=jdbc:mysql://k11a202.p.ssafy.io:3306/ssafy
            - MYSQL_USER=ssafy
            - MYSQL_PASSWORD=ssafy
            - REDIS_URL=k11a202.p.ssafy.io
            - FIREBASE_JSON_PATH=firebase-service-account.json
            ports:
            - '8080:8080'
            restart: always
            depends_on:
            - mysql
            networks:
            - jungkkiri_network

        llm:
            image: person456/llm:latest
            container_name: llm
            ports:
            - '8000:8000'
            depends_on:
            - mysql
            networks:
            - jungkkiri_network
