# CloudSecure Instance Scan - Feature Specification

**Status**: Proposed (not yet implemented)
**Author**: CloudSecure Contributors
**Date**: 2026-03-02
**Target**: Sprint 7+

---

## Overview

Extend CloudSecure from account-level posture assessment to instance-level threat assessment using AWS Systems Manager (SSM) for agentless data collection and AI for attack vector analysis.

### Value Proposition

| | Account Assessment (current) | Instance Scan (new) |
|---|---|---|
| **Scope** | AWS account configuration | Single EC2 instance, live OS |
| **Access** | IAM AssumeRole + API calls | SSM SendCommand / RunCommand |
| **Data** | CloudTrail, IAM, S3, VPCs | Packages, ports, processes, files, configs |
| **AI Output** | "Your account posture is X" | "Your attack vectors on this host are X" |

### Differentiator

This is NOT a vulnerability scanner (Nessus, Qualys) or a pentest tool. It is AI analyzing a running production instance and identifying exactly how an attacker would exploit it. The same analysis a security engineer does manually in 8 hours, automated in 10 minutes.

### Killer Feature

SSM is already deployed across all 150 managed accounts. No agents to install, no SSH access needed, no firewall changes. Connect via SSM, collect data, AI analyzes, generate report.

---

## Interface

### CLI

```bash
cloudsecure assess --account 123456789012          # existing account assessment
cloudsecure scan --instance i-0abc123 --account 123456789012   # NEW: instance scan
cloudsecure scan --instance i-0abc123 --account 123456789012 --mode forensic  # isolated/dead instance
```

### API Endpoints

```
POST /scans                  → Start instance scan
GET  /scans/{scanId}         → Get scan status/results
GET  /scans                  → List scans
```

### Scan Modes

| Mode | Use Case | Context for AI |
|------|----------|----------------|
| `live` (default) | Production instance, proactive assessment | "How would an attacker exploit this system?" |
| `forensic` | Isolated/compromised instance, post-incident | "What did the attacker do? What's the damage?" |

---

## Architecture

### Decision: Separate Step Functions State Machine

The instance scan runs as an independent pipeline, separate from account assessment. Reasons:
- Different lifecycle (scan: 2-5 min vs assessment: 30-120 min)
- Different inputs (instance ID vs account ID)
- Different data model
- Can share: AI synthesis engine, report generator, shared models

### State Machine Flow

```
POST /scans → StartScanLambda → InstanceScanStateMachine:

  1. ValidateSSMAccess
     ├── Verify instance exists and SSM agent is online
     ├── Verify cross-account role has ssm:SendCommand permission
     └── Fail fast if instance not reachable

  2. CollectInstanceData
     ├── Execute SSM Document (CloudSecure-InstanceScan)
     ├── Collect structured JSON output
     └── Store raw data in S3

  3. AnalyzeInstanceData
     ├── Parse collected data
     ├── Identify security risks and misconfigurations
     └── Create ScanFinding objects

  4. AISynthesis
     ├── Reuse existing Bedrock integration
     ├── Different prompt: attack vector analysis
     └── Generate risk score and prioritized remediation

  5. GenerateReport
     ├── Reuse report generator with new template
     ├── JSON report (MVP)
     └── Upload to S3

  6. ScanComplete (status=COMPLETED)
```

### SSM Connectivity Model

Use a custom **SSM Document** (`CloudSecure-InstanceScan`) that runs a structured collection script and outputs JSON to S3.

Advantages:
- Reusable across accounts (deploy via StackSets)
- No output size limits (writes to S3, avoids 24KB RunCommand limit)
- Auditable (SSM tracks all document executions)
- Configurable timeouts per document

---

## Data Collection (Tiered)

### Tier 1 - System Inventory (MVP)

Fast, low-risk, high-value data collection:

