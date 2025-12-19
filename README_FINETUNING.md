# 🧠 Ernie Memories Project - Fine-tuning Guide

A complete pipeline for generating synthetic personal memories and fine-tuning an LLM to act as a personalized memory assistant using LLaMA Factory.

## 📊 Dataset Size for Fine-Tuning

### ✅ Current Configuration: **2,000 entries**

This is the **recommended minimum** for effective fine-tuning with good results:

| Dataset Size    | Quality Level | Training Time  | Use Case                      |
| --------------- | ------------- | -------------- | ----------------------------- |
| 1,000-2,000     | Basic         | ~1 hour        | Testing, proof of concept     |
| **2,000-3,000** | **Good** ✅   | **~1-2 hours** | **Personal use, recommended** |
| 3,000-5,000+    | Production    | ~2-4+ hours    | High-quality deployment       |

### Why 2,000 entries?

1. **Sufficient diversity** - 250 entries per category (8 categories)
2. **Good generalization** - Enough data to learn patterns without overfitting
3. **Reasonable generation time** - ~10 minutes with current rate limiting
4. **Proven effective** - Standard size for LoRA fine-tuning tasks
5. **GPU-friendly** - Works well with RTX 3060 (6GB VRAM)

## 🚀 Quick Start

### 1. Generate Dataset (2,000 entries)

```powershell
# Set Google API key
$env:GOOGLE_API_KEY="your-api-key-here"

# Generate 2,000 memory entries (~10 minutes)
python generate_memories.py
```

**Output:**

- `data/raw/synthetic_memories.json` - Full dataset with metadata
- `data/processed/synthetic_memories.json` - Alpaca format for training
- `data/raw/persona.json` - Generated persona for consistency

### 2. Setup LLaMA Factory Integration

```powershell
python setup_llamafactory.py
```

This will:

- Copy dataset to LLaMA Factory
- Register it in `dataset_info.json`
- Verify dataset size and quality

### 3. Start Fine-Tuning

```powershell
cd LLaMA-Factory
python src/webui.py
```

Then configure in Web UI:

- **Model**: Llama-3.1-8B or similar
- **Dataset**: synthetic_memories
- **LoRA rank**: 8-32
- **Learning rate**: 2e-5 to 5e-5
- **Epochs**: 3-5
- **Batch size**: 4-8

## 📁 Project Structure

```
ernie-memories-project/
├── generate_memories.py          # Main dataset generator (2000 entries default)
├── memory_cateogary.py           # 8 categories, 5 topics each
├── setup_llamafactory.py         # LLaMA Factory integration
├── DATASET_GUIDE.md              # Detailed documentation
├── README_FINETUNING.md          # This file
├── data/
│   ├── raw/
│   │   ├── synthetic_memories.json      # Full dataset
│   │   └── persona.json                 # Generated persona
│   └── processed/
│       └── synthetic_memories.json      # Alpaca format
└── LLaMA-Factory/                # Fine-tuning framework
    └── data/
        └── synthetic_memories.json      # Training dataset
```

## 🎯 Dataset Composition

### 8 Memory Categories (250 entries each)

1. **Childhood** (250) - Early life, family, school
2. **Education** (250) - Learning experiences, teachers
3. **Career** (250) - Work, achievements, challenges
4. **Relationships** (250) - Family, friends, connections
5. **Hobbies** (250) - Interests, passions, activities
6. **Achievements** (250) - Accomplishments, proud moments
7. **Life Events** (250) - Significant moments, transitions
8. **Preferences** (250) - Likes, dislikes, values

**Total: 2,000 diverse memory conversations**

## ⚙️ Customizing Dataset Size

Want more or fewer entries? Edit `generate_memories.py`:

```python
# For faster testing (1,000 entries, ~5 minutes)
NUM_ENTRIES = 1000
RATE_LIMIT_DELAY = 0.3

# For production quality (5,000 entries, ~25 minutes)
NUM_ENTRIES = 5000
RATE_LIMIT_DELAY = 0.3
```

