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
    },
    "13": {
        "name": "Delaunay Triangulation",
        "description": "Connects random points to form triangles, colored by the centroid. (Ref: Mesh Generation)",
        "global_vars": """
let dPoints = [];
let dTriangles = [];
let lastParamA = -1;

function circumcircle(a, b, c) {
  let D = 2 * (a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y));
  // Avoid division by zero for collinear points
  if (abs(D) < 0.001) return {x:0, y:0, r:Infinity};
  let ux = ((a.x * a.x + a.y * a.y) * (b.y - c.y) + (b.x * b.x + b.y * b.y) * (c.y - a.y) + (c.x * c.x + c.y * c.y) * (a.y - b.y)) / D;
  let uy = ((a.x * a.x + a.y * a.y) * (c.x - b.x) + (b.x * b.x + b.y * b.y) * (a.x - c.x) + (c.x * c.x + c.y * c.y) * (b.x - a.x)) / D;
  let r = dist(ux, uy, a.x, a.y);
  return { x: ux, y: uy, r: r };
}
""",
        "draw_loop": """
  background(0);
  video.loadPixels();
  stroke(0);
  strokeWeight(1);
  
  // paramA controls number of points (10 to 25)
  // Kept low because brute-force Delaunay is O(N^4)
  let numPoints = floor(map(paramA, 0, 1, 10, 25));
  
  if (numPoints !== lastParamA) {
    lastParamA = numPoints;
    dPoints = [];
    
    // Add random points
    for (let i = 0; i < numPoints; i++) {
      dPoints.push(createVector(random(width), random(height)));
    }
    // Add corners to ensure screen coverage
    dPoints.push(createVector(0, 0));
    dPoints.push(createVector(width, 0));
    dPoints.push(createVector(width, height));
    dPoints.push(createVector(0, height));
    
    // Brute force Delaunay
    dTriangles = [];
    for (let i = 0; i < dPoints.length; i++) {
      for (let j = i + 1; j < dPoints.length; j++) {
        for (let k = j + 1; k < dPoints.length; k++) {
          let p1 = dPoints[i];
          let p2 = dPoints[j];
          let p3 = dPoints[k];
          
          let circle = circumcircle(p1, p2, p3);
          let valid = true;
          
          // Check if any other point is inside circumcircle
          for (let m = 0; m < dPoints.length; m++) {
            if (m === i || m === j || m === k) continue;
            if (dist(dPoints[m].x, dPoints[m].y, circle.x, circle.y) < circle.r - 0.1) {
              valid = false;
              break;
            }
          }
          
          if (valid) {
            dTriangles.push([p1, p2, p3]);
          }
        }
      }
    }
  }
  
  // Draw triangles
  for (let t of dTriangles) {
    let p1 = t[0];
    let p2 = t[1];
    let p3 = t[2];
    
    // Centroid
    let cx = (p1.x + p2.x + p3.x) / 3;
    let cy = (p1.y + p2.y + p3.y) / 3;
    
    let px = floor(constrain(cx, 0, width - 1));
    let py = floor(constrain(cy, 0, height - 1));
    let idx = (px + py * width) * 4;
    
    fill(video.pixels[idx], video.pixels[idx+1], video.pixels[idx+2]);
    triangle(p1.x, p1.y, p2.x, p2.y, p3.x, p3.y);
  }
"""
    },
    "14": {
        "name": "Quantized Dot Matrix",
        "description": "Fixed-size dots that turn on/off based on a brightness threshold. (Ref: LED Sign)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  video.loadPixels();
  noStroke();
  
  // paramA controls grid size (LED density)
  let step = floor(map(paramA, 0, 1, 8, 30));
  let dotSize = step * 0.8; // Leave some spacing
  
  for (let y = 0; y < height; y += step) {
    for (let x = 0; x < width; x += step) {
      let index = (x + y * width) * 4;
      let r = video.pixels[index];
      let g = video.pixels[index + 1];
      let b = video.pixels[index + 2];
      let bright = (r + g + b) / 3;
      
      // Threshold check: If bright enough, show color, else show dim 'off' state
      if (bright > 80) fill(r, g, b);
      else fill(30);
      
      ellipse(x + step/2, y + step/2, dotSize);
    }
  }
"""
    },
    "15": {
        "name": "Concentric Circles",
        "description": "The image is constructed from concentric rings of varying colors. (Ref: Vinyl Record)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  video.loadPixels();
  noFill();
  
  let cx = width / 2;
  let cy = height / 2;
  let maxRadius = dist(0, 0, cx, cy) + 20;
  
  // paramA controls ring thickness
  let step = floor(map(paramA, 0, 1, 5, 50));
  strokeWeight(step);
  
  for (let r = 0; r < maxRadius; r += step) {
    let sumR = 0, sumG = 0, sumB = 0;
    let count = 0;
    
    // Sample points along the ring to get an average color
    for (let angle = 0; angle < TWO_PI; angle += 0.1) {
      let x = floor(cx + cos(angle) * r);
      let y = floor(cy + sin(angle) * r);
      
      if (x >= 0 && x < width && y >= 0 && y < height) {
        let idx = (x + y * width) * 4;
        sumR += video.pixels[idx];
        sumG += video.pixels[idx+1];
        sumB += video.pixels[idx+2];
        count++;
      }
    }
    
    if (count > 0) {
      stroke(sumR / count, sumG / count, sumB / count);
      ellipse(cx, cy, r * 2, r * 2);
    }
  }
"""
    },
    "16": {
        "name": "Brick Wall",
        "description": "Staggered rectangles filled with the average color of that region. (Ref: Masonry)",
        "global_vars": "",
        "draw_loop": """
  background(50); // Dark mortar color
  video.loadPixels();
  stroke(50);
  strokeWeight(2);
  
  // paramA controls brick height (width is 2x height)
  let bh = floor(map(paramA, 0, 1, 10, 40));
  let bw = bh * 2;
  
  for (let y = 0; y < height; y += bh) {
    // Stagger every other row
    let row = floor(y / bh);
    let startX = (row % 2 === 0) ? 0 : -bw / 2;
    
    for (let x = startX; x < width; x += bw) {
      let rSum = 0, gSum = 0, bSum = 0, count = 0;
      
      // Sample pixels within the brick to calculate average
      // Using a step size of 4 for performance
      for (let sy = 0; sy < bh; sy += 4) {
        for (let sx = 0; sx < bw; sx += 4) {
          let px = floor(x + sx);
          let py = floor(y + sy);
          
          if (px >= 0 && px < width && py >= 0 && py < height) {
            let idx = (px + py * width) * 4;
            rSum += video.pixels[idx];
            gSum += video.pixels[idx+1];
            bSum += video.pixels[idx+2];
            count++;
          }
        }
      }
      
      if (count > 0) {
        fill(rSum / count, gSum / count, bSum / count);
        rect(x, y, bw, bh);
      }
    }
  }
"""
    },
    "17": {
        "name": "Sine Wave Modulation",
        "description": "Rows of sine waves where amplitude is driven by pixel brightness. (Ref: Joy Division Album Cover)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  video.loadPixels();
  stroke(255);
  fill(0); // Fill black to occlude lines behind
  strokeWeight(1);
  
  // paramA controls vertical spacing
  let step = floor(map(paramA, 0, 1, 10, 40));
  
  for (let y = step; y < height; y += step) {
    beginShape();
    vertex(0, y); // Anchor start
    for (let x = 0; x < width; x += 5) {
      let index = (x + y * width) * 4;
      let bright = (video.pixels[index] + video.pixels[index+1] + video.pixels[index+2]) / 3;
      let amp = map(bright, 0, 255, 0, step * 1.5);
      vertex(x, y - amp);
    }
    vertex(width, y); // Anchor end
    endShape();
  }
"""
    },
    "18": {
        "name": "Binary Noise",
        "description": "Random black/white pixels; probability of white is tied to source brightness. (Ref: Dithering)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  video.loadPixels();
  noStroke();
  
  // paramA controls pixel size (resolution)
  let step = floor(map(paramA, 0, 1, 1, 10));
  
  for (let y = 0; y < height; y += step) {
    for (let x = 0; x < width; x += step) {
      let index = (x + y * width) * 4;
      let r = video.pixels[index];
      let g = video.pixels[index + 1];
      let b = video.pixels[index + 2];
      let bright = (r + g + b) / 3;
      
      // Stochastic dithering:
      // Probability of being white is proportional to brightness
      if (random(255) < bright) fill(255);
      else fill(0);
      
      rect(x, y, step, step);
    }
  }
"""
    },
    "19": {
        "name": "Adaptive Quadtree",
        "description": "Recursively divides squares into smaller squares only in areas of high contrast. (Ref: Compression)",
        "global_vars": """
function qtColor(x, y, w, h) {
  let r = 0, g = 0, b = 0;
  let count = 0;
  let step = 2;
  for (let j = y; j < y + h; j += step) {
    for (let i = x; i < x + w; i += step) {
      if (i >= width || j >= height) continue;
      let idx = (floor(i) + floor(j) * width) * 4;
      r += video.pixels[idx];
      g += video.pixels[idx+1];
      b += video.pixels[idx+2];
      count++;
    }
  }
  if (count === 0) return {r:0, g:0, b:0};
  return {r: r/count, g: g/count, b: b/count};
}

function drawQuadtree(x, y, w, h, threshold) {
  let avg = qtColor(x, y, w, h);
  
  // Calculate error (variance)
  let err = 0;
  let count = 0;
  let step = 4;
  for (let j = y; j < y + h; j += step) {
    for (let i = x; i < x + w; i += step) {
      if (i >= width || j >= height) continue;
      let idx = (floor(i) + floor(j) * width) * 4;
      err += abs(video.pixels[idx] - avg.r) + abs(video.pixels[idx+1] - avg.g) + abs(video.pixels[idx+2] - avg.b);
      count++;
    }
  }
  err = (count > 0) ? err / count : 0;

  if (err > threshold && w > 6) {
    let hw = w / 2;
    let hh = h / 2;
    drawQuadtree(x, y, hw, hh, threshold);
    drawQuadtree(x + hw, y, hw, hh, threshold);
    drawQuadtree(x, y + hh, hw, hh, threshold);
    drawQuadtree(x + hw, y + hh, hw, hh, threshold);
  } else {
    fill(avg.r, avg.g, avg.b);
    rect(x, y, w, h);
  }
}
""",
        "draw_loop": """
  background(0);
  video.loadPixels();
  noStroke();
  
  // paramA controls threshold (Detail level)
  let threshold = map(paramA, 0, 1, 100, 15);
  
  drawQuadtree(0, 0, width, height, threshold);
"""
    },
    "20": {
        "name": "Solarization",
        "description": "Inverts pixel values only above a certain brightness threshold. (Ref: Man Ray Photography)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  video.loadPixels();
  loadPixels();
  
  // paramA controls the threshold
  let threshold = map(paramA, 0, 1, 0, 255);
  
  for (let i = 0; i < video.pixels.length; i += 4) {
    let r = video.pixels[i];
    let g = video.pixels[i + 1];
    let b = video.pixels[i + 2];
    
    let bright = (r + g + b) / 3;
    
    if (bright > threshold) {
      pixels[i] = 255 - r;
      pixels[i + 1] = 255 - g;
      pixels[i + 2] = 255 - b;
    } else {
      pixels[i] = r;
      pixels[i + 1] = g;
      pixels[i + 2] = b;
    }
    pixels[i + 3] = 255;
  }
  updatePixels();
"""
    },
    "21": {
        "name": "Posterization",
        "description": "Reduces the color palette to a few distinct bands (e.g., 4 colors). (Ref: Silk Screen)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  video.loadPixels();
  loadPixels();
  
  // paramA controls the number of color levels (2 to 8)
  let levels = floor(map(paramA, 0, 1, 2, 8));
  
  // Calculate bin size for quantization
  let binSize = 255 / (levels - 1);
  
  for (let i = 0; i < video.pixels.length; i += 4) {
    let r = video.pixels[i];
    let g = video.pixels[i + 1];
    let b = video.pixels[i + 2];
    
    // Quantize each channel to the nearest level
    pixels[i] = floor(r / 255 * (levels - 1) + 0.5) * binSize;
    pixels[i + 1] = floor(g / 255 * (levels - 1) + 0.5) * binSize;
    pixels[i + 2] = floor(b / 255 * (levels - 1) + 0.5) * binSize;
    pixels[i + 3] = 255;
  }
  updatePixels();
"""
    },
    "22": {
        "name": "Heatmap Mapping",
        "description": "Maps grayscale brightness to a blue-green-red gradient. (Ref: Thermal Camera)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  video.loadPixels();
  loadPixels();
  
  // paramA shifts the color spectrum center
  let shift = map(paramA, 0, 1, -50, 50);
  
  for (let i = 0; i < video.pixels.length; i += 4) {
    let r = video.pixels[i];
    let g = video.pixels[i + 1];
    let b = video.pixels[i + 2];
    let bright = (r + g + b) / 3;
    
    let val = constrain(bright + shift, 0, 255);
    let outR = 0, outG = 0, outB = 0;
    
    // Thermal gradient: Blue (cold) -> Green -> Red (hot)
    if (val < 128) {
      // Blue to Green
      outR = 0;
      outG = map(val, 0, 128, 0, 255);
      outB = map(val, 0, 128, 255, 0);
    } else {
      // Green to Red
      outR = map(val, 128, 255, 0, 255);
      outG = map(val, 128, 255, 255, 0);
      outB = 0;
    }
    
    pixels[i] = outR;
    pixels[i + 1] = outG;
    pixels[i + 2] = outB;
    pixels[i + 3] = 255;
  }
  updatePixels();
"""
    },
    "23": {
        "name": "Sepia Tone",
        "description": "Applies a brown-orange tint to a desaturated image. (Ref: Old Photography)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  video.loadPixels();
  loadPixels();
  
  // paramA controls intensity
  let amount = map(paramA, 0, 1, 0.5, 1.0);
  
  for (let i = 0; i < video.pixels.length; i += 4) {
    let r = video.pixels[i];
    let g = video.pixels[i + 1];
    let b = video.pixels[i + 2];
    
    let tr = (r * 0.393) + (g * 0.769) + (b * 0.189);
    let tg = (r * 0.349) + (g * 0.686) + (b * 0.168);
    let tb = (r * 0.272) + (g * 0.534) + (b * 0.131);
    
    pixels[i] = lerp(r, constrain(tr, 0, 255), amount);
    pixels[i + 1] = lerp(g, constrain(tg, 0, 255), amount);
    pixels[i + 2] = lerp(b, constrain(tb, 0, 255), amount);
    pixels[i + 3] = 255;
  }
  updatePixels();
"""
    },
    "24": {
        "name": "Duotone",
        "description": "Maps shadows to one specific color and highlights to another. (Ref: Spotify Wraps)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  video.loadPixels();
  loadPixels();
  
  // Define colors: Deep Purple (Shadows) -> Lime Green (Highlights)
  let r1 = 50, g1 = 0, b1 = 150;
  let r2 = 200, g2 = 255, b2 = 50;
  
  for (let i = 0; i < video.pixels.length; i += 4) {
    let bright = (video.pixels[i] + video.pixels[i+1] + video.pixels[i+2]) / 3;
    let t = bright / 255;
    
    pixels[i] = r1 + (r2 - r1) * t;
    pixels[i + 1] = g1 + (g2 - g1) * t;
    pixels[i + 2] = b1 + (b2 - b1) * t;
    pixels[i + 3] = 255;
  }
  updatePixels();
"""
    },
    "25": {
        "name": "Inverted Luma",
        "description": "Inverts brightness while keeping hue intact. (Ref: Negative Film)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  video.loadPixels();
  loadPixels();
  
  for (let i = 0; i < video.pixels.length; i += 4) {
    let r = video.pixels[i] / 255;
    let g = video.pixels[i + 1] / 255;
    let b = video.pixels[i + 2] / 255;
    
    let max = Math.max(r, g, b), min = Math.min(r, g, b);
    let h, s, l = (max + min) / 2;

    if(max == min){ h = s = 0; } 
    else {
        let d = max - min;
        s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
        switch(max){
            case r: h = (g - b) / d + (g < b ? 6 : 0); break;
            case g: h = (b - r) / d + 2; break;
            case b: h = (r - g) / d + 4; break;
        }
        h /= 6;
    }
    
    // Invert Lightness
    l = 1 - l;
    
    let r1, g1, b1;
    if(s === 0){ r1 = g1 = b1 = l; } 
    else {
        let hue2rgb = function(p, q, t){
            if(t < 0) t += 1;
            if(t > 1) t -= 1;
            if(t < 1/6) return p + (q - p) * 6 * t;
            if(t < 1/2) return q;
            if(t < 2/3) return p + (q - p) * (2/3 - t) * 6;
            return p;
        }
        let q = l < 0.5 ? l * (1 + s) : l + s - l * s;
        let p = 2 * l - q;
        r1 = hue2rgb(p, q, h + 1/3);
        g1 = hue2rgb(p, q, h);
        b1 = hue2rgb(p, q, h - 1/3);
    }
    
    pixels[i] = r1 * 255;
    pixels[i + 1] = g1 * 255;
    pixels[i + 2] = b1 * 255;
    pixels[i + 3] = 255;
  }
  updatePixels();
"""
    },
    "26": {
        "name": "Threshold",
        "description": "Converts image to strict black and white based on a cutoff. (Ref: Photocopy)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  video.loadPixels();
  loadPixels();
  
  // paramA controls the threshold level
  let thresh = map(paramA, 0, 1, 0, 255);
  
  for (let i = 0; i < video.pixels.length; i += 4) {
    let bright = (video.pixels[i] + video.pixels[i+1] + video.pixels[i+2]) / 3;
    let val = (bright > thresh) ? 255 : 0;
    pixels[i] = pixels[i+1] = pixels[i+2] = val;
    pixels[i+3] = 255;
  }
  updatePixels();
"""
    },
    "27": {
        "name": "Bit-Crush Color",
        "description": "Reduces color depth (e.g., 3-bit color) for a retro look. (Ref: Gameboy)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  video.loadPixels();
  loadPixels();
  
  // paramA controls bit depth (1 to 8 bits)
  let bits = floor(map(paramA, 0, 1, 1, 8));
  let factor = 255 / (pow(2, bits) - 1);
  
  for (let i = 0; i < video.pixels.length; i += 4) {
    let r = video.pixels[i];
    let g = video.pixels[i + 1];
    let b = video.pixels[i + 2];
    
    pixels[i] = floor(r / factor) * factor;
    pixels[i + 1] = floor(g / factor) * factor;
    pixels[i + 2] = floor(b / factor) * factor;
    pixels[i + 3] = 255;
  }
  updatePixels();
"""
    },
    "28": {
        "name": "Color Isolation",
        "description": "Turns the image grayscale except for one specific hue (e.g., keep only red). (Ref: Sin City)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  video.loadPixels();
  loadPixels();
  
  // paramA controls target hue (0-360)
  let targetHue = map(paramA, 0, 1, 0, 360);
  let threshold = 30; // Hue tolerance
  
  for (let i = 0; i < video.pixels.length; i += 4) {
    let r = video.pixels[i];
    let g = video.pixels[i + 1];
    let b = video.pixels[i + 2];
    
    // Convert RGB to Hue
    let rN = r/255, gN = g/255, bN = b/255;
    let max = Math.max(rN, gN, bN), min = Math.min(rN, gN, bN);
    let h = 0;

    if (max !== min) {
      let d = max - min;
      switch(max) {
        case rN: h = (gN - bN) / d + (gN < bN ? 6 : 0); break;
        case gN: h = (bN - rN) / d + 2; break;
        case bN: h = (rN - gN) / d + 4; break;
      }
      h *= 60;
    }

    // Calculate distance handling 360 wrap-around
    let dist = Math.abs(h - targetHue);
    if (dist > 180) dist = 360 - dist;

    if (dist < threshold) {
      pixels[i] = r;
      pixels[i+1] = g;
      pixels[i+2] = b;
    } else {
      let gray = (r + g + b) / 3;
      pixels[i] = pixels[i+1] = pixels[i+2] = gray;
    }
    pixels[i+3] = 255;
  }
  updatePixels();
"""
    },
    "29": {
        "name": "Luma Keying",
        "description": "Makes pixels transparent if they are too bright/dark (green screen effect). (Ref: Chroma Key)",
        "global_vars": "",
        "draw_loop": """
  clear(); // Clear canvas to transparent
  video.loadPixels();
  loadPixels();
  
  // paramA controls brightness threshold
  let thresh = map(paramA, 0, 1, 0, 255);
  
  for (let i = 0; i < video.pixels.length; i += 4) {
    let r = video.pixels[i];
    let g = video.pixels[i + 1];
    let b = video.pixels[i + 2];
    let bright = (r + g + b) / 3;
    
    pixels[i] = r;
    pixels[i+1] = g;
    pixels[i+2] = b;
    
    // If brighter than threshold, make transparent
    pixels[i+3] = (bright > thresh) ? 0 : 255;
  }
  updatePixels();
"""
    },
    "30": {
        "name": "False Color",
        "description": "Swaps RGB channels (e.g., Red becomes Blue). (Ref: Infrared Photography)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  video.loadPixels();
  loadPixels();
  
  // paramA selects channel permutation (0-5)
  let mode = floor(map(paramA, 0, 1, 0, 6));
  
  for (let i = 0; i < video.pixels.length; i += 4) {
    let r = video.pixels[i];
    let g = video.pixels[i + 1];
    let b = video.pixels[i + 2];
    
    let newR = r, newG = g, newB = b;
    
    if (mode === 1) { newR = r; newG = b; newB = g; }
    else if (mode === 2) { newR = g; newG = r; newB = b; }
    else if (mode === 3) { newR = g; newG = b; newB = r; }
    else if (mode === 4) { newR = b; newG = r; newB = g; }
    else if (mode === 5) { newR = b; newG = g; newB = r; }
    
    pixels[i] = newR;
    pixels[i+1] = newG;
    pixels[i+2] = newB;
    pixels[i+3] = 255;
  }
  updatePixels();
"""
    },
    "31": {
        "name": "Contrast Stretch",
        "description": "Expands the range of brightness values to cover the full spectrum. (Ref: Histogram Equalization)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  video.loadPixels();
  loadPixels();
  
  // paramA controls contrast factor (1.0 to 5.0)
  let contrast = map(paramA, 0, 1, 1, 5);
  let intercept = 128 * (1 - contrast);
  
  for (let i = 0; i < video.pixels.length; i += 4) {
    let r = video.pixels[i];
    let g = video.pixels[i+1];
    let b = video.pixels[i+2];
    
    pixels[i] = constrain(r * contrast + intercept, 0, 255);
    pixels[i+1] = constrain(g * contrast + intercept, 0, 255);
    pixels[i+2] = constrain(b * contrast + intercept, 0, 255);
    pixels[i+3] = 255;
  }
  updatePixels();
"""
    },
    "32": {
        "name": "Vignette Blur",
        "description": "Blurs and darkens the edges of the frame while keeping the center sharp. (Ref: Portraiture)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  
  // 1. Draw Blurred Base
  // paramA controls blur amount
  let blurAmt = map(paramA, 0, 1, 0, 20);
  push();
  drawingContext.filter = `blur(${blurAmt}px)`;
  image(video, 0, 0);
  pop();
  
  // 2. Draw Sharp Center (Clipped)
  drawingContext.save();
  drawingContext.beginPath();
  drawingContext.arc(width/2, height/2, height/2.5, 0, TWO_PI);
  drawingContext.clip();
  image(video, 0, 0);
  drawingContext.restore();
  
  // 3. Vignette Overlay (Dark edges)
  let grad = drawingContext.createRadialGradient(width/2, height/2, height/3, width/2, height/2, height);
  grad.addColorStop(0, 'rgba(0,0,0,0)');
  grad.addColorStop(1, 'rgba(0,0,0,0.8)');
  drawingContext.fillStyle = grad;
  rect(0, 0, width, height);
"""
    },
    "33": {
        "name": "Neon Glow",
        "description": "Detects bright areas and adds a blurred bloom effect around them. (Ref: Cyberpunk)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  
  // 1. Draw base video (dimmed)
  tint(100);
  image(video, 0, 0);
  noTint();
  
  // 2. Draw Bloom
  // paramA controls bloom intensity via threshold/contrast
  push();
  blendMode(SCREEN);
  let blurAmt = 20;
  // High contrast filter helps isolate brights
  drawingContext.filter = `blur(${blurAmt}px) brightness(200%) contrast(150%)`;
  image(video, 0, 0);
  pop();
  
  blendMode(BLEND);
"""
    },
    "34": {
        "name": "CMYK Separation",
        "description": "Simulates misaligned cyan, magenta, yellow, and black printing plates. (Ref: Risograph)",
        "global_vars": "",
        "draw_loop": """
  background(255);
  video.loadPixels();
  noStroke();
  blendMode(MULTIPLY);
  
  // paramA controls offset
  let offset = map(paramA, 0, 1, 0, 20);
  let step = 8; // Grid step for performance
  
  for (let y = 0; y < height; y += step) {
    for (let x = 0; x < width; x += step) {
      let idx = (x + y * width) * 4;
      let r = video.pixels[idx];
      let g = video.pixels[idx+1];
      let b = video.pixels[idx+2];
      
      // CMY approximation (Subtractive)
      let c = 255 - r;
      let m = 255 - g;
      let yel = 255 - b;
      
      // Cyan (Red channel blocked)
      if (c > 50) {
        fill(0, 255, 255, c); 
        ellipse(x - offset, y - offset, step, step);
      }
      
      // Magenta (Green channel blocked)
      if (m > 50) {
        fill(255, 0, 255, m);
        ellipse(x + offset, y - offset, step, step);
      }
      
      // Yellow (Blue channel blocked)
      if (yel > 50) {
        fill(255, 255, 0, yel);
        ellipse(x, y + offset, step, step);
      }
    }
  }
  blendMode(BLEND);
"""
    },
    "35": {
        "name": "Mirror Symmetry",
        "description": "Splits the screen vertically/horizontally and reflects one side. (Ref: Rorschach Test)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  
  // paramA controls mode: <0.5 Vertical Mirror, >0.5 Quad Mirror
  let quad = paramA > 0.5;
  let hw = width / 2;
  let hh = height / 2;
  
  if (!quad) {
    // Vertical Mirror (Left side reflected to Right)
    // Draw Left
    image(video, 0, 0, hw, height, 0, 0, hw, height);
    
    // Draw Right (Mirrored)
    push();
    translate(width, 0);
    scale(-1, 1);
    image(video, 0, 0, hw, height, 0, 0, hw, height);
    pop();
  } else {
    // Quad Mirror (Top-Left reflected to all quadrants)
    // TL
    image(video, 0, 0, hw, hh, 0, 0, hw, hh);
    
    // TR
    push();
    translate(width, 0);
    scale(-1, 1);
    image(video, 0, 0, hw, hh, 0, 0, hw, hh);
    pop();
    
    // BL
    push();
    translate(0, height);
    scale(1, -1);
    image(video, 0, 0, hw, hh, 0, 0, hw, hh);
    pop();
    
    // BR
    push();
    translate(width, height);
    scale(-1, -1);
    image(video, 0, 0, hw, hh, 0, 0, hw, hh);
    pop();
  }
"""
    },
    "36": {
        "name": "Fish-Eye Lens",
        "description": "Bulges the center of the image outward. (Ref: Action Cameras)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  video.loadPixels();
  loadPixels();
  
  let cx = width / 2;
  let cy = height / 2;
  // paramA controls distortion strength
  let k = map(paramA, 0, 1, 0.0, 0.00005);
  
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      let dx = x - cx;
      let dy = y - cy;
      let r2 = dx*dx + dy*dy;
      
      // Barrel distortion mapping
      let f = 1 + k * r2;
      let sx = floor(cx + dx * f);
      let sy = floor(cy + dy * f);
      
      if (sx >= 0 && sx < width && sy >= 0 && sy < height) {
        let destIdx = (x + y * width) * 4;
        let srcIdx = (sx + sy * width) * 4;
        pixels[destIdx] = video.pixels[srcIdx];
        pixels[destIdx+1] = video.pixels[srcIdx+1];
        pixels[destIdx+2] = video.pixels[srcIdx+2];
        pixels[destIdx+3] = 255;
      }
    }
  }
  updatePixels();