| Category | Commands | Purpose |
|----------|----------|---------|
| OS info | `cat /etc/os-release`, `uname -a` | Identify OS, kernel, architecture |
| Packages | `rpm -qa --queryformat '...'` | Full package inventory with versions |
| Processes | `ps aux --no-headers` | Running processes, users, commands |
| Open ports | `ss -tlnp`, `ss -ulnp` | Listening services and bound ports |
| Cron jobs | `crontab -l`, `ls /etc/cron.*` | Scheduled tasks (system + user) |
| Systemd services | `systemctl list-units --type=service` | Enabled/running services |
| Users | `cat /etc/passwd`, `cat /etc/group` | User accounts and groups |
| Sudo config | `cat /etc/sudoers`, `ls /etc/sudoers.d/` | Privilege escalation paths |
| SSH config | `cat /etc/ssh/sshd_config` | SSH hardening status |

### Tier 2 - Web App Analysis (V2)

Medium complexity, requires care:
- Web server config (Apache/Nginx vhosts, modules)
- PHP/Node/Python app directories and versions
- File permissions on web roots
- Upload directories (writable by www-data?)
- `.htaccess` files, PHP `disable_functions`
- Recently modified files (last 7 days)
- Files with SUID/SGID bits

### Tier 3 - Threat Indicators (V3)

Deeper analysis:
- SSH authorized_keys (unexpected keys?)
- `/tmp` and `/var/tmp` suspicious files
- Outbound connections (`ss -tnp`)
- iptables/nftables rules
- SELinux/AppArmor status
- Docker containers running
- Environment variables with secrets

---

## Data Model

### InstanceScan

```python
class ScanMode(str, Enum):
    LIVE = "live"
    FORENSIC = "forensic"

class ScanStatus(str, Enum):
    PENDING = "pending"
    COLLECTING = "collecting"
    ANALYZING = "analyzing"
    COMPLETED = "completed"
    FAILED = "failed"

class InstanceScan(BaseModel):
    scan_id: str                    # UUID
    instance_id: str                # i-0abc123
    account_id: str                 # 123456789012
    region: str                     # eu-west-1
    role_arn: str                   # Cross-account role
    external_id: str                # ExternalId for STS
    scan_mode: ScanMode             # live | forensic
    status: ScanStatus
    progress: int                   # 0-100
    created_at: str
    completed_at: str | None
    error_message: str | None

    # Instance metadata
    instance_type: str | None       # t3.medium
    ami_id: str | None
    platform: str | None            # Amazon Linux 2023

    # Results
    risk_score: int | None          # 0-100
    risk_level: str | None          # CRITICAL, HIGH, MEDIUM, LOW
    attack_vectors: list[dict] | None
    executive_summary: str | None

    # Storage references
    raw_data_s3_key: str | None     # S3 key for collected data
    report_s3_key: str | None       # S3 key for report
    report_url: str | None          # Pre-signed URL
```

### ScanFinding

Reuse existing `Finding` model with `source` set to `"instance-scanner"`.

### DynamoDB Table

New table: `cloudsecure-scans`
- PK: `scanId`
- GSI: `instanceId-index` (for scan history per instance)
- GSI: `accountId-index` (for scans per account)
- TTL: 90 days

### S3 Storage

```
s3://cloudsecure-reports-{account}/
  scans/{scanId}/
    raw-data.json          # Collected system data
    report.json            # Analysis report
    report.html            # HTML report (V2)
```

---

## Module Structure

```
lambdas/
  instance_scanner/
    handler.py              # Lambda: SSM execution + data collection
    collector.py            # SSM command builder + result parser
    collectors/
      system_info.py        # OS, kernel, users
      packages.py           # Package inventory
      network.py            # Ports, connections
      processes.py          # Running processes
    ssm_document.json       # SSM Document definition

  instance_analyzer/
    handler.py              # Lambda: analyze collected data, create findings
    attack_vectors.py       # Map findings to attack patterns

  shared/
    models.py               # + InstanceScan, ScanMode, ScanStatus
    scan_client.py          # SSM utility functions

infrastructure/
  lib/stacks/
    scan-stack.ts           # New CDK stack for instance scan resources
```