## 🔧 Fine-Tuning Configuration

### Recommended Settings for RTX 3060 (6GB VRAM)

```yaml
# Model
base_model: meta-llama/Llama-3.1-8B-Instruct

# LoRA Configuration
lora_rank: 16
lora_alpha: 32
lora_dropout: 0.05

# Training
learning_rate: 3e-5
num_epochs: 3
batch_size: 4
gradient_accumulation_steps: 8
max_length: 512

# Dataset
dataset: synthetic_memories
val_split: 0.1
```

### Training Time Estimates

| Setup             | Time per Epoch | Total (3 epochs) |
| ----------------- | -------------- | ---------------- |
| RTX 3060, batch=4 | ~20-30 min     | ~1-1.5 hours     |
| RTX 4090, batch=8 | ~10-15 min     | ~30-45 min       |

## 📈 Monitoring Training

### Good Signs ✅

- Training loss steadily decreasing
- Validation loss following training loss
- No overfitting (val loss ≈ train loss)
- Model responses becoming more coherent

### Red Flags ❌

- Training loss stuck or increasing
- Validation loss much higher than training (overfitting)
- NaN or Inf losses
- GPU out of memory errors

**Solutions:**

- Reduce batch size if OOM
- Adjust learning rate if stuck
- Add more data if overfitting
- Use gradient checkpointing for memory

## 🧪 Testing Your Model

After fine-tuning, test with queries like:

```
"What was your childhood like?"
"Tell me about your first job"
"What are your hobbies?"
"Do you remember any important life events?"
```

The model should respond **in first person** with details consistent with the generated persona.

## 📊 Dataset Quality Metrics

Our 2,000-entry dataset provides:

✅ **Coverage**: 250 entries per category
✅ **Variety**: Random topic selection for diversity
✅ **Consistency**: Single persona across all memories
✅ **Format**: Alpaca-style instruction-response pairs
✅ **Balance**: Even distribution across life aspects

## 🎓 Advanced: Scaling Up

### For Production (5,000+ entries):

1. **Increase generation**:

   ```python
   NUM_ENTRIES = 5000
   ```

2. **Use batch processing**:

   - Generate in chunks
   - Save progress incrementally
   - Resume if interrupted

3. **Optimize training**:
   - Use DeepSpeed ZeRO-3
   - Multi-GPU training
   - Mixed precision (fp16)

## 🐛 Troubleshooting

### "Dataset too small" warning

- Generate at least 1,000 entries
- Current default (2,000) is recommended

### API rate limits

- Increase `RATE_LIMIT_DELAY` to 1.0
- Use Google AI Studio free tier wisely

### Out of memory during training

- Reduce batch size to 2
- Increase gradient accumulation to 16
- Use gradient checkpointing

### Model not learning

- Check dataset format
- Verify proper registration in dataset_info.json
- Increase learning rate slightly
- Train for more epochs

## 📚 Additional Resources

- [DATASET_GUIDE.md](./DATASET_GUIDE.md) - Comprehensive dataset documentation
- [LLaMA Factory Docs](https://github.com/hiyouga/LLaMA-Factory)
- [LoRA Paper](https://arxiv.org/abs/2106.09685)

## 🎯 Expected Results

With **2,000 entries** and proper training:

✅ Model will remember persona-consistent details
✅ Natural conversational responses
✅ Appropriate emotional depth
✅ Coherent narrative across topics
✅ First-person perspective maintained

## 💡 Tips for Best Results

1. **Start with 2,000 entries** (current default) ✅
2. Monitor training loss - should decrease smoothly
3. Use validation split (10-20%) to prevent overfitting
4. Save checkpoints every epoch
5. Test after each epoch to see improvement
6. Fine-tune hyperparameters based on results

---

**🎉 You're all set!** The default 2,000-entry configuration is optimized for your RTX 3060 and will produce a quality personal memory assistant.
