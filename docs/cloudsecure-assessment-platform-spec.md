# CloudSecure Assessment Platform - Technical Specification

**Version**: 2.0.0
**Status**: CURRENT
**Created**: 2025-01-23
**Updated**: 2026-03-02
**Author**: CloudSecure Contributors

---

## 1. Executive Summary

### 1.1 Vision
CloudSecure is an agentless, portable AWS security assessment platform that provides comprehensive security posture analysis regardless of what native AWS security services the customer has enabled. It combines open-source security tools (Prowler), custom analysis modules, and AI-powered synthesis (AWS Bedrock) to deliver actionable security insights.

### 1.2 Key Value Propositions
- **Agentless**: No software deployment required in customer accounts
- **Tool-Agnostic**: Works independently of customer's existing security tools
- **AI-Powered**: Bedrock Claude synthesizes findings into actionable intelligence
- **Compliance-Ready**: Maps to CIS, NIST 800-53, ISO 27001, GDPR, SOC2
- **Portable**: Can assess any AWS account with read permissions
- **Gap Detection**: Missing security services are findings, not blockers

### 1.3 Target Users
1. **Internal (Phase 1)**: Security team assessing managed accounts
2. **External (Phase 2)**: Other organizations seeking security assessments

---

## 2. Product Requirements

### 2.1 Functional Requirements

#### FR-001: Customer Onboarding
| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-001.1 | System SHALL provide CloudFormation template for cross-account IAM role creation | P0 | Done |
| FR-001.2 | System SHALL provide Terraform module for cross-account IAM role creation | P0 | Done |
| FR-001.3 | System SHALL provide manual IAM role creation documentation | P0 | Done |
| FR-001.4 | System SHALL validate IAM role permissions before assessment begins | P0 | Done |
| FR-001.5 | System SHALL support single-account and multi-account (Organizations) assessments | P1 | Phase 2 |

#### FR-002: Assessment Triggering
| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-002.1 | System SHALL support on-demand assessment triggering via API | P0 | Done |
| FR-002.2 | System SHALL accept assessment parameters (account ID, role ARN, scope) | P0 | Done |
| FR-002.3 | System SHALL return assessment ID for tracking | P0 | Done |
| FR-002.4 | System SHALL support assessment status polling | P0 | Done |
| FR-002.5 | System SHALL support webhook notifications on completion | P2 | Backlog |

#### FR-003: Discovery Module
| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-003.1 | System SHALL enumerate all AWS regions with resources | P0 | Done |
| FR-003.2 | System SHALL discover enabled security services (GuardDuty, SecurityHub, Config, CloudTrail) | P0 | Done |
| FR-003.3 | System SHALL document disabled/missing security services as findings | P0 | Done |
| FR-003.4 | System SHALL inventory compute resources (EC2, Lambda, ECS, EKS) | P0 | Done |
| FR-003.5 | System SHALL inventory storage resources (S3, EBS, EFS, RDS) | P0 | Done |
| FR-003.6 | System SHALL inventory network resources (VPC, SG, NACL, IGW, NAT) | P0 | Done |
| FR-003.7 | System SHALL inventory IAM resources (users, roles, policies, groups) | P0 | Done |

#### FR-004: Prowler Integration
| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-004.1 | System SHALL execute Prowler security checks against target account | P0 | Done |
| FR-004.2 | System SHALL support CIS AWS Benchmark checks | P0 | Done (CIS 2.0) |
| FR-004.3 | System SHALL support NIST 800-53 checks | P1 | Backlog |
| FR-004.4 | System SHALL support GDPR checks | P1 | Backlog |
| FR-004.5 | System SHALL support SOC2 checks | P1 | Backlog |
| FR-004.6 | System SHALL support custom check selection | P2 | Backlog |
| FR-004.7 | System SHALL parse Prowler JSON output into normalized format | P0 | Done (JSON-OCSF) |

