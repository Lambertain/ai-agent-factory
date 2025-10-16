# Module 04: Cloud & Serverless Architecture

**Версия:** 1.0
**Дата:** 2025-10-16
**Автор:** Archon Blueprint Architect

**Назад к:** [Blueprint Architect Knowledge Base](../archon_blueprint_architect_knowledge.md)

---

## 🔧 ТЕХНИЧЕСКИЕ ТРИГГЕРЫ (приоритет для задач Archon)

**Serverless Computing:**
- AWS Lambda, Google Cloud Functions, Azure Functions
- Cold Start optimization, Warm Start, Lambda Layers
- Serverless Framework, SAM (Serverless Application Model)
- Event-driven triggers, API Gateway integration
- Function-as-a-Service (FaaS), Backend-as-a-Service (BaaS)

**Infrastructure as Code (IaC):**
- Terraform (HCL), CloudFormation (YAML/JSON), Pulumi (TypeScript/Python)
- AWS CDK, Azure Resource Manager (ARM) Templates
- Ansible, Chef, Puppet for configuration management
- State Management, Remote State, State Locking
- Module composition, Resource dependencies

**Container Orchestration:**
- Kubernetes (K8s), Docker Swarm, Apache Mesos
- AWS ECS/EKS, Google GKE, Azure AKS
- Helm Charts, Kustomize, Operators
- Service Mesh (Istio, Linkerd), Ingress Controllers
- StatefulSets, DaemonSets, Jobs, CronJobs

**Cloud Services (AWS/GCP/Azure):**
- Storage: S3, Cloud Storage, Azure Blob Storage
- Databases: DynamoDB, RDS, Cloud SQL, Cosmos DB
- Queues: SQS, Cloud Pub/Sub, Service Bus
- Caching: ElastiCache, Memorystore, Azure Cache
- CDN: CloudFront, Cloud CDN, Azure CDN

**Auto-scaling & Elasticity:**
- Horizontal Pod Autoscaler (HPA), Vertical Pod Autoscaler (VPA)
- AWS Auto Scaling Groups, GCP Managed Instance Groups
- KEDA (Kubernetes Event-Driven Autoscaling)
- Load Balancer integration (ALB, NLB, CLB)
- Scaling policies (Target Tracking, Step Scaling)

**Multi-Cloud & Hybrid:**
- Multi-cloud deployment strategies
- Hybrid cloud architecture (on-premise + cloud)
- Cloud migration patterns (Lift-and-Shift, Refactor, Replatform)
- Vendor lock-in prevention, Cloud-agnostic design
- Cross-cloud networking, VPN, Direct Connect

**Cost Optimization:**
- Reserved Instances, Savings Plans, Spot Instances
- Right-sizing resources, Auto-shutdown policies
- Cost allocation tags, Budget alerts
- Serverless cost optimization (execution time, memory)

---

## 🔍 КЛЮЧЕВЫЕ СЛОВА (для общения с пользователем)

**Русские:** облачная архитектура, serverless, lambda, multi-cloud, IaC, terraform, контейнеризация, kubernetes, автоскейлинг

**English:** cloud architecture, serverless, lambda, multi-cloud, IaC, terraform, containerization, kubernetes, auto-scaling

---

## 📌 КОГДА ЧИТАТЬ (контекст)

- Cloud-native приложения
- Auto-scaling архитектуры
- Pay-per-use модели
- Event-driven serverless workflows
- Миграция в облако
- Контейнеризация приложений

---

## Multi-Cloud Strategy
```yaml
# Infrastructure as Code - Terraform example
# variables.tf
variable "cloud_provider" {
  description = "Primary cloud provider"
  type        = string
  default     = "aws"

  validation {
    condition     = contains(["aws", "gcp", "azure"], var.cloud_provider)
    error_message = "Cloud provider must be aws, gcp, or azure."
  }
}

variable "multi_cloud_enabled" {
  description = "Enable multi-cloud deployment"
  type        = bool
  default     = false
}

variable "regions" {
  description = "Deployment regions per cloud"
  type = map(list(string))
  default = {
    aws   = ["us-east-1", "eu-west-1"]
    gcp   = ["us-central1", "europe-west1"]
    azure = ["East US", "West Europe"]
  }
}

# main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

# AWS Resources
module "aws_infrastructure" {
  count  = var.cloud_provider == "aws" || var.multi_cloud_enabled ? 1 : 0
  source = "./modules/aws"

  regions = var.regions.aws
  environment = var.environment
}

# GCP Resources
module "gcp_infrastructure" {
  count  = var.cloud_provider == "gcp" || var.multi_cloud_enabled ? 1 : 0
  source = "./modules/gcp"

  regions = var.regions.gcp
  environment = var.environment
}

# Azure Resources
module "azure_infrastructure" {
  count  = var.cloud_provider == "azure" || var.multi_cloud_enabled ? 1 : 0
  source = "./modules/azure"

  regions = var.regions.azure
  environment = var.environment
}

# Cross-cloud networking
module "cross_cloud_networking" {
  count  = var.multi_cloud_enabled ? 1 : 0
  source = "./modules/cross-cloud"

  aws_vpc_ids    = try(module.aws_infrastructure[0].vpc_ids, [])
  gcp_vpc_names  = try(module.gcp_infrastructure[0].vpc_names, [])
  azure_vnet_ids = try(module.azure_infrastructure[0].vnet_ids, [])
}
```

