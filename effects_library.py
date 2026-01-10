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
    }
}