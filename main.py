"""news-image-18 entry: copy the bundled poster to /output/entry.png.

The poster (poster.png) is a premium editorial infographic summarising
eight world-news stories first reported on 18 November 2026. It was rendered
once with gen_poster.py; shipping the finished bytes keeps the run offline,
deterministic and instant.
"""

import os
import shutil

OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "poster.png")
    shutil.copyfile(src, os.path.join(OUTPUT_DIR, "entry.png"))

if __name__ == "__main__":
    main()
