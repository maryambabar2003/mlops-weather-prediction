# Team Member Assignments

## Quick Reference

### Member 1: Data Pipeline & Infrastructure
**Responsibility**: Data ingestion, orchestration, versioning

| Step | Task | Status |
|------|------|--------|
| 1 | OpenWeather API Setup | 👤 Member 1 |
| 2 | Apache Airflow Setup | 👤 Member 1 |
| 3 | DVC Setup | 👤 Member 1 |

**Git Branches**:
- Feature branch: `feature/member1-data-pipeline`
- Work on: Steps 1, 2, 3
- Create PR to: `dev` after Step 3

---

### Member 2: Model & Deployment
**Responsibility**: Model training, CI/CD, containerization, monitoring

| Step | Task | Status |
|------|------|--------|
| 4 | MLflow & Dagshub Integration | 👤 Member 2 |
| 5 | CI/CD Pipeline Setup | 👤 Member 2 |
| 6 | Docker Containerization | 👤 Member 2 |
| 7 | Prometheus & Grafana | 👤 Member 2 |

**Git Branches**:
- Feature branch: `feature/member2-model-deployment`
- Work on: Steps 4, 5, 6, 7
- Create PRs to: `dev` after each step (or batch)

---

## Workflow Timeline

### Week 1: Data Pipeline (Member 1)
- [ ] Member 1: Step 1 - API Setup
- [ ] Member 1: Step 2 - Airflow Setup
- [ ] Member 1: Step 3 - DVC Setup
- [ ] Member 1: Create PR to `dev`
- [ ] Member 2: Review PR, prepare for Step 4

### Week 2: Model & CI/CD (Member 2)
- [ ] Member 2: Step 4 - MLflow & Dagshub
- [ ] Member 2: Step 5 - CI/CD Setup
- [ ] Member 2: Create PRs to `dev`
- [ ] Member 1: Review PRs, help test

### Week 3: Deployment & Monitoring (Member 2)
- [ ] Member 2: Step 6 - Docker
- [ ] Member 2: Step 7 - Monitoring
- [ ] Member 2: Create final PRs
- [ ] Both: Test integration

### Week 4: Final Integration (Both)
- [ ] Both: End-to-end testing
- [ ] Both: Documentation review
- [ ] Both: Merge to `test` → `master`
- [ ] Both: Prepare presentation

---

## Communication Checklist

### After Each Step:
- [ ] Commit with descriptive message
- [ ] Push to feature branch
- [ ] Notify team member
- [ ] Take screenshots
- [ ] Update progress

### Before Creating PR:
- [ ] All code committed
- [ ] Screenshots captured
- [ ] Documentation updated
- [ ] No sensitive data in code
- [ ] Tested locally

### During PR Review:
- [ ] Review code quality
- [ ] Check screenshots
- [ ] Verify functionality
- [ ] Approve or request changes
- [ ] Merge after approval

---

## Handoff Points

### Handoff 1: Member 1 → Member 2 (After Step 3)
**Member 1 delivers**:
- [ ] Working data extraction
- [ ] Airflow DAG functional
- [ ] DVC configured
- [ ] PR created and ready

**Member 2 receives**:
- [ ] Pull latest `dev` branch
- [ ] Verify data pipeline works
- [ ] Begin Step 4

### Handoff 2: Final Integration (After Step 7)
**Both members**:
- [ ] Review all code
- [ ] Test complete pipeline
- [ ] Verify all components
- [ ] Final merge to master

---

## Git Commands Reference

### Member 1 Workflow:
```bash
# Start working
git checkout dev
git pull origin dev
git checkout -b feature/member1-data-pipeline

# After completing steps
git add .
git commit -m "feat: Step X - [description] - Member 1"
git push origin feature/member1-data-pipeline

# Create PR on GitHub: feature/member1-data-pipeline → dev
```

### Member 2 Workflow:
```bash
# After Member 1's PR is merged
git checkout dev
git pull origin dev
git checkout -b feature/member2-model-deployment

# After completing steps
git add .
git commit -m "feat: Step X - [description] - Member 2"
git push origin feature/member2-model-deployment

# Create PR on GitHub: feature/member2-model-deployment → dev
```

---

## Progress Tracking

Update this file as you complete steps:

### Member 1 Progress:
- [ ] Step 1: API Setup
- [ ] Step 2: Airflow Setup
- [ ] Step 3: DVC Setup
- [ ] PR Created
- [ ] PR Merged

### Member 2 Progress:
- [ ] Step 4: MLflow & Dagshub
- [ ] Step 5: CI/CD
- [ ] Step 6: Docker
- [ ] Step 7: Monitoring
- [ ] All PRs Merged

### Final Integration:
- [ ] End-to-end test passed
- [ ] All screenshots captured
- [ ] Documentation complete
- [ ] Merged to master

