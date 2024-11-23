# Repository Merge Scripts 

Scripts for managing and merging GitHub repository URLs into a TOML configuration file compatible with [Electric Capital's crypto-ecosystems](https://github.com/electric-capital/crypto-ecosystems) directory. 

##  Quick Start

```bash
# Merge new repositories
python merge.py

# Clean and validate the output
python clean.py
```

## File Structure

```
scripts/merge/
├── merge.py      # Main merging utility
├── clean.py      # URL cleaning and validation
├── aptos.toml    # Source configuration
└── new-repos.txt # New repositories to merge
```

## Scripts Overview

### `merge.py`

Merges GitHub URLs while maintaining data integrity.

**Features:**
- ✨ URL normalization and cleaning
- 🔒 HTTPS protocol enforcement
- 🔄 Automatic duplicate removal
- ✅ GitHub repository URL validation
- 📝 TOML format preservation
- 🔤 Case-insensitive sorting

### `clean.py`

Sanitizes TOML configurations to ensure URL consistency and validity.

**Capabilities:**
- 🧹 Removes duplicate entries
- ⚡ Validates URL format
- 🚫 Filters branch/blob references
- 🎯 Ensures owner/repo URL structure
- 💾 Preserves TOML formatting

## Usage Guide

1. **Setup Configuration Files**
   - Place your existing repositories in `aptos.toml`
   - Add new repositories to `new-repos.txt`

2. **Run the Merge Process**
   ```bash
   python merge.py
   ```
   This generates `new-aptos.toml` with merged repositories

3. **Clean the Output**
   ```bash
   python clean.py
   ```
   Ensures all entries are valid and unique

## URL Requirements

All repository URLs must follow these rules:
- ✅ HTTPS protocol required
- ✅ Format: `https://github.com/owner/repo`
- ❌ No branch references (`/tree/`, `/blob/`)
- ❌ No trailing slashes or quotes

## Examples

```toml
# Valid URLs
repositories = [
    "https://github.com/apache/spark",
    "https://github.com/facebook/react"
]

# Invalid URLs
repositories = [
    "http://github.com/user/repo",           # Wrong protocol
    "https://github.com/user/repo/tree/main", # Contains branch
    "https://github.com/user/repo/"          # Trailing slash
]
```