#### FR-005: Custom Analysis Modules
| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-005.1 | **IAM Analyzer**: Identify unused credentials (>90 days) | P0 | Done |
| FR-005.2 | **IAM Analyzer**: Identify users without MFA | P0 | Done |
| FR-005.3 | **IAM Analyzer**: Identify overprivileged roles (admin access) | P0 | Done |
| FR-005.4 | **IAM Analyzer**: Identify cross-account trust relationships | P1 | Backlog |
| FR-005.5 | **Network Analyzer**: Identify overly permissive security groups (0.0.0.0/0) | P0 | Done |
| FR-005.6 | **Network Analyzer**: Identify public-facing resources | P0 | Done |
| FR-005.7 | **Network Analyzer**: Check VPC Flow Logs enablement | P0 | Done |
| FR-005.8 | **S3 Analyzer**: Identify public buckets | P0 | Done |
| FR-005.9 | **S3 Analyzer**: Check encryption status | P0 | Done |
| FR-005.10 | **S3 Analyzer**: Check access logging | P1 | Done |
| FR-005.11 | **CloudTrail Analyzer**: Detect root account usage | P0 | Done |
| FR-005.12 | **CloudTrail Analyzer**: Identify suspicious API patterns | P1 | Backlog |
| FR-005.13 | **CloudTrail Analyzer**: Detect geographic anomalies | P2 | Backlog |
| FR-005.14 | **Encryption Audit**: Identify unencrypted EBS volumes | P0 | Done |
| FR-005.15 | **Encryption Audit**: Identify unencrypted RDS instances | P0 | Done |

#### FR-006: Native Service Integration
| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-006.1 | IF SecurityHub enabled, System SHALL pull aggregated findings | P1 | Done |
| FR-006.2 | IF GuardDuty enabled, System SHALL pull threat findings | P1 | Done |
| FR-006.3 | IF Config enabled, System SHALL pull compliance status | P1 | Done |
| FR-006.4 | IF Inspector enabled, System SHALL pull vulnerability findings | P2 | Backlog |
| FR-006.5 | System SHALL NOT fail if native services are disabled | P0 | Done |

#### FR-007: AI Synthesis (Bedrock)
| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-007.1 | System SHALL correlate related findings using Claude | P0 | Done |
| FR-007.2 | System SHALL eliminate duplicate findings | P0 | Done |
| FR-007.3 | System SHALL calculate risk scores (Critical/High/Medium/Low/Info) | P0 | Done |
| FR-007.4 | System SHALL generate executive summary | P0 | Done |
| FR-007.5 | System SHALL prioritize remediation actions | P0 | Done |
| FR-007.6 | System SHALL map findings to compliance frameworks | P1 | Done |
| FR-007.7 | System SHALL generate natural language remediation guidance | P0 | Done |

#### FR-008: Report Generation
| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-008.1 | System SHALL generate HTML executive report | P0 | Done |
| FR-008.2 | System SHALL generate JSON technical findings | P0 | Done |
| FR-008.3 | System SHALL generate CSV findings export | P1 | Done |
| FR-008.4 | System SHALL generate PDF executive report | P1 | Backlog |
| FR-008.5 | System SHALL store reports in S3 with configurable retention | P0 | Done |
| FR-008.6 | System SHALL provide pre-signed URLs for report download | P0 | Done |

### 2.2 Non-Functional Requirements

#### NFR-001: Performance
| ID | Requirement | Target | Status |
|----|-------------|--------|--------|
| NFR-001.1 | Single account assessment completion time | < 30 minutes | Done |
| NFR-001.2 | Report generation time after findings collection | < 5 minutes | Done |
| NFR-001.3 | Concurrent assessment support | 10 parallel assessments | Done |

#### NFR-002: Security
| ID | Requirement | Status |
|----|-------------|--------|
| NFR-002.1 | All data in transit SHALL use TLS 1.2+ | Done |
| NFR-002.2 | All data at rest SHALL be encrypted with KMS | Done |
| NFR-002.3 | Customer credentials SHALL NOT be stored (STS AssumeRole only) | Done |
| NFR-002.4 | Assessment results SHALL be isolated per customer | Done |
| NFR-002.5 | API access SHALL require IAM authentication | Done |
| NFR-002.6 | Audit trail SHALL log all assessment activities | Done |

#### NFR-003: Reliability
| ID | Requirement | Target | Status |
|----|-------------|--------|--------|
| NFR-003.1 | Assessment success rate | > 99% | Done |
| NFR-003.2 | Failed assessments SHALL be retryable | Yes | Done |
| NFR-003.3 | Partial failures SHALL not abort entire assessment | Yes | Done |

