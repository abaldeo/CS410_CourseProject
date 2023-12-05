# Continuous Integration/Continuous Deployment (CI/CD) Pipeline with GitHub Actions, GCP, Artifact Registry, and Cloud Run

This repository contains a CI/CD pipeline setup using GitHub Actions to build, push Docker containers to Google Artifact Registry, and deploy them as a containerized application on Google Cloud Run upon merging changes into the `main` branch.

## Workflow Overview

The CI/CD workflow performs the following steps:

1. **Authentication Setup**
   - Authenticates to Google Cloud Platform.
   - Authenticates Docker to Google Artifact Registry.

2. **Docker Container Build and Push**
   - Builds a Docker container.
   - Publishes the container to Google Artifact Registry.

3. **Deployment to Cloud Run**
   - Deploys the containerized application using container image published in previous step.

## Prerequisites

If you want to replicate, before using this workflow, ensure the following prerequisites are met:

- **Google Cloud APIs enabled**:
  - Cloud Run (`run.googleapis.com`)
  - Artifact Registry (`artifactregistry.googleapis.com`)

- **IAM Permissions**
  - Cloud Run: `roles/run.admin`, `roles/iam.serviceAccountUser`
  - Artifact Registry: `roles/artifactregistry.admin` (project or repository level)

- **GitHub Secrets**
  - `WIF_PROVIDER` and `WIF_SERVICE_ACCOUNT` for Workload Identity Federation.

- **Environment Variables**
  - `PROJECT_ID`: Google Cloud project ID.
  - `GAR_LOCATION`: Artifact Registry location.
  - `SERVICE`: Cloud Run service name.
  - `REGION`: Cloud Run service region.

## Workflow Configuration

The workflow is triggered on `push` events to the `main` branch. It consists of a single job called `deploy`. This is the minimum needed for this CI/CD workflow. If your needs exceed this pipeline, additional jobs can be run in concert. 

### Steps Overview

- **Checkout**: Retrieves the codebase using `actions/checkout`.

- **Google Auth**: Authenticates to Google Cloud using the specified Workload Identity Federation details.

- **Docker Auth and Build**:
  - Authenticates Docker to Google Artifact Registry.
  - Builds the Docker container and pushes it to Artifact Registry.

- **Deploy to Cloud Run**: Deploys the containerized application to Cloud Run.

## Usage

To use this workflow:

1. Ensure all prerequisites are met.
2. Modify the required environment variables in the workflow YAML file (`google-cloudrun-docker.yml`) to match your project's configurations.
3. Create necessary GitHub secrets for authentication and replace placeholders in the workflow with actual values.
4. Commit and push changes to the `main` branch to trigger the CI/CD pipeline. This can be altered to run the job(s) on any push or merge event, on any branch. 

For more detailed support and information, refer to the [GitHub Actions Marketplace - Deploy to Cloud Run](https://github.com/marketplace/actions/deploy-to-cloud-run) or the provided links in the YAML file for IAM permissions and best practices.

## Author

- [Colton Bailey](https://github.com/Coltinho10)