# Building Windows Executable with GitHub Actions

I've set up an automated build system using GitHub Actions! Here's how it works:

## How It Works

1. You push code to GitHub (to `main` or `dev` branch)
2. GitHub automatically builds the Windows .exe in the cloud
3. You download the ready-to-use executable

## Setup Steps

### 1. Push to GitHub

If you haven't already, push your code:

```bash
git add .
git commit -m "Add PDF merger with GitHub Actions build"
git push origin dev
```

### 2. Check Build Status

1. Go to your GitHub repository
2. Click on the **"Actions"** tab at the top
3. You'll see a workflow running called "Build Windows Executable"
4. Wait for it to complete (usually takes 2-3 minutes)

### 3. Download the Executable

Once the build is complete:

1. Click on the completed workflow run
2. Scroll down to the **"Artifacts"** section
3. Click on **"PDFMerger-Windows"** to download
4. Extract the ZIP file to get `PDFMerger.exe`

## Manual Build

You can also trigger a build manually:

1. Go to the **Actions** tab on GitHub
2. Click on "Build Windows Executable" workflow
3. Click **"Run workflow"** button
4. Select the branch and click "Run workflow"

## What Gets Built

The workflow automatically builds when you change:
- `pdf_merger.py`
- `requirements.txt`
- `pdf_merger.spec`
- The workflow file itself

## Artifact Retention

- Built executables are kept for **90 days**
- After that, you can always rebuild by re-running the workflow

## Testing the Executable

Once you download `PDFMerger.exe`:

1. Copy it to a folder with some PDF files
2. Double-click to run
3. All PDFs in that folder will be merged into one file

## Troubleshooting

### Build Fails
- Check the workflow logs in the Actions tab
- Make sure all files are committed and pushed

### Can't Find Artifacts
- Wait for the green checkmark (build complete)
- Artifacts appear at the bottom of the workflow run page

### Need to Rebuild
- Just push a new commit, or
- Use "Run workflow" button in Actions tab

---

**You're all set!** Just push your code and GitHub will build the Windows executable automatically.