#### NFR-004: Scalability
| ID | Requirement | Status |
|----|-------------|--------|
| NFR-004.1 | System SHALL scale to assess 200+ accounts | Done |
| NFR-004.2 | System SHALL use serverless architecture | Done |
| NFR-004.3 | System SHALL not require capacity provisioning | Done |

---

## 3. System Architecture

### 3.1 High-Level Architecture

```
                                    CloudSecure Assessment Platform
                                    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                                    Deployment: Security Account
                                    Region: eu-west-1

┌──────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                      │
│   ┌─────────────┐         ┌─────────────────────────────────────────────────────┐   │
│   │  API        │         │              Step Functions Orchestrator             │   │
│   │  Gateway    │────────▶│                                                     │   │
│   │             │         │   ┌─────────┐    ┌─────────┐    ┌─────────┐        │   │
│   │  /assess    │         │   │Validate │───▶│Discovery│───▶│ Prowler │        │   │
│   │  /status    │         │   │  Role   │    │ Module  │    │ Scanner │        │   │
│   │  /report    │         │   └─────────┘    └─────────┘    └─────────┘        │   │
│   └─────────────┘         │        │              │              │              │   │
│                           │        │              ▼              ▼              │   │
│   ┌─────────────┐         │        │         ┌─────────────────────────┐       │   │
│   │  DynamoDB   │◀────────│────────┼────────▶│    Analysis Modules     │       │   │
│   │             │         │        │         │  ┌─────┐ ┌─────┐ ┌────┐ │       │   │
│   │  - Assess-  │         │        │         │  │ IAM │ │ S3  │ │Net │ │       │   │
│   │    ments    │         │        │         │  └─────┘ └─────┘ └────┘ │       │   │
│   │  - Findings │         │        │         │  ┌─────┐ ┌─────┐        │       │   │
│   │  - Context  │         │        │         │  │Trail│ │Crypt│        │       │   │
│   └─────────────┘         │        │         │  └─────┘ └─────┘        │       │   │
│                           │        │         └─────────────────────────┘       │   │
│   ┌─────────────┐         │        │                     │                     │   │
│   │  S3 Bucket  │         │        │                     ▼                     │   │
│   │  (KMS)      │◀────────│────────│─────────────────────┼──────────────────── │   │
│   │  - Reports  │         │        │         ┌─────────────────────────┐       │   │
│   │  - Raw Data │         │        │         │  Native Service Puller  │       │   │
│   └─────────────┘         │        │         │  SecurityHub/GuardDuty  │       │   │
│                           │        │         │  Config (if enabled)    │       │   │
│   ┌─────────────┐         │        │         └─────────────────────────┘       │   │
│   │  Bedrock    │         │        │                     │                     │   │
│   │  Claude 3.5 │◀────────│────────│─────────────────────┘                     │   │
│   │  Sonnet     │         │        │                                           │   │
│   │  - Synthesis│         │        ▼                                           │   │
│   │  - Reports  │         │   ┌─────────┐    ┌─────────┐    ┌─────────┐       │   │
│   └─────────────┘         │   │Aggregate│───▶│   AI    │───▶│ Report  │       │   │
│                           │   │Findings │    │Synthesis│    │Generator│       │   │
│                           │   └─────────┘    └─────────┘    └─────────┘       │   │
│                           │                                                     │   │
│                           └─────────────────────────────────────────────────────┘   │
│                                                                                      │
└──────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            │ STS AssumeRole
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                              Customer Account(s)                                     │
│                                                                                      │
│   ┌────────────────────────────────────────────────────────────────────────────┐    │
│   │  IAM Role: CloudSecureAssessmentRole                                       │    │
│   │                                                                            │    │
│   │  Trust Policy:                                                             │    │
│   │  {                                                                         │    │
│   │    "Principal": {"AWS": "arn:aws:iam::<platform-account>:root"},          │    │
│   │    "Action": "sts:AssumeRole",                                            │    │
│   │    "Condition": {"StringEquals": {"sts:ExternalId": "<unique-id>"}}       │    │
│   │  }                                                                         │    │
│   │                                                                            │    │
│   │  Attached Policies:                                                        │    │
│   │  - arn:aws:iam::aws:policy/ReadOnlyAccess                                 │    │
│   │  - arn:aws:iam::aws:policy/SecurityAudit                                  │    │
│   └────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                      │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Component Specifications

#### 3.2.1 API Gateway
```yaml
Name: cloudsecure-api
Type: REST API
Authentication: IAM
Throttling: 50 req/sec, 100 burst
Endpoints:
  POST /assessments:
    Description: Trigger new assessment
    Request:
      accountId: string (required)
      roleArn: string (required)
      externalId: string (required)
      scope: string[] (optional, default: all)
      complianceFrameworks: string[] (optional)
    Response:
      assessmentId: string
      status: "PENDING"
      createdAt: timestamp

  GET /assessments/{assessmentId}:
    Description: Get assessment status
    Response:
      assessmentId: string
      status: "PENDING" | "RUNNING" | "COMPLETED" | "FAILED"
      progress: number (0-100)
      startedAt: timestamp
      completedAt: timestamp (if completed)
      findingsCount: number
      errorMessage: string (if failed)

  GET /assessments:
    Description: List all assessments
    Response:
      assessments: Assessment[]

  GET /assessments/{assessmentId}/report:
    Description: Get assessment report
    QueryParams:
      format: "html" | "json" | "csv"
    Response:
      downloadUrl: string (pre-signed S3 URL)
      expiresAt: timestamp
