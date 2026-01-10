let video;
let paramA = 0.0; // MouseX normalized (0.0 to 1.0)
let paramB = 0.0; // MouseY normalized (0.0 to 1.0)
let helpVisible = false;

// [INJECTED GLOBAL VARIABLES START]
{{GLOBAL_VARS}}
// [INJECTED GLOBAL VARIABLES END]

function setup() {
  createCanvas(800, 600);
  pixelDensity(1); // Ensure 1:1 pixel mapping for performance
  
  video = createCapture(VIDEO);
  video.size(width, height);
  video.hide(); // Hide the default HTML video element
  
  noStroke();

  // UI Controls
  let btnSave = createButton('Save');
  btnSave.position(10, 10);
  btnSave.mousePressed(() => saveCanvas('pyprism_output', 'png'));

  let btnHelp = createButton('Help');
  btnHelp.position(60, 10);
  btnHelp.mousePressed(() => helpVisible = !helpVisible);

  let btnExit = createButton('Exit');
  btnExit.position(110, 10);
  btnExit.mousePressed(() => {
    console.log("Exiting sketch...");
    noLoop();
    video.pause();
    fetch('/shutdown').finally(() => window.close());
  });
}

function draw() {
  // Standardized Input Mapping
  // Map mouseX to paramA (0.0 to 1.0)
  paramA = constrain(mouseX / width, 0.0, 1.0);
  // Map mouseY to paramB (0.0 to 1.0)
  paramB = constrain(mouseY / height, 0.0, 1.0);

  // [INJECTED DRAW LOOP LOGIC START]
  {{DRAW_LOOP_LOGIC}}
  // [INJECTED DRAW LOOP LOGIC END]

  if (helpVisible) {
    push();
    fill(0, 200);
    rect(0, 0, width, height);
    fill(255);
    textSize(16);
    textAlign(CENTER, CENTER);
    text("Controls:\nMouse X/Y: Adjust Effect\n'S': Save Screenshot\n'H': Toggle Help\n'E': Exit", width / 2, height / 2);
    pop();
  }
}

function keyPressed() {
  if (key === 's' || key === 'S') saveCanvas('pixelsynth_output', 'png');
  if (key === 'h' || key === 'H') helpVisible = !helpVisible;
  if (key === 'e' || key === 'E') {
    noLoop();
    video.pause();
    fetch('/shutdown').finally(() => window.close());
  }
}