"""
    },
    "37": {
        "name": "Pinch Distortion",
        "description": "Sucks pixels toward a specific point (mouse position). (Ref: Black Hole)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  video.loadPixels();
  loadPixels();
  
  // Center of pinch is mouse position (paramA, paramB)
  let cx = paramA * width;
  let cy = paramB * height;
  let radius = 200;
  
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      let dx = x - cx;
      let dy = y - cy;
      let dist = sqrt(dx*dx + dy*dy);
      
      let sx = x;
      let sy = y;
      
      if (dist < radius) {
        // Non-linear pinch
        let amount = 1 - sin((dist / radius) * HALF_PI);
        let distortion = amount * 0.5; // Strength
        sx = cx + dx / (1 - distortion);
        sy = cy + dy / (1 - distortion);
      }
      
      sx = floor(sx);
      sy = floor(sy);
      
      if (sx >= 0 && sx < width && sy >= 0 && sy < height) {
        let destIdx = (x + y * width) * 4;
        let srcIdx = (sx + sy * width) * 4;
        pixels[destIdx] = video.pixels[srcIdx];
        pixels[destIdx+1] = video.pixels[srcIdx+1];
        pixels[destIdx+2] = video.pixels[srcIdx+2];
        pixels[destIdx+3] = 255;
      }
    }
  }
  updatePixels();
"""
    },
    "38": {
        "name": "Swirl",
        "description": "Rotates pixels around the center, with more rotation at the core. (Ref: Latte Art)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  video.loadPixels();
  loadPixels();
  
  let cx = width / 2;
  let cy = height / 2;
  // paramA controls twist amount
  let maxAngle = map(paramA, 0, 1, 0, TWO_PI * 2);
  let radius = min(width, height) / 1.5;
  
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      let dx = x - cx;
      let dy = y - cy;
      let dist = sqrt(dx*dx + dy*dy);
      
      let sx = x;
      let sy = y;
      
      if (dist < radius) {
        let percent = (radius - dist) / radius;
        let theta = percent * percent * maxAngle;
        
        // Rotate coordinate system
        let s_dx = dx * cos(theta) - dy * sin(theta);
        let s_dy = dx * sin(theta) + dy * cos(theta);
        sx = cx + s_dx;
        sy = cy + s_dy;
      }
      
      sx = floor(sx);
      sy = floor(sy);
      
      if (sx >= 0 && sx < width && sy >= 0 && sy < height) {
        let destIdx = (x + y * width) * 4;
        let srcIdx = (sx + sy * width) * 4;
        pixels[destIdx] = video.pixels[srcIdx];
        pixels[destIdx+1] = video.pixels[srcIdx+1];
        pixels[destIdx+2] = video.pixels[srcIdx+2];
        pixels[destIdx+3] = 255;
      }
    }
  }
  updatePixels();
