import os
import platform
import argparse
import yaml
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def get_cross_platform_cjk_font():
   """
   DevOps helper to automatically locate a CJK-compatible font
   based on the host operating system.
   """
   # 1. First choice: Look for a local font file in your current working directory
   # You can download 'NotoSansTC-Regular.ttf' and put it in the same folder!
   if os.path.exists("NotoSansTC-Regular.ttf"):
       return "NotoSansTC-Regular.ttf"
      
   current_os = platform.system()
  
   # 2. Dynamic OS check
   if current_os == "Windows":
       paths = [
           "C:\\Windows\\Fonts\\msjh.ttc",       # 微軟正黑體 (Microsoft JhengHei)
           "C:\\Windows\\Fonts\\simsun.ttc",     # SimSun
           "C:\\Windows\\Fonts\\malgun.ttf"      # Malgun Gothic (Good Unicode coverage)
       ]
   elif current_os == "Darwin":  # macOS
       paths = [
           "/System/Library/Fonts/PingFang.ttc", # PingFang TC
           "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
           "/Library/Fonts/Arial Unicode.ttf"
       ]
   else:  # Linux (Ubuntu/Debian/CentOS)
       paths = [
           "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
           "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
           "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
       ]

   # Return the first font path that actually exists on the host machine
   for path in paths:
       if os.path.exists(path):
           print(f"[+] Found system CJK font at: {path}")
           return path
          
   return None

def generate_image(
    text: str,
    output_path: str = "output.png",
    size: tuple = (800, 600),
    bg_image_path: str = None,
    bg_color: str = "black",
    blur_radius: float = 0.0,
    text_color: str = "white",
    font_size: int = 36,
    line_spacing: int = 40,
    source: str = None,
    display_source: bool = False
):
   if bg_image_path and os.path.exists(bg_image_path):
       img = Image.open(bg_image_path).convert("RGB").resize(size, Image.Resampling.LANCZOS)
       if blur_radius > 0:
           img = img.filter(ImageFilter.GaussianBlur(blur_radius))
   else:
       img = Image.new("RGB", size, color=bg_color)

   draw = ImageDraw.Draw(img)

   # Automatically resolve the font path dynamically
   font_path = get_cross_platform_cjk_font()
  
   if font_path:
       font = ImageFont.truetype(font_path, font_size)
   else:
       # Absolute fallback if no system fonts match
       print("[-] CRITICAL: No CJK font found on host system. Falling back to default (will cause tofu).")
       print("[!] Quick fix: Download a .ttf font into this directory.")
       font = ImageFont.load_default()

   center_x, center_y = size[0] // 2, size[1] // 2

   draw.multiline_text(
       (center_x, center_y),
       text.strip(),
       fill=text_color,
       font=font,
       anchor="mm",
       align="center",
       spacing=line_spacing
   )

   # Render source if requested
   if display_source and source:
       source_font_size = int(font_size * 0.5)  # Source is 50% smaller
       if font_path:
           source_font = ImageFont.truetype(font_path, source_font_size)
       else:
           source_font = ImageFont.load_default()

       # Position: Bottom right with some padding (e.g. 5% of height)
       # Or centered below the main text. Let's do slightly below main text for now
       # Better: Bottom right of the image
       margin = int(size[1] * 0.05)
       source_text = f"— {source}"
       
       # Draw source text at the bottom right
       draw.text(
           (size[0] - margin, size[1] - margin),
           source_text,
           fill=text_color,
           font=source_font,
           anchor="rb" # Right Bottom
       )

   img.save(output_path)
   print(f"[+] Image successfully saved to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate motivational images from a YAML configuration file.")
    parser.add_argument("-f", "--file", type=str, help="Path to the YAML configuration file.")
    args = parser.parse_args()

    if args.file:
        if not os.path.exists(args.file):
            print(f"[-] Error: Configuration file '{args.file}' not found.")
            exit(1)
        
        with open(args.file, "r", encoding="utf-8") as f:
            tasks = yaml.safe_load(f)
            
        if not tasks or not isinstance(tasks, list):
            print("[-] Error: YAML file must contain a list of tasks.")
            exit(1)
            
        for i, task in enumerate(tasks):
            print(f"[*] Processing task {i+1}/{len(tasks)}...")
            # Use dictionary unpacking to pass arguments to generate_image
            # but handle 'size' tuple conversion if it's a list in YAML
            if "size" in task and isinstance(task["size"], list):
                task["size"] = tuple(task["size"])
                
            generate_image(**task)
    else:
        # Fallback if no file is provided
        print("[!] No configuration file provided. Use -f to specify a YAML file.")
        print("Example: python image_generator.py -f examples.yaml")
