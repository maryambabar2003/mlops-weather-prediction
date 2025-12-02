# MLOps Real-Time Predictive System - Step-by-Step Guide

## Project Overview

**Domain**: Environmental (OpenWeather API)  
**Predictive Task**: Predict temperature 4-6 hours ahead for New York City  
**Target Variable**: Temperature (°C)  
**Prediction Horizon**: 6 hours ahead

## 👥 Team Collaboration

**IMPORTANT**: This project is divided between two team members. See **[COLLABORATION_GUIDE.md](COLLABORATION_GUIDE.md)** for detailed workflow.

### Member Assignments

- **Member 1**: Steps 1, 2, 3 (Data Pipeline & Infrastructure)
- **Member 2**: Steps 4, 5, 6, 7 (Model & Deployment)

## Step-by-Step Implementation Guides

Follow these guides in order, taking screenshots at each step:

1. **[STEP_1_API_SETUP.md](STEP_1_API_SETUP.md)** - OpenWeather API Configuration 👤 Member 1
2. **[STEP_2_AIRFLOW.md](STEP_2_AIRFLOW.md)** - Apache Airflow Setup and DAG Creation 👤 Member 1
3. **[STEP_3_DVC.md](STEP_3_DVC.md)** - Data Version Control Setup 👤 Member 1
4. **[STEP_4_MLFLOW_DAGSHUB.md](STEP_4_MLFLOW_DAGSHUB.md)** - MLflow and Dagshub Integration 👤 Member 2
5. **[STEP_5_CICD.md](STEP_5_CICD.md)** - CI/CD Pipeline Setup 👤 Member 2
6. **[STEP_6_DOCKER.md](STEP_6_DOCKER.md)** - Docker Containerization 👤 Member 2
7. **[STEP_7_MONITORING.md](STEP_7_MONITORING.md)** - Prometheus and Grafana Setup 👤 Member 2

## Important Notes

- **👥 Two-member team**: See [COLLABORATION_GUIDE.md](COLLABORATION_GUIDE.md) and [MEMBER_ASSIGNMENTS.md](MEMBER_ASSIGNMENTS.md)
- **Take screenshots** at each major step
- **Document issues** in a separate issues log
- **Make Git commits** after completing each step
- **Create PRs** for peer review before merging
- **Test each component** before moving to the next step

## Project Structure

You will create this structure as you progress:

```
MLOPsProject/
├── airflow/
│   ├── dags/
│   └── logs/
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── data/
│   ├── models/
│   └── api/
├── config/
├── tests/
├── docker/
├── .github/workflows/
├── models/
└── docs/
```

## Getting Started

1. **Read first**: [COLLABORATION_GUIDE.md](COLLABORATION_GUIDE.md) - Understand the team workflow
2. **Check assignments**: [MEMBER_ASSIGNMENTS.md](MEMBER_ASSIGNMENTS.md) - See who does what
3. **Member 1**: Start with [STEP_1_API_SETUP.md](STEP_1_API_SETUP.md)
4. **Member 2**: Review Member 1's work and prepare for your steps

## Git Workflow Summary

```
feature/member1-data-pipeline (Member 1)
    ↓ PR
dev branch
    ↓ PR (after review)
test branch
    ↓ PR (after review)
master branch (production)
```
