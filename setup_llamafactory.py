"""
Setup script to integrate synthetic memories dataset with LLaMA Factory
"""

import json
import shutil
import os
from pathlib import Path

def setup_llamafactory_dataset():
    """Copy dataset and update LLaMA Factory configuration"""
    
    # Paths
    project_root = Path(__file__).parent
    processed_dataset = project_root / "data" / "processed" / "synthetic_memories.json"
    llamafactory_data = project_root / "LLaMA-Factory" / "data"
    llamafactory_dataset_info = llamafactory_data / "dataset_info.json"
    
    print("="*60)
    print("SETTING UP LLAMAFACTORY DATASET")
    print("="*60)
    
    # Check if dataset exists
    if not processed_dataset.exists():
        print("❌ Error: Dataset not found!")
        print(f"   Please generate the dataset first by running: python generate_memories.py")
        return False
    
    # Check dataset size
    with open(processed_dataset, 'r') as f:
        dataset = json.load(f)
    
    print(f"✓ Found dataset with {len(dataset)} entries")
    
    if len(dataset) < 1000:
        print(f"⚠️  Warning: Dataset has only {len(dataset)} entries.")
        print("   Recommended minimum: 1,000 entries for basic fine-tuning")
        print("   Consider regenerating with more entries.")
    
    # Copy dataset to LLaMA Factory
    print(f"\nCopying dataset to LLaMA Factory...")
    target_file = llamafactory_data / "synthetic_memories.json"
    shutil.copy2(processed_dataset, target_file)
    print(f"✓ Copied to: {target_file}")
    
    # Update dataset_info.json
    print(f"\nUpdating dataset_info.json...")
    
    if llamafactory_dataset_info.exists():
        with open(llamafactory_dataset_info, 'r') as f:
            dataset_info = json.load(f)
    else:
        dataset_info = {}
    
    # Add our dataset configuration
    dataset_info["synthetic_memories"] = {
        "file_name": "synthetic_memories.json",
        "formatting": "alpaca",
        "columns": {
            "prompt": "instruction",
            "query": "input",
            "response": "output"
        },
        "tags": {
            "role_tag": "instruction",
            "content_tag": "input",
            "user_tag": "",
            "assistant_tag": ""
        }
    }
    
    # Save updated dataset_info.json
    with open(llamafactory_dataset_info, 'w') as f:
        json.dump(dataset_info, f, indent=2)
    
    print(f"✓ Updated {llamafactory_dataset_info}")
    
    print("\n" + "="*60)
    print("SETUP COMPLETE!")
    print("="*60)
    print(f"✓ Dataset: {len(dataset)} entries")
    print(f"✓ Location: LLaMA-Factory/data/synthetic_memories.json")
    print(f"✓ Registered in: dataset_info.json")
    
    print("\n📝 Next Steps:")
    print("1. Start LLaMA Factory Web UI:")
    print("   cd LLaMA-Factory")
    print("   python src/webui.py")
    
    print("\n2. In the Web UI:")
    print("   - Select your base model (e.g., Llama-3.1-8B)")
    print("   - Choose 'synthetic_memories' as training dataset")
    print("   - Configure LoRA parameters:")
    print("     * LoRA rank: 8-32")
    print("     * Learning rate: 2e-5 to 5e-5")
    print("     * Epochs: 3-5")
    print("     * Batch size: 4-8 (for RTX 3060)")
    print("   - Start training!")
    
    print("\n💡 Tips:")
    print("   - Monitor training loss - should decrease steadily")
    print("   - Use validation split to prevent overfitting")
    print("   - Save checkpoints regularly")
    print("   - Test model after each epoch")
    
    print("="*60)
    return True

if __name__ == "__main__":
    setup_llamafactory_dataset()
