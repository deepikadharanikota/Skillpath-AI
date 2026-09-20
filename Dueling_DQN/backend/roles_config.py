"""
roles_config.py
---------------
Comprehensive, extensible Target Role Taxonomy and Curriculum Syllabus for SkillPath AI.
Defines:
1. ROLES_REGISTRY: Detailed metadata, focus, core skills, and ordered roadmaps with prerequisites.
2. TOPIC_SYLLABUS: 4-module hierarchical curriculum breakdown per topic with concrete subtopics.
3. Helper functions for roadmap extraction, prerequisite ordering, and syllabus retrieval.
"""

from typing import Dict, List, Any, Optional

# ══════════════════════════════════════════════════════════════════════════════
# TOPIC SYLLABUS: 4 Hierarchical Modules per Topic
# ══════════════════════════════════════════════════════════════════════════════
TOPIC_SYLLABUS: Dict[str, Dict[str, Any]] = {
    "Docker": {
        "title": "Docker Containerization",
        "description": "Container virtualization, images, multi-container orchestration with Docker Compose",
        "modules": {
            "intro": {
                "title": "Module 1: Docker Fundamentals",
                "focus": "Core concepts and installation",
                "subtopics": [
                    "What is Docker & Containerization?",
                    "Containers vs Virtual Machines",
                    "Docker Architecture & Daemon",
                    "Installing & Configuring Docker"
                ]
            },
            "core": {
                "title": "Module 2: Docker Images & Dockerfiles",
                "focus": "Building and managing container images",
                "subtopics": [
                    "Understanding Base Images",
                    "Writing Efficient Dockerfiles",
                    "Docker Build, Tag & Push",
                    "Docker Hub & Image Registries"
                ]
            },
            "advanced": {
                "title": "Module 3: Containers & Networking",
                "focus": "Runtime lifecycle, volumes, and networking",
                "subtopics": [
                    "Container Lifecycle & CLI Commands",
                    "Port Publishing & Binding",
                    "Persistent Storage with Volumes & Bind Mounts",
                    "Bridge, Host & Overlay Networks"
                ]
            },
            "summary": {
                "title": "Module 4: Docker Compose & Orchestration",
                "focus": "Multi-container applications and best practices",
                "subtopics": [
                    "Docker Compose Fundamentals",
                    "Defining Multi-Container Architectures",
                    "Environment Variables & Secrets",
                    "Multi-Stage Builds & Production Optimization"
                ]
            }
        }
    },
    "Kubernetes": {
        "title": "Kubernetes Orchestration",
        "description": "Production container orchestration, scaling, pods, services, ingress, and Helm",
        "modules": {
            "intro": {
                "title": "Module 1: Kubernetes Architecture & Pods",
                "focus": "Cluster control plane and workload primitives",
                "subtopics": [
                    "Kubernetes Architecture (Control Plane & Worker Nodes)",
                    "kubectl CLI & Cluster Contexts",
                    "Pods & Multi-Container Pod Patterns",
                    "Namespaces & Resource Quotas"
                ]
            },
            "core": {
                "title": "Module 2: Deployments & Replicas",
                "focus": "Declarative workloads and updates",
                "subtopics": [
                    "Deployments & ReplicaSets",
                    "Rolling Updates & Rollbacks",
                    "Health Probes (Liveness, Readiness, Startup)",
                    "ConfigMaps & Secrets Management"
                ]
            },
            "advanced": {
                "title": "Module 3: Services, Ingress & Networking",
                "focus": "Service discovery and external traffic routing",
                "subtopics": [
                    "ClusterIP, NodePort & LoadBalancer Services",
                    "Ingress Controllers & Ingress Rules",
                    "PersistentVolumes & PVCs",
                    "NetworkPolicies & Cluster Security"
                ]
            },
            "summary": {
                "title": "Module 4: Helm & Cluster Troubleshooting",
                "focus": "Package management and production operations",
                "subtopics": [
                    "Helm Charts & Template Management",
                    "StatefulSets & DaemonSets",
                    "Cluster Logging & Metrics Troubleshooting",
                    "Production Best Practices & High Availability"
                ]
            }
        }
    },
    "Linux": {
        "title": "Linux Systems & Administration",
        "description": "Operating system fundamentals, bash scripting, file permissions, processes, and SSH",
        "modules": {
            "intro": {
                "title": "Module 1: Linux Fundamentals & File System",
                "focus": "File system navigation and core commands",
                "subtopics": [
                    "Linux File System Hierarchy (FHS)",
                    "Essential CLI Commands (ls, cd, grep, find, cat)",
                    "File Permissions (chmod, chown, umask)",
                    "Text Processing (sed, awk, cut, sort)"
                ]
            },
            "core": {
                "title": "Module 2: Processes, Services & Systemd",
                "focus": "Process management and service daemons",
                "subtopics": [
                    "Process Lifecycle & Monitoring (ps, top, htop, kill)",
                    "Systemd Services & systemctl Management",
                    "Crontab & Scheduled Jobs",
                    "Log Inspection with journalctl & /var/log"
                ]
            },
            "advanced": {
                "title": "Module 3: Bash Scripting & Automation",
                "focus": "Shell scripting, variables, logic, and functions",
                "subtopics": [
                    "Bash Script Anatomy & Shebang",
                    "Variables, Arguments & Environment Variables",
                    "Conditionals, Loops & Exit Codes",
                    "Writing Robust Automation Scripts"
                ]
            },
            "summary": {
                "title": "Module 4: Networking, SSH & Security",
                "focus": "Remote administration and system hardening",
                "subtopics": [
                    "SSH Key Pairs & Secure Remote Access",
                    "Network Tools (netstat, ss, curl, ip, dig)",
                    "User & Group Administration (sudoers)",
                    "Firewall Configuration (iptables, ufw)"
                ]
            }
        }
    },
    "Git": {
        "title": "Git & GitHub Version Control",
        "description": "Distributed version control, branching strategies, collaborative workflows, and merge conflicts",
        "modules": {
            "intro": {
                "title": "Module 1: Git Basics & Commits",
                "focus": "Working directory, staging area, and history",
                "subtopics": [
                    "Version Control Principles",
                    "Initializing Repositories & .gitignore",
                    "Staging, Committing & Git Log",
                    "Viewing Diffs and Inspecting History"
                ]
            },
            "core": {
                "title": "Module 2: Branching & Merging",
                "focus": "Branch creation, merges, and conflicts",
                "subtopics": [
                    "Creating & Switching Branches",
                    "Fast-Forward vs Three-Way Merges",
                    "Identifying & Resolving Merge Conflicts",
                    "Git Stash & Temporary Workspace"
                ]
            },
            "advanced": {
                "title": "Module 3: GitHub & Collaboration",
                "focus": "Remote repositories, PRs, and branch protection",
                "subtopics": [
                    "Remotes (git push, git pull, git fetch)",
                    "Pull Requests & Code Reviews",
                    "Branch Protection Rules & PR Approvals",
                    "Forking & Upstream Synchronization"
                ]
            },
            "summary": {
                "title": "Module 4: Advanced Git & Workflows",
                "focus": "Rebasing, cherry-pick, and team workflows",
                "subtopics": [
                    "Git Rebase vs Merge",
                    "Cherry-Picking & Reset vs Revert",
                    "Git Flow vs Trunk-Based Development",
                    "Git Hooks & Automated Quality Checks"
                ]
            }
        }
    },
    "CI/CD": {
        "title": "CI/CD Pipelines & Automation",
        "description": "Continuous Integration, automated testing, GitHub Actions, Jenkins, and delivery pipelines",
        "modules": {
            "intro": {
                "title": "Module 1: CI/CD Principles & Pipelines",
                "focus": "Continuous integration and build automation",
                "subtopics": [
                    "What is Continuous Integration & Continuous Delivery?",
                    "Anatomy of a Build Pipeline",
                    "Automated Testing in Pipelines",
                    "Artifact Generation & Versioning"
                ]
            },
            "core": {
                "title": "Module 2: GitHub Actions Workflows",
                "focus": "Declarative YAML workflows and triggers",
                "subtopics": [
                    "Workflow Syntax, Events & Triggers",
                    "Jobs, Steps & Community Actions",
                    "Secrets Management & Environment Variables",
                    "Matrix Builds & Parallel Execution"
                ]
            },
            "advanced": {
                "title": "Module 3: Jenkins & Pipeline as Code",
                "focus": "Enterprise Jenkins pipelines and agents",
                "subtopics": [
                    "Jenkins Architecture & Controller-Agent Model",
                    "Jenkinsfile (Declarative vs Scripted)",
                    "Pipeline Stages, Post Actions & Credentials",
                    "Integrating SonarQube & Security Scanners"
                ]
            },
            "summary": {
                "title": "Module 4: Deployment Strategies & Release",
                "focus": "Automated deployments and release safety",
                "subtopics": [
                    "Deploying to Staging & Production",
                    "Rolling, Blue-Green & Canary Deployments",
                    "Pipeline Rollbacks & Automated Health Gates",
                    "DevOps Metrics (DORA Metrics & Lead Time)"
                ]
            }
        }
    },
    "AWS Cloud": {
        "title": "AWS Cloud Architecture",
        "description": "Amazon Web Services infrastructure, compute, storage, networking, IAM, and deployment",
        "modules": {
            "intro": {
                "title": "Module 1: AWS Fundamentals & IAM",
                "focus": "Cloud foundations, regions, and security",
                "subtopics": [
                    "Cloud Computing Concepts & AWS Regions/AZs",
                    "AWS Identity & Access Management (IAM)",
                    "IAM Users, Roles, Policies & Groups",
                    "Least Privilege Security Practices"
                ]
            },
            "core": {
                "title": "Module 2: Compute & Storage (EC2 & S3)",
                "focus": "Virtual machines, auto scaling, and object storage",
                "subtopics": [
                    "Amazon EC2 Instances & AMIs",
                    "Auto Scaling Groups & Elastic Load Balancers (ALB)",
                    "Amazon S3 Buckets, Storage Classes & Lifecycle",
                    "Elastic Block Store (EBS) & Snapshot Backups"
                ]
            },
            "advanced": {
                "title": "Module 3: VPC Networking & Databases",
                "focus": "Virtual private clouds, subnets, and RDS",
                "subtopics": [
                    "VPC Architecture, Subnets & Internet Gateways",
                    "Route Tables, NAT Gateways & Security Groups",
                    "Amazon RDS & Aurora Relational Databases",
                    "Amazon DynamoDB NoSQL Database"
                ]
            },
            "summary": {
                "title": "Module 4: Serverless, Containers & CloudWatch",
                "focus": "ECS, EKS, Lambda, and CloudWatch monitoring",
                "subtopics": [
                    "AWS Lambda & API Gateway Serverless",
                    "Amazon ECS & Elastic Kubernetes Service (EKS)",
                    "CloudWatch Metrics, Alarms & Logs",
                    "CloudFormation & Cloud Deployment Automation"
                ]
            }
        }
    },
    "Terraform": {
        "title": "Infrastructure as Code with Terraform",
        "description": "Declarative infrastructure provisioning, HCL, state management, modules, and providers",
        "modules": {
            "intro": {
                "title": "Module 1: IaC Fundamentals & Terraform Syntax",
                "focus": "HashiCorp Configuration Language (HCL)",
                "subtopics": [
                    "What is Infrastructure as Code (IaC)?",
                    "Terraform Architecture & Providers",
                    "HCL Syntax (Resources, Data Sources, Variables)",
                    "Terraform CLI (init, plan, apply, destroy)"
                ]
            },
            "core": {
                "title": "Module 2: State Management & Backends",
                "focus": "Terraform state, locking, and remote storage",
                "subtopics": [
                    "Understanding terraform.tfstate",
                    "Remote State with AWS S3 & DynamoDB Locking",
                    "State Inspection & State Migration",
                    "Sensitive Variables & Outputs"
                ]
            },
            "advanced": {
                "title": "Module 3: Modular Architecture",
                "focus": "Reusable Terraform modules and environments",
                "subtopics": [
                    "Writing Custom Terraform Modules",
                    "Public Terraform Registry Modules",
                    "Multi-Environment Management (Dev, Stage, Prod)",
                    "Terraform Workspaces vs Directory Layouts"
                ]
            },
            "summary": {
                "title": "Module 4: CI/CD Integration & Security",
                "focus": "Automated Terraform pipelines and policy as code",
                "subtopics": [
                    "Running Terraform in GitHub Actions / GitLab",
                    "Static Code Analysis with tfsec & tflint",
                    "Drift Detection & Remediation",
                    "Ansible Integration for Configuration Management"
                ]
            }
        }
    },
    "Prometheus & Grafana": {
        "title": "Monitoring & Observability",
        "description": "Metrics collection, Prometheus server, PromQL, Alertmanager, and Grafana dashboards",
        "modules": {
            "intro": {
                "title": "Module 1: Observability Foundations",
                "focus": "Metrics, logs, traces, and Prometheus basics",
                "subtopics": [
                    "The Three Pillars of Observability",
                    "Prometheus Architecture & Pull Model",
                    "Metric Types (Counter, Gauge, Histogram, Summary)",
                    "Node Exporter Installation & Metrics Scraping"
                ]
            },
            "core": {
                "title": "Module 2: PromQL & Querying",
                "focus": "Writing expressive PromQL queries",
                "subtopics": [
                    "Instant Vectors vs Range Vectors",
                    "Rate, Increase & Aggregation Functions",
                    "Label Filtering & Regex Matching",
                    "PromQL for System & Application Performance"
                ]
            },
            "advanced": {
                "title": "Module 3: Grafana Dashboard Engineering",
                "focus": "Visualizing metrics and building actionable dashboards",
                "subtopics": [
                    "Connecting Prometheus Data Sources",
                    "Building Responsive Panels & Graphs",
                    "Dashboard Variables & Dynamic Templating",
                    "Golden Signals Dashboards (Latency, Traffic, Errors, Saturation)"
                ]
            },
            "summary": {
                "title": "Module 4: Alertmanager & Production Operations",
                "focus": "Alerting rules, notification channels, and on-call",
                "subtopics": [
                    "Defining Alerting Rules in Prometheus",
                    "Alertmanager Configuration & Grouping",
                    "Routing Alerts to Slack, PagerDuty & Email",
                    "SRE Best Practices: SLOs, SLIs, and Error Budgets"
                ]
            }
        }
    },
    "Networking": {
        "title": "DevOps Networking & Security",
        "description": "TCP/IP, DNS, HTTP/HTTPS, load balancers, reverse proxies, and firewalls",
        "modules": {
            "intro": {
                "title": "Module 1: OSI Model & TCP/IP Protocol",
                "focus": "Network layers and packet transport",
                "subtopics": [
                    "The OSI 7-Layer & TCP/IP Models",
                    "IP Addressing, Subnets & CIDR Notation",
                    "TCP 3-Way Handshake & UDP",
                    "Ports & Socket Connections"
                ]
            },
            "core": {
                "title": "Module 2: DNS, HTTP & SSL/TLS",
                "focus": "Web protocols and domain resolution",
                "subtopics": [
                    "How DNS Works (A, CNAME, MX, TXT Records)",
                    "HTTP/1.1 vs HTTP/2 vs HTTP/3",
                    "HTTPS, SSL/TLS Handshake & Certificates",
                    "Let's Encrypt & Automated Certificate Renewal"
                ]
            },
            "advanced": {
                "title": "Module 3: Reverse Proxies & Load Balancing",
                "focus": "Nginx, HAProxy, and traffic distribution",
                "subtopics": [
                    "Forward vs Reverse Proxies",
                    "Configuring Nginx as a Reverse Proxy",
                    "Load Balancing Algorithms (Round Robin, Least Connections)",
                    "Health Checks, Sticky Sessions & SSL Termination"
                ]
            },
            "summary": {
                "title": "Module 4: Network Security & Firewalls",
                "focus": "Security hardening and perimeter defense",
                "subtopics": [
                    "Firewalls & Packet Filtering (iptables, nftables)",
                    "VPNs, Bastion Hosts & SSH Tunnels",
                    "DDoS Mitigation & Web Application Firewalls (WAF)",
                    "Network Troubleshooting Tools (traceroute, tcpdump, Wireshark)"
                ]
            }
        }
    },
    "DevSecOps": {
        "title": "DevSecOps & Security Engineering",
        "description": "Security in CI/CD, container security, vulnerability scanning, secrets management, and compliance",
        "modules": {
            "intro": {
                "title": "Module 1: DevSecOps Fundamentals",
                "focus": "Shift-left security principles",
                "subtopics": [
                    "Introduction to DevSecOps & Shift-Left",
                    "OWASP Top 10 Security Risks",
                    "Static Application Security Testing (SAST)",
                    "Dynamic Application Security Testing (DAST)"
                ]
            },
            "core": {
                "title": "Module 2: Secrets Management",
                "focus": "Securing credentials and API keys",
                "subtopics": [
                    "Eliminating Hardcoded Secrets",
                    "HashiCorp Vault Architecture & Engines",
                    "AWS Secrets Manager & Parameter Store",
                    "Injecting Secrets into Kubernetes & CI/CD"
                ]
            },
            "advanced": {
                "title": "Module 3: Container & Supply Chain Security",
                "focus": "Image scanning, rootless containers, and SBOM",
                "subtopics": [
                    "Container Vulnerability Scanning (Trivy, Grype)",
                    "Non-Root Containers & Distroless Images",
                    "Software Bill of Materials (SBOM)",
                    "Image Signing & Verification with Cosign"
                ]
            },
            "summary": {
                "title": "Module 4: Policy as Code & Incident Response",
                "focus": "OPA, Gatekeeper, and automated governance",
                "subtopics": [
                    "Open Policy Agent (OPA) & Rego Policies",
                    "Kubernetes Admission Controllers & Kyverno",
                    "Audit Logging & Security Information (SIEM)",
                    "Automated Security Gates in Release Pipelines"
                ]
            }
        }
    },
    "React": {
        "title": "React UI Engineering",
        "description": "Modern React, hooks, state management, component architecture, and responsive design",
        "modules": {
            "intro": {
                "title": "Module 1: React Fundamentals & JSX",
                "focus": "Virtual DOM, JSX, components, and props",
                "subtopics": [
                    "React Architecture & Virtual DOM",
                    "JSX Syntax & Element Rendering",
                    "Functional Components & Props",
                    "Component Composition & Reusability"
                ]
            },
            "core": {
                "title": "Module 2: State & React Hooks",
                "focus": "useState, useEffect, and custom hooks",
                "subtopics": [
                    "useState & State Updates",
                    "useEffect & Component Lifecycles",
                    "Handling Forms & User Input Events",
                    "Building Reusable Custom Hooks"
                ]
            },
            "advanced": {
                "title": "Module 3: State Management & Routing",
                "focus": "Context API, Redux/Zustand, and React Router",
                "subtopics": [
                    "Prop Drilling & React Context API",
                    "Global State with Zustand or Redux Toolkit",
                    "Client-Side Routing with React Router",
                    "Performance Optimization (useMemo, useCallback, memo)"
                ]
            },
            "summary": {
                "title": "Module 4: API Integration & Testing",
                "focus": "REST APIs, testing, and production deployment",
                "subtopics": [
                    "Fetching Data with Axios & React Query",
                    "Error Boundaries & Suspense",
                    "Unit Testing with Jest & React Testing Library",
                    "Vite / Next.js Production Build & Deployment"
                ]
            }
        }
    },
    "JavaScript": {
        "title": "Modern JavaScript (ES6+)",
        "description": "Core language mechanics, asynchronous programming, DOM, closures, and modern patterns",
        "modules": {
            "intro": {
                "title": "Module 1: JavaScript Language Foundations",
                "focus": "Types, variables, operators, and control flow",
                "subtopics": [
                    "Data Types, Primitives & Objects",
                    "let, const, and Block Scoping",
                    "Arrow Functions & Template Literals",
                    "Destructuring, Spread & Rest Operators"
                ]
            },
            "core": {
                "title": "Module 2: Asynchronous JavaScript",
                "focus": "Event loop, promises, and async/await",
                "subtopics": [
                    "The JavaScript Event Loop & Call Stack",
                    "Callbacks & Callback Hell",
                    "Promises & Promise Combinators (all, race)",
                    "Async / Await and Error Handling"
                ]
            },
            "advanced": {
                "title": "Module 3: Closures, Prototypes & Scope",
                "focus": "Execution contexts, prototypes, and OOP",
                "subtopics": [
                    "Lexical Scope & Closures",
                    "The 'this' Keyword & Binding (bind, call, apply)",
                    "Prototypes, Prototypal Inheritance & Classes",
                    "ES Modules (import / export)"
                ]
            },
            "summary": {
                "title": "Module 4: Web APIs, Storage & Tooling",
                "focus": "Browser APIs, Fetch, and module bundlers",
                "subtopics": [
                    "Fetch API & Handling JSON Data",
                    "LocalStorage, SessionStorage & IndexedDB",
                    "Modern Build Tools (Vite, Webpack, Babel)",
                    "Clean Code & Design Patterns in JavaScript"
                ]
            }
        }
    },
    "TypeScript": {
        "title": "TypeScript for Enterprise Applications",
        "description": "Static typing, interfaces, generics, utility types, and TypeScript with React/Node",
        "modules": {
            "intro": {
                "title": "Module 1: TypeScript Fundamentals",
                "focus": "Basic types, type inference, and compiler",
                "subtopics": [
                    "Why TypeScript? Static Typing vs Dynamic",
                    "tsconfig.json & Compiler Options",
                    "Primitive Types, Arrays & Tuples",
                    "Type Annotations vs Type Inference"
                ]
            },
            "core": {
                "title": "Module 2: Interfaces & Type Aliases",
                "focus": "Modeling structured data and functions",
                "subtopics": [
                    "Interfaces vs Type Aliases",
                    "Optional, Readonly & Index Signatures",
                    "Union & Intersection Types",
                    "Type Narrowing & Type Guards"
                ]
            },
            "advanced": {
                "title": "Module 3: Generics & Advanced Types",
                "focus": "Reusable generic functions and utility types",
                "subtopics": [
                    "Generic Functions, Interfaces & Classes",
                    "Generic Constraints (extends keyof)",
                    "Built-in Utility Types (Partial, Pick, Omit, Record)",
                    "Conditional & Mapped Types"
                ]
            },
            "summary": {
                "title": "Module 4: TypeScript in Full-Stack Projects",
                "focus": "React with TypeScript, Node.js APIs, and strict mode",
                "subtopics": [
                    "Typing React Components, Props & Hooks",
                    "Typing Express & FastAPI Backend Payloads",
                    "Strict Null Checks & Eliminating 'any'",
                    "Production Compilation & Type Declarations (.d.ts)"
                ]
            }
        }
    },
    "Python": {
        "title": "Python Software Development",
        "description": "Python language, data structures, OOP, modules, exception handling, and virtual environments",
        "modules": {
            "intro": {
                "title": "Module 1: Python Basics & Data Structures",
                "focus": "Syntax, collections, and control flow",
                "subtopics": [
                    "Variables, Types & Formatting",
                    "Lists, Tuples, Dictionaries & Sets",
                    "Conditionals, Loops & List Comprehensions",
                    "Writing Modular Functions"
                ]
            },
            "core": {
                "title": "Module 2: Object-Oriented Python",
                "focus": "Classes, inheritance, and magic methods",
                "subtopics": [
                    "Classes, Instances & Attributes",
                    "Inheritance & Polymorphism",
                    "Dunder Methods (__str__, __repr__, __len__)",
                    "Properties & Encapsulation"
                ]
            },
            "advanced": {
                "title": "Module 3: Functional & Advanced Features",
                "focus": "Decorators, generators, and context managers",
                "subtopics": [
                    "Decorators & Higher-Order Functions",
                    "Generators & Iterators (yield)",
                    "Context Managers with 'with' Statements",
                    "Exception Handling & Custom Exceptions"
                ]
            },
            "summary": {
                "title": "Module 4: Virtual Envs, Testing & APIs",
                "focus": "Packaging, pytest, and FastAPI basics",
                "subtopics": [
                    "Virtual Environments (venv / poetry)",
                    "Unit Testing with pytest",
                    "Working with JSON, CSV & Files",
                    "Building REST Endpoints with FastAPI"
                ]
            }
        }
    },
    "SQL": {
        "title": "SQL & Relational Databases",
        "description": "Relational schema design, querying, complex joins, indexing, transactions, and PostgreSQL",
        "modules": {
            "intro": {
                "title": "Module 1: SQL Fundamentals & CRUD",
                "focus": "Table creation, basic queries, and filtering",
                "subtopics": [
                    "Relational Database Concepts (RDBMS)",
                    "CREATE, ALTER & DROP Tables",
                    "SELECT, WHERE, ORDER BY, LIMIT",
                    "INSERT, UPDATE & DELETE Operations"
                ]
            },
            "core": {
                "title": "Module 2: Joins, Aggregations & Grouping",
                "focus": "Multi-table queries and analytical aggregations",
                "subtopics": [
                    "INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL JOIN",
                    "Aggregations: COUNT, SUM, AVG, MIN, MAX",
                    "GROUP BY & HAVING Clauses",
                    "Subqueries & Common Table Expressions (WITH / CTE)"
                ]
            },
            "advanced": {
                "title": "Module 3: Indexing, Transactions & Constraints",
                "focus": "ACID compliance, foreign keys, and indexes",
                "subtopics": [
                    "Primary Keys, Foreign Keys & Unique Constraints",
                    "ACID Properties & Transaction Control (COMMIT, ROLLBACK)",
                    "Database Indexes (B-Tree, Hash) & Query Execution Plans",
                    "Window Functions (ROW_NUMBER, RANK, PARTITION BY)"
                ]
            },
            "summary": {
                "title": "Module 4: Normalization & PostgreSQL Administration",
                "focus": "Schema design, migrations, and performance",
                "subtopics": [
                    "Database Normalization (1NF, 2NF, 3NF)",
                    "PostgreSQL Data Types (JSONB, UUID, Arrays)",
                    "Database Migrations & Connection Pooling",
                    "Query Performance Tuning (EXPLAIN ANALYZE)"
                ]
            }
        }
    },
    "System Design": {
        "title": "System Design & Software Architecture",
        "description": "Scalability, microservices, distributed systems, caching, message queues, and load balancing",
        "modules": {
            "intro": {
                "title": "Module 1: System Design Fundamentals",
                "focus": "Scale, latency, throughput, and trade-offs",
                "subtopics": [
                    "Vertical vs Horizontal Scaling",
                    "Latency, Throughput & Bandwidth",
                    "CAP Theorem & PACELC Theorem",
                    "Monolith vs Microservices Architecture"
                ]
            },
            "core": {
                "title": "Module 2: Caching, CDNs & Load Balancing",
                "focus": "High performance and traffic distribution",
                "subtopics": [
                    "Caching Strategies (Write-Through, Cache-Aside, Write-Back)",
                    "Redis & Memcached Architecture",
                    "Content Delivery Networks (CDNs)",
                    "Load Balancing & Reverse Proxies"
                ]
            },
            "advanced": {
                "title": "Module 3: Distributed Data & Message Queues",
                "focus": "Data partitioning, replication, and async workflows",
                "subtopics": [
                    "Database Sharding & Partitioning",
                    "Master-Slave & Multi-Master Replication",
                    "Message Queues (Kafka, RabbitMQ, SQS)",
                    "Event-Driven Architecture & Pub/Sub"
                ]
            },
            "summary": {
                "title": "Module 4: Reliability & Enterprise Case Studies",
                "focus": "Fault tolerance, rate limiting, and real architectures",
                "subtopics": [
                    "Rate Limiting Algorithms (Token Bucket, Leaky Bucket)",
                    "Circuit Breaker Pattern & Fault Tolerance",
                    "Designing a URL Shortener (TinyURL)",
                    "Designing a Collaborative Real-Time Notification System"
                ]
            }
        }
    },
    "QA Testing": {
        "title": "Software Quality Assurance & Test Automation",
        "description": "Manual testing, test planning, automated UI testing with Selenium/Cypress, and API testing",
        "modules": {
            "intro": {
                "title": "Module 1: Testing Fundamentals & Test Design",
                "focus": "Testing levels, test case design, and defect management",
                "subtopics": [
                    "Software Testing Life Cycle (STLC)",
                    "Test Case Design Techniques (Boundary Value, Equivalence)",
                    "Defect Lifecycle & Bug Tracking in Jira",
                    "Manual vs Automated Testing Strategy"
                ]
            },
            "core": {
                "title": "Module 2: Unit & Integration Testing",
                "focus": "Automated testing with Pytest and Jest",
                "subtopics": [
                    "Writing Unit Tests with Pytest / Jest",
                    "Test Fixtures, Parameterization & Assertions",
                    "Mocking Dependencies & Stubs",
                    "Code Coverage Metrics & Reporting"
                ]
            },
            "advanced": {
                "title": "Module 3: API & Web Automation",
                "focus": "API testing with Postman and UI testing with Selenium/Cypress",
                "subtopics": [
                    "REST API Testing with Postman / Requests",
                    "Validating Status Codes, Headers & JSON Payloads",
                    "Selenium / Cypress Architecture & Locators",
                    "Page Object Model (POM) Design Pattern"
                ]
            },
            "summary": {
                "title": "Module 4: End-to-End & CI/CD Testing",
                "focus": "Regression suites, headless execution, and pipeline gates",
                "subtopics": [
                    "End-to-End (E2E) Test Automation Suites",
                    "Headless Browser Execution in Docker",
                    "Integrating Test Automation into GitHub Actions",
                    "Performance & Load Testing Fundamentals (k6 / JMeter)"
                ]
            }
        }
    },
    "Machine Learning": {
        "title": "Machine Learning Engineering",
        "description": "Supervised & unsupervised learning, model evaluation, feature engineering, and Scikit-learn",
        "modules": {
            "intro": {
                "title": "Module 1: ML Foundations & Data Prep",
                "focus": "Data preprocessing, train/test splits, and linear models",
                "subtopics": [
                    "Supervised vs Unsupervised Learning",
                    "Data Preprocessing & Feature Scaling",
                    "Train/Validation/Test Splits",
                    "Linear & Logistic Regression"
                ]
            },
            "core": {
                "title": "Module 2: Tree-Based Models & Ensembles",
                "focus": "Decision trees, Random Forests, and Gradient Boosting",
                "subtopics": [
                    "Decision Tree Classification & Regression",
                    "Random Forests & Bagging Principles",
                    "Gradient Boosting (XGBoost / LightGBM)",
                    "Hyperparameter Tuning with GridSearch & Optuna"
                ]
            },
            "advanced": {
                "title": "Module 3: Model Evaluation & Metrics",
                "focus": "Overfitting, cross-validation, and performance metrics",
                "subtopics": [
                    "Confusion Matrix, Precision, Recall & F1-Score",
                    "ROC-AUC Curves & Threshold Optimization",
                    "K-Fold Cross-Validation & Preventing Leakage",
                    "Bias-Variance Tradeoff Analysis"
                ]
            },
            "summary": {
                "title": "Module 4: Unsupervised Learning & Deployment",
                "focus": "Clustering, dimensionality reduction, and ML APIs",
                "subtopics": [
                    "K-Means Clustering & Hierarchical Clustering",
                    "PCA (Principal Component Analysis)",
                    "Model Serialization (joblib / ONNX)",
                    "Deploying ML Inference APIs with FastAPI"
                ]
            }
        }
    },
    "Deep Learning": {
        "title": "Deep Learning & Neural Networks",
        "description": "Perceptrons, backpropagation, CNNs, RNNs, PyTorch, and TensorFlow architectures",
        "modules": {
            "intro": {
                "title": "Module 1: Neural Network Foundations",
                "focus": "Neurons, activation functions, and gradient descent",
                "subtopics": [
                    "Artificial Neurons & Multi-Layer Perceptrons",
                    "Activation Functions (ReLU, Sigmoid, Softmax)",
                    "Forward Propagation & Loss Functions",
                    "Backpropagation & Stochastic Gradient Descent"
                ]
            },
            "core": {
                "title": "Module 2: Building Models with PyTorch",
                "focus": "PyTorch tensors, autograd, and training loops",
                "subtopics": [
                    "PyTorch Tensors, GPU Acceleration (CUDA)",
                    "torch.nn Modules & Custom Architectures",
                    "Writing a Standard Training & Evaluation Loop",
                    "Regularization (Dropout, Weight Decay, BatchNorm)"
                ]
            },
            "advanced": {
                "title": "Module 3: Convolutional Neural Networks (CNNs)",
                "focus": "Image processing, convolution, pooling, and transfer learning",
                "subtopics": [
                    "Convolutional Layers, Kernels & Stride",
                    "Max Pooling & Spatial Downsampling",
                    "Classic Architectures (ResNet, VGG)",
                    "Transfer Learning & Fine-Tuning"
                ]
            },
            "summary": {
                "title": "Module 4: Sequence Models & Transformers",
                "focus": "RNNs, Attention mechanism, and Transformer blocks",
                "subtopics": [
                    "Recurrent Neural Networks (RNNs) & LSTMs",
                    "The Self-Attention Mechanism",
                    "Transformer Encoder-Decoder Architecture",
                    "Model Optimization & Quantization"
                ]
            }
        }
    },
    "MLOps": {
        "title": "MLOps & ML Production Engineering",
        "description": "Model versioning, MLflow, pipeline orchestration, model monitoring, and automated retraining",
        "modules": {
            "intro": {
                "title": "Module 1: MLOps Principles & Tracking",
                "focus": "Reproducibility, experiment tracking, and MLflow",
                "subtopics": [
                    "What is MLOps? The ML Lifecycle",
                    "Experiment Tracking with MLflow / Weights & Biases",
                    "Logging Hyperparameters, Metrics & Artifacts",
                    "Model Registry & Model Staging"
                ]
            },
            "core": {
                "title": "Module 2: Data & Model Versioning",
                "focus": "DVC, data pipelines, and dataset versioning",
                "subtopics": [
                    "Data Version Control (DVC) Fundamentals",
                    "Connecting DVC to Cloud Storage (S3 / GCS)",
                    "Feature Stores (Feast Architecture)",
                    "Automated Data Validation with Great Expectations"
                ]
            },
            "advanced": {
                "title": "Module 3: Continuous Training Pipelines",
                "focus": "Kubeflow, Airflow, and automated model builds",
                "subtopics": [
                    "Building ML Pipelines with Kubeflow / Airflow",
                    "Automated Model Retraining Triggers",
                    "Containerizing Model Training & Inference",
                    "Canary & Shadow Deployments for ML Models"
                ]
            },
            "summary": {
                "title": "Module 4: Model Monitoring & Drift Detection",
                "focus": "Data drift, concept drift, and performance monitoring",
                "subtopics": [
                    "Data Drift vs Concept Drift",
                    "Monitoring Model Latency, Throughput & Quality",
                    "Evidently AI & Prometheus for Model Metrics",
                    "Feedback Loops & Incident Response for ML Systems"
                ]
            }
        }
    },
    "Data Engineering": {
        "title": "Data Engineering & Pipelines",
        "description": "ETL pipelines, Apache Spark, PySpark, data warehousing, Kafka streaming, and data quality",
        "modules": {
            "intro": {
                "title": "Module 1: Data Engineering Foundations",
                "focus": "Data architectures, OLTP vs OLAP, and Pandas ETL",
                "subtopics": [
                    "Data Engineering Roles & Responsibilities",
                    "OLTP (Transactional) vs OLAP (Analytical) Systems",
                    "Batch vs Stream Processing",
                    "Building Reliable Python ETL Scripts with Pandas"
                ]
            },
            "core": {
                "title": "Module 2: Data Warehousing & SQL Modeling",
                "focus": "Snowflake, BigQuery, and Star/Snowflake schemas",
                "subtopics": [
                    "Data Warehouse Architecture (Snowflake / BigQuery)",
                    "Dimensional Modeling (Facts, Dimensions, Star Schema)",
                    "Data Lakes vs Data Warehouses vs Lakehouses",
                    "dbt (data build tool) for SQL Transformations"
                ]
            },
            "advanced": {
                "title": "Module 3: Big Data with Apache Spark",
                "focus": "Distributed processing, DataFrames, and PySpark",
                "subtopics": [
                    "Apache Spark Architecture (Driver, Executors)",
                    "PySpark DataFrames & SQL Queries",
                    "Transformations vs Actions & Lazy Evaluation",
                    "Partitioning, Shuffling & Performance Tuning"
                ]
            },
            "summary": {
                "title": "Module 4: Orchestration & Real-Time Streaming",
                "focus": "Airflow DAGs, Apache Kafka, and data quality",
                "subtopics": [
                    "Workflow Orchestration with Apache Airflow DAGs",
                    "Apache Kafka Architecture (Topics, Producers, Consumers)",
                    "Streaming Data Ingestion & Processing",
                    "Data Quality, Lineage & Metadata Governance"
                ]
            }
        }
    }
}