"""
    },
    "39": {
        "name": "Sine Wave Ripple",
        "description": "Displaces pixels horizontally based on a sine wave function. (Ref: Underwater)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  video.loadPixels();
  loadPixels();
  
  // paramA controls frequency
  let freq = map(paramA, 0, 1, 0.02, 0.2);
  // paramB controls amplitude
  let amp = map(paramB, 0, 1, 0, 100);
  let time = frameCount * 0.1;
  
  for (let y = 0; y < height; y++) {
    // Calculate horizontal offset
    let offset = sin(y * freq + time) * amp;
    
    for (let x = 0; x < width; x++) {
      let srcX = floor(x + offset);
      srcX = constrain(srcX, 0, width - 1);
      
      let destIdx = (x + y * width) * 4;
      let srcIdx = (srcX + y * width) * 4;
      
      pixels[destIdx] = video.pixels[srcIdx];
      pixels[destIdx+1] = video.pixels[srcIdx+1];
      pixels[destIdx+2] = video.pixels[srcIdx+2];
      pixels[destIdx+3] = 255;
    }
  }
  updatePixels();
"""
    },
    "40": {
        "name": "Pixel Sort",
        "description": "Sorts pixels in a row/column by brightness. (Ref: Glitch Art)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  video.loadPixels();
  loadPixels();
  
  // Sort every row based on brightness
  // paramA controls sort direction (Left-to-Right or Right-to-Left)
  let asc = paramA > 0.5;
  
  for (let y = 0; y < height; y++) {
    // Extract row
    let row = [];
    for (let x = 0; x < width; x++) {
      let idx = (x + y * width) * 4;
      let r = video.pixels[idx];
      let g = video.pixels[idx+1];
      let b = video.pixels[idx+2];
      let bright = (r + g + b) / 3;
      row.push({r, g, b, bright});
    }
    
    // Sort
    if (asc) row.sort((a, b) => a.bright - b.bright);
    else row.sort((a, b) => b.bright - a.bright);
    
    // Put back
    for (let x = 0; x < width; x++) {
      let idx = (x + y * width) * 4;
      pixels[idx] = row[x].r;
      pixels[idx+1] = row[x].g;
      pixels[idx+2] = row[x].b;
      pixels[idx+3] = 255;
    }
  }
  updatePixels();
"""
    },
    "41": {
        "name": "Slit-Scan (Spatial)",
        "description": "Stretches the center vertical line of pixels to the edges. (Ref: 2001: A Space Odyssey)",
        "global_vars": "let slitHistory = [];",
        "draw_loop": """
  background(0);
  video.loadPixels();
  
  // Get center column
  let centerX = floor(width / 2);
  let col = [];
  for (let y = 0; y < height; y++) {
    let idx = (centerX + y * width) * 4;
    col.push([video.pixels[idx], video.pixels[idx+1], video.pixels[idx+2]]);
  }
  
  // Add to history (Newest at index 0)
  slitHistory.unshift(col);
  if (slitHistory.length > width / 2) slitHistory.pop();
  
  loadPixels();
  
  // Draw history radiating outwards
  for (let i = 0; i < slitHistory.length; i++) {
    let c = slitHistory[i];
    let leftX = centerX - i;
    let rightX = centerX + i;
    
    for (let y = 0; y < height; y++) {
      let color = c[y];
      if (leftX >= 0) {
        let idx = (leftX + y * width) * 4;
        pixels[idx] = color[0]; pixels[idx+1] = color[1]; pixels[idx+2] = color[2]; pixels[idx+3] = 255;
      }
      if (rightX < width) {
        let idx = (rightX + y * width) * 4;
        pixels[idx] = color[0]; pixels[idx+1] = color[1]; pixels[idx+2] = color[2]; pixels[idx+3] = 255;
      }
    }
  }
  updatePixels();
"""
    },
    "42": {
        "name": "Broken Glass",
        "description": "Voronoi cells that displace the image inside them slightly. (Ref: Shatter)",
        "global_vars": "let glassSeeds = []; let glassMap = null;",
        "draw_loop": """
  background(0);
  video.loadPixels();
  loadPixels();
  
  let numSeeds = floor(map(paramA, 0, 1, 10, 50));
  
  // Regenerate map if needed
  if (glassSeeds.length !== numSeeds || !glassMap) {
    glassSeeds = [];
    for (let i = 0; i < numSeeds; i++) {
      glassSeeds.push({ x: random(width), y: random(height), offsetX: random(-30, 30), offsetY: random(-30, 30) });
    }
    glassMap = new Int8Array(width * height);
    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        let minDist = Infinity, idx = 0;
        for (let i = 0; i < numSeeds; i++) {
          let d = (x - glassSeeds[i].x)**2 + (y - glassSeeds[i].y)**2;
          if (d < minDist) { minDist = d; idx = i; }
        }
        glassMap[x + y * width] = idx;
      }
    }
  }
  
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      let s = glassSeeds[glassMap[x + y * width]];
      let sx = constrain(floor(x + s.offsetX), 0, width - 1);
      let sy = constrain(floor(y + s.offsetY), 0, height - 1);
      
      let destIdx = (x + y * width) * 4;
      let srcIdx = (sx + sy * width) * 4;
      
      pixels[destIdx] = video.pixels[srcIdx];
      pixels[destIdx+1] = video.pixels[srcIdx+1];
      pixels[destIdx+2] = video.pixels[srcIdx+2];
      pixels[destIdx+3] = 255;
    }
  }
  updatePixels();
