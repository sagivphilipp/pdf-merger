# Building Windows Executable from Mac

This guide explains how to build a Windows executable (.exe) from your Mac.

## Overview

The PDF Merger app will:
- Merge all PDF files in the same folder where the .exe is placed
- Create a merged output file with timestamp
- Can be run by simply double-clicking the .exe file

## Prerequisites

You need Docker installed on your Mac to cross-compile for Windows:
```bash
# Install Docker Desktop for Mac from https://www.docker.com/products/docker-desktop
# Or install via Homebrew:
brew install --cask docker
```

## Method 1: Build Using Docker (Recommended)

This method uses a Windows container to build the executable:

### Step 1: Create a Dockerfile

Create a file named `Dockerfile.windows` in the project directory:

```dockerfile
FROM python:3.11-windowsservercore

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY pdf_merger.py .
COPY pdf_merger.spec .

RUN pyinstaller --clean -y pdf_merger.spec

CMD ["cmd"]
```

### Step 2: Build the Windows executable

Run these commands from the terminal:

```bash
# Build the Docker image
docker build -f Dockerfile.windows -t pdf-merger-builder .

# Create a container and copy the built executable
docker create --name pdf-merger-temp pdf-merger-builder
docker cp pdf-merger-temp:/app/dist/PDFMerger.exe ./PDFMerger.exe
docker rm pdf-merger-temp
```

### Step 3: Transfer to Windows

The `PDFMerger.exe` file will be in your current directory. Transfer it to your Windows machine using:
- USB drive
- Cloud storage (Dropbox, Google Drive, etc.)
- Email
- Network share

## Method 2: Build Using Wine (Alternative)

If you have Wine installed, you can try building directly on Mac:

```bash
# Install Wine via Homebrew
brew install --cask wine-stable

# Install Python dependencies
pip install -r requirements.txt

# Build with PyInstaller for Windows
pyinstaller --clean -y --target-architecture=x86_64 --onefile --console pdf_merger.py --name PDFMerger
```

**Note:** This method is less reliable and may not always work.

## Method 3: Use a Windows VM or Machine

If you have access to a Windows machine or VM:

1. Transfer the project files to Windows
2. Install Python 3.11+ from https://www.python.org/downloads/
3. Open Command Prompt or PowerShell in the project directory
4. Run:
```bash
pip install -r requirements.txt
pyinstaller --clean -y pdf_merger.spec
```
5. Find the executable in `dist/PDFMerger.exe`

## Usage on Windows

Once you have the `PDFMerger.exe`:

1. Copy `PDFMerger.exe` to any folder containing PDF files
2. Double-click `PDFMerger.exe`
3. A console window will open showing the merge progress
4. The merged PDF will be saved as `merged_output_YYYYMMDD_HHMMSS.pdf`
5. Press Enter to close the window

## Troubleshooting

### "Windows Defender" or "SmartScreen" Warning
- This is normal for unsigned executables
- Click "More info" → "Run anyway"

### "Python not found" error
- The executable should be standalone and not require Python
- Try rebuilding with the `--onefile` flag

### Missing DLL errors
- Rebuild using Docker method (Method 1) which includes all dependencies

### PDFs not merging correctly
- Ensure PDF files are not corrupted
- Check that you have at least 2 PDF files in the folder
- Check the console output for specific error messages
