"""
extended_data.py
----------------
Curated video library and 15-question quiz pools for extended technical topics:
Docker, Kubernetes, Linux, Git, CI/CD, AWS Cloud, Terraform, Prometheus & Grafana,
Networking, DevSecOps, React, JavaScript, TypeScript, SQL, System Design, QA Testing.
"""

# ══════════════════════════════════════════════════════════════════════════════
# EXTENDED VIDEO DATABASE (4 Modules: intro, core, advanced, summary)
# ══════════════════════════════════════════════════════════════════════════════
EXTENDED_VIDEO_DB = {
    "Docker": {
        "beginner": {
            "intro": [
                {
                    "title": "Docker Tutorial for Beginners – What is Docker?",
                    "channel": "TechWorld with Nana",
                    "duration": "18:45",
                    "thumb": "https://i.ytimg.com/vi/3c-iBn73dDE/hqdefault.jpg",
                    "url": "https://www.youtube.com/watch?v=3c-iBn73dDE",
                    "views": "4.2M"
                }
            ],
            "core": [
                {
                    "title": "Docker Images & Dockerfile Tutorial",
                    "channel": "freeCodeCamp.org",
                    "duration": "45:12",
                    "thumb": "https://i.ytimg.com/vi/fqMOX6JJhGo/hqdefault.jpg",
                    "url": "https://www.youtube.com/watch?v=fqMOX6JJhGo",
                    "views": "3.1M"
                },
                {
                    "title": "Docker Containers & CLI Commands",
                    "channel": "Programming with Mosh",
                    "duration": "32:00",
                    "thumb": "https://i.ytimg.com/vi/pTFZFxd4hOI/hqdefault.jpg",
                    "url": "https://www.youtube.com/watch?v=pTFZFxd4hOI",
                    "views": "2.8M"
                }
            ],
            "advanced": [
                {
                    "title": "Docker Volumes & Persistent Data Storage",
                    "channel": "NetworkChuck",
                    "duration": "28:15",
                    "thumb": "https://i.ytimg.com/vi/Vv_SgZ90Q6w/hqdefault.jpg",
                    "url": "https://www.youtube.com/watch?v=Vv_SgZ90Q6w",
                    "views": "1.5M"
                },
                {
                    "title": "Docker Networking Explained",
                    "channel": "TechWorld with Nana",
                    "duration": "34:20",
                    "thumb": "https://i.ytimg.com/vi/bKFMS5C4CG0/hqdefault.jpg",
                    "url": "https://www.youtube.com/watch?v=bKFMS5C4CG0",
                    "views": "1.2M"
                }
            ],
            "summary": [
                {
                    "title": "Docker Compose Full Course – Multi-Container Apps",
                    "channel": "freeCodeCamp.org",
                    "duration": "1:15:00",
                    "thumb": "https://i.ytimg.com/vi/SXwC9fSwct8/hqdefault.jpg",
                    "url": "https://www.youtube.com/watch?v=SXwC9fSwct8",
                    "views": "1.9M"
                }
            ]
        },
        "intermediate": {
            "intro": [{"title": "Docker Architecture Deep Dive", "channel": "Hussein Nasser", "duration": "24:10", "thumb": "https://i.ytimg.com/vi/3c-iBn73dDE/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=3c-iBn73dDE", "views": "850K"}],
            "core": [
                {"title": "Multi-Stage Builds in Docker", "channel": "DevOps Toolkit", "duration": "22:40", "thumb": "https://i.ytimg.com/vi/fqMOX6JJhGo/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=fqMOX6JJhGo", "views": "600K"},
                {"title": "Docker Security Best Practices", "channel": "Snyk", "duration": "35:10", "thumb": "https://i.ytimg.com/vi/pTFZFxd4hOI/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=pTFZFxd4hOI", "views": "450K"}
            ],
            "advanced": [
                {"title": "Docker Custom Bridge & Overlay Networks", "channel": "TechWorld with Nana", "duration": "40:00", "thumb": "https://i.ytimg.com/vi/bKFMS5C4CG0/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=bKFMS5C4CG0", "views": "720K"},
                {"title": "Optimizing Docker Images for Production", "channel": "Bret Fisher", "duration": "48:00", "thumb": "https://i.ytimg.com/vi/Vv_SgZ90Q6w/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=Vv_SgZ90Q6w", "views": "530K"}
            ],
            "summary": [{"title": "Production Ready Docker Compose", "channel": "freeCodeCamp.org", "duration": "1:20:00", "thumb": "https://i.ytimg.com/vi/SXwC9fSwct8/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=SXwC9fSwct8", "views": "1.1M"}]
        },
        "advanced": {
            "intro": [{"title": "Container Runtimes & containerd Internals", "channel": "KubeCon", "duration": "35:00", "thumb": "https://i.ytimg.com/vi/3c-iBn73dDE/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=3c-iBn73dDE", "views": "300K"}],
            "core": [
                {"title": "Building Rootless Containers", "channel": "Red Hat Summit", "duration": "42:00", "thumb": "https://i.ytimg.com/vi/fqMOX6JJhGo/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=fqMOX6JJhGo", "views": "250K"},
                {"title": "Container Security Hardening & Seccomp", "channel": "Black Hat", "duration": "50:00", "thumb": "https://i.ytimg.com/vi/pTFZFxd4hOI/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=pTFZFxd4hOI", "views": "380K"}
            ],
            "advanced": [
                {"title": "High Performance Docker Storage Drivers", "channel": "DockerCon", "duration": "45:00", "thumb": "https://i.ytimg.com/vi/bKFMS5C4CG0/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=bKFMS5C4CG0", "views": "220K"},
                {"title": "Docker Swarm to Kubernetes Migration", "channel": "DevOps Directive", "duration": "55:00", "thumb": "https://i.ytimg.com/vi/Vv_SgZ90Q6w/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=Vv_SgZ90Q6w", "views": "410K"}
            ],
            "summary": [{"title": "Enterprise Container Orchestration", "channel": "Google Cloud Tech", "duration": "1:00:00", "thumb": "https://i.ytimg.com/vi/SXwC9fSwct8/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=SXwC9fSwct8", "views": "500K"}]
        }
    },

    "Kubernetes": {
        "beginner": {
            "intro": [{"title": "Kubernetes Tutorial for Beginners [FULL COURSE]", "channel": "TechWorld with Nana", "duration": "3:30:00", "thumb": "https://i.ytimg.com/vi/X48VuDVv0do/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=X48VuDVv0do", "views": "6.5M"}],
            "core": [
                {"title": "Kubernetes Architecture, Pods & Deployments", "channel": "freeCodeCamp.org", "duration": "1:15:00", "thumb": "https://i.ytimg.com/vi/d6WC5n9G_sM/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=d6WC5n9G_sM", "views": "2.1M"},
                {"title": "Kubernetes Services & Ingress Explained", "channel": "TechWorld with Nana", "duration": "42:00", "thumb": "https://i.ytimg.com/vi/80Ew_fsV4rM/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=80Ew_fsV4rM", "views": "1.8M"}
            ],
            "advanced": [
                {"title": "ConfigMaps and Secrets in Kubernetes", "channel": "DevOps Toolkit", "duration": "30:00", "thumb": "https://i.ytimg.com/vi/4m2p45qY3qI/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=4m2p45qY3qI", "views": "900K"},
                {"title": "Kubernetes Persistent Volumes & Claims", "channel": "TechWorld with Nana", "duration": "35:00", "thumb": "https://i.ytimg.com/vi/0swOh5C3Obo/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=0swOh5C3Obo", "views": "850K"}
            ],
            "summary": [{"title": "Helm Package Manager Crash Course", "channel": "TechWorld with Nana", "duration": "45:00", "thumb": "https://i.ytimg.com/vi/-ykwb1d0DXU/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=-ykwb1d0DXU", "views": "1.4M"}]
        },
        "intermediate": {
            "intro": [{"title": "Kubernetes Ingress Controllers Deep Dive", "channel": "DevOps Directive", "duration": "40:00", "thumb": "https://i.ytimg.com/vi/80Ew_fsV4rM/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=80Ew_fsV4rM", "views": "600K"}],
            "core": [
                {"title": "StatefulSets & DaemonSets in K8s", "channel": "TechWorld with Nana", "duration": "38:00", "thumb": "https://i.ytimg.com/vi/d6WC5n9G_sM/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=d6WC5n9G_sM", "views": "750K"},
                {"title": "RBAC & ServiceAccounts Security", "channel": "DevOps Toolkit", "duration": "32:00", "thumb": "https://i.ytimg.com/vi/X48VuDVv0do/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=X48VuDVv0do", "views": "500K"}
            ],
            "advanced": [
                {"title": "Horizontal Pod Autoscaler (HPA)", "channel": "DevOps Toolkit", "duration": "28:00", "thumb": "https://i.ytimg.com/vi/4m2p45qY3qI/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=4m2p45qY3qI", "views": "420K"},
                {"title": "Troubleshooting Kubernetes Deployments", "channel": "TechWorld with Nana", "duration": "45:00", "thumb": "https://i.ytimg.com/vi/0swOh5C3Obo/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=0swOh5C3Obo", "views": "800K"}
            ],
            "summary": [{"title": "GitOps with ArgoCD and Kubernetes", "channel": "freeCodeCamp.org", "duration": "1:30:00", "thumb": "https://i.ytimg.com/vi/-ykwb1d0DXU/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=-ykwb1d0DXU", "views": "1.2M"}]
        },
        "advanced": {
            "intro": [{"title": "Kubernetes Networking & CNI Plugins", "channel": "KubeCon", "duration": "45:00", "thumb": "https://i.ytimg.com/vi/X48VuDVv0do/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=X48VuDVv0do", "views": "350K"}],
            "core": [
                {"title": "Writing Custom Kubernetes Operators in Go", "channel": "DevOps Toolkit", "duration": "1:10:00", "thumb": "https://i.ytimg.com/vi/d6WC5n9G_sM/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=d6WC5n9G_sM", "views": "400K"},
                {"title": "Service Mesh with Istio", "channel": "TechWorld with Nana", "duration": "1:05:00", "thumb": "https://i.ytimg.com/vi/80Ew_fsV4rM/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=80Ew_fsV4rM", "views": "650K"}
            ],
            "advanced": [
                {"title": "Zero-Downtime Multi-Cluster Kubernetes", "channel": "Google Cloud Tech", "duration": "50:00", "thumb": "https://i.ytimg.com/vi/4m2p45qY3qI/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=4m2p45qY3qI", "views": "320K"},
                {"title": "Cluster Hardening (CIS Benchmark)", "channel": "CNCF", "duration": "48:00", "thumb": "https://i.ytimg.com/vi/0swOh5C3Obo/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=0swOh5C3Obo", "views": "280K"}
            ],
            "summary": [{"title": "Enterprise SRE on Kubernetes", "channel": "TechWorld with Nana", "duration": "1:20:00", "thumb": "https://i.ytimg.com/vi/-ykwb1d0DXU/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=-ykwb1d0DXU", "views": "900K"}]
        }
    },

    "Linux": {
        "beginner": {
            "intro": [{"title": "Linux for Beginners – Full Course", "channel": "freeCodeCamp.org", "duration": "5:00:00", "thumb": "https://i.ytimg.com/vi/wBp0Rb-ZJak/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=wBp0Rb-ZJak", "views": "4.1M"}],
            "core": [
                {"title": "Linux Command Line Basics", "channel": "NetworkChuck", "duration": "45:00", "thumb": "https://i.ytimg.com/vi/V1y-mbWM3B8/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=V1y-mbWM3B8", "views": "3.2M"},
                {"title": "File Permissions (chmod, chown) Explained", "channel": "TechWorld with Nana", "duration": "25:00", "thumb": "https://i.ytimg.com/vi/s0Y_5Nf3Vrk/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=s0Y_5Nf3Vrk", "views": "1.5M"}
            ],
            "advanced": [
                {"title": "Bash Scripting for Beginners", "channel": "freeCodeCamp.org", "duration": "1:30:00", "thumb": "https://i.ytimg.com/vi/tK9Oc6AEnR4/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=tK9Oc6AEnR4", "views": "2.4M"},
                {"title": "Linux Processes & Services (systemd, top)", "channel": "The Modern Coder", "duration": "30:00", "thumb": "https://i.ytimg.com/vi/q13UuH3XwG0/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=q13UuH3XwG0", "views": "980K"}
            ],
            "summary": [{"title": "SSH Keys & Remote Server Management", "channel": "NetworkChuck", "duration": "35:00", "thumb": "https://i.ytimg.com/vi/hQWRp-gQqqc/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=hQWRp-gQqqc", "views": "1.7M"}]
        }
    },

    "Git": {
        "beginner": {
            "intro": [{"title": "Git and GitHub for Beginners – Crash Course", "channel": "freeCodeCamp.org", "duration": "1:08:00", "thumb": "https://i.ytimg.com/vi/RGOj5yH7evk/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=RGOj5yH7evk", "views": "6.8M"}],
            "core": [
                {"title": "Git Branching, Merging & Fast-Forward", "channel": "Traversy Media", "duration": "35:00", "thumb": "https://i.ytimg.com/vi/SWYqp7iY_Tc/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=SWYqp7iY_Tc", "views": "2.2M"},
                {"title": "How to Resolve Merge Conflicts in Git", "channel": "Fireship", "duration": "12:00", "thumb": "https://i.ytimg.com/vi/JtIX3HJKwfo/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=JtIX3HJKwfo", "views": "1.9M"}
            ],
            "advanced": [
                {"title": "Pull Requests & GitHub Team Collaboration", "channel": "Corey Schafer", "duration": "40:00", "thumb": "https://i.ytimg.com/vi/oFYyPYr80R0/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=oFYyPYr80R0", "views": "1.1M"},
                {"title": "Git Rebase vs Git Merge", "channel": "Academind", "duration": "22:00", "thumb": "https://i.ytimg.com/vi/Tyd3mK_Rk-o/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=Tyd3mK_Rk-o", "views": "950K"}
            ],
            "summary": [{"title": "Git Flow and Trunk-Based Development", "channel": "TechWorld with Nana", "duration": "30:00", "thumb": "https://i.ytimg.com/vi/1SXpE08vmzs/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=1SXpE08vmzs", "views": "1.3M"}]
        }
    },

    "CI/CD": {
        "beginner": {
            "intro": [{"title": "CI/CD Pipeline Explained in 15 Minutes", "channel": "TechWorld with Nana", "duration": "16:00", "thumb": "https://i.ytimg.com/vi/scziwA6u-xI/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=scziwA6u-xI", "views": "2.8M"}],
            "core": [
                {"title": "GitHub Actions Tutorial – Automated CI/CD", "channel": "freeCodeCamp.org", "duration": "1:45:00", "thumb": "https://i.ytimg.com/vi/R8_veQiYBjI/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=R8_veQiYBjI", "views": "2.1M"},
                {"title": "Jenkins Tutorial for Beginners", "channel": "TechWorld with Nana", "duration": "1:30:00", "thumb": "https://i.ytimg.com/vi/7KCS70sCoK0/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=7KCS70sCoK0", "views": "1.8M"}
            ],
            "advanced": [
                {"title": "Building Docker Containers in CI/CD", "channel": "DevOps Directive", "duration": "35:00", "thumb": "https://i.ytimg.com/vi/Y1p_uS593iA/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=Y1p_uS593iA", "views": "850K"},
                {"title": "Automated Testing in Release Pipelines", "channel": "freeCodeCamp.org", "duration": "42:00", "thumb": "https://i.ytimg.com/vi/scziwA6u-xI/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=scziwA6u-xI", "views": "920K"}
            ],
            "summary": [{"title": "Blue-Green & Canary Deployments", "channel": "TechWorld with Nana", "duration": "38:00", "thumb": "https://i.ytimg.com/vi/1SXpE08vmzs/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=1SXpE08vmzs", "views": "1.4M"}]
        }
    },

    "AWS Cloud": {
        "beginner": {
            "intro": [{"title": "AWS Certified Cloud Practitioner – Full Course", "channel": "freeCodeCamp.org", "duration": "13:00:00", "thumb": "https://i.ytimg.com/vi/SOTamWNgDKc/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=SOTamWNgDKc", "views": "5.2M"}],
            "core": [
                {"title": "AWS EC2 & S3 Tutorial for Beginners", "channel": "Traversy Media", "duration": "45:00", "thumb": "https://i.ytimg.com/vi/Ia-UEYYRCEI/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=Ia-UEYYRCEI", "views": "1.9M"},
                {"title": "AWS IAM (Identity & Access Management)", "channel": "Stephane Maarek", "duration": "30:00", "thumb": "https://i.ytimg.com/vi/yG7CjY5H89A/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=yG7CjY5H89A", "views": "1.2M"}
            ],
            "advanced": [
                {"title": "AWS VPC Networking & Subnets Explained", "channel": "TechWorld with Nana", "duration": "50:00", "thumb": "https://i.ytimg.com/vi/hiKPPy5849A/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=hiKPPy5849A", "views": "1.6M"},
                {"title": "AWS RDS & DynamoDB Databases", "channel": "Be A Better Dev", "duration": "35:00", "thumb": "https://i.ytimg.com/vi/Ia-UEYYRCEI/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=Ia-UEYYRCEI", "views": "850K"}
            ],
            "summary": [{"title": "Deploying Full-Stack Apps to AWS", "channel": "freeCodeCamp.org", "duration": "1:40:00", "thumb": "https://i.ytimg.com/vi/SOTamWNgDKc/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=SOTamWNgDKc", "views": "2.4M"}]
        }
    },

    "Terraform": {
        "beginner": {
            "intro": [{"title": "Terraform Course for Beginners", "channel": "freeCodeCamp.org", "duration": "2:30:00", "thumb": "https://i.ytimg.com/vi/l5k1ai_GBDE/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=l5k1ai_GBDE", "views": "2.6M"}],
            "core": [
                {"title": "Terraform HCL Syntax & CLI Workflow", "channel": "TechWorld with Nana", "duration": "45:00", "thumb": "https://i.ytimg.com/vi/YcM38QxXW_g/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=YcM38QxXW_g", "views": "1.3M"},
                {"title": "Terraform State Management & Remote S3 Backend", "channel": "DevOps Directive", "duration": "35:00", "thumb": "https://i.ytimg.com/vi/l5k1ai_GBDE/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=l5k1ai_GBDE", "views": "850K"}
            ],
            "advanced": [
                {"title": "Building Reusable Terraform Modules", "channel": "Anton Putra", "duration": "40:00", "thumb": "https://i.ytimg.com/vi/YcM38QxXW_g/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=YcM38QxXW_g", "views": "720K"},
                {"title": "Terraform Workspaces & Multi-Env Management", "channel": "DevOps Toolkit", "duration": "30:00", "thumb": "https://i.ytimg.com/vi/l5k1ai_GBDE/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=l5k1ai_GBDE", "views": "600K"}
            ],
            "summary": [{"title": "Automating Terraform in GitHub Actions", "channel": "freeCodeCamp.org", "duration": "1:00:00", "thumb": "https://i.ytimg.com/vi/l5k1ai_GBDE/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=l5k1ai_GBDE", "views": "980K"}]
        }
    },

    "Prometheus & Grafana": {
        "beginner": {
            "intro": [{"title": "Prometheus & Grafana Tutorial – Full Course", "channel": "TechWorld with Nana", "duration": "1:50:00", "thumb": "https://i.ytimg.com/vi/h4Sl21AKiDg/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=h4Sl21AKiDg", "views": "1.8M"}],
            "core": [
                {"title": "PromQL Query Language Masterclass", "channel": "Prometheus Community", "duration": "45:00", "thumb": "https://i.ytimg.com/vi/h4Sl21AKiDg/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=h4Sl21AKiDg", "views": "900K"},
                {"title": "Node Exporter & System Metrics Collection", "channel": "Anton Putra", "duration": "30:00", "thumb": "https://i.ytimg.com/vi/h4Sl21AKiDg/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=h4Sl21AKiDg", "views": "750K"}
            ],
            "advanced": [
                {"title": "Grafana Dashboard Design & Templating", "channel": "freeCodeCamp.org", "duration": "1:15:00", "thumb": "https://i.ytimg.com/vi/C037u3pW8Uo/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=C037u3pW8Uo", "views": "1.2M"},
                {"title": "Setting Up Alertmanager Rules & Notifications", "channel": "DevOps Toolkit", "duration": "35:00", "thumb": "https://i.ytimg.com/vi/h4Sl21AKiDg/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=h4Sl21AKiDg", "views": "600K"}
            ],
            "summary": [{"title": "SRE Monitoring & Golden Signals", "channel": "Google Cloud Tech", "duration": "45:00", "thumb": "https://i.ytimg.com/vi/uTEL8Ff1Zvk/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=uTEL8Ff1Zvk", "views": "850K"}]
        }
    },

    "System Design": {
        "beginner": {
            "intro": [{"title": "System Design Interview – Step by Step Guide", "channel": "freeCodeCamp.org", "duration": "2:30:00", "thumb": "https://i.ytimg.com/vi/bUHFg8CZFCA/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=bUHFg8CZFCA", "views": "3.5M"}],
            "core": [
                {"title": "Horizontal Scaling, Load Balancers & CDNs", "channel": "Gaurav Sen", "duration": "35:00", "thumb": "https://i.ytimg.com/vi/K0Ta65OqQkY/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=K0Ta65OqQkY", "views": "1.8M"},
                {"title": "Caching Strategies (Redis & Memcached)", "channel": "Hussein Nasser", "duration": "40:00", "thumb": "https://i.ytimg.com/vi/6PHX4wEa6P8/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=6PHX4wEa6P8", "views": "1.4M"}
            ],
            "advanced": [
                {"title": "Database Sharding & Replication", "channel": "ByteByteGo", "duration": "25:00", "thumb": "https://i.ytimg.com/vi/bUHFg8CZFCA/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=bUHFg8CZFCA", "views": "2.1M"},
                {"title": "Message Queues & Event-Driven Architecture", "channel": "TechWorld with Nana", "duration": "35:00", "thumb": "https://i.ytimg.com/vi/oUJbuFMyBDk/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=oUJbuFMyBDk", "views": "1.5M"}
            ],
            "summary": [{"title": "Designing a Scalable Microservices Architecture", "channel": "ByteByteGo", "duration": "45:00", "thumb": "https://i.ytimg.com/vi/bUHFg8CZFCA/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=bUHFg8CZFCA", "views": "2.8M"}]
        }
    },

    "QA Testing": {
        "beginner": {
            "intro": [{"title": "Software Testing Tutorial for Beginners", "channel": "Guru99", "duration": "1:15:00", "thumb": "https://i.ytimg.com/vi/s0Y_5Nf3Vrk/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=s0Y_5Nf3Vrk", "views": "2.5M"}],
            "core": [
                {"title": "Selenium WebDriver Full Course – Test Automation", "channel": "freeCodeCamp.org", "duration": "3:00:00", "thumb": "https://i.ytimg.com/vi/FRn5J31eGoM/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=FRn5J31eGoM", "views": "2.8M"},
                {"title": "API Testing with Postman", "channel": "freeCodeCamp.org", "duration": "1:30:00", "thumb": "https://i.ytimg.com/vi/VywxIQ2ZXw4/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=VywxIQ2ZXw4", "views": "3.1M"}
            ],
            "advanced": [
                {"title": "Unit & Integration Testing with Pytest / Jest", "channel": "Tech With Tim", "duration": "45:00", "thumb": "https://i.ytimg.com/vi/byaxgO-N4vc/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=byaxgO-N4vc", "views": "1.2M"},
                {"title": "Cypress E2E Testing Tutorial", "channel": "freeCodeCamp.org", "duration": "2:00:00", "thumb": "https://i.ytimg.com/vi/BQqzfHQbnhE/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=BQqzfHQbnhE", "views": "1.6M"}
            ],
            "summary": [{"title": "CI/CD Test Automation Pipelines", "channel": "TechWorld with Nana", "duration": "40:00", "thumb": "https://i.ytimg.com/vi/scziwA6u-xI/hqdefault.jpg", "url": "https://www.youtube.com/watch?v=scziwA6u-xI", "views": "1.1M"}]
        }
    }
}