"""
    },
    "43": {
        "name": "Scanline Displacement",
        "description": "Shifts every other horizontal line left or right. (Ref: Interlacing)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  video.loadPixels();
  loadPixels();
  
  // paramA controls shift amount
  let shift = floor(map(paramA, 0, 1, 0, 50));
  
  for (let y = 0; y < height; y++) {
    // Determine shift direction based on row parity
    let xOffset = (y % 2 === 0) ? shift : -shift;
    
    for (let x = 0; x < width; x++) {
      let srcX = x - xOffset;
      
      // Wrap around
      if (srcX < 0) srcX += width;
      if (srcX >= width) srcX -= width;
      
      let destIdx = (x + y * width) * 4;
      let srcIdx = (srcX + y * width) * 4;
      
      pixels[destIdx] = video.pixels[srcIdx];
      pixels[destIdx+1] = video.pixels[srcIdx+1];
      pixels[destIdx+2] = video.pixels[srcIdx+2];
      pixels[destIdx+3] = 255;
    }
  }
  updatePixels();
"""
    },
    "44": {
        "name": "Polar Coordinates",
        "description": "Maps the Cartesian (x,y) image into a circle. (Ref: Tiny Planet)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  video.loadPixels();
  loadPixels();
  
  let cx = width / 2;
  let cy = height / 2;
  let maxRadius = dist(0, 0, cx, cy);
  
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      let dx = x - cx;
      let dy = y - cy;
      let angle = atan2(dy, dx); // -PI to PI
      let r = sqrt(dx*dx + dy*dy);
      
      if (r < maxRadius) {
        // Map angle to X, radius to Y
        let srcX = map(angle, -PI, PI, 0, width);
        // paramA controls zoom/radius mapping
        let zoom = map(paramA, 0, 1, 0.5, 2.0);
        let srcY = map(r, 0, maxRadius / zoom, 0, height);
        
        srcX = (srcX + width) % width;
        srcY = constrain(srcY, 0, height - 1);
        
        let sx = floor(srcX);
        let sy = floor(srcY);
        
        let destIdx = (x + y * width) * 4;
        let srcIdx = (sx + sy * width) * 4;
        
        pixels[destIdx] = video.pixels[srcIdx];
        pixels[destIdx+1] = video.pixels[srcIdx+1];
        pixels[destIdx+2] = video.pixels[srcIdx+2];
        pixels[destIdx+3] = 255;
      }
    }
  }
  updatePixels();
