# File Organizer Script

A Python utility that automatically organizes files in a directory by their type/extension.

## Features

- Organizes files into categorized folders (Images, Documents, Videos, etc.)
- Handles file name conflicts automatically
- Dry-run mode to preview changes
- Detailed summary of organized files
- Command-line interface with options

## File Categories

- **Images**: jpg, jpeg, png, gif, bmp, svg, webp, ico
- **Documents**: pdf, doc, docx, txt, rtf, odt, pages
- **Spreadsheets**: xls, xlsx, csv, ods, numbers
- **Presentations**: ppt, pptx, odp, key
- **Videos**: mp4, avi, mkv, mov, wmv, flv, webm, m4v
- **Audio**: mp3, wav, flac, aac, ogg, wma, m4a
- **Archives**: zip, rar, 7z, tar, gz, bz2, xz
- **Code**: py, js, html, css, java, cpp, c, php, rb, go, rs
- **Executables**: exe, msi, deb, rpm, dmg, pkg, app
- **Fonts**: ttf, otf, woff, woff2, eot
- **Others**: Files that don't match any category

## Usage

```bash
# Organize current directory
python organizer.py

# Organize specific directory
python organizer.py /path/to/directory

# Preview changes without moving files (dry run)
python organizer.py ~/Downloads --dry-run

# Organize current directory with preview
python organizer.py . --dry-run
```

## Requirements

- Python 3.6+
- No external dependencies required

## Safety Features

- Dry-run mode to preview changes
- Automatic handling of file name conflicts
- Skips hidden files (starting with '.')
- Error handling for file operations