"""
Generate instruction-output pairs from book chapters using Gemini
For fine-tuning purposes
"""

import json
import os
import time
from pathlib import Path
import google.generativeai as genai
from tqdm import tqdm

# Initialize Gemini
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')

def generate_pairs_batch(chapter_text, chapter_title, batch_size=100):
    """Generate a batch of instruction-output pairs from chapter text"""
    
    # Use smaller text chunk to avoid timeouts
    text_sample = chapter_text[:8000] if len(chapter_text) > 8000 else chapter_text
    
    prompt = f"""Based on this excerpt from "From Emperor to Citizen" by Pu Yi:

{text_sample}

Generate {batch_size} diverse Q&A pairs for AI training.

Questions should be natural and varied (factual, analytical, personal).
Answers should be detailed and conversational, in first person when about Pu Yi's experiences.

Return ONLY this JSON array (no markdown):
[
  {{"instruction": "question", "output": "answer"}},
  ...
]"""

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.8,
                "max_output_tokens": 8000,
            }
        )
        response_text = response.text.strip()
        
        # Extract JSON
        if "```json" in response_text:
            json_str = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            json_str = response_text.split("```")[1].split("```")[0].strip()
        else:
            json_str = response_text
        
        # Clean and fix common JSON issues
        import re
        # Remove trailing commas before closing brackets
        json_str = re.sub(r',\s*}', '}', json_str)
        json_str = re.sub(r',\s*]', ']', json_str)
        # Remove comments if any
        json_str = re.sub(r'//.*?\n', '\n', json_str)
        
        pairs = json.loads(json_str)
        return pairs if isinstance(pairs, list) else []
        
    except json.JSONDecodeError as e:
        # Try to salvage what we can by parsing line by line
        try:
            # Look for individual objects and parse them
            import re
            objects = re.findall(r'\{[^{}]*"instruction"[^{}]*"output"[^{}]*\}', response_text, re.DOTALL)
            valid_pairs = []
            for obj in objects:
                try:
                    pair = json.loads(obj)
                    if 'instruction' in pair and 'output' in pair:
                        valid_pairs.append(pair)
                except:
                    continue
            if valid_pairs:
                return valid_pairs
        except:
            pass
        return []
    except Exception as e:
        return []


def process_chapter(chapter_file, output_dir, pairs_per_chapter=1000, batch_size=50):
    """Process a single chapter and generate all pairs"""
    
    chapter_name = Path(chapter_file).stem
    print(f"\n{'='*60}")
    print(f"Processing: {chapter_name}")
    print(f"{'='*60}")
    
    # Read chapter content
    with open(chapter_file, 'r', encoding='utf-8') as f:
        chapter_text = f.read()
    
    # Skip if chapter is too short (likely table of contents)
    if len(chapter_text) < 5000:
        print(f"⚠️  Skipping - chapter too short ({len(chapter_text)} chars)")
        return
    
    # Calculate number of batches needed
    num_batches = pairs_per_chapter // batch_size
    
    all_pairs = []
    
    print(f"Generating {pairs_per_chapter} pairs in {num_batches} batches of {batch_size}...")
    
    for batch_num in tqdm(range(num_batches), desc="Batches"):
        max_retries = 2
        batch_pairs = []
        
        for retry in range(max_retries):
            try:
                batch_pairs = generate_pairs_batch(chapter_text, chapter_name, batch_size)
                
                if batch_pairs:
                    all_pairs.extend(batch_pairs)
                    print(f"  ✓ Batch {batch_num + 1}/{num_batches}: {len(batch_pairs)} pairs")
                    break
                elif retry < max_retries - 1:
                    time.sleep(1)  # Wait before retry
            except Exception as e:
                if retry == max_retries - 1:
                    print(f"  ✗ Batch {batch_num + 1}/{num_batches}: Failed after {max_retries} attempts")
        
        # Rate limiting
        time.sleep(1)  # 1 second delay between batches
    
    # Save pairs for this chapter
    output_file = os.path.join(output_dir, f"{chapter_name}_pairs.json")
    
    # Format for fine-tuning (Alpaca style)
    alpaca_format = []
    for pair in all_pairs:
        alpaca_format.append({
            "instruction": pair.get("instruction", ""),
            "input": "",
            "output": pair.get("output", ""),
            "source": chapter_name
        })
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(alpaca_format, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Saved {len(alpaca_format)} pairs to: {output_file}")
    
    return alpaca_format


def process_all_chapters(chapters_dir, output_dir, pairs_per_chapter=1000):
    """Process all chapters in the directory"""
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all chapter files (skip the combined file and short chapters)
    chapter_files = sorted([
        f for f in Path(chapters_dir).glob("Chapter_*.txt")
        if not f.name.startswith("00_")
    ])
    
    print(f"{'='*60}")
    print(f"BOOK TO TRAINING DATA GENERATOR")
    print(f"{'='*60}")
    print(f"Found {len(chapter_files)} chapter files")
    print(f"Target: {pairs_per_chapter} pairs per chapter")
    print(f"Total pairs expected: {len(chapter_files) * pairs_per_chapter}")
    print(f"{'='*60}\n")
    
    all_training_data = []
    
    for chapter_file in chapter_files:
        try:
            pairs = process_chapter(
                str(chapter_file), 
                output_dir, 
                pairs_per_chapter=pairs_per_chapter
            )
            if pairs:
                all_training_data.extend(pairs)
        except Exception as e:
            print(f"Error processing {chapter_file.name}: {e}")
            continue
    
    # Save combined training dataset
    combined_file = os.path.join(output_dir, "all_chapters_training_data.json")
    with open(combined_file, 'w', encoding='utf-8') as f:
        json.dump(all_training_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"GENERATION COMPLETE!")
    print(f"{'='*60}")
    print(f"✓ Total pairs generated: {len(all_training_data)}")
    print(f"✓ Individual chapter files saved in: {output_dir}")
    print(f"✓ Combined dataset: {combined_file}")
    print(f"{'='*60}")
    
    return all_training_data


if __name__ == "__main__":
    chapters_dir = r"C:\Users\amrit\Desktop\ernie-memories-project\book_chapters"
    output_dir = r"C:\Users\amrit\Desktop\ernie-memories-project\training_data"
    
    # Generate 1000 pairs per chapter
    process_all_chapters(chapters_dir, output_dir, pairs_per_chapter=1000)
