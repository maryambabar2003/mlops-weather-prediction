# Collaboration Guide - Two Member Team

## Team Member Assignment

### Member 1: Data Pipeline & Infrastructure
- **Focus**: Data ingestion, Airflow orchestration, data versioning
- **Steps**: 1, 2, 3

### Member 2: Model & Deployment
- **Focus**: Model training, CI/CD, containerization, monitoring
- **Steps**: 4, 5, 6, 7

## Git Workflow for Collaboration

### Initial Setup (Both Members)

1. **Member 1** creates the repository and initial structure:
   ```bash
   git init
   git checkout -b dev
   git checkout -b test
   git checkout -b master
   git checkout dev
   ```

2. **Both members** clone and set up:
   ```bash
   git clone <repository-url>
   cd MLOpsProject
   git checkout dev
   ```

### Working Process

1. **Create feature branches from dev**:
   - Member 1: `git checkout -b feature/member1-data-pipeline`
   - Member 2: `git checkout -b feature/member2-model-deployment`

2. **Work independently** on assigned steps

3. **Commit frequently**:
   ```bash
   git add .
   git commit -m "feat: [step description] - Member [1/2]"
   ```

4. **Push to feature branch**:
   ```bash
   git push origin feature/member1-data-pipeline
   ```

5. **Create Pull Request** from feature branch to `dev`

6. **Review and merge** (peer review)

7. **Continue to next step**

## Step-by-Step Collaboration

### Phase 1: Parallel Work (Steps 1-3)

**Member 1** works on:
- Step 1: API Setup
- Step 2: Airflow Setup
- Step 3: DVC Setup

**Member 2** can prepare:
- Review Member 1's PRs
- Set up Dagshub account
- Prepare for Step 4

### Phase 2: Sequential Work (Steps 4-7)

**Member 2** works on:
- Step 4: MLflow & Dagshub (needs Member 1's data pipeline)
- Step 5: CI/CD
- Step 6: Docker
- Step 7: Monitoring

**Member 1** can:
- Review Member 2's PRs
- Help test deployments
- Document issues

## Communication Points

### Handoff from Member 1 to Member 2

After Step 3, Member 1 should:
- [ ] Complete DVC setup
- [ ] Ensure data pipeline works
- [ ] Create PR to dev
- [ ] Notify Member 2 that data pipeline is ready

Member 2 should:
- [ ] Review Member 1's PR
- [ ] Merge to dev
- [ ] Pull latest dev branch
- [ ] Begin Step 4

### Integration Points

- **Step 4**: Member 2 needs Member 1's DAG and data structure
- **Step 5**: Member 2 needs both members' code for CI/CD
- **Step 6**: Member 2 needs Member 1's API structure (if applicable)
- **Step 7**: Member 2 monitors everything both built

## PR Review Checklist

When reviewing a PR, check:
- [ ] Code follows project structure
- [ ] Commits are descriptive
- [ ] Screenshots are included (if applicable)
- [ ] Documentation is updated
- [ ] No sensitive data (API keys, passwords) in code
- [ ] Tests pass (if applicable)

## Conflict Resolution

If conflicts occur:
1. Communicate via issues/comments
2. Member 1 has final say on data pipeline decisions
3. Member 2 has final say on deployment decisions
4. Both agree on architecture decisions

## Final Integration

Before final submission:
1. Both members review all code
2. Test complete pipeline end-to-end
3. Verify all screenshots captured
4. Ensure all documentation complete
5. Final merge to master

## Time Allocation Suggestion

- **Week 1**: Member 1 completes Steps 1-3, Member 2 reviews and prepares
- **Week 2**: Member 2 completes Steps 4-5, Member 1 reviews
- **Week 3**: Member 2 completes Steps 6-7, both test integration
- **Week 4**: Final testing, documentation, presentation prep

