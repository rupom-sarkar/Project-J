const canvas = document.getElementById("neuralCanvas");
const ctx = canvas.getContext("2d");

let W = 0, H = 0, dpr = 1;
let particles = [];
let pulses = [];
let mouse = { x: 0, y: 0, active: false };
let activity = 1;

function resize() {
  dpr = Math.min(window.devicePixelRatio || 1, 2);
  W = window.innerWidth;
  H = window.innerHeight;
  canvas.width = W * dpr;
  canvas.height = H * dpr;
  canvas.style.width = W + "px";
  canvas.style.height = H + "px";
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  createParticles();
}

function createParticles() {
  const count = Math.min(780, Math.max(300, Math.floor((W * H) / 2300)));
  particles = [];

  const cx = W * 0.5;
  const cy = H * 0.52;
  const radius = Math.min(W, H) * 0.23;

  for (let i = 0; i < count; i++) {
    // Dense neural sphere + outward neural filaments.
    const core = Math.random() < 0.78;

    if (core) {
      const a = Math.random() * Math.PI * 2;
      const r = Math.pow(Math.random(), .62) * radius;
      particles.push({
        x: cx + Math.cos(a) * r,
        y: cy + Math.sin(a) * r * (0.88 + Math.random() * .12),
        ox: cx,
        oy: cy,
        vx: (Math.random() - .5) * .22,
        vy: (Math.random() - .5) * .22,
        size: Math.random() * 1.7 + .35,
        alpha: Math.random() * .7 + .18,
        phase: Math.random() * Math.PI * 2,
        speed: Math.random() * .018 + .006,
        core: true
      });
    } else {
      const a = Math.random() * Math.PI * 2;
      const length = radius * (1.0 + Math.random() * 2.1);
      const start = radius * (.65 + Math.random() * .4);
      particles.push({
        x: cx + Math.cos(a) * start,
        y: cy + Math.sin(a) * start,
        angle: a,
        length,
        distance: start,
        wave: Math.random() * 20,
        size: Math.random() * 1.5 + .3,
        alpha: Math.random() * .55 + .12,
        phase: Math.random() * Math.PI * 2,
        speed: Math.random() * .35 + .08,
        core: false
      });
    }
  }
}

function drawGlowDot(x, y, size, alpha) {
  ctx.save();
  ctx.globalAlpha = alpha;
  ctx.shadowBlur = 12 + size * 7;
  ctx.shadowColor = "#ff9d16";
  ctx.fillStyle = "#ffd064";
  ctx.beginPath();
  ctx.arc(x, y, size, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();
}

function animate(t) {
  const time = t * 0.001;
  ctx.clearRect(0, 0, W, H);

  const cx = W * .5;
  const cy = H * .52;
  const coreRadius = Math.min(W, H) * .235;

  // Ambient orange cloud.
  const gradient = ctx.createRadialGradient(cx, cy, 0, cx, cy, coreRadius * 2.8);
  gradient.addColorStop(0, `rgba(255,145,10,${.055 * activity})`);
  gradient.addColorStop(.45, "rgba(255,95,0,.018)");
  gradient.addColorStop(1, "rgba(0,0,0,0)");
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, W, H);

  // Neural filaments.
  ctx.save();
  ctx.lineWidth = .65;
  for (let i = 0; i < particles.length; i++) {
    const p = particles[i];

    if (!p.core) {
      p.distance += Math.sin(time * p.speed + p.phase) * .035;
      const d = p.distance + Math.sin(time * .7 + p.phase) * 5;
      const wave = Math.sin(d * .045 + time * 1.3 + p.wave) * 14;
      const x = cx + Math.cos(p.angle) * d + Math.cos(p.angle + Math.PI/2) * wave;
      const y = cy + Math.sin(p.angle) * d + Math.sin(p.angle + Math.PI/2) * wave;

      ctx.globalAlpha = p.alpha * .55;
      ctx.strokeStyle = "rgba(255,157,20,.7)";
      ctx.beginPath();
      ctx.moveTo(cx + Math.cos(p.angle) * coreRadius * .5, cy + Math.sin(p.angle) * coreRadius * .5);
      ctx.quadraticCurveTo(
        cx + Math.cos(p.angle + .12) * d * .52,
        cy + Math.sin(p.angle + .12) * d * .52,
        x, y
      );
      ctx.stroke();

      if (Math.random() < .0018 * activity) {
        pulses.push({ x, y, a: 1, r: 1 });
      }

      drawGlowDot(x, y, p.size, p.alpha);
      continue;
    }

    const dx = p.x - cx;
    const dy = p.y - cy;
    const dist = Math.sqrt(dx*dx + dy*dy);
    const drift = Math.sin(time * p.speed + p.phase) * 1.5 * activity;

    p.x += p.vx + Math.cos(time * .4 + p.phase) * .012;
    p.y += p.vy + Math.sin(time * .35 + p.phase) * .012;

    // Keep core particles around the neural sphere.
    if (dist > coreRadius * 1.18) {
      p.x = cx + dx / dist * coreRadius * .92;
      p.y = cy + dy / dist * coreRadius * .92;
    }

    const near = Math.abs(dist - coreRadius * .72) < coreRadius * .23;
    if (near && Math.random() < .022 * activity) {
      drawGlowDot(p.x + drift, p.y, p.size * 1.5, p.alpha * .9);
    } else {
      drawGlowDot(p.x + drift, p.y, p.size, p.alpha);
    }
  }
  ctx.restore();

  // Connect nearby particles in the core to create the neural-network look.
  ctx.save();
  ctx.lineWidth = .45;
  for (let i = 0; i < particles.length; i += 2) {
    const a = particles[i];
    if (!a.core) continue;

    for (let j = i + 1; j < Math.min(i + 35, particles.length); j++) {
      const b = particles[j];
      if (!b.core) continue;
      const dx = a.x - b.x;
      const dy = a.y - b.y;
      const d2 = dx*dx + dy*dy;

      if (d2 < 1500) {
        const alpha = (1 - Math.sqrt(d2) / 39) * .22 * activity;
        ctx.strokeStyle = `rgba(255,178,53,${alpha})`;
        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.lineTo(b.x, b.y);
        ctx.stroke();
      }
    }
  }
  ctx.restore();

  // Energy pulses traveling across the interface.
  for (let i = pulses.length - 1; i >= 0; i--) {
    const p = pulses[i];
    p.r += 1.5;
    p.a -= .018;
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
    ctx.strokeStyle = `rgba(255,194,75,${Math.max(0,p.a)})`;
    ctx.lineWidth = 1;
    ctx.shadowBlur = 12;
    ctx.shadowColor = "#ff9d16";
    ctx.stroke();
    if (p.a <= 0) pulses.splice(i, 1);
  }

  // Mouse interaction.
  if (mouse.active) {
    const dx = mouse.x - cx;
    const dy = mouse.y - cy;
    const d = Math.sqrt(dx*dx + dy*dy);
    if (d < coreRadius * 2.4) {
      ctx.beginPath();
      ctx.arc(mouse.x, mouse.y, 18 + Math.sin(time*5)*4, 0, Math.PI*2);
      ctx.strokeStyle = "rgba(255,193,72,.4)";
      ctx.shadowBlur = 20;
      ctx.shadowColor = "#ff9d00";
      ctx.stroke();
    }
  }

  requestAnimationFrame(animate);
}

