"""
PixelSynth Effects Library
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
    },
    "4": {
        "name": "Kaleidoscope",
        "description": "Radial mirror pattern. paramA: Slices, paramB: Zoom/Offset.",
        "global_vars": "",
        "draw_loop": """
  background(0);
  
  // Kaleidoscope settings
  // paramA controls number of slices (4 to 24)
  let slices = int(map(paramA, 0, 1, 4, 24));
  let angle = TWO_PI / slices;
  let radius = max(width, height) * 1.5; // Ensure coverage
  
  translate(width / 2, height / 2);
  
  for (let i = 0; i < slices; i++) {
    push();
    rotate(i * angle);
    
    // Mirror every other slice for seamless pattern
    if (i % 2 === 1) scale(1, -1);
    
    // Use native Canvas API to clip a triangular wedge
    drawingContext.save();
    drawingContext.beginPath();
    drawingContext.moveTo(0, 0);
    drawingContext.lineTo(radius, 0);
    drawingContext.lineTo(radius * cos(angle), radius * sin(angle));
    drawingContext.closePath();
    drawingContext.clip();
    
    // Draw video
    // paramB controls the offset/zoom into the texture
    let zoom = map(paramB, 0, 1, 1.0, 2.5);
    
    imageMode(CENTER);
    // Rotate the source slightly to animate or align
    rotate(frameCount * 0.01);
    image(video, 0, 0, width * zoom, height * zoom);
    
    drawingContext.restore();
    pop();
  }
