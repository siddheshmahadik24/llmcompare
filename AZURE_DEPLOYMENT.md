# Azure Deployment Guide

This guide will help you deploy the LLM Comparison Tool to Azure App Service.

## Prerequisites

- Azure account (free account available: https://azure.microsoft.com/free/)
- Azure CLI installed: https://docs.microsoft.com/cli/azure/install-azure-cli
- Git installed
- Your GitHub repository cloned locally

## Deployment Steps

### Step 1: Create Azure Resources

```bash
# Login to Azure
az login

# Create a resource group
az group create --name llmcompare-rg --location eastus

# Create an App Service plan (Free tier)
az appservice plan create \
  --name llmcompare-plan \
  --resource-group llmcompare-rg \
  --sku F1 \
  --is-linux

# Create the web app
az webapp create \
  --resource-group llmcompare-rg \
  --plan llmcompare-plan \
  --name llmcompare-app \
  --runtime "python|3.11"
```

### Step 2: Configure Environment Variables

```bash
az webapp config appsettings set \
  --resource-group llmcompare-rg \
  --name llmcompare-app \
  --settings \
    OPENAI_API_KEY="your_openai_key" \
    ANTHROPIC_API_KEY="your_anthropic_key" \
    GOOGLE_API_KEY="your_google_key"
```

### Step 3: Enable GitHub Actions Deployment

Option A: Using Azure Portal (Easiest)
1. Go to Azure Portal → App Services → llmcompare-app
2. Click "Deployment Center" in the left sidebar
3. Select "GitHub" as source
4. Authorize and select your repository
5. Select branch: `master`
6. Azure will automatically create a GitHub Actions workflow

Option B: Using Azure CLI

```bash
az webapp deployment github-actions add \
  --repo-url https://github.com/siddheshmahadik24/llmcompare \
  --resource-group llmcompare-rg \
  --name llmcompare-app \
  --branch master
```

### Step 4: Deploy

Once GitHub Actions is configured:
- Push code to GitHub
- GitHub Actions will automatically build and deploy to Azure
- Check deployment status in "Deployment Center" in Azure Portal

## Manual Deployment (Alternative)

If you prefer to deploy manually:

```bash
# Build the app
python -m pip install -r requirements.txt

# Test locally
python llm_comparison_app.py

# Deploy using Azure CLI
az webapp up \
  --resource-group llmcompare-rg \
  --plan llmcompare-plan \
  --name llmcompare-app \
  --runtime "python:3.11" \
  --sku F1
```

## Accessing Your App

After deployment, your app will be available at:
```
https://llmcompare-app.azurewebsites.net
```

(Replace `llmcompare-app` with your actual app name)

## Monitoring and Logs

View logs in Azure Portal:
1. Go to App Services → llmcompare-app
2. Click "Logs" in the sidebar
3. Or use Azure CLI:

```bash
az webapp log tail \
  --resource-group llmcompare-rg \
  --name llmcompare-app
```

## Troubleshooting

### App won't start
- Check Azure logs for errors
- Verify all required packages are in requirements.txt
- Ensure environment variables are set correctly

### Connection issues
- Check that API keys are valid
- Verify firewall rules allow outbound connections to API providers

### Slow response time
- Free tier has limited resources
- Consider upgrading to B1 tier for better performance

## Cost

- **Free tier (F1)**: 60 minutes/day (good for testing)
- **Basic tier (B1)**: ~$10/month (recommended for production)
- **Standard tier and above**: Better performance and reliability

## Scaling

To upgrade your plan:

```bash
az appservice plan update \
  --name llmcompare-plan \
  --resource-group llmcompare-rg \
  --sku B1
```

## Custom Domain

To use a custom domain:
1. Go to Azure Portal → App Services → llmcompare-app
2. Click "Custom domains" in the sidebar
3. Follow the instructions to add and verify your domain

## Support

For issues with Azure deployment:
- Azure Documentation: https://docs.microsoft.com/azure/app-service/
- GitHub Actions: https://docs.github.com/actions

For issues with the app itself:
- Check GitHub repository issues
- Review server logs in Azure Portal