"""
    },
    "45": {
        "name": "Droste Effect",
        "description": "Recursively places the video frame inside itself. (Ref: Picture-in-Picture)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  
  // paramA controls scale decay (0.5 to 0.9)
  let scaleFactor = map(paramA, 0, 1, 0.5, 0.9);
  let depth = 10;
  
  imageMode(CENTER);
  translate(width / 2, height / 2);
  
  let w = width;
  let h = height;
  
  // Draw from outside in
  for (let i = 0; i < depth; i++) {
    image(video, 0, 0, w, h);
    w *= scaleFactor;
    h *= scaleFactor;
  }
"""
    },
    "46": {
        "name": "Tile Scramble",
        "description": "Breaks image into a grid and randomly swaps tile positions. (Ref: Puzzle)",
        "global_vars": "let tileIndices = [];",
        "draw_loop": """
  background(0);
  
  // paramA controls grid size (2 to 10)
  let tiles = floor(map(paramA, 0, 1, 2, 10));
  let tileW = width / tiles;
  let tileH = height / tiles;
  
  // Initialize or reset permutation if grid size changes
  if (tileIndices.length !== tiles * tiles) {
    tileIndices = [];
    for (let i = 0; i < tiles * tiles; i++) tileIndices.push(i);
    // Shuffle
    for (let i = tileIndices.length - 1; i > 0; i--) {
      const j = floor(random(i + 1));
      [tileIndices[i], tileIndices[j]] = [tileIndices[j], tileIndices[i]];
    }
  }
  
  for (let y = 0; y < tiles; y++) {
    for (let x = 0; x < tiles; x++) {
      let idx = tileIndices[x + y * tiles];
      let sx = (idx % tiles) * tileW;
      let sy = floor(idx / tiles) * tileH;
      
      // Use image() instead of copy() for better compatibility with video elements
      // image(img, dx, dy, dWidth, dHeight, sx, sy, sWidth, sHeight)
      image(video, x * tileW, y * tileH, tileW, tileH, sx, sy, tileW, tileH);
    }
  }
"""
    },
    "47": {
        "name": "Barrel Distortion",
        "description": "Squeezes the edges of the image inward. (Ref: CRT TV)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  video.loadPixels();
  loadPixels();
  
  let cx = width / 2;
  let cy = height / 2;
  // paramA controls distortion strength
  let k = map(paramA, 0, 1, 0.0, 0.0001);
  
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      let dx = x - cx;
      let dy = y - cy;
      let r2 = dx*dx + dy*dy;
      
      // Barrel distortion: pull pixels from further out
      let f = 1 + k * r2;
      let sx = floor(cx + dx * f);
      let sy = floor(cy + dy * f);
      
      if (sx >= 0 && sx < width && sy >= 0 && sy < height) {
        let destIdx = (x + y * width) * 4;
        let srcIdx = (sx + sy * width) * 4;
        pixels[destIdx] = video.pixels[srcIdx];
        pixels[destIdx+1] = video.pixels[srcIdx+1];
        pixels[destIdx+2] = video.pixels[srcIdx+2];
        pixels[destIdx+3] = 255;
      }
    }
  }
  updatePixels();