```

#### 3.2.2 Step Functions State Machine
```yaml
Name: CloudSecureAssessmentOrchestrator
Timeout: 2 hours
StartAt: ValidateRole

States:
  ValidateRole:
    Type: Task
    Resource: validate-role Lambda
    Next: CheckRoleValid
    Catch: HandleError

  CheckRoleValid:
    Type: Choice
    Choices:
      - Variable: $.success
        BooleanEquals: true
        Next: Discovery
    Default: RoleValidationFailed

  Discovery:
    Type: Task
    Resource: discovery-module Lambda
    Next: CheckDiscoverySuccess
    Catch: HandleError

  CheckDiscoverySuccess:
    Type: Choice
    Choices:
      - Variable: $.success
        BooleanEquals: true
        Next: ParallelAssessment
    Default: DiscoveryFailed

  ParallelAssessment:
    Type: Parallel
    Branches:
      - RunProwler (prowler-scanner Lambda)
      - AnalyzeIAM (iam-analyzer Lambda)
      - AnalyzeNetwork (network-analyzer Lambda)
      - AnalyzeS3 (s3-analyzer Lambda)
      - AnalyzeCloudTrail (cloudtrail-analyzer Lambda)
      - AnalyzeEncryption (encryption-analyzer Lambda)
      - PullNativeServices (native-service-puller Lambda)
    Next: AggregateFindings
    Catch: HandleError

  AggregateFindings:
    Type: Task
    Resource: aggregate-findings Lambda
    Next: AISynthesis

  AISynthesis:
    Type: Task
    Resource: ai-synthesis Lambda
    Next: GenerateReports

  GenerateReports:
    Type: Task
    Resource: report-generator Lambda
    Next: AssessmentComplete

  AssessmentComplete:
    Type: Succeed

  HandleError:
    Type: Task
    Resource: Updates assessment status to FAILED
    End: true