---

## Serverless Architecture
```python
# Serverless function with AWS Lambda
import json
import boto3
from typing import Dict, Any
import asyncio

class ServerlessEventProcessor:
    """Serverless event processing architecture."""

    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.sqs = boto3.client('sqs')
        self.sns = boto3.client('sns')
        self.s3 = boto3.client('s3')

    async def process_api_request(self, event: Dict[str, Any], context: Any) -> Dict[str, Any]:
        """AWS Lambda handler for API requests."""
        try:
            # Parse request
            body = json.loads(event.get('body', '{}'))
            path = event.get('path', '')
            method = event.get('httpMethod', '')

            # Route to appropriate handler
            if path.startswith('/users') and method == 'POST':
                result = await self._handle_user_creation(body)
            elif path.startswith('/users') and method == 'GET':
                result = await self._handle_user_query(event.get('pathParameters', {}))
            else:
                return {
                    'statusCode': 404,
                    'body': json.dumps({'error': 'Not found'})
                }

            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps(result)
            }

        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }

    async def _handle_user_creation(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle user creation in serverless environment."""
        # Validate input
        if not user_data.get('email') or not user_data.get('name'):
            raise ValueError("Email and name are required")

        # Store in DynamoDB
        table = self.dynamodb.Table('users')
        user_id = f"user_{int(time.time())}"

        table.put_item(Item={
            'user_id': user_id,
            'name': user_data['name'],
            'email': user_data['email'],
            'created_at': datetime.utcnow().isoformat()
        })

        # Send welcome email via SQS
        await self._send_async_notification(user_id, user_data['email'])

        return {'user_id': user_id, 'status': 'created'}

    async def _send_async_notification(self, user_id: str, email: str):
        """Send asynchronous notification via SQS."""
        message = {
            'type': 'welcome_email',
            'user_id': user_id,
            'email': email
        }

        self.sqs.send_message(
            QueueUrl=os.environ['NOTIFICATION_QUEUE_URL'],
            MessageBody=json.dumps(message)
        )

# Serverless deployment configuration
# serverless.yml
service: archon-serverless-api

provider:
  name: aws
  runtime: python3.9
  region: us-east-1
  environment:
    STAGE: ${opt:stage, 'dev'}
    NOTIFICATION_QUEUE_URL: ${self:resources.Outputs.NotificationQueueUrl.Value}

  iamRoleStatements:
    - Effect: Allow
      Action:
        - dynamodb:GetItem
        - dynamodb:PutItem
        - dynamodb:UpdateItem
        - dynamodb:DeleteItem
        - dynamodb:Query
        - dynamodb:Scan
      Resource: "arn:aws:dynamodb:${self:provider.region}:*:table/*"

    - Effect: Allow
      Action:
        - sqs:SendMessage
        - sqs:ReceiveMessage
        - sqs:DeleteMessage
      Resource: "arn:aws:sqs:${self:provider.region}:*:*"

functions:
  api:
    handler: handler.api_handler
    events:
      - http:
          path: /{proxy+}
          method: ANY
          cors: true
    timeout: 30
    memorySize: 512

  notification_processor:
    handler: handler.notification_handler
    events:
      - sqs:
          arn: ${self:resources.Outputs.NotificationQueueArn.Value}
          batchSize: 10
    timeout: 60
    memorySize: 256

resources:
  Resources:
    UsersTable:
      Type: AWS::DynamoDB::Table
      Properties:
        TableName: users-${self:provider.environment.STAGE}
        AttributeDefinitions:
          - AttributeName: user_id
            AttributeType: S
        KeySchema:
          - AttributeName: user_id
            KeyType: HASH
        BillingMode: PAY_PER_REQUEST

    NotificationQueue:
      Type: AWS::SQS::Queue
      Properties:
        QueueName: notifications-${self:provider.environment.STAGE}
        MessageRetentionPeriod: 1209600  # 14 days
        VisibilityTimeoutSeconds: 120

  Outputs:
    NotificationQueueUrl:
      Value:
        Ref: NotificationQueue
    NotificationQueueArn:
      Value:
        Fn::GetAtt: [NotificationQueue, Arn]

plugins:
  - serverless-python-requirements
  - serverless-domain-manager

custom:
  pythonRequirements:
    dockerizePip: true
  customDomain:
    domainName: api.archon.example.com
    basePath: ''
    stage: ${self:provider.environment.STAGE}
    createRoute53Record: true
```

---

**Навигация:**
- [← Предыдущий модуль: Event-Driven Architecture & CQRS](03_event_driven_cqrs.md)
- [↑ Назад к Blueprint Architect Knowledge Base](../archon_blueprint_architect_knowledge.md)
