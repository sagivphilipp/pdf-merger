#!/bin/bash

# Build script for creating Windows executable from Mac using Docker

set -e

echo "=================================="
echo "PDF Merger - Windows Build Script"
echo "=================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed!"
    echo "Please install Docker Desktop from https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "Error: Docker is not running!"
    echo "Please start Docker Desktop and try again."
    exit 1
fi

echo "Step 1: Building Docker image..."
docker build -f Dockerfile.windows -t pdf-merger-builder .

echo ""
echo "Step 2: Creating container and extracting executable..."
docker create --name pdf-merger-temp pdf-merger-builder

echo ""
echo "Step 3: Copying executable..."
docker cp pdf-merger-temp:/app/dist/PDFMerger.exe ./PDFMerger.exe

echo ""
echo "Step 4: Cleaning up..."
docker rm pdf-merger-temp

echo ""
echo "=================================="
echo "✓ Build Complete!"
echo "=================================="
echo ""
echo "The Windows executable is ready: PDFMerger.exe"
echo ""
echo "Next steps:"
echo "1. Transfer PDFMerger.exe to your Windows machine"
echo "2. Place it in a folder with PDF files"
echo "3. Double-click to merge PDFs"
echo ""
