# Synthetic Memories Dataset Generation Guide

## Dataset Size Recommendations for Fine-Tuning

### Minimum Viable Dataset

- **Size**: 1,000-2,000 entries
- **Purpose**: Quick testing and validation
- **Training time**: ~30-60 minutes (depending on hardware)
- **Use case**: Proof of concept, testing the fine-tuning pipeline

### Recommended Dataset

- **Size**: 2,000-3,000 entries ✅ **(Current default: 2,000)**
- **Purpose**: Good quality results for personal use
- **Training time**: ~1-2 hours
- **Use case**: Personal memory assistant with decent performance

### Production Quality Dataset

- **Size**: 3,000-5,000+ entries
- **Purpose**: High-quality production deployment
- **Training time**: ~2-4 hours
- **Use case**: Production-ready personal AI assistant

## Current Dataset Structure

### Categories (8 total)

1. **Childhood** - Early life memories, family, school, friends
2. **Education** - School, college, learning experiences
3. **Career** - Work experiences, achievements, challenges
4. **Relationships** - Family, friends, romantic relationships
5. **Hobbies** - Interests, passions, recreational activities
6. **Achievements** - Personal accomplishments and proud moments
7. **Life Events** - Significant life moments and transitions
8. **Preferences** - Likes, dislikes, values, beliefs

### Topics per Category

- 5 example topics per category
- Random selection for variety
- Multiple variations per topic

## How to Generate Dataset

### Default Configuration (Recommended)

```bash
python generate_memories.py
```

This generates **2,000 entries** with 0.3s delay between API calls.

### Custom Configuration

Edit `generate_memories.py` and modify:

```python
NUM_ENTRIES = 3000  # Adjust this number
RATE_LIMIT_DELAY = 0.5  # Adjust API rate limiting
```

### Expected Generation Time

- **2,000 entries** @ 0.3s delay: ~10 minutes
- **3,000 entries** @ 0.3s delay: ~15 minutes
- **5,000 entries** @ 0.3s delay: ~25 minutes

## Output Files

### Raw Dataset

- **Location**: `data/raw/synthetic_memories.json`
- **Content**: Full dataset with metadata (category, topic)
- **Use**: Analysis and debugging

### Processed Dataset

- **Location**: `data/processed/synthetic_memories.json`
- **Content**: Alpaca format (instruction, input, output only)
- **Use**: Direct input to LLaMA Factory for fine-tuning

### Persona File

- **Location**: `data/raw/persona.json`
- **Content**: Generated persona used for all memories
- **Use**: Consistency reference

## Using with LLaMA Factory

1. **Copy dataset to LLaMA Factory**:

   ```bash
   cp data/processed/synthetic_memories.json LLaMA-Factory/data/
   ```

2. **Register in dataset_info.json**:

   ```json
   {
     "synthetic_memories": {
       "file_name": "synthetic_memories.json",
       "columns": {
         "prompt": "instruction",
         "query": "input",
         "response": "output"
       }
     }
   }
   ```

3. **Start fine-tuning**:
   - Use LLaMA Factory Web UI or CLI
   - Select your base model
   - Choose "synthetic_memories" as training dataset
   - Configure training parameters

## Tips for Best Results

### Dataset Quality

- ✅ Consistent persona across all memories
- ✅ Natural conversational style
- ✅ Varied topics and question styles
- ✅ Emotional depth and personal details

### Training Parameters

- **Learning rate**: 2e-5 to 5e-5
- **Epochs**: 3-5 (monitor validation loss)
- **Batch size**: Based on your GPU (4-8 for RTX 3060)
- **LoRA rank**: 8-32 (higher = more capacity)

### GPU Considerations (RTX 3060)

- **VRAM**: 6GB (enough for LoRA fine-tuning)
- **Recommended batch size**: 4-8
- **Gradient accumulation**: 4-8 steps
- **Model size**: Up to 7B parameters with LoRA

## Environment Setup

Make sure you have set your Google API key:

```powershell
# PowerShell
$env:GOOGLE_API_KEY="your-api-key-here"
```

```bash
# Linux/Mac
export GOOGLE_API_KEY="your-api-key-here"
```

## Troubleshooting

### API Rate Limits

If you hit rate limits, increase `RATE_LIMIT_DELAY` to 1.0 or higher.

### Out of Memory Errors

Reduce batch size or use gradient accumulation in LLaMA Factory.

### Dataset Too Small

Increase `NUM_ENTRIES` to at least 2,000 for meaningful fine-tuning.

### Training Loss Not Decreasing

- Check dataset quality
- Adjust learning rate
- Ensure consistent formatting
- Try different LoRA configurations
