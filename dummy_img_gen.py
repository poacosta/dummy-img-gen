#!/usr/bin/env python3
"""
dummy-img-gen: Your Sanity-Saving Image Placeholder Solution

A lightweight utility for generating numbered placeholder images for development and testing.
"""

import argparse
import os
import sys
from typing import Tuple, List, Optional, Literal

from PIL import Image, ImageDraw, ImageFont, ImageColor


def find_system_font() -> str:
    """
    Find an appropriate system font to use as default.

    Searches platform-specific font directories for common fonts, falling back
    to general font directory traversal if needed.

    Returns:
        Path to a usable font file.

    Raises:
        FileNotFoundError: If no valid font could be found.
    """
    potential_fonts = []
    if os.name == 'nt':
        potential_fonts = [
            "C:\\Windows\\Fonts\\Arial.ttf",
            "C:\\Windows\\Fonts\\Arial Bold.ttf",
            "C:\\Windows\\Fonts\\Calibri.ttf",
            "C:\\Windows\\Fonts\\Segoe UI Bold.ttf"
        ]
    elif sys.platform == 'darwin':
        potential_fonts = [
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/SFCompact-Bold.otf",
            "/Library/Fonts/Arial.ttf",
            "/Library/Fonts/Arial Bold.ttf"
        ]
    else:
        potential_fonts = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/ubuntu/Ubuntu-Bold.ttf",
            "/usr/share/fonts/TTF/Arial.ttf"
        ]

    for font_path in potential_fonts:
        if os.path.exists(font_path):
            return font_path

    font_dirs = [
        "/usr/share/fonts",
        "/usr/local/share/fonts",
        os.path.expanduser("~/.fonts"),
        "C:\\Windows\\Fonts",
        "/Library/Fonts",
        "/System/Library/Fonts"
    ]

    for font_dir in font_dirs:
        if os.path.exists(font_dir):
            for root, _, files in os.walk(font_dir):
                for file in files:
                    if file.lower().endswith(('.ttf', '.otf')):
                        return os.path.join(root, file)

    raise FileNotFoundError("Could not find any usable font. Please specify a font with --font-path.")


def parse_color(color: str) -> Tuple[int, ...]:
    """
    Parse color string (hex or name) to RGBA tuple.

    Supports:
    - 3/4/6/8 character hex formats (#rgb, #rgba, #rrggbb, #rrggbbaa)
    - All CSS3 color names (via PIL.ImageColor)

    Args:
        color: Color specification string

    Returns:
        RGBA tuple with values 0-255

    Raises:
        ValueError: For unrecognized color formats
    """
    try:
        return ImageColor.getcolor(color, "RGBA")
    except ValueError:
        raise ValueError(f"Unrecognized color: {color}")


def calculate_font_size(
        text: str,
        image_size: Tuple[int, int],
        font_path: str,
        target_ratio: float = 0.6
) -> int:
    """
    Calculate optimal font size to fit text in image with proper padding.

    Uses binary search to find the largest font size that keeps text within
    the specified ratio of the image dimensions.

    Args:
        text: Text to measure
        image_size: (width, height) of target image
        font_path: Path to font file
        target_ratio: Maximum proportion of image dimensions text should occupy

    Returns:
        Optimal font size in pixels
    """
    width, height = image_size
    target_width = width * target_ratio
    target_height = height * target_ratio

    size_min, size_max = 10, min(width, height)
    optimal_size = size_min

    while size_min <= size_max:
        mid_size = (size_min + size_max) // 2
        try:
            font = ImageFont.truetype(font_path, mid_size)
            text_bbox = font.getbbox(text)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            if text_width <= target_width and text_height <= target_height:
                optimal_size = mid_size
                size_min = mid_size + 1
            else:
                size_max = mid_size - 1
        except Exception:
            size_max = mid_size - 1

    return optimal_size