# ══════════════════════════════════════════════════════════════════════════════
# ROLES REGISTRY: Structured definitions for all primary and extended roles
# ══════════════════════════════════════════════════════════════════════════════
ROLES_REGISTRY: Dict[str, Dict[str, Any]] = {
    # ── 1. DevOps Engineer / SRE (Primary focus) ──
    "DevOps Engineer": {
        "category": "DevOps & Cloud Infrastructure",
        "description": "Automating software delivery, infrastructure, deployment, monitoring, scalability, and reliability.",
        "skills": [
            "Git", "GitHub", "Linux", "Docker", "Kubernetes", "CI/CD",
            "AWS", "Terraform", "Ansible", "Prometheus", "Grafana",
            "Networking", "DevSecOps", "Bash", "Python"
        ],
        "roadmap": [
            {
                "topic": "Git",
                "title": "1. Git & GitHub Version Control",
                "prerequisites": [],
                "description": "Distributed version control, branching, pull requests, and conflict resolution."
            },
            {
                "topic": "Linux",
                "title": "2. Linux Systems & Administration",
                "prerequisites": [],
                "description": "Operating system fundamentals, bash scripting, file permissions, and services."
            },
            {
                "topic": "Networking",
                "title": "3. DevOps Networking & Protocols",
                "prerequisites": [],
                "description": "TCP/IP, DNS, HTTP/HTTPS, load balancers, reverse proxies, and firewalls."
            },
            {
                "topic": "Docker",
                "title": "4. Docker Containers & Virtualization",
                "prerequisites": ["Linux"],
                "description": "Container virtualization, images, Dockerfiles, and Docker Compose."
            },
            {
                "topic": "CI/CD",
                "title": "5. CI/CD Automated Pipelines",
                "prerequisites": ["Git", "Docker"],
                "description": "Continuous integration, automated testing, GitHub Actions, and Jenkins."
            },
            {
                "topic": "Kubernetes",
                "title": "6. Kubernetes Container Orchestration",
                "prerequisites": ["Docker", "Linux"],
                "description": "Cluster architecture, Pods, Deployments, Services, Helm, and troubleshooting."
            },
            {
                "topic": "AWS Cloud",
                "title": "7. Cloud Infrastructure (AWS)",
                "prerequisites": ["Networking"],
                "description": "Cloud compute, S3, IAM security, VPC networking, and cloud deployment."
            },
            {
                "topic": "Terraform",
                "title": "8. Infrastructure as Code (Terraform)",
                "prerequisites": ["AWS Cloud"],
                "description": "Declarative cloud provisioning, state management, and reusable modules."
            },
            {
                "topic": "Prometheus & Grafana",
                "title": "9. Monitoring & Observability",
                "prerequisites": ["Linux", "Kubernetes"],
                "description": "Metrics collection, PromQL, Grafana visualization, and Alertmanager."
            },
            {
                "topic": "DevSecOps",
                "title": "10. DevSecOps & Security Hardening",
                "prerequisites": ["CI/CD", "Docker"],
                "description": "Secrets management, container security, vulnerability scanning, and policies."
            }
        ]
    },

    "Cloud DevOps Engineer": {
        "category": "DevOps & Cloud Infrastructure",
        "description": "Specializing in multi-cloud DevOps, automated cloud infrastructure, and Kubernetes.",
        "skills": ["AWS", "Docker", "Kubernetes", "Git", "CI/CD", "Terraform", "Linux", "Python", "Prometheus"],
        "roadmap": [
            {"topic": "Git", "title": "1. Git Version Control", "prerequisites": [], "description": "Version control fundamentals."},
            {"topic": "Linux", "title": "2. Linux Administration", "prerequisites": [], "description": "Linux and bash automation."},
            {"topic": "Docker", "title": "3. Containerization", "prerequisites": ["Linux"], "description": "Docker images and containers."},
            {"topic": "AWS Cloud", "title": "4. AWS Cloud Infrastructure", "prerequisites": [], "description": "Cloud architecture and IAM."},
            {"topic": "CI/CD", "title": "5. Automated CI/CD", "prerequisites": ["Git", "Docker"], "description": "Continuous delivery pipelines."},
            {"topic": "Kubernetes", "title": "6. Kubernetes Orchestration", "prerequisites": ["Docker"], "description": "Cluster management and Helm."},
            {"topic": "Terraform", "title": "7. Terraform IaC", "prerequisites": ["AWS Cloud"], "description": "Automated infrastructure code."},
            {"topic": "Prometheus & Grafana", "title": "8. Cloud Monitoring", "prerequisites": ["Kubernetes"], "description": "Observability and alerting."}
        ]
    },

    "Cloud Engineer": {
        "category": "DevOps & Cloud Infrastructure",
        "description": "Designing, deploying, and maintaining enterprise cloud infrastructure and security.",
        "skills": ["AWS", "Docker", "Kubernetes", "Git", "Python", "Linux", "Terraform", "Networking"],
        "roadmap": [
            {"topic": "Networking", "title": "1. Cloud Networking", "prerequisites": [], "description": "VPC, DNS, and protocols."},
            {"topic": "Linux", "title": "2. Linux Systems", "prerequisites": [], "description": "Linux administration and shell."},
            {"topic": "AWS Cloud", "title": "3. AWS Core Services", "prerequisites": ["Networking"], "description": "Compute, storage, IAM, and databases."},
            {"topic": "Docker", "title": "4. Containers on Cloud", "prerequisites": ["Linux"], "description": "Docker containerization."},
            {"topic": "Terraform", "title": "5. Terraform Provisioning", "prerequisites": ["AWS Cloud"], "description": "Infrastructure as Code."},
            {"topic": "Kubernetes", "title": "6. Managed Kubernetes (EKS)", "prerequisites": ["Docker"], "description": "Cluster operations on cloud."}
        ]
    },

    # ── 2. Frontend Developer ──
    "Frontend Developer": {
        "category": "Web & Mobile Development",
        "description": "Building modern, responsive user interfaces and client-side web applications.",
        "skills": [
            "HTML", "CSS", "JavaScript", "TypeScript", "React", "Angular", "Vue",
            "Responsive Design", "Git", "REST API", "Testing"
        ],
        "roadmap": [
            {
                "topic": "JavaScript",
                "title": "1. Modern JavaScript (ES6+)",
                "prerequisites": [],
                "description": "Core mechanics, async/await, closures, and modern DOM methods."
            },
            {
                "topic": "TypeScript",
                "title": "2. TypeScript Typing & Generics",
                "prerequisites": ["JavaScript"],
                "description": "Static typing, interfaces, generics, and enterprise architecture."
            },
            {
                "topic": "Git",
                "title": "3. Git & GitHub for Developers",
                "prerequisites": [],
                "description": "Branching, pull requests, and collaborative code reviews."
            },
            {
                "topic": "React",
                "title": "4. React Component Engineering",
                "prerequisites": ["JavaScript", "TypeScript"],
                "description": "Virtual DOM, hooks, state management, and modern component design."
            },
            {
                "topic": "QA Testing",
                "title": "5. Frontend Testing & Automation",
                "prerequisites": ["React"],
                "description": "Unit testing with Jest, React Testing Library, and E2E with Cypress."
            },
            {
                "topic": "CI/CD",
                "title": "6. Frontend Build & Deployment",
                "prerequisites": ["Git"],
                "description": "Vite builds, GitHub Actions deployment, and CDN hosting."
            }
        ]
    },

    "React Developer": {
        "category": "Web & Mobile Development",
        "description": "Specialized in building high-performance React applications, Next.js, and state management.",
        "skills": ["React", "JavaScript", "TypeScript", "HTML", "CSS", "Git", "REST API", "Redux"],
        "roadmap": [
            {"topic": "JavaScript", "title": "1. Advanced JavaScript", "prerequisites": [], "description": "Modern JS patterns."},
            {"topic": "TypeScript", "title": "2. TypeScript Foundations", "prerequisites": ["JavaScript"], "description": "Type systems for React."},
            {"topic": "React", "title": "3. React Mastery", "prerequisites": ["JavaScript", "TypeScript"], "description": "Hooks, performance, and architecture."},
            {"topic": "Git", "title": "4. Git Collaboration", "prerequisites": [], "description": "Version control workflows."},
            {"topic": "QA Testing", "title": "5. React Testing", "prerequisites": ["React"], "description": "Jest & component testing."}
        ]
    },

    # ── 3. Backend Developer ──
    "Backend Developer": {
        "category": "Backend & Systems Engineering",
        "description": "Server-side development, APIs, databases, authentication, and backend architecture.",
        "skills": [
            "Python", "Node.js", "Java", "SQL", "PostgreSQL", "MongoDB",
            "REST API", "GraphQL", "Docker", "Git", "Security", "FastAPI"
        ],
        "roadmap": [
            {
                "topic": "Python",
                "title": "1. Python Backend Foundations",
                "prerequisites": [],
                "description": "Python language, OOP, exception handling, and FastAPI development."
            },
            {
                "topic": "SQL",
                "title": "2. Relational Databases & SQL",
                "prerequisites": [],
                "description": "Schema design, joins, indexing, transactions, and PostgreSQL."
            },
            {
                "topic": "Git",
                "title": "3. Version Control & Git",
                "prerequisites": [],
                "description": "Branching, collaborative workflows, and pull requests."
            },
            {
                "topic": "Docker",
                "title": "4. Docker for Backend Services",
                "prerequisites": [],
                "description": "Containerizing backend services, database containers, and compose."
            },
            {
                "topic": "System Design",
                "title": "5. System Design & Scalability",
                "prerequisites": ["Python", "SQL"],
                "description": "Microservices, caching with Redis, message queues, and API design."
            },
            {
                "topic": "QA Testing",
                "title": "6. Backend Testing & Automation",
                "prerequisites": ["Python"],
                "description": "Pytest unit tests, integration tests, and API contract testing."
            },
            {
                "topic": "CI/CD",
                "title": "7. Automated API Deployment",
                "prerequisites": ["Git", "Docker"],
                "description": "Automated pipelines, staging environments, and container release."
            }
        ]
    },

    "Python Developer": {
        "category": "Backend & Systems Engineering",
        "description": "Building robust Python applications, backend services, automation scripts, and APIs.",
        "skills": ["Python", "SQL", "FastAPI", "Git", "Docker", "Pandas", "Pytest"],
        "roadmap": [
            {"topic": "Python", "title": "1. Python Advanced Mastery", "prerequisites": [], "description": "OOP, decorators, and concurrency."},
            {"topic": "SQL", "title": "2. SQL & Database Modeling", "prerequisites": [], "description": "Relational databases and ORM."},
            {"topic": "Git", "title": "3. Git & GitHub", "prerequisites": [], "description": "Version control best practices."},
            {"topic": "Docker", "title": "4. Dockerizing Python Apps", "prerequisites": [], "description": "Containerizing FastAPI services."},
            {"topic": "QA Testing", "title": "5. Pytest & Testing", "prerequisites": ["Python"], "description": "Unit testing and test automation."}
        ]
    },

    "Java Developer": {
        "category": "Backend & Systems Engineering",
        "description": "Enterprise backend systems, Spring Boot, microservices, and distributed architecture.",
        "skills": ["Java", "SQL", "Spring Boot", "Docker", "Git", "Microservices", "REST API"],
        "roadmap": [
            {"topic": "Python", "title": "1. Backend Foundations", "prerequisites": [], "description": "Core backend concepts."},
            {"topic": "SQL", "title": "2. SQL & Relational DBs", "prerequisites": [], "description": "Database queries and transactions."},
            {"topic": "System Design", "title": "3. Microservices Architecture", "prerequisites": ["SQL"], "description": "System design and distributed systems."},
            {"topic": "Docker", "title": "4. Containerization", "prerequisites": [], "description": "Containers and Docker Compose."},
            {"topic": "CI/CD", "title": "5. Enterprise CI/CD", "prerequisites": ["Docker"], "description": "Automated build and test pipelines."}
        ]
    },

    # ── 4. Full-Stack Developer ──
    "Full Stack Developer": {
        "category": "Engineering & Architecture",
        "description": "Building complete applications across frontend, backend, database, and deployment.",
        "skills": [
            "HTML", "CSS", "JavaScript", "TypeScript", "React", "Node.js", "Python",
            "REST API", "SQL", "MongoDB", "Git", "Docker", "CI/CD"
        ],
        "roadmap": [
            {"topic": "JavaScript", "title": "1. Modern JavaScript (ES6+)", "prerequisites": [], "description": "Core client and server JavaScript."},
            {"topic": "TypeScript", "title": "2. TypeScript for Full Stack", "prerequisites": ["JavaScript"], "description": "Unified types across frontend and backend."},
            {"topic": "React", "title": "3. Frontend with React", "prerequisites": ["JavaScript"], "description": "Modern UI development and state management."},
            {"topic": "Python", "title": "4. Backend APIs & Services", "prerequisites": [], "description": "Server-side RESTful API development."},
            {"topic": "SQL", "title": "5. Relational Databases & SQL", "prerequisites": [], "description": "Database design, queries, and migrations."},
            {"topic": "Docker", "title": "6. Containerized Full Stack", "prerequisites": [], "description": "Running frontend, backend, and DB with Docker."},
            {"topic": "CI/CD", "title": "7. CI/CD & Deployment", "prerequisites": ["Docker"], "description": "Automated end-to-end deployment."}
        ]
    },

    # ── 5. Quality Assurance / Test Engineer ──
    "QA / Automation Engineer": {
        "category": "Engineering & Architecture",
        "description": "Software testing, test automation, quality assurance, and defect prevention.",
        "skills": [
            "Selenium", "Cypress", "Pytest", "Jest", "Postman", "API Testing",
            "Unit Testing", "Jira", "CI/CD", "Git", "Python"
        ],
        "roadmap": [
            {
                "topic": "QA Testing",
                "title": "1. Testing Fundamentals & Automation",
                "prerequisites": [],
                "description": "Test design, unit testing, Selenium, Cypress, and API testing."
            },
            {
                "topic": "Python",
                "title": "2. Python for Test Automation",
                "prerequisites": [],
                "description": "Scripting automation frameworks and data-driven tests."
            },
            {
                "topic": "Git",
                "title": "3. Git for QA Engineers",
                "prerequisites": [],
                "description": "Managing test repositories and branch workflows."
            },
            {
                "topic": "Docker",
                "title": "4. Containerized Test Environments",
                "prerequisites": [],
                "description": "Running headless browsers and test grids in Docker."
            },
            {
                "topic": "CI/CD",
                "title": "5. CI/CD Automated Test Gates",
                "prerequisites": ["QA Testing", "Git"],
                "description": "Integrating automated smoke and regression tests into pipelines."
            }
        ]
    },

    # ── 6. Software Architect ──
    "Software Architect": {
        "category": "Engineering & Architecture",
        "description": "Designing scalable, reliable, maintainable distributed software systems.",
        "skills": [
            "System Design", "Microservices", "Design Patterns", "SOLID",
            "Distributed Systems", "SQL", "Docker", "Kubernetes", "Cloud Architecture"
        ],
        "roadmap": [
            {
                "topic": "System Design",
                "title": "1. Scalable System Design",
                "prerequisites": [],
                "description": "Scalability, high availability, caching, and distributed architecture."
            },
            {
                "topic": "SQL",
                "title": "2. Advanced Data Architecture",
                "prerequisites": [],
                "description": "Database sharding, replication, normalization, and ACID guarantees."
            },
            {
                "topic": "Docker",
                "title": "3. Microservices Packaging",
                "prerequisites": [],
                "description": "Service decomposition and containerized architectures."
            },
            {
                "topic": "Kubernetes",
                "title": "4. Distributed Container Orchestration",
                "prerequisites": ["Docker"],
                "description": "Service discovery, ingress, and resilient cloud orchestration."
            },
            {
                "topic": "AWS Cloud",
                "title": "5. Enterprise Cloud Architecture",
                "prerequisites": [],
                "description": "Designing multi-region, disaster-recovery cloud infrastructures."
            }
        ]
    },

    # ── 7. Data Engineer ──
    "Data Engineer": {
        "category": "Data & AI Engineering",
        "description": "Building data pipelines, data platforms, ETL systems, and large-scale data infrastructure.",
        "skills": [
            "Python", "SQL", "Spark", "Kafka", "Airflow", "ETL",
            "Docker", "Kubernetes", "AWS", "Git", "Pandas"
        ],
        "roadmap": [
            {
                "topic": "Python",
                "title": "1. Python for Data Engineering",
                "prerequisites": [],
                "description": "Python scripting, data manipulation with Pandas, and data validation."
            },
            {
                "topic": "SQL",
                "title": "2. Advanced SQL & Data Warehousing",
                "prerequisites": [],
                "description": "Analytical queries, window functions, and dimensional modeling."
            },
            {
                "topic": "Data Engineering",
                "title": "3. Distributed Processing with Spark",
                "prerequisites": ["Python", "SQL"],
                "description": "Apache Spark, PySpark, Airflow workflow DAGs, and Kafka streaming."
            },
            {
                "topic": "Docker",
                "title": "4. Containerized Data Workflows",
                "prerequisites": [],
                "description": "Running Airflow, Spark, and databases in containers."
            },
            {
                "topic": "AWS Cloud",
                "title": "5. Cloud Data Lakes & Storage",
                "prerequisites": [],
                "description": "S3 Data Lakes, Redshift/Snowflake, and IAM data security."
            }
        ]
    },

    # ── 8. AI & Machine Learning Roles ──
    "Machine Learning Engineer": {
        "category": "Data & AI Engineering",
        "description": "Training, evaluating, and deploying machine learning models into production systems.",
        "skills": [
            "Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
            "NumPy", "Pandas", "Docker", "Git", "Statistics"
        ],
        "roadmap": [
            {"topic": "Python", "title": "1. Python for Data & ML", "prerequisites": [], "description": "NumPy, Pandas, and data processing."},
            {"topic": "Machine Learning", "title": "2. Supervised & Unsupervised ML", "prerequisites": ["Python"], "description": "Scikit-learn, trees, ensembles, and evaluation."},
            {"topic": "Deep Learning", "title": "3. Deep Neural Networks", "prerequisites": ["Machine Learning"], "description": "PyTorch, CNNs, and backpropagation."},
            {"topic": "MLOps", "title": "4. Model Deployment & MLOps", "prerequisites": ["Machine Learning"], "description": "MLflow tracking, model APIs, and monitoring."},
            {"topic": "Docker", "title": "5. Containerized ML Inference", "prerequisites": [], "description": "Packaging models into Docker containers."}
        ]
    },

    "AI/ML Engineer": {
        "category": "Data & AI Engineering",
        "description": "Developing and scaling AI/ML systems, deep learning models, and production APIs.",
        "skills": ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Docker", "Git", "MLOps"],
        "roadmap": [
            {"topic": "Python", "title": "1. Python Core", "prerequisites": [], "description": "Python programming and libraries."},
            {"topic": "Machine Learning", "title": "2. ML Algorithms", "prerequisites": ["Python"], "description": "Feature engineering and classification."},
            {"topic": "Deep Learning", "title": "3. Neural Networks", "prerequisites": ["Machine Learning"], "description": "PyTorch models and training loops."},
            {"topic": "MLOps", "title": "4. Production MLOps", "prerequisites": ["Machine Learning"], "description": "MLflow and model pipelines."}
        ]
    },

    "Generative AI Engineer": {
        "category": "Data & AI Engineering",
        "description": "Building LLM applications, retrieval-augmented generation (RAG), and fine-tuning models.",
        "skills": ["Python", "Deep Learning", "PyTorch", "NLP", "Git", "Docker", "FastAPI"],
        "roadmap": [
            {"topic": "Python", "title": "1. Python for AI", "prerequisites": [], "description": "Python async programming and APIs."},
            {"topic": "Deep Learning", "title": "2. Transformers & Attention", "prerequisites": ["Python"], "description": "Deep learning architectures and PyTorch."},
            {"topic": "Docker", "title": "3. Dockerizing AI Services", "prerequisites": [], "description": "Containerizing LLM inference servers."},
            {"topic": "System Design", "title": "4. Scalable RAG Systems", "prerequisites": ["Python"], "description": "Vector databases, caching, and rate limiting."}
        ]
    },

    "MLOps Engineer": {
        "category": "Data & AI Engineering",
        "description": "Automating machine learning lifecycles, model registries, CI/CD for ML, and monitoring.",
        "skills": ["Python", "Docker", "Kubernetes", "AWS", "Git", "Machine Learning", "FastAPI", "MLOps"],
        "roadmap": [
            {"topic": "Python", "title": "1. Python for ML", "prerequisites": [], "description": "Scripting and API development."},
            {"topic": "Docker", "title": "2. Containers for ML", "prerequisites": [], "description": "Docker images for training and inference."},
            {"topic": "MLOps", "title": "3. MLOps Pipelines & Tracking", "prerequisites": ["Python", "Docker"], "description": "MLflow, DVC, and model registry."},
            {"topic": "Kubernetes", "title": "4. Kubeflow & Cluster ML", "prerequisites": ["Docker"], "description": "Running distributed ML workloads."},
            {"topic": "CI/CD", "title": "5. Automated ML Pipelines", "prerequisites": ["Docker"], "description": "Continuous training and model release."}
        ]
    },

    "Data Scientist": {
        "category": "Data & AI Engineering",
        "description": "Analyzing complex datasets, statistical modeling, and actionable business intelligence.",
        "skills": ["Python", "SQL", "Pandas", "NumPy", "Statistics", "Machine Learning", "Git"],
        "roadmap": [
            {"topic": "Python", "title": "1. Python & Data Analysis", "prerequisites": [], "description": "Pandas, NumPy, and visualization."},
            {"topic": "SQL", "title": "2. SQL Analytics", "prerequisites": [], "description": "Advanced joins and aggregations."},
            {"topic": "Machine Learning", "title": "3. Predictive Modeling", "prerequisites": ["Python"], "description": "Classification, regression, and clustering."}
        ]
    },

    "Data Analyst": {
        "category": "Data & AI Engineering",
        "description": "Data exploration, SQL querying, dashboarding, statistical summaries, and metrics reporting.",
        "skills": ["Python", "SQL", "Pandas", "NumPy", "Statistics", "Git"],
        "roadmap": [
            {"topic": "SQL", "title": "1. SQL Querying & Joins", "prerequisites": [], "description": "Database queries and data extraction."},
            {"topic": "Python", "title": "2. Python for Data Exploration", "prerequisites": [], "description": "Pandas DataFrames and data cleaning."},
            {"topic": "Git", "title": "3. Git Collaboration", "prerequisites": [], "description": "Version control for analytics scripts."}
        ]
    },

    "Cybersecurity Engineer": {
        "category": "DevOps & Cloud Infrastructure",
        "description": "Securing systems, network defense, penetration testing, DevSecOps, and compliance.",
        "skills": ["Linux", "Networking", "DevSecOps", "Docker", "Python", "Git", "AWS"],
        "roadmap": [
            {"topic": "Linux", "title": "1. Linux Hardening", "prerequisites": [], "description": "Permissions, audit logs, and SSH security."},
            {"topic": "Networking", "title": "2. Network Defense & Protocols", "prerequisites": [], "description": "Firewalls, TLS/SSL, and intrusion detection."},
            {"topic": "DevSecOps", "title": "3. DevSecOps & Vulnerability Scanning", "prerequisites": ["Linux"], "description": "Shift-left security and secrets management."},
            {"topic": "Docker", "title": "4. Container Security", "prerequisites": ["Linux"], "description": "Securing container images and runtimes."}
        ]
    },

    "Mobile App Developer": {
        "category": "Web & Mobile Development",
        "description": "Building mobile applications with React Native, cross-platform frameworks, and mobile APIs.",
        "skills": ["React", "JavaScript", "TypeScript", "Git", "REST API"],
        "roadmap": [
            {"topic": "JavaScript", "title": "1. Modern JavaScript", "prerequisites": [], "description": "Core JS and async programming."},
            {"topic": "TypeScript", "title": "2. TypeScript Foundations", "prerequisites": ["JavaScript"], "description": "Type systems for mobile code."},
            {"topic": "React", "title": "3. React & Component Architecture", "prerequisites": ["JavaScript"], "description": "Component hierarchies, state, and hooks."},
            {"topic": "Git", "title": "4. Git Version Control", "prerequisites": [], "description": "Branching and app releases."}
        ]
    },

    "Software Engineer": {
        "category": "Engineering & Architecture",
        "description": "Generalist software engineering across data structures, backend APIs, testing, and deployment.",
        "skills": ["Python", "Git", "Docker", "SQL", "System Design", "QA Testing"],
        "roadmap": [
            {"topic": "Python", "title": "1. Python Programming", "prerequisites": [], "description": "Core language and data structures."},
            {"topic": "SQL", "title": "2. SQL & Relational DBs", "prerequisites": [], "description": "Database design and querying."},
            {"topic": "Git", "title": "3. Git & GitHub", "prerequisites": [], "description": "Version control best practices."},
            {"topic": "Docker", "title": "4. Docker Containers", "prerequisites": [], "description": "Containerizing applications."},
            {"topic": "System Design", "title": "5. System Architecture", "prerequisites": ["Python", "SQL"], "description": "Scalable design patterns."}
        ]
    },

    "Site Reliability Engineer (SRE)": {
        "category": "DevOps & Cloud Infrastructure",
        "description": "Applying software engineering principles to operations, reliability, uptime, SLOs, and incident response.",
        "skills": ["Linux", "Networking", "Docker", "Kubernetes", "CI/CD", "Prometheus", "Grafana", "AWS", "Python", "DevSecOps"],
        "roadmap": [
            {"topic": "Linux", "title": "1. Linux Internals & Systems", "prerequisites": [], "description": "Kernel parameters, systemd, and troubleshooting."},
            {"topic": "Networking", "title": "2. High Availability Networking", "prerequisites": [], "description": "DNS, TLS, load balancing, and failover."},
            {"topic": "Docker", "title": "3. Container Infrastructure", "prerequisites": ["Linux"], "description": "Container runtimes and resource limits."},
            {"topic": "Kubernetes", "title": "4. Cluster Reliability & Resiliency", "prerequisites": ["Docker"], "description": "Pod disruption budgets, auto-scaling, and probes."},
            {"topic": "Prometheus & Grafana", "title": "5. Observability, SLOs & Alerting", "prerequisites": ["Linux", "Kubernetes"], "description": "SLOs, error budgets, PromQL, and Grafana dashboards."},
            {"topic": "CI/CD", "title": "6. Safe Progressive Deployments", "prerequisites": ["Docker"], "description": "Canary rollouts, blue-green, and rollback automation."},
            {"topic": "System Design", "title": "7. Fault-Tolerant System Design", "prerequisites": ["Networking"], "description": "Circuit breakers, rate limiting, and chaos engineering."}
        ]
    },

    "Node.js Developer": {
        "category": "Backend & Systems Engineering",
        "description": "Building scalable event-driven backend services, REST APIs, and microservices with Node.js and Express.",
        "skills": ["JavaScript", "TypeScript", "SQL", "Git", "Docker", "REST API", "System Design", "QA Testing"],
        "roadmap": [
            {"topic": "JavaScript", "title": "1. Advanced JavaScript & Event Loop", "prerequisites": [], "description": "Asynchronous event-driven programming and streams."},
            {"topic": "TypeScript", "title": "2. TypeScript for Node.js", "prerequisites": ["JavaScript"], "description": "Type-safe backend architecture and decorators."},
            {"topic": "SQL", "title": "3. Relational Databases & ORMs", "prerequisites": [], "description": "PostgreSQL, connection pooling, and Prisma/TypeORM."},
            {"topic": "Git", "title": "4. Git Version Control", "prerequisites": [], "description": "Team workflows and branch management."},
            {"topic": "Docker", "title": "5. Containerizing Node.js Services", "prerequisites": [], "description": "Multi-stage Dockerfiles and Alpine images."},
            {"topic": "QA Testing", "title": "6. Node.js API Testing", "prerequisites": ["JavaScript"], "description": "Jest, Supertest, and integration test suites."},
            {"topic": "System Design", "title": "7. Scalable Backend Design", "prerequisites": ["SQL"], "description": "Caching with Redis, message queues, and clustering."}
        ]
    },

    "Android Developer": {
        "category": "Web & Mobile Development",
        "description": "Developing high-performance Android mobile applications with modern UI and API integration.",
        "skills": ["JavaScript", "TypeScript", "React", "Git", "REST API", "QA Testing"],
        "roadmap": [
            {"topic": "JavaScript", "title": "1. Mobile JavaScript Fundamentals", "prerequisites": [], "description": "Core JavaScript and mobile runtime concepts."},
            {"topic": "TypeScript", "title": "2. TypeScript for Mobile", "prerequisites": ["JavaScript"], "description": "Strong typing for mobile data models."},
            {"topic": "React", "title": "3. Mobile Component Architecture", "prerequisites": ["JavaScript"], "description": "Component layouts, navigation, and state management."},
            {"topic": "Git", "title": "4. Mobile Release Git Workflow", "prerequisites": [], "description": "Feature branches and app version tagging."},
            {"topic": "QA Testing", "title": "5. Mobile Testing & Automation", "prerequisites": ["React"], "description": "Unit testing and mobile UI automation."}
        ]
    },

    "iOS Developer": {
        "category": "Web & Mobile Development",
        "description": "Building responsive, modern iOS applications with fluid animations and secure networking.",
        "skills": ["JavaScript", "TypeScript", "React", "Git", "REST API", "QA Testing"],
        "roadmap": [
            {"topic": "JavaScript", "title": "1. Modern Scripting & Logic", "prerequisites": [], "description": "Async flows, reactive patterns, and JSON parsing."},
            {"topic": "TypeScript", "title": "2. TypeScript Architecture", "prerequisites": ["JavaScript"], "description": "Contract-first development and interfaces."},
            {"topic": "React", "title": "3. Cross-Platform Mobile UI", "prerequisites": ["JavaScript"], "description": "Declarative mobile UI and state containers."},
            {"topic": "Git", "title": "4. Version Control for Mobile", "prerequisites": [], "description": "Branching, PRs, and release workflows."},
            {"topic": "QA Testing", "title": "5. Automated UI & App Testing", "prerequisites": ["React"], "description": "Automated testing and continuous delivery."}
        ]
    },

    "Database Engineer": {
        "category": "Backend & Systems Engineering",
        "description": "Designing, tuning, indexing, and maintaining high-throughput relational and NoSQL databases.",
        "skills": ["SQL", "Python", "Linux", "Docker", "System Design", "AWS"],
        "roadmap": [
            {"topic": "SQL", "title": "1. Advanced SQL & Query Optimization", "prerequisites": [], "description": "Query execution plans, B-Tree indexes, and transactions."},
            {"topic": "Linux", "title": "2. Linux Performance & I/O Tuning", "prerequisites": [], "description": "Disk I/O, memory management, and system buffers."},
            {"topic": "Python", "title": "3. Database Automation Scripting", "prerequisites": [], "description": "Backup scripts, schema migrations, and benchmark harnesses."},
            {"topic": "Docker", "title": "4. Database Containerization", "prerequisites": ["Linux"], "description": "Running Postgres clusters and replicas in containers."},
            {"topic": "System Design", "title": "5. High-Scale Data Partitioning", "prerequisites": ["SQL"], "description": "Sharding, read replicas, replication lag, and CAP theorem."},
            {"topic": "AWS Cloud", "title": "6. Managed Cloud Databases (RDS / Aurora)", "prerequisites": ["SQL"], "description": "Automated failover, backups, and point-in-time recovery."}
        ]
    },

    "Data Architect": {
        "category": "Data & AI Engineering",
        "description": "Designing enterprise data pipelines, data lakehouses, governance, and analytical architectures.",
        "skills": ["SQL", "Data Engineering", "System Design", "AWS", "Python", "Docker"],
        "roadmap": [
            {"topic": "SQL", "title": "1. Enterprise Data Modeling", "prerequisites": [], "description": "Star schemas, snowflake schemas, and Data Vault 2.0."},
            {"topic": "Data Engineering", "title": "2. Lakehouse & Distributed Data Engines", "prerequisites": ["SQL"], "description": "Apache Spark, Delta Lake, and pipeline orchestration."},
            {"topic": "System Design", "title": "3. Distributed Systems & Streaming Architecture", "prerequisites": ["SQL"], "description": "Event sourcing, Kafka streaming, and lambda architectures."},
            {"topic": "AWS Cloud", "title": "4. Enterprise Cloud Data Platforms", "prerequisites": ["SQL"], "description": "S3 Data Lakes, Redshift, Snowflake, and governance."},
            {"topic": "DevSecOps", "title": "5. Data Security & Compliance", "prerequisites": [], "description": "Column-level encryption, role-based access, and GDPR/HIPAA."}
        ]
    },

    "Cloud Architect": {
        "category": "DevOps & Cloud Infrastructure",
        "description": "Architecting resilient, cost-effective, multi-region cloud infrastructures and enterprise governance.",
        "skills": ["AWS", "Networking", "Linux", "Terraform", "Docker", "Kubernetes", "System Design", "DevSecOps"],
        "roadmap": [
            {"topic": "Networking", "title": "1. Enterprise Cloud Networking & Transit", "prerequisites": [], "description": "VPC peering, Transit Gateway, Route 53, and Direct Connect."},
            {"topic": "AWS Cloud", "title": "2. Multi-Region AWS Architecture", "prerequisites": ["Networking"], "description": "Well-Architected Framework pillars and disaster recovery."},
            {"topic": "Terraform", "title": "3. Enterprise Infrastructure as Code", "prerequisites": ["AWS Cloud"], "description": "Terraform Cloud, modular landing zones, and state isolation."},
            {"topic": "Kubernetes", "title": "4. Managed Cloud Orchestration", "prerequisites": ["AWS Cloud"], "description": "Amazon EKS, multi-cluster federation, and GitOps."},
            {"topic": "System Design", "title": "5. Large-Scale Distributed Architecture", "prerequisites": ["Networking"], "description": "Zero-downtime migrations, caching, and edge acceleration."},
            {"topic": "DevSecOps", "title": "6. Cloud Governance & Security", "prerequisites": ["AWS Cloud"], "description": "IAM boundaries, SCPs, compliance auditing, and encryption."}
        ]
    },

    "Security Engineer": {
        "category": "DevOps & Cloud Infrastructure",
        "description": "Protecting systems, infrastructure, and networks from cyber threats and vulnerabilities.",
        "skills": ["Linux", "Networking", "DevSecOps", "Docker", "AWS", "Python", "Git"],
        "roadmap": [
            {"topic": "Linux", "title": "1. Linux Security Hardening", "prerequisites": [], "description": "SELinux/AppArmor, auditd, SSH hardening, and kernel tuning."},
            {"topic": "Networking", "title": "2. Network Security & Packet Analysis", "prerequisites": [], "description": "Wireshark, firewalls, IDS/IPS, TLS 1.3, and VPNs."},
            {"topic": "DevSecOps", "title": "3. Vulnerability Scanning & DevSecOps", "prerequisites": ["Linux"], "description": "Trivy, OWASP dependency check, SonarQube, and policy-as-code."},
            {"topic": "Docker", "title": "4. Container Security & Sandboxing", "prerequisites": ["Linux"], "description": "Rootless containers, distroless images, and runtime defense."},
            {"topic": "AWS Cloud", "title": "5. Cloud Identity & Access Security", "prerequisites": ["Networking"], "description": "AWS GuardDuty, Security Hub, KMS, and CloudTrail forensics."}
        ]
    },

    "Automation Engineer": {
        "category": "Engineering & Architecture",
        "description": "Building end-to-end automation frameworks across software testing, delivery pipelines, and environments.",
        "skills": ["Python", "QA Testing", "Git", "Linux", "Docker", "CI/CD", "Bash"],
        "roadmap": [
            {"topic": "Python", "title": "1. Python for Automation & Scripting", "prerequisites": [], "description": "Automation scripts, file handling, and CLI tools."},
            {"topic": "QA Testing", "title": "2. Automated Test Frameworks", "prerequisites": ["Python"], "description": "Pytest, Selenium, Cypress, and API automation."},
            {"topic": "Git", "title": "3. Git Automation & Hooks", "prerequisites": [], "description": "Pre-commit hooks, git automation, and release tags."},
            {"topic": "Docker", "title": "4. Containerized Test Runners", "prerequisites": [], "description": "Headless browser containers and parallel test execution."},
            {"topic": "CI/CD", "title": "5. Automated Deployment Pipelines", "prerequisites": ["Git", "Docker"], "description": "Automated regression gates and continuous delivery."}
        ]
    },

    "Embedded Systems Engineer": {
        "category": "Engineering & Architecture",
        "description": "Developing low-level software, real-time operating systems, firmware, and hardware-interfacing code.",
        "skills": ["Linux", "Git", "Python", "Networking", "QA Testing"],
        "roadmap": [
            {"topic": "Linux", "title": "1. Embedded Linux & Kernel Basics", "prerequisites": [], "description": "Kernel architecture, cross-compilation, and device trees."},
            {"topic": "Git", "title": "2. Version Control for Hardware/Firmware", "prerequisites": [], "description": "Tracking releases, submodules, and firmware revisions."},
            {"topic": "Python", "title": "3. Python for Hardware Prototyping", "prerequisites": [], "description": "Serial communication, hardware testing, and sensor polling."},
            {"topic": "Networking", "title": "4. Embedded IoT Protocols & Networking", "prerequisites": [], "description": "MQTT, CoAP, TCP/IP, and socket programming."},
            {"topic": "QA Testing", "title": "5. Firmware Testing & Verification", "prerequisites": ["Python"], "description": "Hardware-in-the-loop (HIL) testing and test harnesses."}
        ]
    },

    "AI Engineer": {
        "category": "Data & AI Engineering",
        "description": "Integrating foundational AI models, building intelligent agents, and deploying cognitive workflows.",
        "skills": ["Python", "Machine Learning", "Deep Learning", "MLOps", "Docker", "System Design"],
        "roadmap": [
            {"topic": "Python", "title": "1. Advanced Python for AI", "prerequisites": [], "description": "Asynchronous APIs, NumPy, and data manipulation."},
            {"topic": "Machine Learning", "title": "2. Machine Learning Foundations", "prerequisites": ["Python"], "description": "Supervised learning, feature engineering, and metrics."},
            {"topic": "Deep Learning", "title": "3. Deep Neural Networks & Transformers", "prerequisites": ["Machine Learning"], "description": "PyTorch, attention mechanisms, and fine-tuning."},
            {"topic": "Docker", "title": "4. Containerized AI Workloads", "prerequisites": [], "description": "GPU containerization with NVIDIA Docker runtime."},
            {"topic": "MLOps", "title": "5. Model Serving & Observability", "prerequisites": ["Machine Learning"], "description": "FastAPI inference, latency monitoring, and drift detection."},
            {"topic": "System Design", "title": "6. Scalable AI Systems Architecture", "prerequisites": ["Python"], "description": "Vector search, caching, embedding pipelines, and rate limiting."}
        ]
    },

    "Deep Learning Engineer": {
        "category": "Data & AI Engineering",
        "description": "Designing and training deep neural architectures, vision transformers, sequence models, and loss functions.",
        "skills": ["Python", "Machine Learning", "Deep Learning", "PyTorch", "Docker", "MLOps"],
        "roadmap": [
            {"topic": "Python", "title": "1. Scientific Python & Linear Algebra", "prerequisites": [], "description": "NumPy vectorization, tensor operations, and broadcasting."},
            {"topic": "Machine Learning", "title": "2. Statistical Foundations & Optimization", "prerequisites": ["Python"], "description": "Gradient descent, loss functions, and regularization."},
            {"topic": "Deep Learning", "title": "3. PyTorch Deep Neural Networks", "prerequisites": ["Machine Learning"], "description": "Custom PyTorch modules, autograd, CNNs, and transformers."},
            {"topic": "Docker", "title": "4. Distributed Training Containers", "prerequisites": [], "description": "Containerizing training jobs with CUDA support."},
            {"topic": "MLOps", "title": "5. Experiment Tracking & Model Registry", "prerequisites": ["Deep Learning"], "description": "Weights & Biases, MLflow, and model artifact checkpointing."}
        ]
    },

    "NLP Engineer": {
        "category": "Data & AI Engineering",
        "description": "Natural Language Processing, tokenization, transformer architectures, text generation, and semantic search.",
        "skills": ["Python", "Machine Learning", "Deep Learning", "Docker", "MLOps"],
        "roadmap": [
            {"topic": "Python", "title": "1. Python for Text Processing", "prerequisites": [], "description": "String parsing, regular expressions, and corpus preprocessing."},
            {"topic": "Machine Learning", "title": "2. Classical NLP & Classification", "prerequisites": ["Python"], "description": "TF-IDF, word embeddings, and text classification."},
            {"topic": "Deep Learning", "title": "3. Transformer Models & HuggingFace", "prerequisites": ["Machine Learning"], "description": "BERT, GPT, attention mechanics, and fine-tuning."},
            {"topic": "Docker", "title": "4. Deploying NLP Microservices", "prerequisites": [], "description": "Serving transformer models with FastAPI and Docker."},
            {"topic": "System Design", "title": "5. Semantic Search & Vector Databases", "prerequisites": ["Python"], "description": "Dense vector retrieval, cosine similarity, and RAG pipelines."}
        ]
    },

    "Computer Vision Engineer": {
        "category": "Data & AI Engineering",
        "description": "Computer vision algorithms, image classification, object detection (YOLO), segmentation, and OpenCV.",
        "skills": ["Python", "Machine Learning", "Deep Learning", "Docker", "MLOps"],
        "roadmap": [
            {"topic": "Python", "title": "1. Image Processing with Python & NumPy", "prerequisites": [], "description": "Pixel matrices, transformations, and color spaces."},
            {"topic": "Machine Learning", "title": "2. Feature Extraction & Traditional CV", "prerequisites": ["Python"], "description": "Edge detection, thresholding, and morphological operations."},
            {"topic": "Deep Learning", "title": "3. CNNs & Vision Transformers", "prerequisites": ["Machine Learning"], "description": "ResNet, YOLO object detection, segmentation, and PyTorch."},
            {"topic": "Docker", "title": "4. Real-Time Vision Inference Containers", "prerequisites": [], "description": "GPU-accelerated container inference pipelines."},
            {"topic": "MLOps", "title": "5. Edge Deployment & Optimization", "prerequisites": ["Deep Learning"], "description": "TensorRT, ONNX quantization, and latency optimization."}
        ]
    },

    "AI Research Engineer": {
        "category": "Data & AI Engineering",
        "description": "Novel architecture experimentation, theoretical deep learning, model benchmarking, and paper reproduction.",
        "skills": ["Python", "Machine Learning", "Deep Learning", "MLOps", "Data Engineering"],
        "roadmap": [
            {"topic": "Python", "title": "1. Python & Mathematical Computation", "prerequisites": [], "description": "Numerical computation, autograd internals, and vector calculus."},
            {"topic": "Machine Learning", "title": "2. Advanced Statistical Learning", "prerequisites": ["Python"], "description": "Probabilistic modeling, Bayesian methods, and empirical risk."},
            {"topic": "Deep Learning", "title": "3. Frontier Deep Learning Architectures", "prerequisites": ["Machine Learning"], "description": "Transformer variants, diffusion models, and self-supervised learning."},
            {"topic": "Data Engineering", "title": "4. Large-Scale Dataset Curation", "prerequisites": ["Python"], "description": "Distributed data preprocessing and tokenization pipelines."},
            {"topic": "MLOps", "title": "5. Distributed Experiment Reproducibility", "prerequisites": ["Deep Learning"], "description": "Multi-node training tracking, checkpointing, and evaluation suites."}
        ]
    },

    "Blockchain Developer": {
        "category": "Engineering & Architecture",
        "description": "Smart contract development, decentralized applications (dApps), cryptography, and blockchain protocols.",
        "skills": ["JavaScript", "TypeScript", "Python", "Git", "Docker", "Networking", "System Design"],
        "roadmap": [
            {"topic": "JavaScript", "title": "1. JavaScript & Async Mechanics", "prerequisites": [], "description": "Async programming, event handling, and JSON-RPC."},
            {"topic": "TypeScript", "title": "2. TypeScript for Smart Contracts", "prerequisites": ["JavaScript"], "description": "Type-safe blockchain interactions and Web3 contracts."},
            {"topic": "Networking", "title": "3. P2P Protocols & Cryptography", "prerequisites": [], "description": "Asymmetric encryption, digital signatures, hashing, and P2P networks."},
            {"topic": "Git", "title": "4. Git for Immutable Code Repositories", "prerequisites": [], "description": "Auditable commit histories, branch workflows, and releases."},
            {"topic": "Docker", "title": "5. Local Blockchain Node Containers", "prerequisites": [], "description": "Spinning up local testnet nodes and dev environments with Docker."},
            {"topic": "System Design", "title": "6. Decentralized System Architecture", "prerequisites": ["Networking"], "description": "Consensus mechanisms, state machines, and off-chain indexing."}
        ]
    }
}

