"""
Segment the book text file into chapters
"""

import os
import re

def segment_book_into_chapters(input_file, output_dir):
    """Split the book text into separate chapter files"""
    
    print(f"Reading: {input_file}")
    
    # Read the entire text
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Split by chapter markers
    # Pattern to match "CHAPTER ONE", "CHAPTER TWO", etc. at the start of a line
    chapter_pattern = r'^CHAPTER\s+(ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN|[A-Z]+|\d+)'
    
    # Find all chapter positions
    chapters = []
    lines = content.split('\n')
    
    current_chapter = None
    current_chapter_lines = []
    chapter_count = 0
    
    for i, line in enumerate(lines):
        if re.match(chapter_pattern, line.strip()):
            # Save previous chapter if exists
            if current_chapter is not None:
                chapters.append({
                    'title': current_chapter,
                    'content': '\n'.join(current_chapter_lines),
                    'number': chapter_count
                })
            
            # Start new chapter
            chapter_count += 1
            current_chapter = line.strip()
            current_chapter_lines = [line]
            print(f"Found: {current_chapter}")
        else:
            if current_chapter is not None:
                current_chapter_lines.append(line)
    
    # Save last chapter
    if current_chapter is not None:
        chapters.append({
            'title': current_chapter,
            'content': '\n'.join(current_chapter_lines),
            'number': chapter_count
        })
    
    # Save each chapter to a separate file
    print(f"\n{'='*60}")
    print(f"Saving {len(chapters)} chapters to: {output_dir}")
    print(f"{'='*60}\n")
    
    for chapter in chapters:
        # Create safe filename
        safe_title = re.sub(r'[^\w\s-]', '', chapter['title'])
        safe_title = re.sub(r'\s+', '_', safe_title)
        filename = f"Chapter_{chapter['number']:02d}_{safe_title}.txt"
        filepath = os.path.join(output_dir, filename)
        
        # Save chapter
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(chapter['content'])
        
        print(f"✓ {filename} ({len(chapter['content']):,} chars)")
    
    # Also create a combined file with clear chapter separations
    combined_path = os.path.join(output_dir, "00_All_Chapters_Combined.txt")
    with open(combined_path, 'w', encoding='utf-8') as f:
        for chapter in chapters:
            f.write(f"\n\n{'='*80}\n")
            f.write(f"{chapter['title']}\n")
            f.write(f"{'='*80}\n\n")
            f.write(chapter['content'])
            f.write("\n\n")
    
    print(f"\n✓ Combined file: 00_All_Chapters_Combined.txt")
    
    print(f"\n{'='*60}")
    print(f"✓ Segmentation complete!")
    print(f"✓ Total chapters: {len(chapters)}")
    print(f"{'='*60}")


if __name__ == "__main__":
    input_file = r"C:\Users\amrit\Desktop\ernie-memories-project\emperor_to_citizen_text.txt"
    output_dir = r"C:\Users\amrit\Desktop\ernie-memories-project\book_chapters"
    
    segment_book_into_chapters(input_file, output_dir)
