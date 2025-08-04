#!/usr/bin/env python3
import os
import shutil
import argparse
from pathlib import Path
from collections import defaultdict

class FileOrganizer:
    def __init__(self):
        self.file_types = {
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico'],
            'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.pages'],
            'Spreadsheets': ['.xls', '.xlsx', '.csv', '.ods', '.numbers'],
            'Presentations': ['.ppt', '.pptx', '.odp', '.key'],
            'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
            'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
            'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'],
            'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php', '.rb', '.go', '.rs'],
            'Executables': ['.exe', '.msi', '.deb', '.rpm', '.dmg', '.pkg', '.app'],
            'Fonts': ['.ttf', '.otf', '.woff', '.woff2', '.eot']
        }
        self.stats = defaultdict(int)

    def get_file_category(self, file_path):
        """Determine the category of a file based on its extension."""
        extension = file_path.suffix.lower()
        
        for category, extensions in self.file_types.items():
            if extension in extensions:
                return category
        
        return 'Others'

    def create_folder_if_not_exists(self, folder_path):
        """Create a folder if it doesn't exist."""
        if not folder_path.exists():
            folder_path.mkdir(parents=True, exist_ok=True)
            print(f"📁 Created folder: {folder_path}")

    def organize_directory(self, source_dir, dry_run=False):
        """Organize files in the specified directory."""
        source_path = Path(source_dir)
        
        if not source_path.exists():
            print(f"❌ Directory '{source_dir}' does not exist!")
            return

        if not source_path.is_dir():
            print(f"❌ '{source_dir}' is not a directory!")
            return

        print(f"🔍 Scanning directory: {source_path}")
        print(f"{'🧪 DRY RUN MODE - No files will be moved!' if dry_run else '📦 Organizing files...'}")
        print("-" * 60)

        files_to_organize = []
        
        # Scan for files
        for item in source_path.iterdir():
            if item.is_file() and not item.name.startswith('.'):
                files_to_organize.append(item)

        if not files_to_organize:
            print("📝 No files to organize!")
            return

        # Group files by category
        categorized_files = defaultdict(list)
        for file_path in files_to_organize:
            category = self.get_file_category(file_path)
            categorized_files[category].append(file_path)

        # Organize files
        for category, files in categorized_files.items():
            category_folder = source_path / category
            
            if not dry_run:
                self.create_folder_if_not_exists(category_folder)

            print(f"\n📂 {category} ({len(files)} files):")
            
            for file_path in files:
                destination = category_folder / file_path.name
                
                if dry_run:
                    print(f"   Would move: {file_path.name} → {category}/")
                else:
                    try:
                        # Handle file name conflicts
                        counter = 1
                        original_destination = destination
                        while destination.exists():
                            stem = original_destination.stem
                            suffix = original_destination.suffix
                            destination = category_folder / f"{stem}_{counter}{suffix}"
                            counter += 1

                        shutil.move(str(file_path), str(destination))
                        print(f"   ✅ Moved: {file_path.name} → {category}/")
                        self.stats[category] += 1
                        
                    except Exception as e:
                        print(f"   ❌ Error moving {file_path.name}: {e}")

        self.print_summary(dry_run)

    def print_summary(self, dry_run=False):
        """Print organization summary."""
        print("\n" + "=" * 60)
        print(f"📊 {'PREVIEW' if dry_run else 'ORGANIZATION'} SUMMARY")
        print("=" * 60)
        
        if not dry_run and self.stats:
            total_files = sum(self.stats.values())
            print(f"Total files organized: {total_files}")
            print("\nFiles by category:")
            for category, count in sorted(self.stats.items()):
                print(f"  {category}: {count} files")
        elif dry_run:
            print("Run without --dry-run to actually organize the files.")
        else:
            print("No files were organized.")

def main():
    parser = argparse.ArgumentParser(
        description="Organize files in a directory by type",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python organizer.py /path/to/directory
  python organizer.py ~/Downloads --dry-run
  python organizer.py . --dry-run
        """
    )
    
    parser.add_argument(
        'directory',
        nargs='?',
        default='.',
        help='Directory to organize (default: current directory)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview what would be organized without actually moving files'
    )

    args = parser.parse_args()

    organizer = FileOrganizer()
    
    try:
        organizer.organize_directory(args.directory, args.dry_run)
    except KeyboardInterrupt:
        print("\n\n⏹️ Organization cancelled by user.")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")

if __name__ == "__main__":
    main()