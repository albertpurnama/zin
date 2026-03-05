---
name: gemini-image-gen
description: Generate images using Google's Gemini API (Gemini 3 Pro image generation, aka "nanobanana"). Use when the user wants to create images, generate visuals, or produce AI-generated artwork. Supports various aspect ratios (1:1, 16:9, 4:3, 3:4, 9:16) and sizes (1K, 2K, 4K).
---

# Gemini Image Generation

Generate images using Google's Gemini 3 Pro image generation API.

## Requirements

- `GEMINI_API_KEY` environment variable set, or passed via `--api-key`
- `google-genai` Python package installed (`pip install google-genai`)

## Usage

### Command Line

```bash
# Basic usage
python scripts/generate_image.py "a cat wearing a spacesuit"

# With options
python scripts/generate_image.py "a futuristic city" \
    --output cityscape \
    --aspect-ratio 16:9 \
    --size 2K
```

### From Python

```python
from scripts.generate_image import generate_image

files = generate_image(
    prompt="a serene mountain landscape at sunset",
    output_name="mountain",
    aspect_ratio="16:9",
    size="2K"
)
```

## Parameters

- **prompt** (required): Text description of the image to generate
- **output_name**: Base filename for output (default: "generated_image")
- **aspect_ratio**: Image proportions
  - `1:1` - Square (default)
  - `16:9` - Widescreen
  - `4:3` - Standard
  - `3:4` - Portrait
  - `9:16` - Mobile vertical
- **size**: Resolution
  - `1K` - 1024px (default)
  - `2K` - Higher resolution
  - `4K` - Maximum resolution

## Output

Generated images are saved to the current directory with auto-detected extensions (usually `.png` or `.jpg`). Multiple images may be generated for a single prompt.