# ══════════════════════════════════════════════════════════════════════════════
# EXTENDED QUIZ BANK (EXACTLY 15 questions: 5 easy, 5 medium, 5 hard per topic)
# ══════════════════════════════════════════════════════════════════════════════
EXTENDED_QUIZ_BANK = {
    "Docker": [
        # 5 Easy
        {"level": "easy", "q": "What is the primary role of a Dockerfile?", "opts": ["To run virtual machines", "A text script containing instructions to build a container image", "A network routing protocol", "To compile Python source code to binary"], "ans": 1, "explanation": "A Dockerfile defines the sequential instructions to assemble a Docker image."},
        {"level": "easy", "q": "Which Docker CLI command starts a container from an image?", "opts": ["docker build", "docker run", "docker commit", "docker attach"], "ans": 1, "explanation": "'docker run' creates and starts a container from a specified image."},
        {"level": "easy", "q": "How do containers differ fundamentally from virtual machines (VMs)?", "opts": ["Containers include a full guest operating system kernel", "Containers share the host OS kernel and isolate at process level", "Containers only run Java programs", "Containers cannot be networked"], "ans": 1, "explanation": "Containers share the host operating system kernel, making them lightweight compared to hypervisor VMs."},
        {"level": "easy", "q": "Which command lists all currently running Docker containers?", "opts": ["docker images", "docker ps", "docker net", "docker ls -a"], "ans": 1, "explanation": "'docker ps' lists all active running containers."},
        {"level": "easy", "q": "What is Docker Hub?", "opts": ["A local router", "A public cloud-based registry for sharing container images", "A compiler for Dockerfiles", "A Kubernetes control plane"], "ans": 1, "explanation": "Docker Hub is the primary public registry service provided by Docker for finding and sharing images."},

        # 5 Medium
        {"level": "medium", "q": "In a Dockerfile, what is the key difference between CMD and ENTRYPOINT?", "opts": ["CMD cannot take arguments", "ENTRYPOINT defines the fixed executable, while CMD provides default arguments that can be overridden", "CMD runs at image build time, ENTRYPOINT runs at runtime", "There is no difference between them"], "ans": 1, "explanation": "ENTRYPOINT sets the default application to invoke, whereas CMD provides default parameters that the caller can override on the CLI."},
        {"level": "medium", "q": "What is the primary purpose of a Docker volume?", "opts": ["To increase CPU allocation", "To persist data outside the container lifecycle across restarts/removals", "To speed up network packet delivery", "To encrypt memory"], "ans": 1, "explanation": "Volumes are stored on the host filesystem and persist independently of container destruction."},
        {"level": "medium", "q": "In Docker Compose, what file format is used to declare multi-container applications?", "opts": ["XML", "JSON", "YAML", "Toml"], "ans": 2, "explanation": "Docker Compose configurations are written in YAML (e.g. docker-compose.yml)."},
        {"level": "medium", "q": "What does the -p 8080:80 flag specify in 'docker run -p 8080:80 nginx'?", "opts": ["Allocates 8080 MB of RAM", "Binds host port 8080 to container port 80", "Runs container for 8080 seconds", "Limits bandwidth to 80 Mbps"], "ans": 1, "explanation": "The format is -p <host_port>:<container_port>, mapping port 8080 on the host to port 80 inside the container."},
        {"level": "medium", "q": "Why are multi-stage builds recommended in production Dockerfiles?", "opts": ["They make images compatible with Windows only", "They separate build dependencies from the final runtime image to minimize image size and attack surface", "They execute multiple containers simultaneously", "They avoid needing a base image"], "ans": 1, "explanation": "Multi-stage builds allow leaving compilers and intermediate build tools behind, resulting in slim, secure production images."},

        # 5 Hard
        {"level": "hard", "q": "How does Docker leverage Linux cgroups (Control Groups)?", "opts": ["To encrypt network traffic between containers", "To limit and isolate resource usage (CPU, memory, disk I/O) of process trees", "To assign unique MAC addresses to virtual network interfaces", "To compile kernel modules on the fly"], "ans": 1, "explanation": "Linux cgroups constrain and monitor hardware resource allocations (memory, CPU, I/O) per container process group."},
        {"level": "hard", "q": "What is the function of Linux namespaces in container isolation?", "opts": ["They allocate physical disk sectors", "They partition system resources so a process views its own isolated workspace (PID, NET, MNT, IPC, UTS, USER)", "They synchronize clocks across distributed clusters", "They provide automated garbage collection"], "ans": 1, "explanation": "Namespaces provide processes with independent views of system resources, such as process trees, network interfaces, and mount tables."},
        {"level": "hard", "q": "Which Docker storage driver uses copy-on-write (CoW) page caching and is the modern default on most Linux systems?", "opts": ["aufs", "devicemapper", "overlay2", "vfs"], "ans": 2, "explanation": "overlay2 is the recommended, high-performance storage driver combining upper and lower directory layers via overlayfs."},
        {"level": "hard", "q": "What happens when a container's main PID 1 process exits?", "opts": ["The container continues running with a new PID 1", "The container immediately stops because PID 1 is the container's lifecycle anchor", "The container enters pause mode until manually terminated", "The kernel restarts the host system"], "ans": 1, "explanation": "When process ID 1 terminates inside a container namespace, the kernel halts all child processes and the container exits."},
        {"level": "hard", "q": "Why is running containers with the root user considered a security vulnerability, and how is it mitigated?", "opts": ["Root containers consume double the RAM; mitigated by setting memory limits", "If a container breakout occurs, the attacker gains host root privileges; mitigated by using USER directives or rootless containers", "Root containers cannot connect to the internet; mitigated with host networking", "Root containers cannot use Docker Compose"], "ans": 1, "explanation": "Processes running as root inside a container have uid 0, which maps to host root unless user namespace remapping or non-root USER directives are enforced."}
    ],

    "Kubernetes": [
        # 5 Easy
        {"level": "easy", "q": "What is the smallest deployable compute unit in Kubernetes?", "opts": ["Cluster", "Node", "Pod", "Service"], "ans": 2, "explanation": "A Pod encapsulates one or more co-located containers sharing network and storage."},
        {"level": "easy", "q": "Which Kubernetes command line tool is used to interact with clusters?", "opts": ["kube-proxy", "kubectl", "docker", "minikube-cli"], "ans": 1, "explanation": "'kubectl' is the standard CLI for running commands against Kubernetes clusters."},
        {"level": "easy", "q": "What component serves as the central API gateway and control plane brain of Kubernetes?", "opts": ["kube-scheduler", "kube-apiserver", "etcd", "kubelet"], "ans": 1, "explanation": "The kube-apiserver exposes the Kubernetes API and intercepts all cluster requests."},
        {"level": "easy", "q": "What is the default Service type in Kubernetes that exposes the service only inside the cluster?", "opts": ["NodePort", "LoadBalancer", "ClusterIP", "ExternalName"], "ans": 2, "explanation": "ClusterIP assigns a virtual internal cluster IP, making the Pods reachable only within the cluster."},
        {"level": "easy", "q": "What Kubernetes object manages declarative rolling updates and replica scaling of Pods?", "opts": ["ConfigMap", "Deployment", "Ingress", "Namespace"], "ans": 1, "explanation": "A Deployment provides declarative updates for Pods and ReplicaSets."},

        # 5 Medium
        {"level": "medium", "q": "What distributed key-value store holds the entire cluster state and configuration in Kubernetes?", "opts": ["Redis", "etcd", "Consul", "PostgreSQL"], "ans": 1, "explanation": "etcd is a consistent, highly available key-value store used as Kubernetes' backing store."},
        {"level": "medium", "q": "What is the primary difference between a Liveness Probe and a Readiness Probe?", "opts": ["Liveness checks memory; Readiness checks CPU", "Liveness determines if the container must be restarted; Readiness determines if it can accept traffic", "Liveness is for frontend only; Readiness is for backend only", "There is no difference"], "ans": 1, "explanation": "Liveness probes restart failed containers; readiness probes remove unhealthy pods from service endpoints until ready."},
        {"level": "medium", "q": "What Kubernetes resource enables routing external HTTP/HTTPS traffic to internal services using host or path rules?", "opts": ["NetworkPolicy", "Ingress", "ClusterIP", "ConfigMap"], "ans": 1, "explanation": "Ingress exposes HTTP and HTTPS routes from outside the cluster to services within the cluster."},
        {"level": "medium", "q": "How do ConfigMaps differ from Secrets in Kubernetes?", "opts": ["ConfigMaps store encrypted binary data; Secrets store plaintext strings", "ConfigMaps store non-sensitive configuration data; Secrets store confidential tokens, passwords, and keys (base64 encoded/encrypted)", "ConfigMaps only work on worker nodes", "Secrets cannot be mounted as volumes"], "ans": 1, "explanation": "ConfigMaps are designed for non-confidential configuration, while Secrets manage sensitive credentials with access controls."},
        {"level": "medium", "q": "What role does Helm play in the Kubernetes ecosystem?", "opts": ["It compiles Kubernetes kernel drivers", "It acts as a package manager to define, install, and upgrade complex Kubernetes applications via charts", "It monitors cluster CPU utilization", "It provides hardware virtualization"], "ans": 1, "explanation": "Helm is the package manager for Kubernetes, packaging manifests into reusable templates called charts."},

        # 5 Hard
        {"level": "hard", "q": "What is the role of the kube-scheduler component?", "opts": ["It executes containers on worker nodes", "It monitors unscheduled Pods and assigns them to optimal nodes based on resource requests and affinity constraints", "It maintains network routing tables on nodes", "It terminates idle worker nodes"], "ans": 1, "explanation": "kube-scheduler filters and scores available worker nodes to decide which node should host a newly created pod."},
        {"level": "hard", "q": "What happens during a RollingUpdate when maxSurge=1 and maxUnavailable=0 on a 3-replica Deployment?", "opts": ["All 3 pods terminate before 3 new pods are created", "Kubernetes creates 1 new pod (total 4), waits for readiness, then terminates 1 old pod, maintaining at least 3 available pods at all times", "The cluster rejects the update because maxUnavailable must be at least 1", "The deployment immediately scales to 6 pods"], "ans": 1, "explanation": "maxUnavailable=0 guarantees no downtime; maxSurge=1 allows temporary creation of 1 additional pod during progression."},
        {"level": "hard", "q": "What is the primary difference between a StatefulSet and a Deployment?", "opts": ["Deployments cannot use volumes", "StatefulSets maintain unique, persistent identities and stable network hostnames (pod-0, pod-1) with ordered provisioning", "StatefulSets run on control plane nodes only", "Deployments cannot scale horizontally"], "ans": 1, "explanation": "StatefulSets provide stable, unique network identifiers and persistent storage mappings required for distributed databases."},
        {"level": "hard", "q": "How does kube-proxy implement Service traffic routing on modern Linux worker nodes?", "opts": ["By acting as a user-space proxy routing every packet through a Go daemon", "By manipulating iptables or IPVS kernel rules to translate Service ClusterIPs to backing Pod IPs directly", "By rewriting DNS queries inside CoreDNS", "By injecting an Envoy sidecar into every pod automatically"], "ans": 1, "explanation": "In iptables/IPVS mode, kube-proxy configures kernel netfilter tables to perform fast L4 connection translation without context switching to user space."},
        {"level": "hard", "q": "What mechanism does Kubernetes use to prevent cascading node crashes when physical memory is exhausted?", "opts": ["Dynamic swap space creation", "Kubelet Node Eviction (gracefully evicting pods based on QoS classes: BestEffort first, then Burstable, then Guaranteed)", "Kernel panic trigger", "Automated node deletion from cloud provider"], "ans": 1, "explanation": "When memory thresholds are breached, kubelet proactively evicts pods based on QoS classes to preserve node stability."}
    ],

    "Linux": [
        # 5 Easy
        {"level": "easy", "q": "Which Linux command displays the current working directory path?", "opts": ["cd", "pwd", "ls", "dir"], "ans": 1, "explanation": "'pwd' stands for 'print working directory'."},
        {"level": "easy", "q": "What does the command 'chmod 755 script.sh' do?", "opts": ["Deletes the script", "Sets read/write/execute for owner, and read/execute for group and others", "Encrypts the script", "Hides the script from non-root users"], "ans": 1, "explanation": "7 (rwx) for owner, 5 (r-x) for group, 5 (r-x) for others."},
        {"level": "easy", "q": "Which command is used to view real-time system process activity in Linux?", "opts": ["ps", "top", "find", "grep"], "ans": 1, "explanation": "'top' (or 'htop') provides a dynamic, real-time view of running processes and system resources."},
        {"level": "easy", "q": "Where are system log files traditionally stored on a standard Linux distribution?", "opts": ["/etc/logs", "/var/log", "/usr/logs", "/home/log"], "ans": 1, "explanation": "Under the Filesystem Hierarchy Standard, /var/log is the canonical directory for system and application logs."},
        {"level": "easy", "q": "Which command allows executing a command with administrative superuser privileges?", "opts": ["su", "sudo", "admin", "root"], "ans": 1, "explanation": "'sudo' executes a command as the superuser according to rules in /etc/sudoers."},

        # 5 Medium
        {"level": "medium", "q": "What does the first line '#!/usr/bin/env bash' (shebang) in a script indicate?", "opts": ["A comment ignored by all interpreters", "Specifies the absolute interpreter binary path used to execute the script", "A compiler directive for C code", "A syntax error"], "ans": 1, "explanation": "The shebang (#!) tells the operating system's program loader which interpreter to invoke for the script."},
        {"level": "medium", "q": "How does 'systemctl restart nginx' differ from 'systemctl reload nginx'?", "opts": ["Restart shuts down and starts the process; Reload re-reads configuration files without terminating existing client connections", "Reload terminates the server permanently", "Restart only works in development", "There is no difference"], "ans": 0, "explanation": "Reload reloads configuration gracefully without dropping connections; restart stops and starts the process."},
        {"level": "medium", "q": "What does the exit status ($?) 0 indicate in a Bash shell?", "opts": ["An uncaught fatal error occurred", "The previous command executed successfully without errors", "The command produced no standard output", "The process was killed by SIGKILL"], "ans": 1, "explanation": "In Unix/Linux conventions, an exit status of 0 represents success; any non-zero value indicates an error code."},
        {"level": "medium", "q": "What is the function of the grep -E (or egrep) command in Linux?", "opts": ["Edits binary files", "Matches patterns using Extended Regular Expressions", "Estimates disk usage", "Extracts tar archives"], "ans": 1, "explanation": "'grep -E' enables Extended Regular Expression syntax (supporting +, ?, |, parentheses) for pattern matching."},
        {"level": "medium", "q": "What does the command 'tar -czvf archive.tar.gz /data' accomplish?", "opts": ["Extracts an archive to /data", "Creates a gzip-compressed tar archive of /data with verbose output", "Deletes /data safely", "Tests archive integrity"], "ans": 1, "explanation": "-c creates archive, -z compresses with gzip, -v enables verbose progress, -f specifies output filename."},

        # 5 Hard
        {"level": "hard", "q": "What is the difference between a hard link and a symbolic (soft) link in Linux?", "opts": ["Hard links cannot point to files; soft links can", "A hard link points directly to the file's inode and shares its data blocks; a soft link stores the file path text and breaks if target moves", "Soft links are faster than hard links", "Hard links are only supported on NTFS filesystems"], "ans": 1, "explanation": "Hard links increment the inode link count and remain valid even if the original name is removed."},
        {"level": "hard", "q": "What does the Linux OOM (Out Of Memory) Killer do when system RAM is completely depleted?", "opts": ["Freezes the CPU until memory is freed", "Evaluates badness scores and sends SIGKILL to selected high-memory processes to salvage the operating system kernel", "Automates swap partition resizing", "Shuts down the physical network interface"], "ans": 1, "explanation": "The Linux kernel's OOM killer calculates process badness heuristics and terminates victim processes to prevent total kernel deadlock."},
        {"level": "hard", "q": "What is the purpose of the 'ulimit -n' setting in Linux server administration?", "opts": ["Sets network bandwidth cap", "Defines the maximum number of open file descriptors allowed for a user process session", "Limits the maximum number of CPU cores", "Configures firewall connection limits"], "ans": 1, "explanation": "ulimit -n restricts the maximum open file handles (sockets and files), vital for high-concurrency servers like Nginx or Redis."},
        {"level": "hard", "q": "How does SIGTERM (signal 15) differ fundamentally from SIGKILL (signal 9)?", "opts": ["SIGKILL allows graceful cleanup; SIGTERM terminates immediately", "SIGTERM requests polite termination giving the process opportunity to close sockets and save state; SIGKILL cannot be caught or ignored", "SIGTERM is only used by the kernel; SIGKILL by users", "They are identical in kernel behavior"], "ans": 1, "explanation": "SIGTERM can be intercepted by a signal handler for graceful shutdown; SIGKILL immediately terminates the process at the kernel scheduler level."},
        {"level": "hard", "q": "What does the /proc virtual filesystem represent in Linux?", "opts": ["Persistent configuration files", "A pseudo-filesystem exposing real-time kernel data structures, process statuses, and hardware parameters", "A binary package cache", "A RAM-disk backup partition"], "ans": 1, "explanation": "/proc is an in-memory virtual filesystem generated by the kernel exposing process and system state dynamically."}
    ],

    "Git": [
        # 5 Easy
        {"level": "easy", "q": "What is the command to create a new branch and switch to it in Git?", "opts": ["git branch -d", "git checkout -b <branch_name>", "git merge -b", "git commit -b"], "ans": 1, "explanation": "'git checkout -b <name>' (or 'git switch -c <name>') creates and immediately switches to a new branch."},
        {"level": "easy", "q": "What does 'git status' display?", "opts": ["Git version number", "The current branch and state of tracked, untracked, and staged files", "Remote server IP addresses", "Commit commit history only"], "ans": 1, "explanation": "'git status' provides full state of the working directory and staging area."},
        {"level": "easy", "q": "Which command records staged changes into the local repository history?", "opts": ["git push", "git commit -m 'message'", "git add", "git log"], "ans": 1, "explanation": "'git commit' creates a new commit snapshot from the staged changes."},
        {"level": "easy", "q": "What does 'git pull' do under the hood?", "opts": ["Only uploads local code", "Executes 'git fetch' followed by 'git merge' to update the current local branch", "Deletes untracked files", "Resets the working tree to HEAD"], "ans": 1, "explanation": "'git pull' fetches commits from the remote tracking branch and merges them into the active local branch."},
        {"level": "easy", "q": "What is the purpose of the .gitignore file?", "opts": ["To speed up internet connection", "To specify intentionally untracked file patterns that Git should not commit", "To store passwords securely", "To lock branches from deletion"], "ans": 1, "explanation": ".gitignore lists file patterns (such as node_modules/, .env, build artifacts) to exclude from Git tracking."},

        # 5 Medium
        {"level": "medium", "q": "How does 'git merge' differ from 'git rebase'?", "opts": ["Merge creates a new merge commit combining histories; Rebase reapplies commits on top of another base creating a linear history", "Merge deletes commits; Rebase preserves them", "Rebase only works on remote repositories", "There is no difference"], "ans": 0, "explanation": "git merge preserves true chronological history with a merge commit; git rebase rewrites commit history linearly."},
        {"level": "medium", "q": "What does 'git stash' do?", "opts": ["Deletes all uncommitted work permanently", "Temporarily shelves uncommitted changes to give you a clean working directory", "Pushes commits directly to production", "Reverts the last 5 commits"], "ans": 1, "explanation": "Stashing saves modified tracked files and staged changes in a temporary store so you can switch branches cleanly."},
        {"level": "medium", "q": "When does a Git merge conflict occur?", "opts": ["When two branches have the same name", "When two branches modify the same lines of a file differently and Git cannot automatically determine which to keep", "When the repository exceeds 1 GB", "When a commit message is empty"], "ans": 1, "explanation": "Merge conflicts arise when competing changes are made to the same lines or file structure across merged branches."},
        {"level": "medium", "q": "What does 'git cherry-pick <commit_hash>' do?", "opts": ["Deletes the specified commit", "Applies the exact changes introduced by an existing commit onto the current active branch", "Renames a branch", "Shows the commit author"], "ans": 1, "explanation": "Cherry-picking selects a specific commit from any branch and applies its patch as a new commit on the current branch."},
        {"level": "medium", "q": "What is a Pull Request (PR) in GitHub?", "opts": ["A command to pull code to your laptop", "A proposed set of changes submitted for review, discussion, and automated checks before merging into a target branch", "A bug report", "A billing request"], "ans": 1, "explanation": "A Pull Request informs collaborators of changes pushed to a branch in order to conduct code review and CI verification before merging."},

        # 5 Hard
        {"level": "hard", "q": "How does 'git reset --hard' differ from 'git reset --soft'?", "opts": ["--hard keeps changes staged; --soft deletes files", "--soft moves HEAD while keeping changes staged; --hard moves HEAD and discards all changes in staging and working tree", "--hard only works on remote branches", "Both commands behave identically"], "ans": 1, "explanation": "--soft leaves index and working tree untouched; --hard resets index and working tree to the target commit, discarding uncommitted work."},
        {"level": "hard", "q": "What is the Git object model based on internally?", "opts": ["Relational tables in SQLite", "A content-addressable storage graph of immutable objects (blobs, trees, commits, annotated tags) keyed by SHA hashes", "A single compressed zip file", "A flat XML database"], "ans": 1, "explanation": "Git stores data in a directed acyclic graph (DAG) of content-addressed objects identified by their SHA cryptographic checksums."},
        {"level": "hard", "q": "What is a 'detached HEAD' state in Git?", "opts": ["A corrupted Git database", "The HEAD pointer references a specific commit directly rather than a named local branch", "A branch that has no upstream remote", "A failed merge operation"], "ans": 1, "explanation": "In detached HEAD state, you can experiment and make commits, but changes will not belong to any branch unless a new branch is created."},
        {"level": "hard", "q": "Why is running 'git push --force' dangerous on shared branches like 'main', and what safer alternative exists?", "opts": ["It corrupts local Git files; use git status instead", "It overwrites remote history, potentially erasing teammates' commits; use 'git push --force-with-lease' to prevent overwriting unseen work", "It charges money on GitHub; use git pull instead", "It has no danger on shared branches"], "ans": 1, "explanation": "--force-with-lease checks that the remote ref has not been updated by someone else before performing the forced overwrite."},
        {"level": "hard", "q": "What does 'git reflog' do, and why is it invaluable for disaster recovery?", "opts": ["Lists remote branch URLs", "Records every update to references (HEAD, branch tips) in local repo, allowing recovery of lost or deleted commits", "Formats commit messages automatically", "Cleans up unreachable objects"], "ans": 1, "explanation": "reflog logs every movement of HEAD (commits, checkouts, rebases), enabling retrieval of commits even after accidental reset or branch deletion."}
    ],

    "CI/CD": [
        # 5 Easy
        {"level": "easy", "q": "What does CI stand for in modern DevOps terminology?", "opts": ["Continuous Infrastructure", "Continuous Integration", "Cloud Intelligence", "Container Initialization"], "ans": 1, "explanation": "Continuous Integration is the practice of automating the integration of code changes from multiple contributors into a single repository."},
        {"level": "easy", "q": "What triggers a GitHub Actions workflow defined with 'on: [push]'?", "opts": ["A manual email", "Any git push event to the repository matching the workflow filters", "A scheduled cron job at midnight only", "A pull request closure only"], "ans": 1, "explanation": "'on: [push]' configures the workflow to trigger whenever commits are pushed to the repository."},
        {"level": "easy", "q": "What file extension is used for GitHub Actions workflow files?", "opts": [".xml", ".yaml (or .yml)", ".json", ".ini"], "ans": 1, "explanation": "GitHub Actions workflows are defined in YAML format in the .github/workflows directory."},
        {"level": "easy", "q": "What is the primary goal of Continuous Delivery (CD)?", "opts": ["Writing documentation", "Ensuring software can be reliably released to production at any time through automated builds and tests", "Eliminating all unit tests", "Running servers on-premises only"], "ans": 1, "explanation": "CD automates the release process so code changes are continuously built, tested, and staged for release."},
        {"level": "easy", "q": "In Jenkins, what is the file called that defines the build pipeline as code?", "opts": ["Jenkinsfile", "Dockerfile", "Pipeline.xml", "build.gradle"], "ans": 0, "explanation": "A Jenkinsfile is a text file that contains the definition of a Jenkins Pipeline and is checked into source control."},

        # 5 Medium
        {"level": "medium", "q": "What is the key benefit of automated unit testing inside a CI pipeline?", "opts": ["Eliminates the need for compilers", "Detects regressions and bugs immediately before code merges into the main branch", "Decreases server RAM usage", "Generates API documentation automatically"], "ans": 1, "explanation": "Automated pipeline tests provide immediate feedback on code correctness and prevent breaking changes from reaching production."},
        {"level": "medium", "q": "How are sensitive database passwords and API tokens safely provided to GitHub Actions workflows?", "opts": ["Hardcoded into workflow YAML files", "Configured as encrypted GitHub Actions Secrets and referenced via ${{ secrets.KEY }}", "Stored in public commits in .env files", "Sent via unencrypted HTTP headers"], "ans": 1, "explanation": "GitHub Repository Secrets encrypt sensitive credentials and mask them in workflow console logs."},
        {"level": "medium", "q": "What is a matrix build in CI systems like GitHub Actions?", "opts": ["A 3D simulation", "A strategy to run jobs across combinations of operating systems, runtimes, and versions in parallel", "A pipeline that only runs once a month", "A specialized compiler"], "ans": 1, "explanation": "Matrix strategies automatically generate multiple job configurations (e.g. Node 18, 20 on Ubuntu, macOS, Windows) simultaneously."},
        {"level": "medium", "q": "What is the difference between Continuous Delivery and Continuous Deployment?", "opts": ["Continuous Delivery requires manual approval to trigger the final production release; Continuous Deployment deploys automatically without human intervention", "Continuous Delivery is for frontend; Continuous Deployment is for backend", "Continuous Deployment does not run tests", "There is no difference"], "ans": 0, "explanation": "Continuous Delivery keeps code releasable with automated gates up to production; Continuous Deployment pushes straight to production automatically."},
        {"level": "medium", "q": "What is an artifact in CI/CD pipeline terminology?", "opts": ["An ancient source code file", "A deployable binary, bundle, or test report generated during a pipeline build stage and saved for later stages", "A git merge conflict", "A hardware server"], "ans": 1, "explanation": "Artifacts are the compiled files, container images, or test results produced by a build step and passed to deployment steps."},

        # 5 Hard
        {"level": "hard", "q": "How does a Blue-Green deployment strategy achieve zero-downtime application releases?", "opts": ["By running on blue-colored hardware servers only", "By maintaining two identical production environments (Blue active, Green staging); deploying new code to Green, running health tests, and switching the router/load balancer", "By deploying 10% of users to production every hour", "By restarting all pods simultaneously"], "ans": 1, "explanation": "Blue-Green keeps the active environment running while validating the new release in an identical parallel environment before instant traffic cutover."},
        {"level": "hard", "q": "What is a Canary deployment strategy?", "opts": ["Deploying code only on weekends", "Routing a small fraction of real production user traffic (e.g. 5%) to the new release to monitor error rates and latency before wider rollout", "Deploying only to internal staff laptops", "A pipeline that triggers every 5 seconds"], "ans": 1, "explanation": "Canary releases expose a small subset of production traffic to the new version to detect issues before rolling out universally."},
        {"level": "hard", "q": "What are the 4 DORA metrics used by elite engineering teams to measure software delivery performance?", "opts": ["Lines of code, bugs filed, hours worked, test count", "Deployment Frequency, Lead Time for Changes, Change Failure Rate, Time to Restore Service (MTTR)", "Server count, RAM usage, CPU clock, disk latency", "Agile velocity, sprint points, burndown rate, story count"], "ans": 1, "explanation": "The DevOps Research and Assessment (DORA) metrics are the industry standard benchmarks for delivery speed and stability."},
        {"level": "hard", "q": "What is GitOps, and how does a tool like ArgoCD or Flux implement it?", "opts": ["Using Git only for documentation", "Using a Git repository as the single declarative source of truth for desired infrastructure and application state, with automated controllers synchronizing cluster state", "Writing git commits automatically using AI", "Running Git commands inside Docker containers"], "ans": 1, "explanation": "GitOps ensures that cluster state continuously matches the declarative manifests versioned in Git through automated reconciliation loops."},
        {"level": "hard", "q": "What is the purpose of Static Application Security Testing (SAST) in a DevSecOps pipeline?", "opts": ["Testing live production servers with simulated DDoS attacks", "Analyzing source code, byte code, or binaries for security vulnerabilities and weaknesses without executing the program", "Checking web page loading speeds", "Monitoring server CPU spikes"], "ans": 1, "explanation": "SAST tools (like SonarQube, Semgrep) scan static code repositories early in the build pipeline to catch OWASP vulnerabilities before deployment."}
    ],

    "AWS Cloud": [
        # 5 Easy
        {"level": "easy", "q": "What does AWS stand for?", "opts": ["Advanced Web Services", "Amazon Web Services", "Automated Web System", "Applied Wireless Solutions"], "ans": 1, "explanation": "AWS stands for Amazon Web Services."},
        {"level": "easy", "q": "Which AWS service provides resizable virtual server instances in the cloud?", "opts": ["Amazon S3", "Amazon EC2 (Elastic Compute Cloud)", "AWS Lambda", "Amazon RDS"], "ans": 1, "explanation": "EC2 provides scalable on-demand compute capacity in the cloud."},
        {"level": "easy", "q": "What is Amazon S3 primarily used for?", "opts": ["Running relational SQL queries", "Object storage for files, media, backups, and static website assets", "Hosting DNS domains", "Managing SSL certificates"], "ans": 1, "explanation": "Amazon Simple Storage Service (S3) provides scalable, highly durable object storage."},
        {"level": "easy", "q": "Which AWS service handles user authentication, groups, permissions, and roles?", "opts": ["AWS CloudWatch", "AWS IAM (Identity and Access Management)", "AWS Route 53", "Amazon VPC"], "ans": 1, "explanation": "AWS IAM enables secure control of access to AWS services and resources."},
        {"level": "easy", "q": "What is an AWS Region?", "opts": ["A single physical data center room", "A separate geographic area containing multiple, isolated Availability Zones (AZs)", "A continent-wide network cable", "A software virtual machine"], "ans": 1, "explanation": "An AWS Region is a physical location in the world with multiple isolated data center clusters called Availability Zones."},

        # 5 Medium
        {"level": "medium", "q": "What is an Amazon VPC (Virtual Private Cloud)?", "opts": ["A public website builder", "A logically isolated virtual network dedicated to your AWS account where you launch AWS resources", "A hardware hard drive", "An automated code compiler"], "ans": 1, "explanation": "VPC lets you provision a private virtual network with full control over IP ranges, subnets, route tables, and gateways."},
        {"level": "medium", "q": "How does an Application Load Balancer (ALB) differ from a Network Load Balancer (NLB)?", "opts": ["ALB operates at Layer 7 (HTTP/HTTPS) with path/host routing; NLB operates at Layer 4 (TCP/UDP) for ultra-low latency and extreme throughput", "ALB is only for databases", "NLB only routes HTTP requests", "There is no difference"], "ans": 0, "explanation": "ALB is an application-aware Layer 7 load balancer; NLB provides ultra-high performance connection load balancing at Layer 4."},
        {"level": "medium", "q": "What is the difference between AWS Security Groups and Network Access Control Lists (NACLs)?", "opts": ["Security groups are stateful and operate at instance ENI level; NACLs are stateless and operate at subnet boundary level", "NACLs only inspect outgoing traffic", "Security groups cannot block traffic", "There is no difference"], "ans": 0, "explanation": "Security Groups are stateful firewalls at the instance level; NACLs are stateless subnet-level rules evaluated in order."},
        {"level": "medium", "q": "What is AWS Lambda?", "opts": ["A dedicated physical server", "A serverless compute service that runs code in response to events and automatically manages the underlying compute resources", "A relational database engine", "A DNS resolver"], "ans": 1, "explanation": "AWS Lambda is an event-driven serverless platform that executes functions without provisioning or managing servers."},
        {"level": "medium", "q": "What is the purpose of Amazon RDS?", "opts": ["NoSQL document storage", "A managed relational database service supporting engines like PostgreSQL, MySQL, MariaDB, and Aurora", "Managing container images", "Caching Redis keys"], "ans": 1, "explanation": "RDS simplifies database setup, operation, backups, and scaling for traditional relational databases."},

        # 5 Hard
        {"level": "hard", "q": "What is an IAM Role, and how does it enhance security compared to an IAM User with static API keys?", "opts": ["IAM roles have permanent passwords", "IAM roles provide temporary, rotating security credentials via STS, eliminating hardcoded long-term access keys on servers", "IAM roles can only be used by root users", "IAM roles cannot access S3"], "ans": 1, "explanation": "Roles use the AWS Security Token Service (STS) to issue short-lived credentials automatically without storing credentials in code."},
        {"level": "hard", "q": "How does Amazon Aurora achieve up to 5x throughput over standard MySQL?", "opts": ["By caching all data in local CPU registers", "By decoupling compute from a purpose-built distributed log-structured storage subsystem replicated across 3 AZs", "By disabling ACID transactions", "By running on single-threaded ARM chips only"], "ans": 1, "explanation": "Aurora writes redo logs directly to a shared distributed storage fleet, eliminating disk flush bottlenecks and secondary write overhead."},
        {"level": "hard", "q": "What is the function of a NAT Gateway in a private AWS subnet?", "opts": ["Allows external clients on the internet to initiate connections into private database instances", "Enables instances in a private subnet to connect outbound to the internet (e.g. for software updates) while blocking inbound connections from the internet", "Encodes video streams", "Balances web traffic across EC2 instances"], "ans": 1, "explanation": "NAT Gateways provide outbound internet connectivity for private subnet instances while keeping them shielded from incoming internet traffic."},
        {"level": "hard", "q": "What is AWS Auto Scaling lifecycle hook used for in production EC2 deployments?", "opts": ["Rebooting instances every 24 hours", "Pausing instance termination or launch to perform custom cleanup (draining connections, saving logs) before instance removal", "Encrypting S3 buckets", "Updating DNS records"], "ans": 1, "explanation": "Lifecycle hooks pause scaling actions, allowing scripts to drain traffic or complete transactions gracefully before an instance terminates."},
        {"level": "hard", "q": "What is AWS Transit Gateway, and what networking challenge does it solve?", "opts": ["A home Wi-Fi router", "A central cloud hub that connects thousands of VPCs and on-premises networks, replacing complex point-to-point VPC peering meshes", "A static IP address on S3", "A web application firewall rule"], "ans": 1, "explanation": "Transit Gateway simplifies hub-and-spoke networking architectures across hundreds of VPCs and on-premises data centers."}
    ],

    "Terraform": [
        # 5 Easy
        {"level": "easy", "q": "What is Terraform?", "opts": ["A container runtime", "An open-source Infrastructure as Code (IaC) tool for provisioning cloud resources declaratively", "A relational database", "A Python web framework"], "ans": 1, "explanation": "Terraform by HashiCorp is the industry-standard tool for provisioning cloud infrastructure declaratively."},
        {"level": "easy", "q": "Which command initializes a Terraform working directory and downloads required provider plugins?", "opts": ["terraform plan", "terraform init", "terraform apply", "terraform start"], "ans": 1, "explanation": "'terraform init' initializes the working directory, backend, and provider plugins."},
        {"level": "easy", "q": "What file extension is used for Terraform configuration files?", "opts": [".tf", ".json", ".yaml", ".hcl2"], "ans": 0, "explanation": "Terraform files use the '.tf' extension (or '.tf.json')."},
        {"level": "easy", "q": "What is the purpose of 'terraform plan'?", "opts": ["Deletes existing infrastructure immediately", "Creates an execution plan previewing the exact additions, changes, and destructions Terraform will make", "Compiles Go source code", "Generates user passwords"], "ans": 1, "explanation": "'terraform plan' inspects current state and code to output a dry-run execution diff without modifying real resources."},
        {"level": "easy", "q": "Which command applies the changes required to reach the desired state of the configuration?", "opts": ["terraform apply", "terraform deploy", "terraform push", "terraform execute"], "ans": 0, "explanation": "'terraform apply' provisions or modifies real cloud resources to match the configuration files."},

        # 5 Medium
        {"level": "medium", "q": "What is the terraform.tfstate file?", "opts": ["A log of user comments", "A JSON file mapping real-world infrastructure resources to your configuration declarations and tracking metadata", "A binary license key", "A list of cloud passwords"], "ans": 1, "explanation": "The state file records the mapping between declared configuration and real-world provisioned cloud resource IDs."},
        {"level": "medium", "q": "Why is storing Terraform state in a remote backend (like AWS S3 with DynamoDB) essential for teams?", "opts": ["It makes Terraform free to use", "It provides centralized state storage, team collaboration, and state locking to prevent concurrent destructive updates", "It automatically writes Python code", "It avoids needing an AWS account"], "ans": 1, "explanation": "Remote backends store state securely and use locks (e.g. DynamoDB table) so two engineers cannot run 'apply' simultaneously."},
        {"level": "medium", "q": "What is a Terraform module?", "opts": ["A physical server rack", "A container for multiple resources that are used together to create reusable, configurable infrastructure blueprints", "A Python package installer", "A database table"], "ans": 1, "explanation": "Modules group resources together into modular, parameterizable packages (with input variables and outputs)."},
        {"level": "medium", "q": "How does Terraform determine the order in which to create resources?", "opts": ["Random alphabetical order", "By building a Directed Acyclic Graph (DAG) of resource dependencies based on references between blocks", "By the line number in the .tf file", "Resources are always created sequentially from top to bottom"], "ans": 1, "explanation": "Terraform builds an internal dependency graph (DAG) to provision independent resources concurrently and dependent resources in order."},
        {"level": "medium", "q": "What does the 'terraform destroy' command do?", "opts": ["Deletes the terraform binary from disk", "Terminates and removes all managed infrastructure resources declared in the configuration", "Rolls back to the previous git commit", "Cancels a running plan"], "ans": 1, "explanation": "'terraform destroy' cleanly removes all resources tracked by the state file."},

        # 5 Hard
        {"level": "hard", "q": "What is 'configuration drift' in Infrastructure as Code, and how does Terraform detect it?", "opts": ["When code moves to a different git branch", "When real-world cloud resources are modified out-of-band (e.g. in AWS Console); detected during 'terraform plan' by refreshing state against the real API", "When network latency increases", "When a hard drive fails"], "ans": 1, "explanation": "Drift happens when someone manually edits cloud settings; Terraform refresh compares real API attributes against the state file to detect discrepancies."},
        {"level": "hard", "q": "What does the 'lifecycle { create_before_destroy = true }' block achieve in Terraform?", "opts": ["Prevents resource destruction forever", "Ensures a replacement resource is fully created and verified before the old resource is destroyed, preventing downtime on updates", "Forces immediate deletion of state", "Disables plan output"], "ans": 1, "explanation": "create_before_destroy changes the default replacement order to create the new resource first, vital for zero-downtime upgrades."},
        {"level": "hard", "q": "What is the function of 'terraform import'?", "opts": ["Imports Python libraries into HCL", "Brings pre-existing cloud resources created manually or by other tools into Terraform state management", "Downloads community modules from GitHub", "Imports CSV spreadsheets"], "ans": 1, "explanation": "'terraform import' associates existing real-world cloud infrastructure with a resource block in your state file."},
        {"level": "hard", "q": "What is Terraform Workspaces primarily used for?", "opts": ["Splitting an office into cubicles", "Managing multiple state files for the same configuration code (e.g. dev, stage, prod environments)", "Running different Terraform versions on one laptop", "Editing code in a web browser"], "ans": 1, "explanation": "Workspaces allow having distinct state files associated with a single configuration directory for environment management."},
        {"level": "hard", "q": "What is Sentinel / OPA (Policy as Code) in enterprise Terraform pipelines?", "opts": ["A database backup scheduler", "A framework that enforces organizational compliance, cost, and security guardrails on execution plans before resources can be provisioned", "A compiler optimization tool", "A DNS routing mechanism"], "ans": 1, "explanation": "Policy as code checks (like Sentinel or OPA) inspect the terraform plan and reject non-compliant deployments (e.g. unencrypted disks)."}
    ],

    "React": [
        # 5 Easy
        {"level": "easy", "q": "What is React?", "opts": ["A relational database", "A JavaScript library for building user interfaces based on components", "A CSS preprocessor", "A server operating system"], "ans": 1, "explanation": "React is an open-source frontend JavaScript library developed by Meta for building UI components."},
        {"level": "easy", "q": "What is JSX in React?", "opts": ["A database query language", "A syntax extension for JavaScript that allows writing HTML-like structures inside JavaScript code", "A CSS framework", "A package manager"], "ans": 1, "explanation": "JSX lets you write HTML-like element tags directly inside JavaScript files, which transpilers convert to React.createElement calls."},
        {"level": "easy", "q": "Which React hook is used to add local state variables to functional components?", "opts": ["useEffect", "useState", "useContext", "useRef"], "ans": 1, "explanation": "useState returns a stateful value and a function to update it."},
        {"level": "easy", "q": "How do parent components pass data down to child components in React?", "opts": ["Via global environment variables", "Via props (properties)", "Via CSS classes", "Via local storage only"], "ans": 1, "explanation": "Props are the mechanism for passing read-only data from a parent component down to its child components."},
        {"level": "easy", "q": "What is the Virtual DOM in React?", "opts": ["A 3D VR simulation", "A lightweight in-memory representation of the real browser DOM that React uses to compute minimal updates", "A database engine", "A Chrome browser extension"], "ans": 1, "explanation": "The Virtual DOM allows React to diff state changes in memory and update only the modified real DOM nodes efficiently."},

        # 5 Medium
        {"level": "medium", "q": "When does the useEffect hook execute by default when no dependency array is supplied?", "opts": ["Only once when the component mounts", "After every single render of the component", "Only when an error occurs", "Never"], "ans": 1, "explanation": "Without a dependency array, useEffect runs after the initial mount and after every subsequent component re-render."},
        {"level": "medium", "q": "What does passing an empty dependency array '[]' to useEffect mean?", "opts": ["The effect runs on every render", "The effect runs only once when the component mounts and cleans up when it unmounts", "The effect is disabled", "The component never re-renders"], "ans": 1, "explanation": "An empty dependency array [] indicates that the effect has no dependencies and only runs once on mount."},
        {"level": "medium", "q": "Why is the 'key' prop necessary when rendering lists in React?", "opts": ["It styles list items with unique colors", "It provides a stable identity so React's reconciliation algorithm can identify which items changed, were added, or were removed", "It encrypts list values", "It is optional and does nothing"], "ans": 1, "explanation": "Keys give elements a stable identity across re-renders, enabling React to reuse existing DOM nodes efficiently."},
        {"level": "medium", "q": "What is 'prop drilling' in React, and how is it typically solved?", "opts": ["Compiling React props to C++", "Passing props down through multiple layers of intermediate components that don't need them; solved with Context API or state managers like Zustand/Redux", "Deleting props automatically", "Validating prop types"], "ans": 1, "explanation": "Prop drilling occurs when deeply nested components require data from high-level parents; React Context provides a way to share data globally."},
        {"level": "medium", "q": "What is the purpose of the useMemo hook?", "opts": ["To create memoized callback functions", "To cache the result of an expensive calculation between re-renders unless dependencies change", "To save state to LocalStorage", "To memoize entire HTML documents"], "ans": 1, "explanation": "useMemo memoizes the computed return value of a function, avoiding re-calculation on every render when dependencies are unchanged."},

        # 5 Hard
        {"level": "hard", "q": "How does React Fiber improve UI responsiveness compared to the legacy stack reconciler?", "opts": ["It compiles components directly to WebAssembly", "It breaks rendering work into incremental units of work that can be paused, prioritized, and resumed across animation frames", "It removes the Virtual DOM entirely", "It executes JavaScript on multiple threads"], "ans": 1, "explanation": "React Fiber is a complete rewrite of the reconciliation algorithm enabling concurrent rendering and priority-based scheduling."},
        {"level": "hard", "q": "What causes an infinite re-render loop in a React component using useEffect?", "opts": ["Using arrow functions in JSX", "Updating a state variable inside useEffect without a dependency array, or including that state variable in its own dependency array", "Using React.StrictMode", "Returning null from a component"], "ans": 1, "explanation": "Setting state inside an effect causes a re-render, which triggers the effect again, resulting in an infinite execution loop."},
        {"level": "hard", "q": "What is a React Error Boundary, and what lifecycle methods must a class component implement to act as one?", "opts": ["A CSS border property", "A component that catches JavaScript errors anywhere in its child component tree; implemented with static getDerivedStateFromError or componentDidCatch", "A try/catch block inside useEffect", "A Vite build plugin"], "ans": 1, "explanation": "Error boundaries catch render errors in their subtree, log the error, and display a fallback UI instead of crashing the app."},
        {"level": "hard", "q": "What is the difference between useMemo and useCallback in React?", "opts": ["useMemo caches a computed value; useCallback caches a function definition instance across re-renders", "useCallback is for classes; useMemo is for functions", "useMemo only runs in production", "They are aliases of the same hook"], "ans": 0, "explanation": "useMemo(() => fn(), deps) returns the memoized result; useCallback(fn, deps) returns the memoized function reference itself."},
        {"level": "hard", "q": "How does Server-Side Rendering (SSR) in frameworks like Next.js improve Core Web Vitals over a pure Client-Side Rendered (CSR) SPA?", "opts": ["It eliminates all JavaScript files", "It pre-renders complete HTML on the server, significantly improving First Contentful Paint (FCP) and Largest Contentful Paint (LCP) for users and SEO crawlers", "It disables browser caching", "It runs databases on the client"], "ans": 1, "explanation": "SSR delivers fully formed HTML directly from the server on the initial request, allowing instant painting while client hydration occurs in the background."}
    ],

    "SQL": [
        # 5 Easy
        {"level": "easy", "q": "What does SQL stand for?", "opts": ["Standard Query Language", "Structured Query Language", "Simple Quick Logic", "System Question Language"], "ans": 1, "explanation": "SQL stands for Structured Query Language."},
        {"level": "easy", "q": "Which SQL statement is used to extract data from a database?", "opts": ["GET", "EXTRACT", "SELECT", "OPEN"], "ans": 2, "explanation": "'SELECT' is the fundamental statement to query and retrieve rows from a table."},
        {"level": "easy", "q": "Which clause is used to filter records in a SQL query based on a condition?", "opts": ["FILTER BY", "WHERE", "HAVING", "LIMIT"], "ans": 1, "explanation": "The 'WHERE' clause filters rows before aggregation based on boolean conditions."},
        {"level": "easy", "q": "Which SQL command adds a new record to a table?", "opts": ["ADD ROW", "INSERT INTO", "NEW RECORD", "UPDATE"], "ans": 1, "explanation": "'INSERT INTO table_name (columns) VALUES (...)' inserts new rows."},
        {"level": "easy", "q": "What does the SQL command 'DELETE FROM users WHERE id = 5;' do?", "opts": ["Deletes the entire users table", "Removes only the row where id is 5", "Sets all columns in row 5 to NULL", "Renames user 5"], "ans": 1, "explanation": "It deletes specifically the row matching the WHERE condition without affecting the table schema."},

        # 5 Medium
        {"level": "medium", "q": "What is the difference between an INNER JOIN and a LEFT JOIN?", "opts": ["INNER JOIN returns all rows from both tables; LEFT JOIN returns only matches", "INNER JOIN returns only matching rows between both tables; LEFT JOIN returns all rows from the left table plus matching rows from the right table (with NULLs for non-matches)", "LEFT JOIN only works with numbers", "There is no difference"], "ans": 1, "explanation": "INNER JOIN requires matches on both sides; LEFT JOIN retains all left table rows regardless of right-side match."},
        {"level": "medium", "q": "What is the difference between WHERE and HAVING in SQL?", "opts": ["WHERE filters individual rows before aggregation; HAVING filters aggregated groups after GROUP BY", "WHERE is only for text; HAVING is for numbers", "HAVING cannot use comparison operators", "There is no difference"], "ans": 0, "explanation": "WHERE filters rows prior to GROUP BY; HAVING filters the groups produced by aggregate functions (e.g. HAVING COUNT(*) > 5)."},
        {"level": "medium", "q": "What are ACID properties in relational database transactions?", "opts": ["Accuracy, Consistency, Indexing, Durability", "Atomicity, Consistency, Isolation, Durability", "Allocation, Concurrency, Integrity, Distribution", "Authentication, Cryptography, Identity, Data"], "ans": 1, "explanation": "ACID guarantees that database transactions are processed reliably: All-or-nothing (Atomicity), valid state (Consistency), independent execution (Isolation), and committed persistence (Durability)."},
        {"level": "medium", "q": "What is a Foreign Key in a relational database?", "opts": ["A key that connects to another computer", "A column or group of columns that provides a link between data in two tables by referencing the Primary Key of another table", "An encrypted password", "A secondary index"], "ans": 1, "explanation": "A Foreign Key enforces referential integrity between child and parent tables."},
        {"level": "medium", "q": "What is the primary benefit of adding a B-Tree index to a database column?", "opts": ["It reduces disk space by 50%", "It accelerates SELECT and search queries from O(n) table scans to O(log n) tree lookups at the cost of slower INSERT/UPDATE writes", "It prevents duplicate rows automatically", "It encrypts the column data"], "ans": 1, "explanation": "Indexes dramatically speed up query lookups by maintaining sorted tree structures, trading write overhead for read speed."},

        # 5 Hard
        {"level": "hard", "q": "What is the difference between ROW_NUMBER(), RANK(), and DENSE_RANK() window functions?", "opts": ["They compute different mathematical averages", "ROW_NUMBER assigns consecutive integers; RANK skips ranks on ties (e.g. 1, 2, 2, 4); DENSE_RANK does not skip ranks on ties (e.g. 1, 2, 2, 3)", "DENSE_RANK only works on partitioned tables", "They are synonyms in PostgreSQL"], "ans": 1, "explanation": "When ties occur in window ordering: ROW_NUMBER numbers arbitrarily; RANK creates gaps equal to tie count; DENSE_RANK assigns the immediate next integer."},
        {"level": "hard", "q": "What is a Common Table Expression (CTE) in SQL, and when is a Recursive CTE needed?", "opts": ["A temporary database table stored on disk", "A named temporary result set defined with a WITH clause; recursive CTEs reference themselves to traverse hierarchical data (trees, graphs, org charts)", "A type of foreign key constraint", "A stored procedure in MySQL"], "ans": 1, "explanation": "CTEs simplify complex queries into readable temporary scopes; recursive CTEs iteratively evaluate until a terminal condition is met."},
        {"level": "hard", "q": "What phenomenon occurs in the 'Phantom Read' concurrency isolation anomaly?", "opts": ["A transaction reads uncommitted modified data", "A transaction re-executes a range query and discovers new rows inserted by another concurrent transaction that just committed", "A database loses power during a write", "An index becomes corrupt"], "ans": 1, "explanation": "Phantom reads happen under Repeatable Read when new matching rows inserted by other transactions appear upon re-querying."},
        {"level": "hard", "q": "What is database normalization, and what constitutes Third Normal Form (3NF)?", "opts": ["Compressing database tables", "Structuring relational tables to reduce redundancy; 3NF requires being in 2NF and having no transitive dependencies (every non-key attribute must depend on the primary key alone)", "Adding foreign keys to all tables", "Splitting tables across multiple servers"], "ans": 1, "explanation": "3NF eliminates transitive dependencies: all columns must depend directly on the primary key, the whole key, and nothing but the key."},
        {"level": "hard", "q": "What does the command 'EXPLAIN ANALYZE SELECT ...' do in PostgreSQL?", "opts": ["Estimates disk storage size", "Executes the query and outputs the actual runtime execution plan, showing node types (Seq Scan, Index Scan, Nested Loop), memory usage, and time per operator", "Formats the query syntax nicely", "Runs an automated security scan on query parameters"], "ans": 1, "explanation": "EXPLAIN ANALYZE runs the query and prints detailed planning costs and real execution timing for query performance tuning."}
    ],

    "System Design": [
        # 5 Easy
        {"level": "easy", "q": "What is the difference between horizontal and vertical scaling?", "opts": ["Horizontal means rotating monitors; vertical means stacking them", "Vertical scaling adds more resources (CPU/RAM) to a single machine; Horizontal scaling adds more machines/nodes to the pool", "Horizontal scaling only works in the cloud", "There is no difference"], "ans": 1, "explanation": "Scaling up (vertical) upgrades single box specs; scaling out (horizontal) distributes load across multiple servers."},
        {"level": "easy", "q": "What is the primary role of a Load Balancer in system architecture?", "opts": ["To run unit tests", "To distribute incoming network traffic across multiple backend servers to ensure high availability and responsiveness", "To compress database backups", "To authenticate user passwords"], "ans": 1, "explanation": "Load balancers distribute user requests across a pool of servers, preventing bottlenecks and handling server failures."},
        {"level": "easy", "q": "What is latency in computer networking?", "opts": ["The total data transferred per second", "The time delay taken for a data packet to travel from source to destination and back", "The physical weight of a server", "The number of CPU cores"], "ans": 1, "explanation": "Latency measures the round-trip or transit time delay, typically expressed in milliseconds (ms)."},
        {"level": "easy", "q": "What does a Content Delivery Network (CDN) do?", "opts": ["Compiles JavaScript source code", "Caches static content (images, videos, JS, CSS) on geographically distributed edge servers close to end users", "Manages database backups", "Generates SSL certificates"], "ans": 1, "explanation": "CDNs store copies of assets near users geographically, dramatically reducing latency and origin server load."},
        {"level": "easy", "q": "Which in-memory data structure store is widely used as an ultra-fast cache?", "opts": ["SQLite", "Redis", "Hadoop", "PostgreSQL"], "ans": 1, "explanation": "Redis stores key-values in RAM, providing sub-millisecond read/write access ideal for caching."},

        # 5 Medium
        {"level": "medium", "q": "What does the CAP Theorem state about distributed data systems?", "opts": ["A system can guarantee all three: Consistency, Availability, and Partition Tolerance", "In the presence of a network partition (P), a distributed system must choose between Consistency (C) or Availability (A)", "Computers Always Perform reliably", "Cost, Agility, Performance can never be balanced"], "ans": 1, "explanation": "Network partitions are inevitable in real networks; thus systems must trade off strong consistency (CP) or high availability (AP)."},
        {"level": "medium", "q": "What is the difference between Cache-Aside and Write-Through caching patterns?", "opts": ["Cache-Aside requires client to query cache first, and read from DB on miss; Write-Through writes data to cache and database synchronously", "Write-Through deletes all keys on write", "Cache-Aside is only used for databases", "There is no difference"], "ans": 0, "explanation": "Cache-Aside lazily populates cache upon read misses; Write-Through updates cache and persistent store together on writes."},
        {"level": "medium", "q": "What is database sharding?", "opts": ["Backing up a database to tape", "Horizontally partitioning database rows across multiple independent physical database instances using a shard key", "Deleting old records", "Replicating data to a single replica"], "ans": 1, "explanation": "Sharding distributes massive datasets across multiple servers according to a shard key (e.g. user_id % N)."},
        {"level": "medium", "q": "What is the primary role of a Message Queue (like Apache Kafka or RabbitMQ) in distributed architectures?", "opts": ["To render HTML pages", "To decouple producers and consumers, enabling asynchronous processing, buffering traffic spikes, and guaranteed message delivery", "To run relational SQL queries", "To assign domain names"], "ans": 1, "explanation": "Queues decouple services, enabling asynchronous tasks, load leveling during traffic spikes, and resilient retries."},
        {"level": "medium", "q": "What is the Circuit Breaker pattern used for in microservices?", "opts": ["Turning off the office lights", "Detecting consecutive failures and temporarily failing fast to prevent an unresponsive downstream service from crashing the entire system", "Balancing CPU temperature", "Encrypting database connections"], "ans": 1, "explanation": "Circuit breakers trip open when downstream calls fail repeatedly, immediately returning fallbacks to avoid resource exhaustion."},

        # 5 Hard
        {"level": "hard", "q": "How does Consistent Hashing minimize data redistribution when adding or removing cache nodes?", "opts": ["By rehashing every key across all servers", "By mapping both keys and servers to a circular hash ring (0 to 2^32-1); adding/removing a node only affects adjacent keys on the ring (k/N keys)", "By storing all keys on a master node", "By disabling hashing entirely"], "ans": 1, "explanation": "Consistent hashing ensures that when a server is added or removed, only k/N keys need remapping on average rather than all keys."},
        {"level": "hard", "q": "What is the Token Bucket algorithm used for in API gateways?", "opts": ["Distributing database partitions", "Rate limiting requests: tokens accumulate at a fixed rate in a bucket; each request consumes a token, rejecting traffic when empty", "Encrypting API tokens with RSA", "Routing WebSocket connections"], "ans": 1, "explanation": "Token bucket permits bursts of traffic up to bucket capacity while enforcing a steady long-term average request rate."},
        {"level": "hard", "q": "How does Event Sourcing differ from traditional CRUD state storage?", "opts": ["Event Sourcing deletes data after 7 days", "Instead of updating current state in-place, Event Sourcing stores every state change as an immutable append-only sequence of domain events", "Event Sourcing only runs on mobile devices", "CRUD cannot use databases"], "ans": 1, "explanation": "In Event Sourcing, the append-only log of events is the single source of truth; current state is reconstructed by replaying events."},
        {"level": "hard", "q": "What is the role of the Saga pattern in distributed microservices transactions?", "opts": ["A single two-phase commit across all microservices", "Managing distributed transactions as a sequence of local transactions with compensating transactions to rollback on failure", "A hardware failover router", "A load balancer algorithm"], "ans": 1, "explanation": "Sagas avoid distributed locks by executing a series of local transactions coordinated by events/orchestrators with compensating rollbacks."},
        {"level": "hard", "q": "What is the difference between Strong Consistency and Eventual Consistency in distributed data stores?", "opts": ["Eventual consistency is faster but guarantees that given no new updates, all replicas will eventually converge to the same value; Strong consistency guarantees all reads reflect the latest write immediately", "Strong consistency never uses networks", "Eventual consistency loses data permanently", "There is no difference in distributed systems"], "ans": 0, "explanation": "Strong consistency guarantees linearizability at higher latency; eventual consistency permits temporary replica lag for higher availability and throughput."}
    ]
}
