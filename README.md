# pixelsynth

A creative coding tool that uses Python to procedurally compile and generate interactive p5.js (JavaScript) sketches for live webcam manipulation.

## Description

This project acts as a template engine. It allows you to select an artistic effect from a Python library and outputs a fully functional web directory (HTML + JS) ready to run locally.

**Available Effects:**
1. **ASCII Matrix**: Maps pixel brightness to characters.
2. **RGB Channel Split**: Offsets red/blue channels based on mouse position.
3. **Scanline Slit-Scan**: Time displacement effect.
4. **Kaleidoscope**: Radial mirror pattern.
5. **Standard Pixelate**: Reduces resolution by sampling colors at larger intervals.
6. **Circle Halftone**: Maps pixel brightness to the diameter of black circles on a white grid.
7. **Line Halftone**: Uses varying line thicknesses to represent brightness.
8. **Cross-Hatch**: Layers perpendicular lines; density increases with darkness.
9. **Hexagonal Mosaic**: Samples colors into a honeycomb grid.
10. **Triangle Mesh**: Divides the screen into equilateral triangles filled with average color.
11. **RGB Split Grid**: Displays R, G, and B channels as separate sub-pixels side-by-side.
12. **Voronoi Stained Glass**: Cells grow from random seeds, colored by the underlying pixel.
13. **Delaunay Triangulation**: Connects random points to form triangles, colored by the centroid.
14. **Quantized Dot Matrix**: Fixed-size dots that turn on/off based on a brightness threshold.
15. **Concentric Circles**: The image is constructed from concentric rings of varying colors.
16. **Brick Wall**: Staggered rectangles filled with the average color of that region.
17. **Sine Wave Modulation**: Rows of sine waves where amplitude is driven by pixel brightness.
18. **Binary Noise**: Random black/white pixels; probability of white is tied to source brightness.
19. **Adaptive Quadtree**: Recursively divides squares into smaller squares only in areas of high contrast.
20. **Solarization**: Inverts pixel values only above a certain brightness threshold.
21. **Posterization**: Reduces the color palette to a few distinct bands.
22. **Heatmap Mapping**: Maps grayscale brightness to a blue-green-red gradient.
23. **Sepia Tone**: Applies a brown-orange tint to a desaturated image.
24. **Duotone**: Maps shadows to one specific color and highlights to another.
25. **Inverted Luma**: Inverts brightness while keeping hue intact.
26. **Threshold**: Converts image to strict black and white based on a cutoff.
27. **Bit-Crush Color**: Reduces color depth (e.g., 3-bit color) for a retro look.
28. **Color Isolation**: Turns the image grayscale except for one specific hue.
29. **Luma Keying**: Makes pixels transparent if they are too bright/dark.
30. **False Color**: Swaps RGB channels (e.g., Red becomes Blue).


## How to Use

1. **Generate a Sketch**
   Run the generator script to choose an effect. The server will start automatically.
   ```bash
   python3 generator.py
   ```