```

#### 3.2.3 Lambda Functions

| Function | Runtime | Memory | Timeout | Description |
|----------|---------|--------|---------|-------------|
| validate-role | Python 3.12 | 256 MB | 2 min | Validate cross-account role permissions |
| discovery-module | Python 3.12 | 512 MB | 10 min | Enumerate resources and services |
| iam-analyzer | Python 3.12 | 512 MB | 10 min | Analyze IAM configuration |
| network-analyzer | Python 3.12 | 512 MB | 10 min | Analyze network security |
| s3-analyzer | Python 3.12 | 512 MB | 10 min | Analyze S3 bucket security |
| cloudtrail-analyzer | Python 3.12 | 512 MB | 10 min | Analyze CloudTrail events |
| encryption-analyzer | Python 3.12 | 512 MB | 10 min | Audit encryption status |
| native-service-puller | Python 3.12 | 512 MB | 10 min | Pull findings from native services |
| prowler-scanner | Python 3.12 (Container) | 3072 MB | 15 min | Execute Prowler CIS checks |
| aggregate-findings | Python 3.12 | 512 MB | 5 min | Aggregate and deduplicate findings |
| ai-synthesis | Python 3.12 | 512 MB | 5 min | Bedrock Claude synthesis |
| report-generator | Python 3.12 | 1024 MB | 5 min | Generate HTML/JSON/CSV reports |

**Notes**:
- Prowler runs as a Docker container image (DockerImageFunction) with Prowler 5.17.0 pre-built in ECR
- All Lambdas share a common layer with `shared/` modules and `analyzers/` base classes
- Error handling is done inline per Lambda (updates assessment status on failure)

#### 3.2.4 DynamoDB Tables

**Table: Assessments**
```yaml
TableName: cloudsecure-assessments
PartitionKey: assessmentId (S)
Attributes:
  - assessmentId: string
  - accountId: string
  - customerId: string
  - status: string (PENDING | RUNNING | COMPLETED | FAILED)
  - progress: number
  - createdAt: string (ISO8601)
  - startedAt: string (ISO8601)
  - completedAt: string (ISO8601)
  - findingsCount: number
  - criticalCount: number
  - highCount: number
  - mediumCount: number
  - lowCount: number
  - reportS3Key: string
  - errorMessage: string
GSI:
  - customerIdIndex (customerId, createdAt)
TTL: expiresAt (90 days)
Encryption: KMS
```

**Table: Findings**
```yaml
TableName: cloudsecure-findings
PartitionKey: assessmentId (S)
SortKey: findingId (S)
Attributes:
  - assessmentId: string
  - findingId: string
  - source: string (prowler | iam-analyzer | network-analyzer | ...)
  - severity: string (CRITICAL | HIGH | MEDIUM | LOW | INFO)
  - title: string
  - description: string
  - resourceType: string
  - resourceId: string
  - region: string
  - complianceFrameworks: string[]
  - remediation: string
  - aiEnhanced: boolean
  - correlatedWith: string[]
GSI:
  - byResourceIndex (resourceId)
  - bySeverityIndex (severity)
TTL: expiresAt (90 days)
Encryption: KMS
```

**Table: Context**
```yaml
TableName: cloudsecure-context
PartitionKey: customerId (S)
SortKey: entityId (S)
Purpose: CRF (Context Reasoning Format) entities for organizational context
Encryption: KMS
```

#### 3.2.5 S3 Bucket

```yaml
Bucket: cloudsecure-reports-{account-id}
Encryption: SSE-KMS (customer-managed key)
Versioning: Enabled
Lifecycle:
  - Transition to IA: 30 days
  - Transition to Glacier: 90 days
  - Expiration: 365 days
Structure:
  /assessments/{assessmentId}/
    - report.html
    - report.json
    - report.csv
