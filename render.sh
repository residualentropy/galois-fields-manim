#!/bin/bash

echo "[render.sh] Activating venv..."
source ./.venv/bin/activate

echo "[render.sh] Rendering slides..."
manim-slides render $1 scenes.py $2

echo "[render.sh] Converting slides to HTML..."
manim-slides convert $2 output.html

echo "[render.sh] All done (visible at output.html)."
