#!/usr/bin/env python3
"""
PDF Folder Watcher - Monitors a folder and auto-merges PDFs
Watches a specified folder for new PDF files and automatically merges them.
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime
from threading import Timer

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("Error: watchdog library not found!")
    print("Please install it with: pip install watchdog")
    input("Press Enter to exit...")
    sys.exit(1)

try:
    from pypdf import PdfWriter, PdfReader
except ImportError:
    print("Error: pypdf library not found!")
    print("Please install it with: pip install pypdf")
    input("Press Enter to exit...")
    sys.exit(1)


class PDFWatcher(FileSystemEventHandler):
    """Handles file system events for PDF files."""

    def __init__(self, watch_dir, merge_delay=3):
        """
        Initialize the PDF watcher.

        Args:
            watch_dir: Directory to watch for PDF files
            merge_delay: Seconds to wait after last PDF before merging (default: 3)
        """
        self.watch_dir = Path(watch_dir)
        self.merge_delay = merge_delay
        self.merge_timer = None
        self.pending_merge = False

    def on_created(self, event):
        """Called when a file is created."""
        if event.is_directory:
            return

        file_path = Path(event.src_path)
        if file_path.suffix.lower() == '.pdf':
            print(f"[{datetime.now().strftime('%H:%M:%S')}] New PDF detected: {file_path.name}")
            self.schedule_merge()

    def on_modified(self, event):
        """Called when a file is modified."""
        if event.is_directory:
            return

        file_path = Path(event.src_path)
        if file_path.suffix.lower() == '.pdf':
            # File might still be writing, schedule merge
            self.schedule_merge()

    def schedule_merge(self):
        """Schedule a merge operation after a delay."""
        # Cancel existing timer if any
        if self.merge_timer:
            self.merge_timer.cancel()

        # Schedule new merge
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Merge scheduled in {self.merge_delay} seconds...")
        self.merge_timer = Timer(self.merge_delay, self.merge_pdfs)
        self.merge_timer.start()

    def merge_pdfs(self):
        """Merge all PDF files in the watched directory."""
        try:
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Starting merge operation...")
            print("-" * 60)

            # Find all PDF files
            pdf_files = sorted([f for f in self.watch_dir.glob("*.pdf")])

            if len(pdf_files) < 2:
                print(f"Found {len(pdf_files)} PDF(s). Need at least 2 PDFs to merge.")
                print("Waiting for more PDFs...")
                print("-" * 60)
                return

            print(f"Found {len(pdf_files)} PDF files to merge:")
            for i, pdf in enumerate(pdf_files, 1):
                print(f"  {i}. {pdf.name}")

            # Create output filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"merged_output_{timestamp}.pdf"
            output_path = self.watch_dir / output_filename

            print(f"\nMerging into: {output_filename}")

            # Merge PDFs
            merger = PdfWriter()
            total_pages = 0

            for pdf_file in pdf_files:
                try:
                    print(f"  Adding: {pdf_file.name}...", end=" ")
                    reader = PdfReader(pdf_file)
                    pages = len(reader.pages)
                    for page in reader.pages:
                        merger.add_page(page)
                    total_pages += pages
                    print(f"({pages} pages)")
                except Exception as e:
                    print(f"ERROR: {e}")
                    continue

            # Write merged PDF
            with open(output_path, 'wb') as output_file:
                merger.write(output_file)

            print("-" * 60)
            print(f"✓ SUCCESS! Merged PDF created:")
            print(f"  File: {output_filename}")
            print(f"  Total pages: {total_pages}")
            print(f"  Location: {output_path}")
            print("-" * 60)

            # Create archive folder and move all PDFs
            archive_folder = self.watch_dir / f"merged_{timestamp}"
            archive_folder.mkdir(exist_ok=True)
            print(f"\nMoving all PDFs to archive folder: {archive_folder.name}")

            # Move all PDF files (including source PDFs and merged output)
            all_pdfs = list(self.watch_dir.glob("*.pdf"))
            for pdf_file in all_pdfs:
                try:
                    destination = archive_folder / pdf_file.name
                    pdf_file.rename(destination)
                    print(f"  Moved: {pdf_file.name}")
                except Exception as e:
                    print(f"  ERROR moving {pdf_file.name}: {e}")

            print("-" * 60)
            print(f"✓ All PDFs moved to: {archive_folder}")
            print(f"  Watch folder is now empty and ready for new PDFs")
            print("-" * 60)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Waiting for new PDFs...\n")

        except Exception as e:
            print(f"ERROR during merge: {e}")
            import traceback
            traceback.print_exc()
            print("-" * 60)


def main():
    """Main function to run the PDF watcher."""
    print("=" * 60)
    print("PDF Folder Watcher - Auto-Merge Tool")
    print("=" * 60)

    # Get the directory to watch
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        default_dir = Path(sys.executable).parent
    else:
        # Running as script
        default_dir = Path(__file__).parent

    print(f"\nDefault watch directory: {default_dir}")
    print("\nOptions:")
    print("  1. Watch current directory (where this program is located)")
    print("  2. Enter a custom directory path")

    while True:
        choice = input("\nEnter choice (1 or 2): ").strip()

        if choice == "1":
            watch_dir = default_dir
            break
        elif choice == "2":
            custom_path = input("Enter directory path to watch: ").strip()
            watch_dir = Path(custom_path)
            if not watch_dir.exists():
                print(f"ERROR: Directory does not exist: {watch_dir}")
                continue
            if not watch_dir.is_dir():
                print(f"ERROR: Path is not a directory: {watch_dir}")
                continue
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

    print(f"\n✓ Watching directory: {watch_dir}")
    print("\nSettings:")
    print("  - Auto-merge delay: 3 seconds after last PDF detected")
    print("  - Merged files will be named: merged_output_YYYYMMDD_HHMMSS.pdf")
    print("\nPress Ctrl+C to stop watching...\n")
    print("=" * 60)

    # Set up the watcher
    event_handler = PDFWatcher(watch_dir, merge_delay=3)
    observer = Observer()
    observer.schedule(event_handler, str(watch_dir), recursive=False)
    observer.start()

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Monitoring started. Waiting for PDF files...\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nStopping watcher...")
        observer.stop()
        observer.join()
        print("Watcher stopped. Goodbye!")


if __name__ == "__main__":
    main()