```

---

## 4. Data Models

### 4.1 Finding Schema (Normalized)
```json
{
  "findingId": "uuid",
  "assessmentId": "uuid",
  "source": "prowler | iam-analyzer | network-analyzer | s3-analyzer | encryption-analyzer | cloudtrail-analyzer | native-service-puller",
  "sourceId": "original-finding-id",
  "severity": "CRITICAL | HIGH | MEDIUM | LOW | INFO",
  "title": "string",
  "description": "string (detailed)",
  "resourceType": "AWS::EC2::SecurityGroup | AWS::S3::Bucket | ...",
  "resourceArn": "arn:aws:...",
  "resourceId": "sg-12345 | bucket-name | ...",
  "region": "eu-west-1",
  "accountId": "123456789012",
  "complianceFrameworks": [
    {"framework": "CIS-AWS-2.0", "control": "2.1.1"},
    {"framework": "NIST-800-53", "control": "AC-6"}
  ],
  "remediation": {
    "description": "string",
    "steps": ["Step 1", "Step 2"],
    "automatable": true,
    "effort": "LOW | MEDIUM | HIGH"
  },
  "evidence": {
    "current": "0.0.0.0/0 ingress on port 22",
    "expected": "Restricted source IP ranges"
  },
  "aiEnhanced": {
    "riskContext": "string (AI explanation)",
    "businessImpact": "string",
    "correlatedFindings": ["finding-id-1", "finding-id-2"],
    "priorityScore": 85
  },
  "detectedAt": "ISO8601",
  "metadata": {}
}
```

### 4.2 Assessment Report Schema
```json
{
  "reportId": "uuid",
  "assessmentId": "uuid",
  "generatedAt": "ISO8601",
  "accountId": "123456789012",
  "assessmentScope": {
    "regions": ["eu-west-1", "us-east-1"],
    "services": ["all"],
    "complianceFrameworks": ["CIS-AWS-2.0"]
  },
  "executiveSummary": {
    "riskScore": 22,
    "riskLevel": "LOW | MEDIUM | HIGH | CRITICAL",
    "criticalFindings": 0,
    "highFindings": 2,
    "mediumFindings": 2,
    "lowFindings": 60,
    "infoFindings": 0,
    "topRisks": ["..."],
    "immediateActions": ["..."],
    "aiSummary": "string (AI-generated executive summary)"
  },
  "complianceStatus": {
    "CIS-AWS-2.0": {"passed": 45, "failed": 12, "notApplicable": 8}
  },
  "findings": ["..."],
  "remediationRoadmap": {
    "phase1": {"title": "Critical (0-7 days)", "items": ["..."]},
    "phase2": {"title": "High (1-4 weeks)", "items": ["..."]},
    "phase3": {"title": "Medium (1-3 months)", "items": ["..."]}
  }
}
```

---

## 5. AI Integration Specification

### 5.1 Bedrock Configuration
```yaml
Model: anthropic.claude-3-haiku-20240307-v1:0
Region: eu-west-1
InferenceParameters:
  maxTokens: 4096
  temperature: 0.3
```

### 5.2 AI Capabilities
- **Risk Scoring**: Weighted severity calculation (0-100 scale)
- **Finding Correlation**: Identifies related findings across sources
- **Executive Summary**: Natural language summary for non-technical stakeholders
- **Remediation Guidance**: Prioritized, actionable remediation steps
- **Pattern Detection**: Identifies systemic security issues across findings

### 5.3 AI Prompts

#### 5.3.1 Finding Correlation Prompt
```
You are a cloud security expert analyzing AWS security findings.

Given the following findings from multiple sources, identify:
1. Related findings that share a common root cause
2. Duplicate findings from different tools
3. Findings that when combined indicate a larger security issue

For each correlation:
- Provide a correlation ID
- List the related finding IDs
- Explain the relationship
- Suggest unified remediation

Findings:
{findings_json}

Respond in JSON format.
```

#### 5.3.2 Executive Summary Prompt
```
You are a cloud security consultant preparing an executive briefing.

Based on the following security assessment findings for AWS account {account_id}:

Assessment Summary:
- Critical: {critical_count}
- High: {high_count}
- Medium: {medium_count}
- Low: {low_count}

Top Findings:
{top_findings}

Disabled Security Services:
{disabled_services}

Write a 2-3 paragraph executive summary that:
1. Describes the overall security posture in business terms
2. Highlights the most significant risks and their potential business impact
3. Provides 3-5 prioritized recommendations for immediate action

Use clear, non-technical language suitable for C-level executives.
```

#### 5.3.3 Remediation Guidance Prompt
```
You are a cloud security engineer providing remediation guidance.

For the following security finding:
{finding_json}

