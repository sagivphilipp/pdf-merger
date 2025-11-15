#!/usr/bin/env python3
"""
PDF Merger - Double-click executable to merge PDF files
Merges all PDF files in the same directory into one output file.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

try:
    from pypdf import PdfWriter, PdfReader
except ImportError:
    print("Error: pypdf library not found!")
    input("Press Enter to exit...")
    sys.exit(1)


def merge_pdfs():
    """Merge all PDF files in the current directory."""
    try:
        # Get the directory where the executable/script is located
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            current_dir = Path(sys.executable).parent
        else:
            # Running as script
            current_dir = Path(__file__).parent

        print(f"Looking for PDF files in: {current_dir}")
        print("-" * 50)

        # Find all PDF files in the directory
        pdf_files = sorted([f for f in current_dir.glob("*.pdf")])

        if len(pdf_files) < 2:
            print(f"Error: Found only {len(pdf_files)} PDF file(s).")
            print("Need at least 2 PDF files to merge.")
            input("\nPress Enter to exit...")
            return

        print(f"Found {len(pdf_files)} PDF files:")
        for i, pdf in enumerate(pdf_files, 1):
            print(f"  {i}. {pdf.name}")

        # Create output filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"merged_output_{timestamp}.pdf"
        output_path = current_dir / output_filename

        print(f"\nMerging PDFs into: {output_filename}")
        print("-" * 50)

        # Merge PDFs
        merger = PdfWriter()

        for pdf_file in pdf_files:
            print(f"Adding: {pdf_file.name}")
            try:
                reader = PdfReader(pdf_file)
                for page in reader.pages:
                    merger.add_page(page)
            except Exception as e:
                print(f"  Warning: Error reading {pdf_file.name}: {e}")
                continue

        # Write the merged PDF
        with open(output_path, 'wb') as output_file:
            merger.write(output_file)

        print("-" * 50)
        print(f"✓ Success! Merged PDF saved as: {output_filename}")
        print(f"  Total pages: {len(merger.pages)}")

    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()

    finally:
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    merge_pdfs()
