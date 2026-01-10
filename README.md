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
31. **Contrast Stretch**: Expands the range of brightness values to cover the full spectrum.
32. **Vignette Blur**: Blurs and darkens the edges of the frame while keeping the center sharp.
33. **Neon Glow**: Detects bright areas and adds a blurred bloom effect around them.
34. **CMYK Separation**: Simulates misaligned cyan, magenta, yellow, and black printing plates.
35. **Mirror Symmetry**: Splits the screen vertically/horizontally and reflects one side.
36. **Fish-Eye Lens**: Bulges the center of the image outward.
37. **Pinch Distortion**: Sucks pixels toward a specific point (mouse position).
38. **Swirl**: Rotates pixels around the center, with more rotation at the core.
39. **Sine Wave Ripple**: Displaces pixels horizontally based on a sine wave function.
40. **Pixel Sort**: Sorts pixels in a row/column by brightness.
41. **Slit-Scan (Spatial)**: Stretches the center vertical line of pixels to the edges.
42. **Broken Glass**: Voronoi cells that displace the image inside them slightly.
43. **Scanline Displacement**: Shifts every other horizontal line left or right.
44. **Polar Coordinates**: Maps the Cartesian (x,y) image into a circle.
45. **Droste Effect**: Recursively places the video frame inside itself.
46. **Tile Scramble**: Breaks image into a grid and randomly swaps tile positions.
47. **Barrel Distortion**: Squeezes the edges of the image inward.
48. **Liquid Displacement**: Uses Perlin noise to warp pixel coordinates smoothly.
49. **Motion Blur**: Blends the current frame with the previous 5 frames with opacity.
50. **Ghosting / Trails**: Only updates the background slowly, leaving trails of moving objects.
51. **Slit-Scan (Temporal)**: Each column of pixels comes from a different point in time.
52. **Frame Delay Grid**: A grid of videos, each delayed by 1 second more than the last.
53. **Motion Detection**: Subtracts the previous frame from the current one to show only movement.
54. **RGB Delay**: Shows Red channel instantly, Green with 5-frame delay, Blue with 10-frame delay.
55. **Video Feedback**: Draws the previous frame slightly zoomed in and rotated.
56. **Pixel Accumulation**: Pixels "pile up" at the bottom if they are dark (physics simulation).
57. **Freeze Frame Mask**: Freezes parts of the screen that haven't moved in X seconds.
58. **Time Displacement Map**: Uses a grayscale map to determine which "time" (past frame) to sample from.
59. **Optical Flow Particles**: Particles flow in the direction of movement detected in the video.
60. **Frame Averaging**: Averages the last 100 frames to remove moving objects entirely.


## How to Use

1. **Generate a Sketch**
   Run the generator script to choose an effect. The server will start automatically.
   ```bash
   python3 generator.py
   ```
