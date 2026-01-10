"""
PyPrism Effects Library
Stores the logic for procedural generation of p5.js sketches.
"""

EFFECTS = {
    "1": {
        "name": "ASCII Matrix",
        "description": "Maps pixel brightness to characters. paramA controls resolution.",
        "global_vars": """
const density = "Ñ@#W$9876543210?!abc;:+=-,._ ";
""",
        "draw_loop": """
  background(0);
  video.loadPixels(); // Load webcam pixels into memory
  
  // Calculate grid resolution based on paramA (Mouse X)
  // Ranges from 5px to 20px blocks
  let w = floor(map(paramA, 0, 1, 5, 20));
  let h = w;
  
  fill(255);
  textSize(w);
  
  // Loop through the video pixels in a grid
  for (let i = 0; i < width; i += w) {
    for (let j = 0; j < height; j += h) {
      // Calculate the index of the pixel in the video array
      const pixelIndex = (i + j * video.width) * 4;
      
      const r = video.pixels[pixelIndex + 0];
      const g = video.pixels[pixelIndex + 1];
      const b = video.pixels[pixelIndex + 2];
      
      // Calculate brightness
      const avg = (r + g + b) / 3;
      
      // Map brightness to a character in the density string
      const len = density.length;
      const charIndex = floor(map(avg, 0, 255, len - 1, 0));
      
      text(density.charAt(charIndex), i, j);
    }
  }
"""
    },
    "2": {
        "name": "RGB Channel Split",
        "description": "Offsets Red and Blue channels. paramA controls offset amount.",
        "global_vars": "",
        "draw_loop": """
  background(0);
  video.loadPixels(); // Load webcam pixels
  loadPixels();       // Load canvas pixels to write to
  
  // Determine offset based on paramA (Mouse X)
  // Max offset of 50 pixels
  let offset = floor(map(paramA, 0, 1, 0, 50));
  
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      let index = (x + y * width) * 4;
      
      // Calculate shifted indices
      // Red channel: shifted left
      let rIndex = ((x - offset + width) % width + y * width) * 4;
      
      // Blue channel: shifted right
      let bIndex = ((x + offset) % width + y * width) * 4;
      
      // Assign pixels
      pixels[index + 0] = video.pixels[rIndex + 0]; // Red
      pixels[index + 1] = video.pixels[index + 1];  // Green (Original)
      pixels[index + 2] = video.pixels[bIndex + 2]; // Blue
      pixels[index + 3] = 255;                      // Alpha
    }
  }
  updatePixels(); // Push changes to canvas
"""
    },
    "3": {
        "name": "Scanline Slit-Scan",
        "description": "Time displacement effect. Copies center column to moving scanline.",
        "global_vars": "let scanX = 0;",
        "draw_loop": """
  video.loadPixels();
  
  // Copy a vertical slice (1px wide) from the center of the video
  // to the current scanX position on the canvas
  copy(video, width/2, 0, 1, height, scanX, 0, 1, height);
  
  // Move the scanline forward
  scanX = (scanX + 1) % width;
  
  // Draw a red indicator line at the current scan position
  stroke(255, 0, 0);
  line(scanX, 0, scanX, height);
"""
    }
}