window.addEventListener("resize", resize);
window.addEventListener("mousemove", e => {
  mouse.x = e.clientX;
  mouse.y = e.clientY;
  mouse.active = true;
});
window.addEventListener("mouseleave", () => mouse.active = false);

// UI / command interaction.
const commandBtn = document.getElementById("commandBtn");
const consolePanel = document.getElementById("console");
const closeConsole = document.getElementById("closeConsole");
const input = document.getElementById("commandInput");
const send = document.getElementById("sendCommand");

commandBtn.addEventListener("click", () => {
  consolePanel.classList.add("open");
  setTimeout(() => input.focus(), 180);
  activity = 1.5;
});

closeConsole.addEventListener("click", () => {
  consolePanel.classList.remove("open");
  activity = 1;
});

send.addEventListener("click", runCommand);
input.addEventListener("keydown", e => {
  if (e.key === "Enter") runCommand();
});

function runCommand() {
  const value = input.value.trim();
  if (!value) return;

  document.getElementById("listenState").textContent = "COMMAND RECEIVED...";
  document.getElementById("processState").textContent = "NEURAL PROCESSING...";
  document.getElementById("respondState").textContent = "RESPONDING...";

  activity = 2.2;
  for (let i = 0; i < 20; i++) {
    const angle = Math.random() * Math.PI * 2;
    const r = Math.min(W, H) * .18;
    pulses.push({
      x: W*.5 + Math.cos(angle)*r,
      y: H*.52 + Math.sin(angle)*r,
      a: 1,
      r: 1
    });
  }

  setTimeout(() => {
    document.getElementById("listenState").textContent = "LISTENING...";
    document.getElementById("processState").textContent = "PROCESSING...";
    document.getElementById("respondState").textContent = "RESPONDING...";
    activity = 1;
  }, 1800);

  input.value = "";
}

// Tiny simulated activity changes so the UI feels alive even before a backend is connected.
setInterval(() => {
  const states = [
    ["LISTENING...", "PROCESSING...", "RESPONDING..."],
    ["VOICE INPUT...", "ANALYZING...", "READY..."],
    ["NEURAL SYNC...", "PROCESSING...", "STANDING BY..."]
  ];
  const s = states[Math.floor(Math.random() * states.length)];
  document.getElementById("listenState").textContent = s[0];
  document.getElementById("processState").textContent = s[1];
  document.getElementById("respondState").textContent = s[2];
}, 4200);

resize();
requestAnimationFrame(animate);
