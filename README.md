# pixelsynth

A creative coding tool that uses Python to procedurally compile and generate interactive p5.js (JavaScript) sketches for live webcam manipulation.

## Description

This project acts as a template engine. It allows you to select an artistic effect from a Python library and outputs a fully functional web directory (HTML + JS) ready to run locally.

**Available Effects:**
1. **ASCII Matrix**: Maps pixel brightness to characters.
2. **RGB Channel Split**: Offsets red/blue channels based on mouse position.
3. **Scanline Slit-Scan**: Time displacement effect.

## How to Use

1. **Generate a Sketch**
   Run the generator script to choose an effect. The server will start automatically.
   ```bash
   python3 generator.py
   ```