---

## AI Prompt Strategy

The AI prompt for instance scans is fundamentally different from account assessments:

### Live Mode Prompt

```
You are a senior penetration tester analyzing a live production EC2 instance.
Given the following system configuration data, identify:

1. **Attack Vectors**: How would an attacker compromise this system? List each
   vector with likelihood (HIGH/MEDIUM/LOW) and impact.
2. **Lateral Movement**: Once inside, how would an attacker move laterally?
3. **Data Exfiltration**: What sensitive data is accessible and how?
4. **Persistence**: How would an attacker maintain access?
5. **Remediation Priorities**: Ordered list of fixes, most critical first.

System data:
{collected_data_json}

Scan mode: live (production instance, focus on prevention)
```

### Forensic Mode Prompt

```
You are a digital forensics analyst investigating a potentially compromised
EC2 instance. Given the following system state, determine:

1. **Indicators of Compromise**: What evidence suggests the system was breached?
2. **Attack Timeline**: Reconstruct probable sequence of events.
3. **Scope of Impact**: What was accessed, modified, or exfiltrated?
4. **Persistence Mechanisms**: Are there backdoors or scheduled tasks?
5. **Containment Actions**: Immediate steps to limit damage.

System data:
{collected_data_json}

Scan mode: forensic (isolated instance, focus on investigation)
```

---

## OS Support

| Phase | Operating Systems |
|-------|------------------|
| MVP | Amazon Linux 2, Amazon Linux 2023 |
| V2 | + Ubuntu 20.04, 22.04, 24.04 |
| V3 | + RHEL 8/9, CentOS Stream, Debian |

OS detection via `/etc/os-release` determines which commands to run (e.g., `rpm -qa` vs `dpkg -l`).

---

## IAM Permissions Required

The cross-account CloudSecure role needs additional permissions:

```json
{
  "Effect": "Allow",
  "Action": [
    "ssm:SendCommand",
    "ssm:GetCommandInvocation",
    "ssm:DescribeInstanceInformation",
    "ec2:DescribeInstances"
  ],
  "Resource": "*"
}
```

The SSM Document should be scoped to read-only operations (no modifications to the instance).

---

## Phased Roadmap

### Sprint 7: MVP
- SSM connection + Tier 1 system inventory
- Single Lambda (collector + analyzer combined for simplicity)
- AI analysis with attack vector identification
- JSON report only
- Amazon Linux 2/2023 support
- `POST /scans` + `GET /scans/{scanId}` API endpoints
- New DynamoDB table + S3 prefix
- Raw data stored in S3

### Sprint 8: V2
- Web app analysis (Tier 2 data collection)
- Ubuntu support
- Separate collector/analyzer Lambdas
- Step Functions state machine
- HTML report with new template
- Forensic mode

### Sprint 9: V3
- Threat indicators (Tier 3 data collection)
- CVE cross-referencing for detected package versions
- Batch scan (all instances in an account)
- Integration with account assessment ("deep dive on flagged instances")
- RHEL/CentOS/Debian support

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| SSM command timeout | Scan fails on large instances | Timeout per command, collect in stages |
| OS variance | Commands fail on unsupported OS | OS detection first, fail gracefully |
| Shell output parsing | Structured data extraction brittle | Use JSON-friendly command flags where possible |
| SSM agent offline | Can't connect to instance | Validate SSM status before starting scan |
| Large output data | S3 costs, Lambda memory | Limit collection scope, compress output |
| Permission scope | SSM is powerful | SSM Document restricts to read-only commands |

---

## Test Case: ITC Incident

The manual ITC security investigation (8 hours) becomes the first validation test case:

> "This is what CloudSecure detects automatically in 10 minutes vs the 8 hours it took manually."

The scan should detect the same issues found during manual investigation: suspicious files, misconfigured permissions, outdated packages, exposed services.
