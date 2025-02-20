# dummy-img-gen: Your Sanity-Saving Image Placeholder Solution 🖼️

A lightweight, no-nonsense Python utility for generating numbered placeholder images that won't make your development workflow hate you.

## Why This Exists

Ever found yourself manually creating dozens of test images or, worse, using Lorem Picsum for the 500th time? Yeah, me too. This little tool was born from that specific frustration - needing consistent, numbered, controllable test images without the overhead of firing up Photoshop or fighting with online generators.

## Feature Landscape

- **Core Capabilities**:
  - Generate sequentially numbered images (because counting is hard)
  - Full control over dimensions, colors, and formats (PNG/JPEG/WebP)
  - Intelligent text centering with proper baseline alignment
  - Sensible defaults that don't make your eyes bleed
  - Both CLI and programmatic interfaces (for automation enthusiasts)

- **Technical Flexibility**:
  - Custom font support (for when Helvetica just won't cut it)
  - Configurable number sequences (start wherever your heart desires)
  - Smart padding controls for perfect visual balance
  - Format-specific optimizations (quality settings that make sense)
  - Lightweight dependencies (just Pillow, because bloat is bad)

The tool strikes that delicate balance between "too simple to be useful" and "so complex I need documentation to generate a rectangle." Perfect for development environments, testing suites, or those moments when you need 50 product placeholders yesterday.

## Getting Started (The Easy Part)

```bash
# Clone it
git clone https://github.com/poacosta/dummy-img-gen.git
cd dummy-img-gen

# Feed it (minimal dependencies, because who needs dependency hell?)
pip install pillow
```

## Command-line Interface: Your Developer-Friendly Control Panel

Need to see all the options? Just ask for help:

```bash
python dummy_img_gen.py --help
```

You'll get this comprehensive guide to all parameters:

```
usage: dummy_img_gen.py [-h] [--count COUNT] [--start START] [--width WIDTH] [--height HEIGHT] 
                        [--bg-color BG_COLOR] [--text-color TEXT_COLOR] [--format {png,jpg,webp}] 
                        [--prefix PREFIX] [--font-path FONT_PATH] [--font-size FONT_SIZE] 
                        [--jpg-quality JPG_QUALITY] [--overwrite] [--padding PADDING]
                        output_dir

Generate numbered placeholder images for development and testing

positional arguments:
  output_dir            Directory to save images

options:
  -h, --help            show this help message and exit
  --count COUNT         Number of images to generate (default: 10)
  --start START         First number in sequence (default: 1)
  --width WIDTH         Image width in pixels (default: 800)
  --height HEIGHT       Image height in pixels (default: 600)
  --bg-color BG_COLOR   Background color (hex/name) (default: #cccccc)
  --text-color TEXT_COLOR
                        Text color (hex/name) (default: #333333)
  --format {png,jpg,webp}
                        Image format (default: png)
  --prefix PREFIX       Filename prefix (default: img_)
  --font-path FONT_PATH
                        Path to custom font (.ttf/.otf) (default: None)
  --font-size FONT_SIZE
                        Font size (auto-calculated if omitted) (default: None)
  --jpg-quality JPG_QUALITY
                        JPEG/WebP quality (1-100) (default: 90)
  --overwrite           Overwrite existing files (default: False)
  --padding PADDING     Padding around text (0.0-0.5) (default: 0.2)
```

### Command Examples: From Zero to Hero

```bash
# The vanilla experience - 10 decent looking images
python dummy_img_gen.py output_folder

# The power-user experience
python dummy_img_gen.py output_folder --count 50 --width 1200 --height 800 \
  --bg-color "#f0f0f0" --text-color "#0066cc" --format jpg

# "I need to start at 100 because reasons"
python dummy_img_gen.py output_folder --start 100 --count 20

# Typography nerd mode
python dummy_img_gen.py output_folder --font-path "/path/to/font.ttf" --font-size 120

# Perfect centering mode
python dummy_img_gen.py output_folder --padding 0.15
```

## API Usage (For The Programmatically Inclined)

```python
from dummy_img_gen import generate_placeholder_images

# "Just make it work" mode
paths = generate_placeholder_images("output_dir")

# "I have very specific requirements" mode
paths = generate_placeholder_images(
    output_dir="product_images",
    count=24,
    start_num=1,
    size=(1200, 1200),
    bg_color="#ffffff",
    text_color="#222222",
    format="webp",
    prefix="product_",
    font_size=200,
    font_path="fonts/Roboto-Bold.ttf",
    jpg_quality=95,
    padding=0.25,
    overwrite=True
)
```

## Configuration Options (The Control Panel)

| Option | What It Actually Does | Default |
|--------|-------------|---------|
| `output_dir` | Where your images will live | (Required) |
| `count` | How many images to generate | 10 |
| `start_num` | First number in sequence | 1 |
| `size` | Dimensions in pixels (width, height) | (800, 600) |
| `bg_color` | Background color (hex/name) | "#cccccc" |
| `text_color` | Text color (hex/name) | "#333333" |
| `format` | Image format (png/jpg/webp) | "png" |
| `prefix` | Filename prefix | "img_" |
| `font_size` | Text size in pixels | auto-calculated |
| `font_path` | Custom font location | system fonts |
| `jpg_quality` | JPEG/WebP quality (1-100) | 90 |
| `padding` | Spacing around text (0.0-0.5) | 0.2 |
| `overwrite` | Whether to steamroll existing files | False |

## The Secret Sauce: Smart Centering

Unlike other placeholder generators that just slap text on an image (looking at you, every online generator ever), dummy-img-gen uses:

1. **Intelligent Baseline Alignment** - Properly centers text based on font metrics, not just bounding boxes
2. **Optical Balancing** - Small adjustments for visual perfection because humans don't perceive geometric center correctly
3. **Adaptive Sizing** - Text scales proportionally based on image dimensions and digit count
4. **Custom Padding Control** - Fine-tune the text:background ratio for your specific needs

This means your placeholders actually look *good*, not just *functional*. Your designer friends might even stop judging you.

## System Requirements (Minimal)

- Python 3.10+ (because it's 2025, please upgrade)
- Pillow library (the successor to PIL, for the trivia enthusiasts)

## License

MIT - Take it. Use it. Modify it.

## Contributing

Found a bug? Have a feature idea? PRs welcome! The code is intentionally straightforward, so don't be intimidated. I promise I don't bite during code reviews.