# ══════════════════════════════════════════════════════════════════════════════
# Helper Functions
# ══════════════════════════════════════════════════════════════════════════════

def get_role_config(role_name: str) -> Dict[str, Any]:
    """Returns the full configuration for a target role, with safe fallback."""
    if role_name in ROLES_REGISTRY:
        return ROLES_REGISTRY[role_name]
    # Fuzzy / default fallback
    for k in ROLES_REGISTRY:
        if k.lower() in (role_name or "").lower():
            return ROLES_REGISTRY[k]
    return ROLES_REGISTRY["DevOps Engineer"]

def get_all_roles() -> List[str]:
    """Returns sorted list of all available role names."""
    return list(ROLES_REGISTRY.keys())

def get_role_roadmap(role_name: str) -> List[Dict[str, Any]]:
    """Returns the ordered topic roadmap for a specific role."""
    conf = get_role_config(role_name)
    return conf.get("roadmap", [])

def get_topic_syllabus(topic_name: str) -> Optional[Dict[str, Any]]:
    """Returns the 4-module syllabus for a given topic."""
    return TOPIC_SYLLABUS.get(topic_name)

def filter_gaps_with_prerequisites(
    role_name: str,
    existing_skills: List[str],
    completed_topics: List[str]
) -> List[Dict[str, Any]]:
    """
    Evaluates the role's sequential roadmap against existing resume skills and completed topics.
    Identifies what the user already knows, what they should learn first based on prerequisites,
    and returns an actionable, prioritized roadmap list.
    """
    conf = get_role_config(role_name)
    roadmap = conf.get("roadmap", [])
    
    existing_set = {s.lower().strip() for s in (existing_skills or [])}
    completed_set = {t.lower().strip() for t in (completed_topics or [])}

    prioritized_roadmap = []

    for item in roadmap:
        t = item["topic"]
        t_lower = t.lower().strip()
        
        # Check if already mastered via resume or completion
        is_in_resume = any(s in existing_set for s in [t_lower, f"{t_lower} basics", f"{t_lower} fundamentals"])
        is_completed = t_lower in completed_set
        
        # Check prerequisites
        prereqs = item.get("prerequisites", [])
        unmet_prereqs = []
        for p in prereqs:
            p_lower = p.lower().strip()
            p_satisfied = (p_lower in existing_set) or (p_lower in completed_set)
            if not p_satisfied:
                unmet_prereqs.append(p)

        if is_completed:
            status = "completed"
            action = "Review Content"
        elif is_in_resume:
            status = "mastered_via_resume"
            action = "Review Advanced"
        elif len(unmet_prereqs) > 0:
            status = "locked"
            action = f"Requires {', '.join(unmet_prereqs)}"
        else:
            status = "ready_to_learn"
            action = "Start Learning"

        prioritized_roadmap.append({
            "topic": t,
            "title": item.get("title", t),
            "description": item.get("description", ""),
            "prerequisites": prereqs,
            "unmet_prerequisites": unmet_prereqs,
            "status": status,
            "action_label": action,
            "syllabus": TOPIC_SYLLABUS.get(t)
        })

    return prioritized_roadmap