"""
    },
    "5": {
        "name": "Standard Pixelate",
        "description": "Reduces resolution by sampling colors at larger intervals. (Ref: 8-bit Art)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  video.loadPixels();
  
  // paramA controls pixel size (from 4px to 40px)
  let gridSize = floor(map(paramA, 0, 1, 4, 40));
  
  noStroke();
  
  for (let y = 0; y < height; y += gridSize) {
    for (let x = 0; x < width; x += gridSize) {
      // Get pixel color from the video array at the current grid position
      let index = (x + y * width) * 4;
      
      fill(video.pixels[index], video.pixels[index + 1], video.pixels[index + 2]);
      rect(x, y, gridSize, gridSize);
    }
  }
"""
    },
    "6": {
        "name": "Circle Halftone",
        "description": "Maps pixel brightness to the diameter of black circles on a white grid. (Ref: Newspaper Print)",
        "global_vars": "",
        "draw_loop": """
  background(255);
  video.loadPixels();
  noStroke();
  fill(0);

  // paramA controls grid size (resolution)
  let gridSize = floor(map(paramA, 0, 1, 6, 20));

  for (let y = 0; y < height; y += gridSize) {
    for (let x = 0; x < width; x += gridSize) {
      let index = (x + y * width) * 4;
      let r = video.pixels[index];
      let g = video.pixels[index + 1];
      let b = video.pixels[index + 2];
      
      // Calculate brightness
      let bright = (r + g + b) / 3;

      // Map brightness to circle diameter (darker = larger circle)
      let diameter = map(bright, 0, 255, gridSize, 0);
      
      ellipse(x + gridSize / 2, y + gridSize / 2, diameter);
    }
  }
"""
    },
    "7": {
        "name": "Line Halftone",
        "description": "Uses varying line thicknesses to represent brightness. (Ref: Engraving)",
        "global_vars": "",
        "draw_loop": """
  background(255);
  video.loadPixels();
  stroke(0);
  
  // paramA controls line density/resolution
  let step = floor(map(paramA, 0, 1, 5, 20));
  
  for (let y = 0; y < height; y += step) {
    for (let x = 0; x < width; x += step) {
      const index = (x + y * width) * 4;
      const r = video.pixels[index];
      const g = video.pixels[index + 1];
      const b = video.pixels[index + 2];
      
      const bright = (r + g + b) / 3;
      
      // Map brightness to line thickness (Darker = thicker lines)
      let weight = map(bright, 0, 255, step, 0);
      
      strokeWeight(weight);
      line(x, y, x + step, y + step);
    }
  }
"""
    },
    "8": {
        "name": "Cross-Hatch",
        "description": "Layers perpendicular lines; density increases with darkness. (Ref: Sketching)",
        "global_vars": "",
        "draw_loop": """
  background(255);
  video.loadPixels();
  stroke(0);
  
  // paramA controls line spacing
  let step = floor(map(paramA, 0, 1, 8, 20));
  strokeWeight(1); // Keep lines thin for sketching look
  
  for (let y = 0; y < height; y += step) {
    for (let x = 0; x < width; x += step) {
      const index = (x + y * width) * 4;
      const r = video.pixels[index];
      const g = video.pixels[index + 1];
      const b = video.pixels[index + 2];
      
      const bright = (r + g + b) / 3;
      
      // Layer 1: Light shading (Diagonal /)
      if (bright < 200) {
        line(x, y, x + step, y + step);
      }
      
      // Layer 2: Mid-tone shading (Diagonal \\)
      if (bright < 150) {
        line(x + step, y, x, y + step);
      }
      
      // Layer 3: Dark shading (Vertical |)
      if (bright < 100) {
        line(x, y, x, y + step);
      }
    }
  }
"""
    },
    "9": {
        "name": "Hexagonal Mosaic",
        "description": "Samples colors into a honeycomb grid. (Ref: Tiling)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  video.loadPixels();
  noStroke();
  
  // paramA controls hexagon radius
  let r = floor(map(paramA, 0, 1, 3, 20));
  let h = r * sqrt(3);
  
  // Function to draw a single hexagon
  function drawHex(cx, cy, rad) {
    let px = floor(constrain(cx, 0, width-1));
    let py = floor(constrain(cy, 0, height-1));
    let idx = (px + py * width) * 4;
    
    fill(video.pixels[idx], video.pixels[idx+1], video.pixels[idx+2]);
    
    beginShape();
    for (let i = 0; i < 6; i++) {
      let angle = TWO_PI / 6 * i;
      vertex(cx + rad * cos(angle), cy + rad * sin(angle));
    }
    endShape(CLOSE);
  }

  for (let y = -h; y < height + h; y += h) {
    for (let x = -r; x < width + r * 3; x += r * 3) {
       drawHex(x, y, r);
       drawHex(x + r * 1.5, y + h / 2, r);
    }
  }
"""
    },
    "10": {
        "name": "Triangle Mesh",
        "description": "Divides the screen into equilateral triangles filled with average color. (Ref: Low Poly)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  video.loadPixels();
  noStroke();
  
  // paramA controls triangle scale
  let scale = floor(map(paramA, 0, 1, 10, 50));
  let h = scale * sqrt(3) / 2;
  
  for (let j = 0; j <= height / h + 1; j++) {
    for (let i = 0; i <= width / (scale / 2) + 1; i++) {
      let x = i * (scale / 2) - scale;
      let y = j * h;
      
      // Determine orientation: (i + j) % 2 determines if it points up or down
      let isUp = (i + j) % 2 === 0;
      
      let x1, y1, x2, y2, x3, y3;
      
      if (isUp) {
         x1 = x;             y1 = y + h;
         x2 = x + scale;     y2 = y + h;
         x3 = x + scale / 2; y3 = y;
      } else {
         x1 = x;             y1 = y;
         x2 = x + scale;     y2 = y;
         x3 = x + scale / 2; y3 = y + h;
      }
      
      let cx = (x1 + x2 + x3) / 3;
      let cy = (y1 + y2 + y3) / 3;
      
      let px = floor(constrain(cx, 0, width - 1));
      let py = floor(constrain(cy, 0, height - 1));
      let idx = (px + py * width) * 4;
      
      fill(video.pixels[idx], video.pixels[idx+1], video.pixels[idx+2]);
      triangle(x1, y1, x2, y2, x3, y3);
    }
  }
"""
    },
    "11": {
        "name": "RGB Split Grid",
        "description": "Displays R, G, and B channels as separate sub-pixels side-by-side. (Ref: CRT Monitor)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  video.loadPixels();
  noStroke();
  
  // paramA controls pixel size (CRT phosphor size)
  let scale = floor(map(paramA, 0, 1, 3, 30));
  let subW = scale / 3;
  
  for (let y = 0; y < height; y += scale) {
    for (let x = 0; x < width; x += scale) {
      let index = (x + y * width) * 4;
      
      let r = video.pixels[index];
      let g = video.pixels[index + 1];
      let b = video.pixels[index + 2];
      
      // Red sub-pixel
      fill(r, 0, 0);
      rect(x, y, subW, scale);
      
      // Green sub-pixel
      fill(0, g, 0);
      rect(x + subW, y, subW, scale);
      
      // Blue sub-pixel
      fill(0, 0, b);
      rect(x + 2 * subW, y, subW, scale);
    }
  }
"""
    },
    "12": {
        "name": "Voronoi Stained Glass",
        "description": "Cells grow from random seeds, colored by the underlying pixel. (Ref: Voronoi Diagram)",
        "global_vars": "let vSeeds = [];",
        "draw_loop": """
  background(0);
  video.loadPixels();
  noStroke();
  
  // paramA controls number of seeds (10 to 50)
  let numSeeds = floor(map(paramA, 0, 1, 10, 100));
  
  // Regenerate seeds if count changes
  if (vSeeds.length !== numSeeds) {
    vSeeds = [];
    for (let i = 0; i < numSeeds; i++) {
      vSeeds.push({
        x: random(width),
        y: random(height)
      });
    }
  }
  
  // Resolution of the Voronoi approximation (higher step = blockier but faster)
  let step = 6; 
  
  for (let y = 0; y < height; y += step) {
    for (let x = 0; x < width; x += step) {
      let minDist = Infinity;
      let closestSeedIndex = -1;
      
      // Find closest seed
      for (let i = 0; i < vSeeds.length; i++) {
        let dx = x - vSeeds[i].x;
        let dy = y - vSeeds[i].y;
        let d = dx*dx + dy*dy; // Squared distance is faster
        if (d < minDist) {
          minDist = d;
          closestSeedIndex = i;
        }
      }
      
      // Color based on the video pixel at the SEED's location (Stained Glass look)
      let s = vSeeds[closestSeedIndex];
      let sx = floor(constrain(s.x, 0, width - 1));
      let sy = floor(constrain(s.y, 0, height - 1));
      let idx = (sx + sy * width) * 4;
      
      fill(video.pixels[idx], video.pixels[idx+1], video.pixels[idx+2]);
      rect(x, y, step, step);
    }
  }
"""
    }
}