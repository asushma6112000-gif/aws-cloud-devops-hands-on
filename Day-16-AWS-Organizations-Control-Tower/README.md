# Day 16 – AWS Organizations & AWS Control Tower

## 1. Overview

In this session, I learned about AWS Organizations and AWS Control Tower, which help organizations manage multiple AWS accounts centrally.

Large companies use multiple AWS accounts to separate development, testing, production, security, and logging environments.

AWS Organizations provides centralized account management, consolidated billing, and Service Control Policies (SCPs).

AWS Control Tower helps automate the setup and governance of a secure multi-account AWS environment.

## 2. What is AWS Organizations?

AWS Organizations is an AWS service that allows companies to centrally manage multiple AWS accounts under one organization.

Instead of managing every AWS account independently, companies can organize and manage them from a central management account.

### Why do companies use AWS Organizations?

- Centralized management of multiple AWS accounts.
- Consolidated billing.
- Account separation for different teams and environments.
- Service Control Policies (SCPs).
- Organizational Units (OUs).
- Improved security and governance.

## 3. AWS Organizations Architecture

```text
                  AWS Organization
                         |
                  Management Account
                         |
                    Organization
                         |
          +--------------+--------------+
          |              |              |
       Data OU       Middleware OU    Security OU
          |              |              |
       +--+--+         +--+--+        Security
       |  |  |         |  |  |
      Dev Pre Prod    Dev Pre Prod
```

Each AWS account has its own unique AWS account ID and its own root user.

The management account centrally manages the organization.

## 4. Important Components of AWS Organizations

### Management Account
- Creates and manages the organization.
- Invites existing AWS accounts.
- Creates new member accounts.
- Manages consolidated billing.

### Member Account
- An individual AWS account that belongs to an organization.
- Has its own account ID and its own root user.
- Is centrally managed through the organization.

### Organizational Units (OU)

OUs are logical groups used to organize AWS accounts.

Example:
- Development OU
- Production OU
- Security OU
- Testing OU

### Service Control Policies (SCP)

SCPs define the maximum permissions available to IAM users and roles in member accounts.

Example:

A company can restrict certain AWS services or actions in production accounts.

Important: SCPs do not grant permissions. IAM policies must also allow the requested actions.

## 5. Adding an Existing AWS Account

An existing AWS account can join an organization through an invitation.

### Workflow

1. Log in to the management account.
2. Open AWS Organizations.
3. Select Add an AWS Account.
4. Select Invite an existing AWS account.
5. Enter the existing AWS account ID or email address.
6. Send the invitation.
7. Log in to the invited AWS account.
8. Open the Organizations invitation.
9. Accept the invitation.
10. The account becomes a member account.

### Architecture

```text
Management Account
        |
        | Send Invitation
        |
        v
Existing AWS Account
        |
        | Accept Invitation
        |
        v
Member Account
        |
        v
AWS Organization
```

## 6. Creating a New AWS Account

AWS Organizations also allows the management account to create additional AWS accounts.

Example:

```text
AWS Organization
       |
Management Account
       |
       +------ Create Account
                    |
               Development
                    |
               New Account ID
```

A newly created account is automatically added to the organization.

## 7. Consolidated Billing

Consolidated billing allows a company to view charges from multiple AWS accounts centrally.

Example:

```text
              AWS Organization
                     |
              Management Account
                     |
          +----------+----------+
          |          |          |
         Dev       Testing      Prod
          |          |          |
        Bills      Bills       Bills
          |          |          |
          +----------+----------+
                     |
              Consolidated Bill
```

Benefits:
- Centralized billing visibility.
- Combined usage information.
- Easier cost management.
- Potential volume pricing benefits.

AWS Organizations itself has no additional service charge, but AWS resources running in member accounts can generate charges.

## 8. What is AWS Control Tower?

AWS Control Tower is a service that helps companies set up and govern a secure multi-account AWS environment.

This standardized environment is called a Landing Zone.

It uses AWS Organizations and integrates with other AWS services to establish governance and security baselines.

### Why do companies use Control Tower?

- Automated multi-account environment setup.
- Standardized account provisioning.
- Centralized governance.
- Security and compliance controls.
- Centralized logging and auditing.

## 9. AWS Control Tower Architecture

```text
                 AWS Control Tower
                         |
                         v
                 Landing Zone
                         |
                  AWS Organizations
                         |
             +-----------+-----------+
             |           |           |
        Management   Log Archive   Audit
         Account      Account     Account
             |
             v
       Organizational Units
             |
       +-----+------+
       |            |
   Development   Production
       OU            OU
       |             |
     Accounts      Accounts
```

### Important Control Tower Components

**Landing Zone:** A governed multi-account AWS environment with standardized security and operational configurations.

**Account Factory:** Helps provision new AWS accounts using predefined configurations.

**Log Archive Account:** Dedicated account for centrally storing and protecting logs.

**Audit Account:** Dedicated account for security auditing and compliance activities.

**Guardrails / Controls:** Preventive, detective, and proactive controls that help enforce governance requirements.

## 10. AWS Organizations vs AWS Control Tower

| AWS Organizations | AWS Control Tower |
|---|---|
| Manages multiple AWS accounts | Establishes a governed multi-account environment |
| Supports consolidated billing | Provides landing zone setup |
| Supports SCPs | Provides governance controls |
| Allows account creation and invitations | Provides Account Factory |
| Central account management | Automated governance and standardization |

## 11. Real-Time Company Scenario

Consider a company called Bharati that currently runs its infrastructure using on-premises NAS and SAN storage.

The company wants to migrate its applications, historical data, and infrastructure to AWS.

It has different teams:

- Data Team
- Full Stack Team
- Middleware Team
- QA Team
- Security Team

Each team needs separate development, pre-production, and production environments.

AWS Organizations helps centrally manage these separate AWS accounts.

AWS Control Tower helps establish a standardized multi-account landing zone with security and governance controls.

## 12. What I Learned

- AWS Organizations and its purpose.
- Management accounts and member accounts.
- Organizational Units (OUs).
- Service Control Policies (SCPs).
- Inviting existing AWS accounts.
- Creating new AWS accounts.
- Consolidated billing.
- AWS Control Tower and Landing Zones.
- Account Factory and governance controls.
- Differences between AWS Organizations and Control Tower.

## 13. Practical Scope

This session was completed through theoretical learning and architecture study.

- Studied AWS Organizations.
- Understood the existing account invitation workflow.
- Studied consolidated billing.
- Understood SCPs and OUs.
- Studied AWS Control Tower architecture.
- Did not deploy AWS Control Tower or create additional AWS accounts as part of this learning session.

## 14. Conclusion

AWS Organizations and AWS Control Tower are important services for companies managing large AWS environments.

AWS Organizations provides centralized account management, while AWS Control Tower simplifies multi-account environment setup and governance.

Understanding these services helps in designing secure and well-organized AWS cloud infrastructure.