"""
    },
    "48": {
        "name": "Liquid Displacement",
        "description": "Uses Perlin noise to warp pixel coordinates smoothly. (Ref: Oil on Water)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  video.loadPixels();
  loadPixels();
  
  // paramA controls noise scale
  let scale = map(paramA, 0, 1, 0.002, 0.01);
  // paramB controls displacement magnitude
  let mag = map(paramB, 0, 1, 0, 100);
  let time = frameCount * 0.01;
  
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      let angle = noise(x * scale, y * scale, time) * TWO_PI * 2;
      let sx = floor(x + cos(angle) * mag);
      let sy = floor(y + sin(angle) * mag);
      
      sx = constrain(sx, 0, width - 1);
      sy = constrain(sy, 0, height - 1);
      
      let destIdx = (x + y * width) * 4;
      let srcIdx = (sx + sy * width) * 4;
      
      pixels[destIdx] = video.pixels[srcIdx];
      pixels[destIdx+1] = video.pixels[srcIdx+1];
      pixels[destIdx+2] = video.pixels[srcIdx+2];
      pixels[destIdx+3] = 255;
    }
  }
  updatePixels();
"""
    },
    "49": {
        "name": "Motion Blur",
        "description": "Blends the current frame with the previous 5 frames with opacity. (Ref: Long Exposure)",
        "global_vars": "let mbHistory = [];",
        "draw_loop": """
  background(0);
  
  // Store current frame
  mbHistory.push(video.get());
  
  // paramA controls trail length (2 to 20)
  let maxHist = floor(map(paramA, 0, 1, 2, 20));
  
  if (mbHistory.length > maxHist) mbHistory.shift();
  
  // Draw all frames in history with low opacity
  for (let i = 0; i < mbHistory.length; i++) {
    tint(255, 255 / mbHistory.length);
    image(mbHistory[i], 0, 0);
  }
  noTint();
"""
    },
    "50": {
        "name": "Ghosting / Trails",
        "description": "Only updates the background slowly, leaving trails of moving objects. (Ref: Echo)",
        "global_vars": "",
        "draw_loop": """
  // No background() call to preserve previous frames
  
  // paramA controls fade speed (alpha of black overlay)
  // Lower alpha = longer trails
  let fade = map(paramA, 0, 1, 5, 50);
  
  noStroke();
  fill(0, fade);
  rect(0, 0, width, height);
  
  // Draw current video with transparency to blend with history
  tint(255, 150);
  image(video, 0, 0);
  noTint();
"""
    },
    "51": {
        "name": "Slit-Scan (Temporal)",
        "description": "Each column of pixels comes from a different point in time. (Ref: Time Warp Scan)",
        "global_vars": "let tScanY = 0; let tFrozen;",
        "draw_loop": """
  if (!tFrozen || tFrozen.width !== width || tFrozen.height !== height) {
    tFrozen = createGraphics(width, height);
    tFrozen.clear();
  }
  
  // Draw live video background (bottom part)
  image(video, 0, 0);
  
  // paramA controls scan speed
  let speed = floor(map(paramA, 0, 1, 1, 10));
  
  // Copy strip from video to frozen buffer
  tFrozen.copy(video, 0, tScanY, width, speed, 0, tScanY, width, speed);
  
  // Draw frozen part on top
  image(tFrozen, 0, 0);
  
  // Draw scanline indicator
  stroke(0, 255, 0);
  strokeWeight(2);
  line(0, tScanY + speed, width, tScanY + speed);
  
  tScanY += speed;
  if (tScanY >= height) {
    tScanY = 0;
    tFrozen.clear();
  }
"""
    },
    "52": {
        "name": "Frame Delay Grid",
        "description": "A grid of videos, each delayed by 1 second more than the last. (Ref: CCTV Wall)",
        "global_vars": "let fdBuffer = [];",
        "draw_loop": """
  background(0);
  
  // paramA controls grid size (2 to 5)
  let grid = floor(map(paramA, 0, 1, 2, 5));
  let cellW = width / grid;
  let cellH = height / grid;
  
  let delayStep = 15; // Frames delay per cell
  let maxBuffer = (grid * grid) * delayStep;
  
  fdBuffer.push(video.get());
  if (fdBuffer.length > maxBuffer) fdBuffer.shift();
  
  for (let y = 0; y < grid; y++) {
    for (let x = 0; x < grid; x++) {
      let cellIdx = x + y * grid;
      // Calculate frame index: Cell 0 is newest, Cell N is oldest
      let frameIdx = fdBuffer.length - 1 - (cellIdx * delayStep);
      
      if (frameIdx >= 0) {
        image(fdBuffer[frameIdx], x * cellW, y * cellH, cellW, cellH);
      }
    }
  }
"""
    },
    "53": {
        "name": "Motion Detection",
        "description": "Subtracts the previous frame from the current one to show only movement. (Ref: Security Cam)",
        "global_vars": "let prevFrame;",
        "draw_loop": """
  if (!prevFrame || prevFrame.width !== width) {
    prevFrame = createGraphics(width, height);
    prevFrame.pixelDensity(1);
  }
  
  video.loadPixels();
  prevFrame.loadPixels();
  loadPixels();
  
  // paramA controls threshold
  let thresh = map(paramA, 0, 1, 10, 100);
  
  if (video.pixels.length > 0 && prevFrame.pixels.length === video.pixels.length) {
    for (let i = 0; i < video.pixels.length; i += 4) {
      let r = video.pixels[i];
      let g = video.pixels[i+1];
      let b = video.pixels[i+2];
      
      let pr = prevFrame.pixels[i];
      let pg = prevFrame.pixels[i+1];
      let pb = prevFrame.pixels[i+2];
      
      let diff = abs(r - pr) + abs(g - pg) + abs(b - pb);
      
      if (diff > thresh) {
        pixels[i] = 255; pixels[i+1] = 255; pixels[i+2] = 255;
      } else {
        pixels[i] = 0; pixels[i+1] = 0; pixels[i+2] = 0;
      }
      pixels[i+3] = 255;
    }
    updatePixels();
  }
  
  // Save current frame
  prevFrame.image(video, 0, 0, width, height);
"""
    },
    "54": {
        "name": "RGB Delay",
        "description": "Shows Red channel instantly, Green with 5-frame delay, Blue with 10-frame delay. (Ref: Chromatic Aberration)",
        "global_vars": "let rgbBuffer = [];",
        "draw_loop": """
  background(0);
  
  // Store current frame
  rgbBuffer.push(video.get());
  if (rgbBuffer.length > 11) rgbBuffer.shift();
  
  if (rgbBuffer.length > 10) {
    let current = rgbBuffer[rgbBuffer.length - 1];
    let mid = rgbBuffer[rgbBuffer.length - 6];
    let old = rgbBuffer[0];
    
    current.loadPixels();
    mid.loadPixels();
    old.loadPixels();
    loadPixels();
    
    for (let i = 0; i < pixels.length; i+=4) {
      pixels[i] = current.pixels[i];     // R (Instant)
      pixels[i+1] = mid.pixels[i+1];     // G (Delayed)
      pixels[i+2] = old.pixels[i+2];     // B (More Delayed)
      pixels[i+3] = 255;
    }
    updatePixels();
  } else {
    image(video, 0, 0);
  }
"""
    },
    "55": {
        "name": "Video Feedback",
        "description": "Draws the previous frame slightly zoomed in and rotated. (Ref: Infinity Mirror)",
        "global_vars": "",
        "draw_loop": """
  // Capture the canvas before clearing
  let prev = get();
  
  background(0);
  
  push();
  imageMode(CENTER);
  translate(width/2, height/2);
  
  // paramA controls zoom (1.0 to 1.2)
  let zoom = map(paramA, 0, 1, 1.0, 1.2);
  // paramB controls rotation
  let rot = map(paramB, 0, 1, -0.1, 0.1);
  
  scale(zoom);
  rotate(rot);
  
  // Draw previous frame with slight transparency to create decay
  tint(255, 240);
  image(prev, 0, 0);
  pop();
  
  // Draw new video frame on top with blend
  blendMode(SCREEN);
  tint(255, 150);
  image(video, 0, 0);
  blendMode(BLEND);
"""
    },
    "56": {
        "name": "Pixel Accumulation",
        "description": "Pixels 'pile up' at the bottom if they are dark (physics simulation). (Ref: Sand Art)",
        "global_vars": "let sandPg; let sandPile = []; let activeSand = [];",
        "draw_loop": """
  if (!sandPg || sandPg.width !== width) {
    sandPg = createGraphics(width, height);
    sandPg.clear();
    sandPile = new Array(width).fill(height);
  }
  
  background(0);
  
  // Spawn sand from dark pixels
  video.loadPixels();
  let spawnRate = 50;
  for(let i=0; i<spawnRate; i++) {
    let x = floor(random(width));
    let y = floor(random(height));
    let idx = (x + y * width) * 4;
    let b = (video.pixels[idx] + video.pixels[idx+1] + video.pixels[idx+2])/3;
    
    // paramA controls brightness threshold
    let thresh = map(paramA, 0, 1, 50, 150);
    
    if (b < thresh) {
      activeSand.push({
        x: x, 
        y: y, 
        c: [video.pixels[idx], video.pixels[idx+1], video.pixels[idx+2]]
      });
    }
  }
  
  // Update physics
  for (let i = activeSand.length - 1; i >= 0; i--) {
    let s = activeSand[i];
    s.y += 5; // Gravity
    
    let floorY = sandPile[s.x];
    if (s.y >= floorY) {
      s.y = floorY;
      sandPile[s.x] -= 2; // Pile grows
      
      // Draw to persistent buffer
      sandPg.noStroke();
      sandPg.fill(s.c[0], s.c[1], s.c[2]);
      sandPg.rect(s.x, s.y, 2, 2);
      
      activeSand.splice(i, 1);
    }
  }
  
  // Draw buffer and active sand
  image(sandPg, 0, 0);
  
  noStroke();
  for (let s of activeSand) {
    fill(s.c[0], s.c[1], s.c[2]);
    rect(s.x, s.y, 2, 2);
  }
"""
    },
    "57": {
        "name": "Freeze Frame Mask",
        "description": "Freezes parts of the screen that haven't moved in X seconds. (Ref: Photobooth)",
        "global_vars": "let ffBuffer; let ffPrev;",
        "draw_loop": """
  if (!ffPrev || ffPrev.width !== width) {
    ffPrev = createGraphics(width, height);
    ffPrev.pixelDensity(1);
    ffPrev.image(video, 0, 0, width, height);
  }
  
  if (!ffBuffer || ffBuffer.width !== width) {
    ffBuffer = createGraphics(width, height);
    ffBuffer.pixelDensity(1);
    ffBuffer.image(video, 0, 0, width, height);
  }

  video.loadPixels();
  ffPrev.loadPixels();
  ffBuffer.loadPixels();
  
  // paramA controls sensitivity
  let thresh = map(paramA, 0, 1, 10, 100);
  
  if (video.pixels.length > 0 && ffPrev.pixels.length === video.pixels.length) {
    for (let i = 0; i < video.pixels.length; i += 4) {
      let r = video.pixels[i];
      let g = video.pixels[i+1];
      let b = video.pixels[i+2];
      
      let pr = ffPrev.pixels[i];
      let pg = ffPrev.pixels[i+1];
      let pb = ffPrev.pixels[i+2];
      
      let diff = abs(r - pr) + abs(g - pg) + abs(b - pb);
      
      // If motion detected, update buffer with NEW video pixel
      if (diff > thresh) {
         ffBuffer.pixels[i] = r;
         ffBuffer.pixels[i+1] = g;
         ffBuffer.pixels[i+2] = b;
         ffBuffer.pixels[i+3] = 255;
      }
    }
    ffBuffer.updatePixels();
  }
  
  image(ffBuffer, 0, 0);
  
  // Update previous frame
  ffPrev.image(video, 0, 0, width, height);
"""
    },
    "58": {
        "name": "Time Displacement Map",
        "description": "Uses a grayscale map to determine which 'time' (past frame) to sample from. (Ref: Doctor Who Intro)",
        "global_vars": "let tdHistory = [];",
        "draw_loop": """
  // Buffer history
  tdHistory.push(video.get());
  let maxFrames = 50;
  if (tdHistory.length > maxFrames) tdHistory.shift();
  
  background(0);
  
  if (tdHistory.length > 0) {
    // Ensure current frame pixels are loaded
    tdHistory[tdHistory.length-1].loadPixels();
    loadPixels();
    
    let cx = width/2;
    let cy = height/2;
    
    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        // Calculate delay based on radial distance
        let d = dist(x, y, cx, cy);
        let maxD = dist(0, 0, cx, cy);
        let normD = d / maxD; 
        
        // paramA modifies the pattern
        let delayIndex = floor(map(normD, 0, 1, 0, tdHistory.length - 1));
        if (paramA > 0.5) delayIndex = tdHistory.length - 1 - delayIndex;
        
        delayIndex = constrain(delayIndex, 0, tdHistory.length - 1);
        
        let frame = tdHistory[delayIndex];
        // Lazy load pixels if needed
        if (!frame.pixels || frame.pixels.length === 0) frame.loadPixels();
        
        let idx = (x + y * width) * 4;
        pixels[idx] = frame.pixels[idx];
        pixels[idx+1] = frame.pixels[idx+1];
        pixels[idx+2] = frame.pixels[idx+2];
        pixels[idx+3] = 255;
      }
    }
    updatePixels();
  }
"""
    },
    "59": {
        "name": "Optical Flow Particles",
        "description": "Particles flow in the direction of movement detected in the video. (Ref: Wind Simulation)",
        "global_vars": "let ofParticles = []; let ofPrevPixels;",
        "draw_loop": """
  background(0, 50); // Trails
  
  if (ofParticles.length === 0) {
    for(let i=0; i<200; i++) ofParticles.push({x: random(width), y: random(height), vx: 0, vy: 0});
  }
  
  video.loadPixels();
  if (!ofPrevPixels) ofPrevPixels = new Uint8ClampedArray(video.pixels);
  
  for (let p of ofParticles) {
    let x = floor(p.x);
    let y = floor(p.y);
    let idx = (x + y * width) * 4;
    
    if (x > 0 && x < width-1 && y > 0 && y < height-1) {
       let curr = (video.pixels[idx] + video.pixels[idx+1] + video.pixels[idx+2]) / 3;
       let prev = (ofPrevPixels[idx] + ofPrevPixels[idx+1] + ofPrevPixels[idx+2]) / 3;
       
       // Simplified Gradient-based Flow
       let idxLeft = (x - 1 + y * width) * 4;
       let idxRight = (x + 1 + y * width) * 4;
       let idxUp = (x + (y - 1) * width) * 4;
       let idxDown = (x + (y + 1) * width) * 4;
       
       let left = (video.pixels[idxLeft] + video.pixels[idxLeft+1] + video.pixels[idxLeft+2]) / 3;
       let right = (video.pixels[idxRight] + video.pixels[idxRight+1] + video.pixels[idxRight+2]) / 3;
       let up = (video.pixels[idxUp] + video.pixels[idxUp+1] + video.pixels[idxUp+2]) / 3;
       let down = (video.pixels[idxDown] + video.pixels[idxDown+1] + video.pixels[idxDown+2]) / 3;
       
       let Ix = (right - left) * 0.5;
       let Iy = (down - up) * 0.5;
       let It = curr - prev;
       
       let denom = Ix*Ix + Iy*Iy + 100; // Epsilon to prevent div by zero
       let u = -It * Ix / denom;
       let v = -It * Iy / denom;
       
       let scale = map(paramA, 0, 1, 10, 100);
       p.vx += u * scale;
       p.vy += v * scale;
    }
    
    p.vx *= 0.9; // Friction
    p.vy *= 0.9;
    p.x += p.vx;
    p.y += p.vy;
    
    if (p.x < 0) p.x = width;
    if (p.x > width) p.x = 0;
    if (p.y < 0) p.y = height;
    if (p.y > height) p.y = 0;
    
    stroke(255);
    point(p.x, p.y);
  }
  
  ofPrevPixels.set(video.pixels);
"""
    },
    "60": {
        "name": "Frame Averaging",
        "description": "Averages the last 100 frames to remove moving objects entirely. (Ref: Empty Streets)",
        "global_vars": "let faSum; let faHistory = [];",
        "draw_loop": """
  if (!faSum || faSum.length !== width * height * 3) {
    faSum = new Float32Array(width * height * 3);
    faHistory = [];
  }
  
  video.loadPixels();
  
  // Add current frame
  let currentFrameData = new Uint8ClampedArray(video.pixels);
  faHistory.push(currentFrameData);
  
  // Add to sum
  for (let i = 0, j = 0; i < video.pixels.length; i += 4, j += 3) {
    faSum[j] += video.pixels[i];
    faSum[j+1] += video.pixels[i+1];
    faSum[j+2] += video.pixels[i+2];
  }
  
  // Remove old frame if buffer full
  let maxFrames = 100;
  if (faHistory.length > maxFrames) {
    let old = faHistory.shift();
    for (let i = 0, j = 0; i < old.length; i += 4, j += 3) {
      faSum[j] -= old[i];
      faSum[j+1] -= old[i+1];
      faSum[j+2] -= old[i+2];
    }
  }
  
  // Display average
  loadPixels();
  let count = faHistory.length;
  for (let i = 0, j = 0; i < pixels.length; i += 4, j += 3) {
    pixels[i] = faSum[j] / count;
    pixels[i+1] = faSum[j+1] / count;
    pixels[i+2] = faSum[j+2] / count;
    pixels[i+3] = 255;
  }
  updatePixels();
"""
    },
    "61": {
        "name": "Stroboscope",
        "description": "Only updates the video frame every X milliseconds. (Ref: Stop Motion)",
        "global_vars": "let lastUpdate = 0; let strobeFrame;",
        "draw_loop": """
  if (!strobeFrame || strobeFrame.width !== width) {
    strobeFrame = createGraphics(width, height);
    strobeFrame.pixelDensity(1);
  }

  // paramA controls delay (200ms to 2000ms)
  let delay = map(paramA, 0, 1, 200, 2000);
  
  if (millis() - lastUpdate > delay) {
    strobeFrame.image(video, 0, 0, width, height);
    lastUpdate = millis();
  }
  
  image(strobeFrame, 0, 0);
"""
    },
    "62": {
        "name": "Decay",
        "description": "Bright pixels fade to black slowly over time. (Ref: Phosphor Burn-in)",
        "global_vars": "let decayBuffer;",
        "draw_loop": """
  if (!decayBuffer || decayBuffer.width !== width) {
    decayBuffer = createGraphics(width, height);
    decayBuffer.pixelDensity(1);
    decayBuffer.background(0);
  }
  
  // Draw semi-transparent black rect to fade out old pixels
  // paramA controls decay speed (fade amount)
  let fade = map(paramA, 0, 1, 1, 20);
  
  decayBuffer.noStroke();
  decayBuffer.fill(0, fade);
  decayBuffer.rect(0, 0, width, height);
  
  // Draw current video on top using LIGHTEST blend mode to keep bright pixels
  decayBuffer.blendMode(LIGHTEST);
  decayBuffer.image(video, 0, 0, width, height);
  decayBuffer.blendMode(BLEND);
  
  image(decayBuffer, 0, 0);
"""
    },
    "63": {
        "name": "Difference Clouds",
        "description": "Multiplies the video feed by Perlin noise that evolves over time. (Ref: Fog)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  video.loadPixels();
  loadPixels();
  
  let scale = 0.02;
  let time = frameCount * 0.01;
  // paramA controls noise intensity/mix
  let mix = map(paramA, 0, 1, 0.5, 1.0);
  
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      let idx = (x + y * width) * 4;
      
      let n = noise(x * scale, y * scale, time);
      let factor = lerp(1, n, mix); // 1 means no effect, n means full noise mult
      
      pixels[idx] = video.pixels[idx] * factor;
      pixels[idx+1] = video.pixels[idx+1] * factor;
      pixels[idx+2] = video.pixels[idx+2] * factor;
      pixels[idx+3] = 255;
    }
  }
  updatePixels();
