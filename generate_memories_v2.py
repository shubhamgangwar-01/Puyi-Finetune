"""
Generate synthetic personal memories dataset
"""

import json
import random
import re
import time
from typing import List, Dict
import google.generativeai as genai
import os
from tqdm import tqdm
from memory_cateogary import MEMORY_CATEGORIES, CONVERSATION_TYPES

# Initialize Google Gemini API
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# Simple configuration - no fancy settings that might cause hangs
model = genai.GenerativeModel('gemini-2.0-flash')

def generate_persona() -> Dict:
    """Generate a consistent persona for the memories"""
    
    prompt = """Generate a detailed persona for a fictional person. Include:
    - Name, age, location
    - Background (childhood, education, career)
    - Personality traits
    - Key relationships
    - Hobbies and interests
    - Major life events
    - Values and beliefs
    
    Make it realistic and consistent. Return as JSON."""
    
    response = model.generate_content(prompt)
    
    # Parse and return persona
    persona_text = response.text
    return {"persona_description": persona_text}


def generate_memory_entry(persona: Dict, category: str, topic: str) -> Dict:
    """Generate a single memory entry with Q&A format"""
    
    category_info = MEMORY_CATEGORIES[category]
    
    prompt = f"""Given this persona:
{persona['persona_description']}

Generate a realistic personal memory about: {topic} (category: {category})
{category_info['description']}

Create:
1. A natural user question asking about this memory
2. A detailed, personal response with specific details and emotions
3. Keep it conversational

Return ONLY this JSON (no markdown, no extra text):
{{
    "instruction": "question here",
    "input": "",
    "output": "detailed memory response here",
    "category": "{category}",
    "topic": "{topic}"
}}
"""
    
    response = model.generate_content(prompt)
    response_text = response.text
    
    # Parse JSON from response - robust approach
    try:
        # Extract JSON from markdown if present
        if "```json" in response_text:
            json_str = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            json_str = response_text.split("```")[1].split("```")[0].strip()
        else:
            json_str = response_text.strip()
        
        # Simple fix: Just parse it
        memory_data = json.loads(json_str)
        return memory_data
        
    except json.JSONDecodeError:
        # If JSON parsing fails, skip this entry silently
        return None
    except Exception as e:
        print(f"\nError: {e}")
        return None


def generate_full_dataset(num_entries: int = 2000, rate_limit_delay: float = 0.3) -> List[Dict]:
    """Generate complete synthetic memories dataset
    
    Args:
        num_entries: Total number of memory entries to generate (recommended: 2000-5000 for fine-tuning)
        rate_limit_delay: Delay between API calls in seconds (default: 0.3)
    
    Recommended sizes for fine-tuning:
        - Basic training: 1,000-2,000 entries
        - Good quality: 2,000-3,000 entries  
        - Production quality: 3,000-5,000+ entries
    """
    
    print(f"Generating dataset with {num_entries} entries...")
    print("Generating persona...")
    persona = generate_persona()
    
    # Create data directories if they don't exist
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    
    # Save persona for reference
    with open('data/raw/persona.json', 'w') as f:
        json.dump(persona, f, indent=2)
    
    print("Generating memories...")
    dataset = []
    
    # Distribute entries across categories
    categories = list(MEMORY_CATEGORIES.keys())
    entries_per_category = num_entries // len(categories)
    
    print(f"Generating {entries_per_category} entries per category across {len(categories)} categories")
    
    for category in tqdm(categories, desc="Categories"):
        topics = MEMORY_CATEGORIES[category]["examples"]
        
        for i in range(entries_per_category):
            # Use random selection for better variety
            topic = random.choice(topics)
            
            try:
                memory_entry = generate_memory_entry(persona, category, topic)
                
                if memory_entry:
                    dataset.append(memory_entry)
                else:
                    print(f"\nWarning: Failed to generate entry for {category}/{topic}")
            except Exception as e:
                print(f"\nError generating entry for {category}/{topic}: {e}")
            
            # Rate limiting - be nice to the API
            time.sleep(rate_limit_delay)
    
    return dataset


def save_dataset(dataset: List[Dict], filename: str):
    """Save dataset in Alpaca format"""
    
    # Save full dataset with metadata
    with open(f'data/raw/{filename}', 'w') as f:
        json.dump(dataset, f, indent=2)
    
    # Save in LLaMA Factory format (only instruction, input, output)
    alpaca_format = []
    for entry in dataset:
        alpaca_format.append({
            "instruction": entry["instruction"],
            "input": entry.get("input", ""),
            "output": entry["output"]
        })
    
    with open(f'data/processed/{filename}', 'w') as f:
        json.dump(alpaca_format, f, indent=2)
    
    print(f"✓ Saved {len(dataset)} entries to data/processed/{filename}")


if __name__ == "__main__":
    # Configuration for dataset generation
    # Adjust num_entries based on your needs:
    # - 1000-2000: Quick testing and basic fine-tuning
    # - 2000-3000: Recommended for good quality results
    # - 3000-5000+: Production-quality fine-tuning
    NUM_ENTRIES = 2000  # Increased from 500 for better fine-tuning results
    RATE_LIMIT_DELAY = 0.3  # Seconds between API calls (adjust based on your API limits)
    
    print("="*60)
    print("SYNTHETIC MEMORIES DATASET GENERATOR")
    print("="*60)
    print(f"Target entries: {NUM_ENTRIES}")
    print(f"Categories: {len(MEMORY_CATEGORIES)}")
    print(f"Estimated time: ~{(NUM_ENTRIES * RATE_LIMIT_DELAY) / 60:.1f} minutes")
    print("="*60 + "\n")
    
    # Generate dataset
    dataset = generate_full_dataset(num_entries=NUM_ENTRIES, rate_limit_delay=RATE_LIMIT_DELAY)
    
    # Save dataset
    save_dataset(dataset, "synthetic_memories.json")
    
    print("\n" + "="*60)
    print("DATASET GENERATION COMPLETE")
    print("="*60)
    print(f"✓ Total entries generated: {len(dataset)}")
    print(f"✓ Categories covered: {len(MEMORY_CATEGORIES)}")
    print(f"✓ Average entries per category: {len(dataset) // len(MEMORY_CATEGORIES)}")
    print(f"\n✓ Raw dataset saved to: data/raw/synthetic_memories.json")
    print(f"✓ Processed dataset saved to: data/processed/synthetic_memories.json")
    print(f"\n💡 This dataset is ready for LLaMA Factory fine-tuning!")
    print("="*60)
    
    if len(dataset) > 0:
        print("\nSample entry:")
        print(json.dumps(dataset[0], indent=2))