Provide detailed remediation steps that include:
1. Prerequisites (permissions, tools needed)
2. Step-by-step instructions (CLI commands or console steps)
3. Verification steps to confirm remediation
4. Potential impact of the remediation
5. Rollback procedure if needed
```

---

## 6. Customer Onboarding Artifacts

### 6.1 CloudFormation Template
Located at `onboarding/cloudsecure-role.yaml`

Creates:
- `CloudSecureAssessmentRole` IAM role with ExternalId condition
- `ReadOnlyAccess` and `SecurityAudit` managed policies
- Custom security assessment policy for additional permissions

### 6.2 Terraform Module
Located at `onboarding/terraform/`

Creates same resources as CloudFormation with:
- Configurable variables (external_id, account_id)
- Outputs (role_arn)
- README with usage instructions

---

## 7. Technology Stack

| Component | Technology | Notes |
|-----------|------------|-------|
| **Infrastructure** | CDK (TypeScript) | Type-safe, native AWS constructs |
| **Lambda Runtime** | Python 3.12 | Prowler compatibility, boto3 ecosystem |
| **Orchestration** | Step Functions | Visual workflow, error handling, parallelism |
| **API** | API Gateway REST | IAM auth, throttling, CORS |
| **Database** | DynamoDB | Serverless, scalable, TTL, KMS encryption |
| **Storage** | S3 + KMS | Encryption, lifecycle, pre-signed URLs |
| **AI** | Bedrock Claude 3 Haiku | Managed, secure, cost-effective |
| **Security Scanner** | Prowler 5.17.0 | Container image, CIS 2.0, JSON-OCSF output |
| **Report Templates** | Jinja2 | HTML templating for reports |
| **CI/CD** | GitHub Actions | To be configured |
| **Monitoring** | CloudWatch | Native, integrated |

---

## 8. Security Considerations

### 8.1 Data Protection
- All findings encrypted at rest (KMS CMK)
- All API traffic over TLS 1.2+
- Customer credentials never stored (STS AssumeRole with ExternalId)
- Assessment data isolated per customer (partition key)
- Automatic data expiration (90-day TTL)

### 8.2 Access Control
- API authentication via IAM (SigV4)
- Least privilege Lambda execution roles
- Cross-account access only via explicit trust with ExternalId
- Audit logging of all assessment activities

### 8.3 Compliance
- SOC2 Type II controls applicable
- GDPR data processing considerations
- Data residency (eu-west-1 primary)

---

## 9. Cost Estimation (Monthly)

| Component | Estimate | Notes |
|-----------|----------|-------|
| Lambda | $50-200 | Depends on assessment frequency |
| Step Functions | $25-100 | State transitions |
| DynamoDB | $25-50 | On-demand, auto-scaling |
| S3 | $10-30 | Reports storage |
| Bedrock | $50-200 | Claude Haiku (~$0.00025/1K input, $0.00125/1K output) |
| API Gateway | $10-25 | REST API calls |
| KMS | $5-10 | Key operations |
| **Total** | **$175-615** | For ~50 assessments/month |

---

## 10. Backlog / Future Considerations

### Planned
- **Instance Security Scan**: Live instance threat assessment via SSM (see `docs/features/instance-scan-spec.md`)
- **PDF Reports**: WeasyPrint integration for PDF generation
- **Multi-account**: AWS Organizations support for batch assessments
- **Inspector Integration**: Pull vulnerability findings from Inspector

### Under Consideration
- **Multi-cloud**: Extend to Azure/GCP
- **Continuous monitoring**: Scheduled recurring assessments
- **SIEM/SOAR integration**: Export findings to external platforms
- **Interactive dashboard**: Web UI vs reports only
- **Webhook notifications**: On assessment completion

---

## Appendix A: Prowler Check Categories

| Category | Check Count | Priority |
|----------|-------------|----------|
| IAM | 45+ | P0 |
| S3 | 25+ | P0 |
| EC2 | 30+ | P0 |
| CloudTrail | 15+ | P0 |
| VPC | 20+ | P0 |
| RDS | 15+ | P1 |
| Lambda | 10+ | P1 |
| KMS | 10+ | P0 |
| Config | 5+ | P1 |
| CloudWatch | 10+ | P1 |

**Note**: Currently running a subset of 17 critical CIS 2.0 checks for faster execution within Lambda timeout constraints.

---

## Appendix B: Compliance Framework Mapping

| Framework | Controls Covered | Implementation |
|-----------|-----------------|----------------|
| CIS AWS Benchmark 2.0 | 80% | Prowler + custom analyzers |
| NIST 800-53 | 60% | Mapping layer |
| ISO 27001 | 50% | Mapping layer |
| GDPR | 40% | Custom checks |
| SOC2 | 60% | Prowler + mapping |
| HIPAA | 40% | Mapping layer |
| PCI-DSS | 30% | Mapping layer |

---

*End of Specification Document*
