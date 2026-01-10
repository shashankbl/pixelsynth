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

## How to Use

1. **Generate a Sketch**
   Run the generator script to choose an effect. The server will start automatically.
   ```bash
   python3 generator.py
   ```
