# PDF Merger & Watcher Tools

Windows executables for merging PDF files - includes both a manual merger and an automatic folder watcher.

## 🔧 Tools Included

### 1. PDFMerger.exe - Manual Merge
Double-click to merge all PDFs in the current folder.

**Usage:**
1. Place `PDFMerger.exe` in a folder with PDF files
2. Double-click the executable
3. All PDFs are merged into `merged_output_YYYYMMDD_HHMMSS.pdf`

**Features:**
- Merges PDFs in alphabetical order
- Creates timestamped output files
- Shows progress in console
- No Python installation required

---

### 2. PDFWatcher.exe - Auto-Merge
Monitors a folder and automatically merges PDFs when new files are added.

**Usage:**
1. Run `PDFWatcher.exe`
2. Choose to watch:
   - Current directory (where the .exe is), or
   - A custom directory path
3. The program runs continuously, watching for new PDFs
4. When new PDFs are detected, waits 3 seconds then auto-merges
5. Press Ctrl+C to stop watching

**Features:**
- Real-time folder monitoring
- Automatic merge on new PDF detection
- 3-second delay to handle multiple files being added
- **Auto-archives**: Moves all PDFs to timestamped subfolder after merge
- **Prevents recursive merging**: Watch folder stays clean and ready for new PDFs
- Timestamped output files and archive folders
- Console shows live status updates

---

## 📥 Download

Get the latest executables from [GitHub Actions Artifacts](../../actions):

- **PDFMerger-Windows.zip** - Manual merge tool
- **PDFWatcher-Windows.zip** - Auto-watch and merge tool

## 🚀 Quick Start

### Manual Merge Example
```
C:\Documents\
  ├── PDFMerger.exe
  ├── chapter1.pdf
  ├── chapter2.pdf
  └── chapter3.pdf
```

Double-click `PDFMerger.exe` → Creates `merged_output_20251115_143022.pdf`

### Auto-Watch Example
```
C:\Inbox\
  └── PDFWatcher.exe
```

1. Run `PDFWatcher.exe`
2. Select option 1 (watch current directory)
3. Copy `file1.pdf` and `file2.pdf` into C:\Inbox\
4. Watcher auto-merges after 3 seconds
5. **All PDFs moved** to `C:\Inbox\merged_20251115_143022\`
6. C:\Inbox\ is now empty and ready for new PDFs!
7. Repeat as needed - keeps watching!

**Result:**
```
C:\Inbox\
  ├── PDFWatcher.exe
  └── merged_20251115_143022\
      ├── file1.pdf (original)
      ├── file2.pdf (original)
      └── merged_output_20251115_143022.pdf (merged result)
```

---

## 🛠️ Building from Source

Both executables are automatically built via GitHub Actions when you push changes.

### Manual Build (on Windows)
```bash
# Install dependencies
pip install -r requirements.txt

# Build manual merger
pyinstaller --clean -y pdf_merger.spec

# Build watcher
pyinstaller --clean -y pdf_watcher.spec
```

Find executables in `dist/` folder.

---

## ⚙️ Requirements

**For Users:**
- Windows 7 or later
- No Python needed!

**For Developers:**
- Python 3.11+
- Dependencies in `requirements.txt`

---

## 📋 How It Works

### PDFMerger
- Scans current directory for `*.pdf` files
- Sorts alphabetically
- Merges using pypdf library
- Outputs timestamped merged file

### PDFWatcher
- Uses `watchdog` library for file system monitoring
- Detects `.pdf` file creation/modification events
- Waits 3 seconds after last change (debounce)
- Auto-runs merge operation
- Creates timestamped archive folder (e.g., `merged_20251115_143022/`)
- Moves all PDFs (originals + merged output) into archive folder
- Clears watch folder to prevent recursive merging
- Continues monitoring after merge

---

## 🔒 Windows Security Warning

Both executables may trigger Windows SmartScreen warnings because they're not digitally signed.

**To run:**
1. Click "More info"
2. Click "Run anyway"

This is normal for unsigned executables and safe to bypass.

---

## 📝 License

MIT License - feel free to use and modify!

---

## 🤖 Credits

Generated with [Claude Code](https://claude.com/claude-code)
