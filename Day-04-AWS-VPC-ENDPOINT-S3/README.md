# Day 4 — AWS VPC Endpoint with S3

## 📌 Project Overview

In this hands-on project, I learned how an **AWS VPC Endpoint** provides private connectivity between resources inside a VPC and AWS services such as Amazon S3.

I created a VPC with **public and private subnets**, launched public and private EC2 instances, created an S3 bucket, attached an IAM role with S3 permissions to the EC2 instances, and configured an **S3 Gateway VPC Endpoint** for private access from the private EC2 instance.

The main concept I learned is:

> **IAM provides permission, while a VPC Endpoint provides private network connectivity to AWS services.**

---

## 🏗️ Architecture

```text
                         AWS Cloud
                             |
                    +--------+--------+
                    |       VPC       |
                    |                 |
              +-----+-----+     +-----+------+
              | Public    |     | Private    |
              | Subnet    |     | Subnet     |
              |           |     |            |
              | Public EC2|---->| Private EC2|
              |           | SSH |            |
              +-----------+     +-----+------+
                                      |
                                      |
                              Private Route Table
                                      |
                                      |
                            S3 Gateway VPC Endpoint
                                      |
                                      |
                               Amazon S3 Bucket
                                      |
                                day4-test.txt
```

### Service-to-Service Flow

```text
Public EC2
    |
    | SSH
    v
Private EC2
    |
    | Route Table
    v
S3 Gateway VPC Endpoint
    |
    | Private connectivity
    v
Amazon S3
```

IAM works alongside this flow:

```text
EC2
 |
 | IAM Role
 | Amazon S3 permissions
 v
Permission to access S3
```

---

# 🎯 What I Learned

## 1. VPC

I learned how to create a VPC and understand the relationship between:

* VPC
* Availability Zone
* Public Subnet
* Private Subnet
* Route Table
* Internet Gateway
* VPC Endpoint

For this lab, I created one public subnet and one private subnet.

---

## 2. Public Subnet vs Private Subnet

### Public Subnet

The public subnet had:

* Route to Internet Gateway
* Auto-assign public IPv4 enabled
* Public EC2 instance

### Private Subnet

The private subnet had:

* No public IPv4 address
* Private EC2 instance
* Private route table
* S3 Gateway VPC Endpoint

The private EC2 did not need a public IP to communicate with S3 through the Gateway Endpoint.

---

# 3. EC2

I launched two EC2 instances:

### Public EC2

Used for:

* Internet connectivity
* Connecting to the private EC2
* Testing AWS CLI access

### Private EC2

Used for:

* Testing private subnet connectivity
* Accessing S3 through the VPC Endpoint

Both EC2 instances used an IAM role with S3 permissions.

---

# 4. IAM Role

I attached an IAM role containing:

```text
AmazonS3FullAccess
```

to both EC2 instances.

This taught me an important distinction:

```text
IAM Role
    ↓
Provides permission
    ↓
EC2 is authorized to access S3
```

IAM does **not** create network connectivity.

---

# 5. Amazon S3

I created an S3 bucket:

```text
sushma-day4-vpc-endpoint-s3-2026
```

I uploaded:

```text
day4-test.txt
```

The object was used to test S3 access from the EC2 instances.

---

# 6. VPC Endpoint

I created an:

**S3 Gateway VPC Endpoint**

Service:

```text
com.amazonaws.ap-south-2.s3
```

Region:

```text
Asia Pacific (Hyderabad)
ap-south-2
```

Endpoint type:

```text
Gateway
```

The endpoint was associated with the **private subnet's route table**.

---

# 7. Why Gateway Endpoint?

For Amazon S3, I used a **Gateway VPC Endpoint**.

The important difference I learned is:

```text
Gateway Endpoint
    ↓
Uses route tables
    ↓
No ENI required
    ↓
No Security Group required
```

For this lab, I selected the private route table.

---

# 🔄 Project Workflow — Step by Step

## Step 1 — Create the VPC

I created a VPC using the AWS VPC creation wizard.

Configuration included:

* VPC
* 1 Availability Zone
* 1 Public Subnet
* 1 Private Subnet
* No NAT Gateway
* No VPC Endpoint initially

---

## Step 2 — Configure Public Subnet

I enabled:

```text
Auto-assign public IPv4 address
```

This allowed the EC2 launched in the public subnet to receive a public IP.

---

## Step 3 — Configure Private Subnet

The private subnet did not automatically assign public IPv4 addresses.

The private EC2 therefore communicated using its private IP.

---

## Step 4 — Launch Public EC2

I launched an EC2 instance in the public subnet.

The public EC2 received a public IPv4 address.

I used it as the entry point to connect to the private EC2.

---

## Step 5 — Launch Private EC2

I launched another EC2 instance in the private subnet.

The private EC2 did not have a public IPv4 address.

---

## Step 6 — Create S3 Bucket

I created:

```text
sushma-day4-vpc-endpoint-s3-2026
```

and uploaded:

```text
day4-test.txt
```

---

## Step 7 — Attach IAM Role

I attached an IAM role with:

```text
AmazonS3FullAccess
```

to both EC2 instances.

This allowed the AWS CLI running on EC2 to authenticate and access S3 according to the IAM permissions.

---

## Step 8 — Test S3 Access from Public EC2

I connected to the public EC2 and verified the AWS CLI.

Example:

```bash
aws --version
```

Then I tested access to the S3 object.

This confirmed that the public EC2 had the required IAM permission and network access.

---

## Step 9 — Connect from Public EC2 to Private EC2

Because the private EC2 had no public IP, I connected to it through the public EC2.

Flow:

```text
My Computer
     |
     | SSH
     v
Public EC2
     |
     | SSH using private IP
     v
Private EC2
```

---

## Step 10 — Test S3 Access from Private EC2

Before the endpoint configuration, I tested S3 access from the private EC2.

The test demonstrated that **having IAM permission alone is not the same as having the required network path**.

I then configured the VPC Endpoint.

---

## Step 11 — Create S3 Gateway VPC Endpoint

I created:

```text
S3 Gateway VPC Endpoint
```

Service:

```text
com.amazonaws.ap-south-2.s3
```

I selected my VPC and associated the endpoint with the **private route table**.

---

## Step 12 — Route Table Integration

The important flow became:

```text
Private EC2
     |
     v
Private Subnet
     |
     v
Private Route Table
     |
     v
S3 Gateway VPC Endpoint
     |
     v
Amazon S3
```

The endpoint provides the private network path to S3.

---

## Step 13 — Test Again from Private EC2

From the private EC2, I ran:

```bash
aws s3 cp s3://sushma-day4-vpc-endpoint-s3-2026/day4-test.txt .
```

The file was successfully downloaded.

This verified that the private EC2 could access the S3 object through the configured S3 Gateway VPC Endpoint.

---

# 🔐 Security Understanding

For this lab, I temporarily used an open Security Group rule to simplify testing.

```text
Inbound: All traffic from 0.0.0.0/0
```

This was **lab-only**.

In a production environment, I would use the principle of least privilege and allow only the required ports, sources, and protocols.

---

# 🧠 Most Important Concept

The most important lesson from this project is:

```text
IAM
 ↓
"Are you allowed?"

VPC Endpoint
 ↓
"How does the traffic privately reach S3?"
```

Both are different.

### IAM

Controls:

```text
Authentication / Authorization
Permissions
```

### VPC Endpoint

Provides:

```text
Private network connectivity
```

Therefore:

```text
IAM Permission
       +
Network Connectivity
       =
Successful S3 Access
```

---

# 📸 Project Screenshots

## 1. Public and Private EC2

`01-Public-Private-EC2.png`

Shows the two EC2 instances used in the lab.

## 2. S3 Bucket and Test Object

`02-S3-Bucket-Day4-Test-Object.png`

Shows the S3 bucket and `day4-test.txt`.

## 3. Private Route Table and S3 Endpoint

`03-Private-Route-Table-S3-Endpoint.png`

Shows the private route table associated with the endpoint.

## 4. Public EC2 → Private EC2 → S3 Test

`04-Public-EC2-to-Private-EC2-and-S3-Test.png`

Shows the connection from the public EC2 to the private EC2 and the S3 access test.

## 5. S3 Gateway VPC Endpoint

`05-S3-Gateway-VPC-Endpoint-Available.png`

Shows the S3 Gateway VPC Endpoint in **Available** state.

---

# 💻 Commands Used

Check AWS CLI:

```bash
aws --version
```

Check current identity:

```bash
aws sts get-caller-identity
```

List S3 buckets:

```bash
aws s3 ls
```

Copy the test object from S3:

```bash
aws s3 cp s3://sushma-day4-vpc-endpoint-s3-2026/day4-test.txt .
```

List files:

```bash
ls
```

---

# 🎤 Interview Explanation

### Question: What did you do in this project?

**Answer:**

I created a VPC with a public and private subnet and launched two EC2 instances. I created an S3 bucket and uploaded a test object. I attached an IAM role with S3 permissions to the EC2 instances.

I connected to the private EC2 through the public EC2 and tested S3 access. Then I created an S3 Gateway VPC Endpoint and associated it with the private subnet's route table.

After configuring the endpoint, the private EC2 successfully downloaded the S3 object without requiring a public IP or NAT Gateway.

The key concept I learned is that **IAM controls permission, while the VPC Endpoint provides private connectivity to S3**.

---

# ⭐ Senior-Level Understanding

A VPC Endpoint is useful when workloads in private subnets need to communicate with supported AWS services without sending that traffic through the public internet.

For Amazon S3, a Gateway Endpoint can be associated with route tables.

The architecture I implemented was:

```text
Private EC2
     ↓
Private Subnet
     ↓
Private Route Table
     ↓
S3 Gateway VPC Endpoint
     ↓
Amazon S3
```

This can help reduce the need for NAT Gateway connectivity for S3 access and keeps the traffic on AWS's private networking path.

---

# 📚 Key Takeaways

* VPC provides network isolation.
* Public and private subnets serve different purposes.
* EC2 can have private connectivity without a public IP.
* IAM controls permissions.
* IAM does not provide network connectivity.
* S3 Gateway VPC Endpoint provides private connectivity to S3.
* Gateway Endpoints use route tables.
* NAT Gateway was not required for this S3 access path.
* Route tables determine where network traffic is sent.
* Least-privilege Security Groups should be used in production.
* Private workloads can access AWS services without requiring public internet access.

---

## 🏁 Final Architecture Flow

```text
                 AWS VPC
                   |
        +----------+----------+
        |                     |
   Public Subnet         Private Subnet
        |                     |
   Public EC2             Private EC2
        |                     |
        | SSH                 |
        +-------------------->|
                              |
                       Private Route Table
                              |
                              v
                    S3 Gateway VPC Endpoint
                              |
                              v
                         Amazon S3
                              |
                              v
                       day4-test.txt
```

### Core Formula

```text
IAM = Permission
VPC Endpoint = Private Connectivity
Route Table = Traffic Direction
S3 = AWS Service
```

**Result:** Private EC2 successfully accessed the S3 object through the S3 Gateway VPC Endpoint.

