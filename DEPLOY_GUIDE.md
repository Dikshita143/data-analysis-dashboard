# Deployment Guide - Sales, Employee & Customer Data Analysis

A complete step-by-step guide to deploy this project on **Streamlit Cloud** (free hosting).

---

## Prerequisites

Before deploying, make sure you have:

1. A **GitHub account** — [Sign up here](https://github.com/join) if you do not have one.
2. A **Streamlit Cloud account** — [Sign up here](https://share.streamlit.io) (free, uses your GitHub login).
3. **Git installed** on your computer — [Download Git](https://git-scm.com/downloads).

---

## Step 1: Create a GitHub Repository

1. Go to [github.com/new](https://github.com/new).
2. Enter a **Repository name**, for example: `data-analysis-dashboard`.
3. Set it to **Public** (required for free Streamlit Cloud hosting).
4. Do **NOT** check "Add a README" (we already have one).
5. Click **Create repository**.
6. Copy the repository URL (it will look like `https://github.com/yourusername/data-analysis-dashboard.git`).

---

## Step 2: Push Your Project to GitHub

Open **Terminal / Command Prompt** and run these commands one by one:

```bash
# Navigate to your project folder
cd "F:\New folder"

# Initialize Git
git init

# Add all files
git add .

# Create your first commit
git commit -m "Initial commit - Sales Employee Customer Data Analysis"

# Connect to your GitHub repository (replace with YOUR URL)
git remote add origin https://github.com/yourusername/data-analysis-dashboard.git

# Push the code
git branch -M main
git push -u origin main
```

After this, refresh your GitHub page — you should see all your project files there.

---

## Step 3: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io).
2. Click **"New app"** button (top right).
3. Fill in the form:
   - **Repository**: Select your `data-analysis-dashboard` repo.
   - **Branch**: `main`
   - **Main file path**: `app.py`
4. Click **"Deploy!"**

Streamlit Cloud will now:
- Install all packages from `requirements.txt`
- Launch your `app.py`
- Give you a **public URL** like `https://yourusername-data-analysis-dashboard.streamlit.app`

This process takes about **2-3 minutes** for the first deployment.

---

## Step 4: Verify Your Deployment

1. Open the public URL provided by Streamlit Cloud.
2. You should see the landing page with "Sales, Employee & Customer Data Analysis".
3. Try uploading a CSV file to make sure everything works.
4. Test the Data Assistant in the sidebar.
5. Check that all 4 steps load correctly (Explorer, Insights, Visuals, Predictions).

---

## Updating Your Deployed App

Whenever you make changes to your code locally, just push to GitHub and Streamlit will **auto-update**:

```bash
git add .
git commit -m "Updated dashboard"
git push
```

The live app will refresh within 1-2 minutes automatically.

---

## Project Files Required for Deployment

Make sure these files are in your GitHub repository:

| File | Purpose |
|------|---------|
| `app.py` | Main application code |
| `requirements.txt` | Python package list |
| `.streamlit/config.toml` | Theme and server settings |
| `utils/style.css` | Custom CSS styling |
| `README.md` | Project documentation |

---

## Troubleshooting

### "ModuleNotFoundError" on Streamlit Cloud
Make sure all packages are listed in `requirements.txt`. Currently required:
```
streamlit
pandas
numpy
plotly
scikit-learn
```

### App crashes on upload
Check that your CSV file is well-formatted (has headers, no corrupt rows).

### Theme does not apply
Ensure `.streamlit/config.toml` is pushed to GitHub. Streamlit Cloud reads this file for theme settings.

### App is slow
Large CSV files (50MB+) may take longer to process. Consider filtering your data before uploading.

---

## Sharing Your App

Once deployed, share your app URL with anyone:

```
https://yourusername-data-analysis-dashboard.streamlit.app
```

No installation needed — it runs directly in the browser on any device.

---

Made by **Dikshita** | Built with Streamlit & Python
