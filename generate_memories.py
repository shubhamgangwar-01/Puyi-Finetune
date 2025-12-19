"""
Generate synthetic personal memories dataset
"""

import json
import random
from typing import List, Dict
import google.generativeai as genai
import os
from tqdm import tqdm
from memory_cateogary import MEMORY_CATEGORIES, CONVERSATION_TYPES

# Initialize Google Gemini API
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
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
    # You might need to clean this up or parse it properly
    return {"persona_description": persona_text}


def generate_memory_entry(persona: Dict, category: str, topic: str) -> Dict:
    """Generate a single memory entry with Q&A format"""
    
    category_info = MEMORY_CATEGORIES[category]
    
    prompt = f"""Given this persona:
{persona['persona_description']}

Generate a realistic personal memory about: {topic} (category: {category})
{category_info['description']}

Create:
1. A natural user question asking about this memory (as if talking to a personal AI assistant)
2. A detailed, personal response that includes specific details, emotions, and context
3. Make it conversational and authentic

Return in this JSON format:
{{
    "instruction": "the user's question",
    "input": "",
    "output": "your detailed memory response",
    "category": "{category}",
    "topic": "{topic}"
}}
"""
    
    response = model.generate_content(prompt)
    response_text = response.text
    
    # Parse JSON from response
    try:
        # Try to extract JSON from markdown code blocks if present
        if "```json" in response_text:
            json_str = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            json_str = response_text.split("```")[1].split("```")[0].strip()
        else:
            json_str = response_text.strip()
        
        memory_data = json.loads(json_str)
        return memory_data
    except Exception as e:
        print(f"Error parsing response: {e}")
        print(f"Response: {response_text}")
        return None


def generate_full_dataset(num_entries: int = 500) -> List[Dict]:
    """Generate complete synthetic memories dataset"""
    
    print("Generating persona...")
    persona = generate_persona()
    
    # Save persona for reference
    with open('data/raw/persona.json', 'w') as f:
        json.dump(persona, f, indent=2)
    
    print("Generating memories...")
    dataset = []
    
    # Distribute entries across categories
    categories = list(MEMORY_CATEGORIES.keys())
    entries_per_category = num_entries // len(categories)
    
    for category in tqdm(categories, desc="Categories"):
        topics = MEMORY_CATEGORIES[category]["examples"]
        
        for i in range(entries_per_category):
            # Pick a topic (cycle through or random)
            topic = topics[i % len(topics)]
            
            memory_entry = generate_memory_entry(persona, category, topic)
            
            if memory_entry:
                dataset.append(memory_entry)
            
            # Rate limiting - be nice to the API
            import time
            time.sleep(1)
    
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
    # Generate dataset
    dataset = generate_full_dataset(num_entries=500)
    
    # Save dataset
    save_dataset(dataset, "synthetic_memories.json")
    
    print("\n=== Dataset Generation Complete ===")
    print(f"Total entries: {len(dataset)}")
    print(f"Categories: {len(MEMORY_CATEGORIES)}")
    print("\nSample entry:")
    print(json.dumps(dataset[0], indent=2))