def generate_placeholder_image(
        number: int,
        output_path: str,
        size: Tuple[int, int] = (800, 600),
        bg_color: str = "#cccccc",
        text_color: str = "#333333",
        format: Literal["png", "jpg", "webp"] = "png",
        font_path: Optional[str] = None,
        font_size: Optional[int] = None,
        jpg_quality: int = 90,
        overwrite: bool = False,
        padding: float = 0.2
) -> str:
    """
    Generate a single placeholder image with a centered number.

    Args:
        number: The number to display
        output_path: Where to save the image
        size: (width, height) tuple
        bg_color: Background color (hex or name)
        text_color: Text color (hex or name)
        format: Output format (png/jpg/webp)
        font_path: Path to font file (auto-detected if None)
        font_size: Font size in pixels (auto-calculated if None)
        jpg_quality: Quality for JPG/WebP (1-100)
        overwrite: Whether to override existing files
        padding: Proportion of image to leave as padding (0-0.5)

    Returns:
        Path to the saved image

    Raises:
        ValueError: For invalid colors or font issues
        OSError: For file writing problems
    """
    if os.path.exists(output_path) and not overwrite:
        print(f"Skipping {output_path} (already exists)")
        return output_path

    if not font_path:
        font_path = find_system_font()

    bg_rgba = parse_color(bg_color)
    text_rgba = parse_color(text_color)

    if format == "jpg":
        bg_rgb = bg_rgba[:3]
        text_rgb = text_rgba[:3]
        img = Image.new('RGB', size, bg_rgb)
    else:
        img = Image.new('RGBA', size, bg_rgba)
    draw = ImageDraw.Draw(img)

    text = str(number)
    try:
        if font_size is None:
            target_ratio = 1.0 - 2 * padding
            font_size = calculate_font_size(text, size, font_path, target_ratio)
        font = ImageFont.truetype(font_path, font_size)
    except Exception as e:
        raise ValueError(f"Font error: {e}")

    text_bbox = font.getbbox(text)
    text_width = text_bbox[2] - text_bbox[0]
    x = (size[0] - text_width) // 2
    y = (size[1] - text_bbox[1] - text_bbox[3]) // 2

    fill_color = text_rgba[:3] if format == "jpg" else text_rgba
    draw.text((x, y), text, font=font, fill=fill_color)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    save_args = {}
    if format == "jpg":
        img.save(output_path, "JPEG", quality=jpg_quality, optimize=True)
    elif format == "webp":
        img.save(output_path, "WEBP", quality=jpg_quality, method=6)
    else:
        img.save(output_path, "PNG", optimize=True)

    return output_path


def generate_placeholder_images(
        output_dir: str,
        count: int = 10,
        start_num: int = 1,
        size: Tuple[int, int] = (800, 600),
        bg_color: str = "#cccccc",
        text_color: str = "#333333",
        format: Literal["png", "jpg", "webp"] = "png",
        prefix: str = "img_",
        font_size: Optional[int] = None,
        font_path: Optional[str] = None,
        jpg_quality: int = 90,
        overwrite: bool = False,
        padding: float = 0.2
) -> List[str]:
    """
    Generate multiple placeholder images with sequential numbers.

    Args:
        output_dir: Directory to save images in
        count: Number of images to generate
        start_num: First number in sequence
        size: (width, height) tuple
        bg_color: Background color (hex or name)
        text_color: Text color (hex or name)
        format: Output format (png/jpg/webp)
        prefix: Filename prefix
        font_size: Font size in pixels (auto-calculated if None)
        font_path: Path to font file (auto-detected if None)
        jpg_quality: Quality for JPG/WebP (1-100)
        overwrite: Whether to override existing files
        padding: Proportion of image to leave as padding (0-0.5)

    Returns:
        List of paths to saved images

    Raises:
        OSError: If output directory can't be created
    """
    os.makedirs(output_dir, exist_ok=True)
    generated_files = []

    for i in range(count):
        current_num = start_num + i
        filename = f"{prefix}{current_num}.{format}"
        output_path = os.path.join(output_dir, filename)

        try:
            path = generate_placeholder_image(
                current_num, output_path, size, bg_color, text_color, format,
                font_path, font_size, jpg_quality, overwrite, padding
            )
            generated_files.append(path)
            print(f"Generated: {path}")
        except Exception as e:
            print(f"Error generating {output_path}: {e}")

    return generated_files


def main():
    """Command line interface for dummy-img-gen."""
    parser = argparse.ArgumentParser(
        description="Generate numbered placeholder images for development and testing",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("output_dir", help="Directory to save images")
    parser.add_argument("--count", type=int, default=10, help="Number of images to generate")
    parser.add_argument("--start", type=int, default=1, help="First number in sequence")
    parser.add_argument("--width", type=int, default=800, help="Image width in pixels")
    parser.add_argument("--height", type=int, default=600, help="Image height in pixels")
    parser.add_argument("--bg-color", default="#cccccc", help="Background color (hex/name)")
    parser.add_argument("--text-color", default="#333333", help="Text color (hex/name)")
    parser.add_argument("--format", choices=["png", "jpg", "webp"], default="png", help="Image format")
    parser.add_argument("--prefix", default="img_", help="Filename prefix")
    parser.add_argument("--font-path", help="Path to custom font (.ttf/.otf)")
    parser.add_argument("--font-size", type=int, help="Font size (auto-calculated if omitted)")
    parser.add_argument("--jpg-quality", type=int, default=90, help="JPEG/WebP quality (1-100)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files")
    parser.add_argument("--padding", type=float, default=0.2, help="Padding around text (0.0-0.5)")

    args = parser.parse_args()

    try:
        generate_placeholder_images(
            output_dir=args.output_dir,
            count=args.count,
            start_num=args.start,
            size=(args.width, args.height),
            bg_color=args.bg_color,
            text_color=args.text_color,
            format=args.format,
            prefix=args.prefix,
            font_path=args.font_path,
            font_size=args.font_size,
            jpg_quality=args.jpg_quality,
            overwrite=args.overwrite,
            padding=args.padding
        )
        print(f"\nSuccessfully generated {args.count} images in {args.output_dir}")

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
