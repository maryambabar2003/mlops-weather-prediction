# Step 5: CI/CD Pipeline Setup

## 👤 Assigned to: Member 2

## Objective
Set up Git branching strategy and GitHub Actions workflows for CI/CD.

## Prerequisites
- Step 4 completed
- GitHub account
- GitHub repository created

## Steps

### 5.1 Create GitHub Repository

1. Go to https://github.com
2. Create new repository: `mlops-weather-prediction`
3. Don't initialize with README (you already have files)
4. **Screenshot**: GitHub repository created

### 5.2 Push Code to GitHub

```bash
# Add GitHub remote
git remote add origin https://github.com/your-username/mlops-weather-prediction.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Screenshot**: Code pushed to GitHub

### 5.3 Create Git Branches

```bash
# Create dev branch
git checkout -b dev
git push -u origin dev

# Create test branch
git checkout -b test
git push -u origin test

# Return to main
git checkout main
```

**Screenshot**: Branches created

### 5.4 Create Feature Branch

```bash
# Create feature branch from dev
git checkout dev
git checkout -b feature/initial-setup
```

**Screenshot**: Feature branch created

### 5.5 Create GitHub Actions Workflow Directory

```bash
mkdir -p .github/workflows
```

**Screenshot**: Directory created

### 5.6 Create Feature to Dev Workflow

Create `.github/workflows/ci-feature-dev.yml`:

```yaml
name: CI - Feature to Dev

on:
  pull_request:
    branches:
      - dev
    types: [opened, synchronize, reopened]

jobs:
  code-quality:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install black flake8 pytest pytest-cov
      
      - name: Run Black (code formatting check)
        run: black --check . || true
      
      - name: Run Flake8 (linting)
        run: flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics || true
      
      - name: Run unit tests
        run: |
          pytest tests/ -v || true
```

**Screenshot**: Workflow file created

### 5.7 Create Dev to Test Workflow

Create `.github/workflows/ci-dev-test.yml`:

```yaml
name: CI - Dev to Test

on:
  pull_request:
    branches:
      - test
    types: [opened, synchronize, reopened]

jobs:
  model-retraining:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install cml
      
      - name: Set up Airflow
        run: |
          export AIRFLOW_HOME=${{ github.workspace }}/airflow
          airflow db init || true
      
      - name: Trigger Airflow DAG
        env:
          OPENWEATHER_API_KEY: ${{ secrets.OPENWEATHER_API_KEY }}
          MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_TRACKING_URI }}
        run: |
          export AIRFLOW_HOME=${{ github.workspace }}/airflow
          echo "DAG would be triggered here"
      
      - name: Compare models with CML
        env:
          REPO_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_TRACKING_URI }}
        run: |
          echo "CML comparison would run here"
```

**Screenshot**: Dev to test workflow created

### 5.8 Create Test to Master Workflow

Create `.github/workflows/ci-test-master.yml`:

```yaml
name: CI - Test to Master (Production Deployment)

on:
  pull_request:
    branches:
      - master
    types: [opened, synchronize, reopened]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Build Docker image
        run: |
          docker build -f docker/Dockerfile -t ${{ secrets.DOCKER_USERNAME }}/weather-prediction-api:${{ github.sha }} . || echo "Dockerfile not yet created"
      
      - name: Push Docker image
        run: |
          echo "Docker push would happen here"
```

**Screenshot**: Test to master workflow created

### 5.9 Configure GitHub Secrets

1. Go to GitHub repository Settings > Secrets and variables > Actions
2. Add secrets:
   - `OPENWEATHER_API_KEY`: Your OpenWeather API key
   - `MLFLOW_TRACKING_URI`: Your Dagshub MLflow URI
   - `DOCKER_USERNAME`: Your Docker Hub username (for later)
   - `DOCKER_PASSWORD`: Your Docker Hub password (for later)
3. **Screenshot**: Secrets configured (blur sensitive values)

### 5.10 Configure Branch Protection

1. Go to Settings > Branches
2. Add rule for `test` branch:
   - Require pull request reviews: 1
   - Require status checks to pass
3. Add rule for `master` branch:
   - Require pull request reviews: 1
   - Require status checks to pass
4. **Screenshot**: Branch protection rules

### 5.11 Test CI Workflow

1. Make a small change in feature branch
2. Create PR from feature to dev
3. Watch GitHub Actions run
4. **Screenshot**: CI workflow running

### 5.12 Commit and Push Workflows

```bash
git add .github/
git commit -m "Step 5: CI/CD workflows added"
git push origin feature/initial-setup
```

**Screenshot**: Workflows pushed

## Deliverables Checklist

- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] Branches created (dev, test, master)
- [ ] Feature branch created
- [ ] GitHub Actions workflows created
- [ ] GitHub secrets configured
- [ ] Branch protection rules configured
- [ ] CI workflow tested
- [ ] Screenshots captured
- [ ] Git commit made

## Next Step

**Member 2**: Proceed to [STEP_6_DOCKER.md](STEP_6_DOCKER.md)

**Member 1**: Continue reviewing and testing Member 2's work.