"""
    },
    "64": {
        "name": "Pointillism",
        "description": "Draws random colored circles; density is higher in detailed areas. (Ref: Seurat)",
        "global_vars": "",
        "draw_loop": """
  // Don't clear background completely to build up density
  noStroke();
  fill(0, 10);
  rect(0, 0, width, height);
  
  video.loadPixels();
  
  // paramA controls dot size
  let dotSize = map(paramA, 0, 1, 4, 15);
  let numDots = 500;
  
  for (let i = 0; i < numDots; i++) {
    let x = floor(random(width));
    let y = floor(random(height));
    let idx = (x + y * width) * 4;
    
    let r = video.pixels[idx];
    let g = video.pixels[idx+1];
    let b = video.pixels[idx+2];
    
    fill(r, g, b, 200);
    ellipse(x, y, dotSize, dotSize);
  }
"""
    },
    "65": {
        "name": "Oil Painting",
        "description": "Scans local neighborhoods and outputs the most frequent color (Kuwahara filter). (Ref: Impressionism)",
        "global_vars": "",
        "draw_loop": """
  video.loadPixels();
  noStroke();
  
  // Simplified Kuwahara Filter (Optimized for performance)
  // We process a grid instead of every pixel to maintain frame rate
  
  // paramA controls brush size / grid step
  let step = floor(map(paramA, 0, 1, 4, 10));
  let radius = step;
  
  for (let y = radius; y < height - radius; y += step) {
    for (let x = radius; x < width - radius; x += step) {
      
      // Analyze 4 sub-regions (TL, TR, BL, BR)
      let bestMean = [0,0,0];
      let minVar = Infinity;
      
      // Offsets for 4 quadrants relative to center
      let quadrants = [
        [-radius, -radius, 0, 0], // TL
        [0, -radius, radius, 0],  // TR
        [-radius, 0, 0, radius],  // BL
        [0, 0, radius, radius]    // BR
      ];
      
      for (let q of quadrants) {
        let meanR = 0, meanG = 0, meanB = 0;
        let count = 0;
        
        // Sample pixels in quadrant
        for (let j = q[1]; j <= q[3]; j+=2) {
          for (let i = q[0]; i <= q[2]; i+=2) {
             let idx = ((x + i) + (y + j) * width) * 4;
             meanR += video.pixels[idx];
             meanG += video.pixels[idx+1];
             meanB += video.pixels[idx+2];
             count++;
          }
        }
        meanR /= count; meanG /= count; meanB /= count;
        
        // Calculate Variance (simplified: just brightness variance)
        let variance = 0;
        for (let j = q[1]; j <= q[3]; j+=2) {
          for (let i = q[0]; i <= q[2]; i+=2) {
             let idx = ((x + i) + (y + j) * width) * 4;
             let val = (video.pixels[idx] + video.pixels[idx+1] + video.pixels[idx+2])/3;
             let meanVal = (meanR + meanG + meanB)/3;
             variance += (val - meanVal) * (val - meanVal);
          }
        }
        
        if (variance < minVar) {
          minVar = variance;
          bestMean = [meanR, meanG, meanB];
        }
      }
      
      fill(bestMean[0], bestMean[1], bestMean[2]);
      // Draw slightly overlapping rects for painterly look
      rect(x - step/2, y - step/2, step + 2, step + 2);
    }
  }
"""
    },
    "66": {
        "name": "Watercolor",
        "description": "Layers semi-transparent blobs of color with jagged edges. (Ref: Wet-on-wet)",
        "global_vars": "",
        "draw_loop": """
  // Fade background to white slowly (Wet paper effect)
  noStroke();
  fill(255, 10);
  rect(0, 0, width, height);
  
  video.loadPixels();
  
  // paramA controls blob spread
  let spread = map(paramA, 0, 1, 10, 40);
  let numBlobs = 30;
  
  for (let i = 0; i < numBlobs; i++) {
    let x = random(width);
    let y = random(height);
    let idx = (floor(x) + floor(y) * width) * 4;
    
    let r = video.pixels[idx];
    let g = video.pixels[idx+1];
    let b = video.pixels[idx+2];
    
    // Very low opacity for layering
    fill(r, g, b, 40);
    
    beginShape();
    // Create jagged/organic shape
    for (let a = 0; a < TWO_PI; a += 0.5) {
      let offset = random(-5, 5);
      let rad = spread + offset;
      let vx = x + cos(a) * rad;
      let vy = y + sin(a) * rad;
      curveVertex(vx, vy);
    }
    endShape(CLOSE);
  }
"""
    },
    "67": {
        "name": "Impasto",
        "description": "Uses brightness to simulate thick paint strokes with 'height'. (Ref: Van Gogh)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  video.loadPixels();
  noStroke();
  
  // paramA controls stroke size
  let step = floor(map(paramA, 0, 1, 5, 20));
  
  for (let y = 0; y < height; y += step) {
    for (let x = 0; x < width; x += step) {
      let idx = (x + y * width) * 4;
      let r = video.pixels[idx];
      let g = video.pixels[idx+1];
      let b = video.pixels[idx+2];
      let bright = (r + g + b) / 3;
      
      // Angle based on brightness
      let angle = map(bright, 0, 255, 0, TWO_PI);
      
      push();
      translate(x, y);
      rotate(angle);
      
      // Shadow (offset)
      fill(0, 100);
      rect(2, 2, step, step/2);
      
      // Stroke
      fill(r, g, b);
      rect(0, 0, step, step/2);
      pop();
    }
  }
"""
    },
    "68": {
        "name": "Charcoal",
        "description": "High contrast edge detection with added grain noise. (Ref: Sketch)",
        "global_vars": "",
        "draw_loop": """
  background(255);
  video.loadPixels();
  loadPixels();
  
  // paramA controls threshold
  let thresh = map(paramA, 0, 1, 10, 60);
  
  for (let y = 0; y < height - 1; y++) {
    for (let x = 0; x < width - 1; x++) {
      let idx = (x + y * width) * 4;
      let idxRight = ((x + 1) + y * width) * 4;
      let idxDown = (x + (y + 1) * width) * 4;
      
      let b = (video.pixels[idx] + video.pixels[idx+1] + video.pixels[idx+2]) / 3;
      let bRight = (video.pixels[idxRight] + video.pixels[idxRight+1] + video.pixels[idxRight+2]) / 3;
      let bDown = (video.pixels[idxDown] + video.pixels[idxDown+1] + video.pixels[idxDown+2]) / 3;
      
      let diff = abs(b - bRight) + abs(b - bDown);
      
      let destIdx = (x + y * width) * 4;
      
      if (diff > thresh) {
        // Edge: Black with some noise
        let val = random(50);
        pixels[destIdx] = val;
        pixels[destIdx+1] = val;
        pixels[destIdx+2] = val;
      } else {
        // Background: White with grain
        let val = 255 - random(20);
        pixels[destIdx] = val;
        pixels[destIdx+1] = val;
        pixels[destIdx+2] = val;
      }
      pixels[destIdx+3] = 255;
    }
  }
  updatePixels();
"""
    },
    "69": {
        "name": "Mosaic Tiles",
        "description": "Irregular polygonal shapes with thick mortar lines between them. (Ref: Roman Floors)",
        "global_vars": "",
        "draw_loop": """
  background(50); // Dark mortar
  video.loadPixels();
  noStroke();
  
  // paramA controls tile size
  let step = floor(map(paramA, 0, 1, 10, 30));
  
  for (let y = 0; y < height; y += step) {
    for (let x = 0; x < width; x += step) {
      // Sample center color
      let cx = floor(x + step/2);
      let cy = floor(y + step/2);
      if (cx >= width || cy >= height) continue;
      
      let idx = (cx + cy * width) * 4;
      fill(video.pixels[idx], video.pixels[idx+1], video.pixels[idx+2]);
      
      // Draw irregular quad inside the grid cell
      // Shrink slightly to show mortar
      let gap = 2;
      let x1 = x + gap + random(2);
      let y1 = y + gap + random(2);
      let x2 = x + step - gap - random(2);
      let y2 = y + gap + random(2);
      let x3 = x + step - gap - random(2);
      let y3 = y + step - gap - random(2);
      let x4 = x + gap + random(2);
      let y4 = y + step - gap - random(2);
      
      beginShape();
      vertex(x1, y1);
      vertex(x2, y2);
      vertex(x3, y3);
      vertex(x4, y4);
      endShape(CLOSE);
    }
  }
"""
    },
    "70": {
        "name": "Stained Glass (Glow)",
        "description": "High saturation Voronoi cells with a bloom filter. (Ref: Cathedral)",
        "global_vars": "let sgSeeds = []; let sgPg;",
        "draw_loop": """
  if (!sgPg || sgPg.width !== width) {
    sgPg = createGraphics(width, height);
    sgPg.pixelDensity(1);
  }

  video.loadPixels();
  
  // paramA controls cell count
  let numSeeds = floor(map(paramA, 0, 1, 20, 80));
  
  if (sgSeeds.length !== numSeeds) {
    sgSeeds = [];
    for (let i = 0; i < numSeeds; i++) {
      sgSeeds.push({x: random(width), y: random(height)});
    }
  }
  
  sgPg.background(0);
  sgPg.noStroke();
  
  // Draw Voronoi to offscreen buffer
  let step = 6;
  for (let y = 0; y < height; y += step) {
    for (let x = 0; x < width; x += step) {
      let minDist = Infinity;
      let closest = -1;
      
      for (let i = 0; i < sgSeeds.length; i++) {
        let d = (x - sgSeeds[i].x)**2 + (y - sgSeeds[i].y)**2;
        if (d < minDist) { minDist = d; closest = i; }
      }
      
      let s = sgSeeds[closest];
      let sx = floor(constrain(s.x, 0, width-1));
      let sy = floor(constrain(s.y, 0, height-1));
      let idx = (sx + sy * width) * 4;
      
      // Boost saturation simply by increasing max channel and decreasing min
      let r = video.pixels[idx];
      let g = video.pixels[idx+1];
      let b = video.pixels[idx+2];
      
      // Simple saturation boost
      let maxC = Math.max(r, g, b);
      if (r !== maxC) r *= 0.8;
      if (g !== maxC) g *= 0.8;
      if (b !== maxC) b *= 0.8;
      
      sgPg.fill(r * 1.2, g * 1.2, b * 1.2);
      sgPg.rect(x, y, step, step);
    }
  }
  
  // Draw buffer
  image(sgPg, 0, 0);
  
  // Draw bloom (buffer drawn again with blur and ADD blend)
  push();
  blendMode(ADD);
  drawingContext.filter = 'blur(15px)';
  image(sgPg, 0, 0);
  drawingContext.filter = 'none';
  pop();
"""
    },
    "71": {
        "name": "Spray Paint",
        "description": "Random splatter particles appear where the image is darkest. (Ref: Graffiti)",
        "global_vars": "",
        "draw_loop": """
  // Fade background slowly
  noStroke();
  fill(255, 10);
  rect(0, 0, width, height);
  
  video.loadPixels();
  
  // paramA controls spray density
  let density = map(paramA, 0, 1, 50, 200);
  
  for (let i = 0; i < density; i++) {
    let x = floor(random(width));
    let y = floor(random(height));
    let idx = (x + y * width) * 4;
    
    let r = video.pixels[idx];
    let g = video.pixels[idx+1];
    let b = video.pixels[idx+2];
    let bright = (r + g + b) / 3;
    
    // Only spray on dark areas
    if (bright < 100) {
      let radius = random(5, 15);
      let colorVar = random(-20, 20);
      
      fill(r + colorVar, g + colorVar, b + colorVar);
      
      // Draw splatter cluster
      for (let j = 0; j < 5; j++) {
        let ox = random(-radius, radius);
        let oy = random(-radius, radius);
        if (ox*ox + oy*oy < radius*radius) {
           ellipse(x + ox, y + oy, 2, 2);
        }
      }
    }
  }
"""
    },
    "72": {
        "name": "Cubism",
        "description": "Overlays multiple perspectives or shifted blocks of the image. (Ref: Picasso)",
        "global_vars": "",
        "draw_loop": """
  background(0);
  
  // paramA controls fragmentation
  let cols = floor(map(paramA, 0, 1, 2, 8));
  let rows = cols;
  let w = width / cols;
  let h = height / rows;
  
  for (let y = 0; y < rows; y++) {
    for (let x = 0; x < cols; x++) {
      let px = x * w;
      let py = y * h;
      
      // Random offset for source rectangle
      let ox = random(-20, 20);
      let oy = random(-20, 20);
      
      // Random scale/rotation for that block
      push();
      translate(px + w/2, py + h/2);
      rotate(random(-0.1, 0.1));
      
      // Draw part of video
      // source x, y, w, h -> dest x, y, w, h
      // We are drawing centered at 0,0 because of translate
      let sx = px + ox;
      let sy = py + oy;
      
      // Ensure source is within bounds
      sx = constrain(sx, 0, width - w);
      sy = constrain(sy, 0, height - h);
      
      image(video, -w/2, -h/2, w, h, sx, sy, w, h);
      
      // Draw border
      noFill();
      stroke(0);
      strokeWeight(2);
      rect(-w/2, -h/2, w, h);
      pop();
    }
  }
"""
    },
    "73": {
        "name": "Ink Wash",
        "description": "Converts to grayscale and simulates ink diffusion/bleeding. (Ref: Sumi-e)",
        "global_vars": "",
        "draw_loop": """
  // Slow fade for trail effect
  noStroke();
  fill(255, 20);
  rect(0, 0, width, height);
  
  video.loadPixels();
  
  // paramA controls number of drops
  let drops = floor(map(paramA, 0, 1, 10, 50));
  
  for (let i = 0; i < drops; i++) {
    let x = floor(random(width));
    let y = floor(random(height));
    let idx = (x + y * width) * 4;
    
    let bright = (video.pixels[idx] + video.pixels[idx+1] + video.pixels[idx+2]) / 3;
    
    // Ink is dark
    if (bright < 150) {
      let radius = map(bright, 0, 150, 20, 2); // Darker = larger blob
      
      fill(0, 50); // Semi-transparent black
      
      beginShape();
      for (let a = 0; a < TWO_PI; a += 0.5) {
        let r = radius + random(-2, 2);
        vertex(x + cos(a) * r, y + sin(a) * r);
      }
      endShape(CLOSE);
    }
  }
"""
    },
    "74": {
        "name": "Pastel",
        "description": "Softens colors and adds a rough paper texture overlay. (Ref: Chalk)",
        "global_vars": "let paperTexture;",
        "draw_loop": """
  if (!paperTexture) {
    paperTexture = createGraphics(width, height);
    paperTexture.noStroke();
    for (let i = 0; i < 10000; i++) {
      paperTexture.fill(random(200, 255), 50);
      paperTexture.rect(random(width), random(height), 2, 2);
    }
  }

  video.loadPixels();
  loadPixels();
  
  // paramA controls color simplification
  let levels = floor(map(paramA, 0, 1, 4, 12));
  let bin = 255 / levels;
  
  for (let i = 0; i < pixels.length; i += 4) {
    let r = video.pixels[i];
    let g = video.pixels[i+1];
    let b = video.pixels[i+2];
    
    // Quantize and brighten (Pastel look)
    r = floor(r / bin) * bin + bin/2 + 20;
    g = floor(g / bin) * bin + bin/2 + 20;
    b = floor(b / bin) * bin + bin/2 + 20;
    
    pixels[i] = constrain(r, 0, 255);
    pixels[i+1] = constrain(g, 0, 255);
    pixels[i+2] = constrain(b, 0, 255);
    pixels[i+3] = 255;
  }
  updatePixels();
  
  // Overlay texture
  image(paperTexture, 0, 0);
"""
    },
    "75": {
        "name": "Pencil Hatching",
        "description": "Uses generated flow fields to direct pencil strokes along image contours. (Ref: Drawing)",
        "global_vars": "",
        "draw_loop": """
  background(255);
  video.loadPixels();
  stroke(0, 150);
  strokeWeight(1);
  
  // paramA controls stroke density
  let density = floor(map(paramA, 0, 1, 1000, 5000));
  
  for (let i = 0; i < density; i++) {
    let x = floor(random(width));
    let y = floor(random(height));
    
    // Sobel-like gradient approximation
    let idx = (x + y * width) * 4;
    let idxRight = (min(x+1, width-1) + y * width) * 4;
    let idxDown = (x + min(y+1, height-1) * width) * 4;
    
    let b = (video.pixels[idx] + video.pixels[idx+1] + video.pixels[idx+2]) / 3;
    let bRight = (video.pixels[idxRight] + video.pixels[idxRight+1] + video.pixels[idxRight+2]) / 3;
    let bDown = (video.pixels[idxDown] + video.pixels[idxDown+1] + video.pixels[idxDown+2]) / 3;
    
    // Only draw in darker areas
    if (b < 200) {
      let dx = bRight - b;
      let dy = bDown - b;
      
      // Angle perpendicular to gradient (contour)
      let angle = atan2(dy, dx) + HALF_PI;
      
      let len = map(b, 0, 200, 10, 2);
      
      push();
      translate(x, y);
      rotate(angle);
      line(-len, 0, len, 0);
      pop();
    }
  }
"""
    }
}