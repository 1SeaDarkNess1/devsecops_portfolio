/* BBM Lab — 3D Threat Globe (three.js, no extra deps) */
(() => {
  const mount = document.getElementById('globe-container');
  if (!mount || !window.THREE) return;

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ---------- Helpers ----------
  function ll2vec(lat, lng, r = 1) {
    const phi = (90 - lat) * Math.PI / 180;
    const theta = (lng + 180) * Math.PI / 180;
    return new THREE.Vector3(
      -Math.sin(phi) * Math.cos(theta) * r,
       Math.cos(phi) * r,
       Math.sin(phi) * Math.sin(theta) * r
    );
  }
  async function loadThreats() {
    try {
      const r = await fetch('/api/threats', { cache: 'no-store' });
      if (!r.ok) throw new Error();
      const j = await r.json();
      const list = Array.isArray(j) ? j : (j.attacks || j.threats || []);
      // Normalize: accept lon or lng, coerce to numbers.
      const norm = list.map(a => ({
        lat: typeof a.lat === 'number' ? a.lat : parseFloat(a.lat),
        lng: typeof a.lng === 'number' ? a.lng : (typeof a.lon === 'number' ? a.lon : parseFloat(a.lon ?? a.lng)),
        country: a.country || a.name || '',
        count: a.count || a.hits || 1
      })).filter(x => Number.isFinite(x.lat) && Number.isFinite(x.lng));
      if (norm.length) return norm;
    } catch (_) {}
    // fallback dataset
    return [
      { lat: 39.9042, lng: 116.4074, country: 'China',         count: 245 },
      { lat: 55.7558, lng:  37.6173, country: 'Russia',        count: 180 },
      { lat: 38.9072, lng: -77.0369, country: 'United States', count: 310 },
      { lat: -23.5505, lng: -46.6333, country: 'Brazil',       count: 140 },
      { lat:  1.3521, lng: 103.8198, country: 'Singapore',     count:  92 },
      { lat: 48.8566, lng:   2.3522, country: 'France',        count:  88 },
      { lat: -33.8688, lng: 151.2093, country: 'Australia',    count:  75 },
      { lat: 35.6895, lng: 139.6917, country: 'Japan',         count: 125 },
      { lat: 28.6139, lng:  77.2090, country: 'India',         count: 210 },
      { lat: -34.6037, lng: -58.3816, country: 'Argentina',    count:  65 },
    ];
  }

  // ---------- Continent mask — Natural Earth (public domain) ----------
  function loadMaskCanvas() {
    return new Promise((resolve) => {
      const img = new Image();
      // Served locally to avoid CSP blocking unpkg.com
      img.src = '/static/img/earth-mask.png';
      img.onload = () => {
        const c = document.createElement('canvas');
        c.width = 1024; c.height = 512;
        const ctx = c.getContext('2d', { willReadFrequently: true });
        ctx.drawImage(img, 0, 0, c.width, c.height);
        resolve(ctx.getImageData(0, 0, c.width, c.height));
      };
      img.onerror = () => resolve(null);
    });
  }

  function isLandAt(mask, lat, lng) {
    if (!mask) {
      const x = Math.sin((lng + 180) * Math.PI / 180);
      const y = Math.cos((90 - lat) * Math.PI / 180);
      const z = Math.cos((lng + 180) * Math.PI / 180);
      const n = Math.sin(x * 3.1) * Math.cos(y * 2.3) + Math.sin(z * 2.8 + 1.3) * Math.cos(x * 3.7);
      return n > 0.55;
    }
    const u = (lng + 180) / 360;
    const v = (90 - lat) / 180;
    const W = mask.width, H = mask.height;
    const cx = Math.min(W - 1, Math.max(0, Math.floor(u * W)));
    const cy = Math.min(H - 1, Math.max(0, Math.floor(v * H)));
    // 5×5 dilation with a lenient threshold — if ANY pixel in the 25-cell
    // neighbourhood reads above threshold, the candidate counts as land.
    // Closes the last pixel-scale holes in anti-aliased regions (coastal
    // transitions, small Pacific/Caribbean islands) without bleeding into
    // open ocean: 5 pixels on a 1024×512 texture ≈ 200 km of reach, well
    // within continental-shelf noise.
    const T = 5;
    for (let dy = -2; dy <= 2; dy++) {
      const py = Math.min(H - 1, Math.max(0, cy + dy));
      for (let dx = -2; dx <= 2; dx++) {
        const px = Math.min(W - 1, Math.max(0, cx + dx));
        if (mask.data[(py * W + px) * 4] > T) return true;
      }
    }
    return false;
  }

  // Reusable radial-gradient canvas → THREE.Texture for soft glows.
  // One texture, many sprites: cheap on GPU, gives every marker a luminous
  // halo instead of a flat dot.
  function glowTexture() {
    const size = 128;
    const c = document.createElement('canvas');
    c.width = c.height = size;
    const ctx = c.getContext('2d');
    const g = ctx.createRadialGradient(size/2, size/2, 0, size/2, size/2, size/2);
    g.addColorStop(0.0, 'rgba(255,255,255,1.0)');
    g.addColorStop(0.25, 'rgba(255,255,255,0.55)');
    g.addColorStop(0.55, 'rgba(255,255,255,0.12)');
    g.addColorStop(1.0, 'rgba(255,255,255,0.0)');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, size, size);
    const tex = new THREE.CanvasTexture(c);
    tex.minFilter = THREE.LinearFilter;
    return tex;
  }

  // ---------- Scene ----------
  async function init() {
    const GLOW_TEX = glowTexture();
    const threats = await loadThreats();
    threats.sort((a, b) => (b.count || 0) - (a.count || 0));
    const total = threats.reduce((s, t) => s + (t.count || 0), 0);

    // HUD text
    const gbCountries = document.getElementById('gb-countries');
    const gbAttacks   = document.getElementById('gb-attacks');
    const gbTop       = document.getElementById('gb-top');
    const gbTotal     = document.getElementById('gb-total');
    if (gbCountries) gbCountries.textContent = threats.length;
    if (gbAttacks)   gbAttacks.textContent   = total.toLocaleString();
    if (gbTop && threats[0]) gbTop.textContent = `${threats[0].country} · ${threats[0].count}`;
    if (gbTotal)     gbTotal.textContent     = total.toLocaleString();

    const HQ = { lat: 50.11, lng: 8.68 };
    const hqVec = ll2vec(HQ.lat, HQ.lng);

    const w0 = mount.clientWidth || 520;
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(42, 1, 0.1, 100);
    camera.position.set(0, 0, 3.4);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(w0, w0, false);
    mount.appendChild(renderer.domElement);

    // --- dark core (opaque, writes depth so back-side markers are occluded) ---
    const core = new THREE.Mesh(
      new THREE.SphereGeometry(0.998, 64, 64),
      new THREE.MeshBasicMaterial({ color: 0x0b1914 })
    );
    core.renderOrder = 0;
    scene.add(core);

    // --- Fresnel atmosphere ---
    const atmo = new THREE.Mesh(
      new THREE.SphereGeometry(1.08, 64, 64),
      new THREE.ShaderMaterial({
        vertexShader: `varying vec3 vNormal;
          void main(){
            vNormal = normalize(normalMatrix * normal);
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
          }`,
        fragmentShader: `varying vec3 vNormal; uniform vec3 uColor;
          void main(){
            float i = pow(0.72 - dot(vNormal, vec3(0.0, 0.0, 1.0)), 3.2);
            gl_FragColor = vec4(uColor, 1.0) * i;
          }`,
        uniforms: { uColor: { value: new THREE.Color('#BEF264') } },
        blending: THREE.AdditiveBlending,
        side: THREE.BackSide,
        transparent: true,
      })
    );
    scene.add(atmo);

    // --- wireframe meridians + parallels ---
    const wire = new THREE.Group();
    const wireMat = new THREE.LineBasicMaterial({ color: 0xBEF264, transparent: true, opacity: 0.16 });
    for (let lon = -180; lon < 180; lon += 15) {
      const pts = [];
      for (let lat = -90; lat <= 90; lat += 4) pts.push(ll2vec(lat, lon));
      wire.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), wireMat));
    }
    for (let lat = -75; lat <= 75; lat += 15) {
      const pts = [];
      for (let lon = -180; lon <= 180; lon += 4) pts.push(ll2vec(lat, lon));
      wire.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), wireMat));
    }
    // brighter equator
    (() => {
      const pts = [];
      for (let lon = -180; lon <= 180; lon += 2) pts.push(ll2vec(0, lon));
      wire.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts),
        new THREE.LineBasicMaterial({ color: 0xBEF264, transparent: true, opacity: 0.42 })));
    })();
    scene.add(wire);

    // --- continent dots (masked with Natural Earth texture) ---
    const mask = await loadMaskCanvas();
    const continents = await buildContinents(mask);
    scene.add(continents);

    // --- HQ marker: bright core + glow sprite + two staggered ripple rings ---
    const hqGroup = new THREE.Group();
    const hqPos = hqVec.clone().multiplyScalar(1.012);

    const hqCore = new THREE.Mesh(
      new THREE.SphereGeometry(0.02, 16, 16),
      new THREE.MeshBasicMaterial({ color: 0xBEF264 })
    );
    hqCore.position.copy(hqPos);
    hqGroup.add(hqCore);

    const hqGlow = new THREE.Sprite(new THREE.SpriteMaterial({
      map: GLOW_TEX, color: 0xBEF264,
      blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, opacity: 0.95,
    }));
    hqGlow.position.copy(hqPos);
    hqGlow.scale.setScalar(0.18);
    hqGroup.add(hqGlow);

    // Expanding ripple rings — two staggered copies on a 2s loop
    const hqRipples = [];
    for (let i = 0; i < 2; i++) {
      const ring = new THREE.Mesh(
        new THREE.RingGeometry(0.022, 0.028, 48),
        new THREE.MeshBasicMaterial({
          color: 0xBEF264, side: THREE.DoubleSide,
          transparent: true, opacity: 0, depthWrite: false,
        })
      );
      ring.position.copy(hqPos);
      ring.lookAt(0, 0, 0);
      ring.userData = { t: i * 0.5 }; // stagger by half a cycle
      hqGroup.add(ring);
      hqRipples.push(ring);
    }
    scene.add(hqGroup);

    // --- threat markers + arcs ---
    const markerGroup = new THREE.Group();
    const arcGroup = new THREE.Group();
    const arcs = [];
    scene.add(markerGroup, arcGroup);

    threats.forEach((t, idx) => {
      const origin = ll2vec(t.lat, t.lng);
      const pos = origin.clone().multiplyScalar(1.01);
      const sev = t.count > 200 ? 'high' : t.count > 100 ? 'med' : 'low';
      const color = sev === 'high' ? 0xfca5a5 : sev === 'med' ? 0xfbbf24 : 0x5EEAD4;

      // Bright dot (hard pixel on top)
      const dot = new THREE.Mesh(
        new THREE.SphereGeometry(0.014, 14, 14),
        new THREE.MeshBasicMaterial({ color })
      );
      dot.position.copy(pos);
      dot.userData = { kind: 'dot', phase: Math.random() * Math.PI * 2 };
      markerGroup.add(dot);

      // Soft additive glow sprite — turns every marker into a luminous pulse
      const glowBase = 0.11 + (sev === 'high' ? 0.05 : sev === 'med' ? 0.025 : 0);
      const glow = new THREE.Sprite(new THREE.SpriteMaterial({
        map: GLOW_TEX, color,
        blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, opacity: 0.8,
      }));
      glow.position.copy(pos);
      glow.scale.setScalar(glowBase);
      glow.userData = { kind: 'glow', phase: Math.random() * Math.PI * 2, baseScale: glowBase };
      markerGroup.add(glow);

      // Expanding ripple ring — radiates outward once per cycle
      const ripple = new THREE.Mesh(
        new THREE.RingGeometry(0.018, 0.022, 40),
        new THREE.MeshBasicMaterial({
          color, side: THREE.DoubleSide,
          transparent: true, opacity: 0, depthWrite: false,
        })
      );
      ripple.position.copy(origin.clone().multiplyScalar(1.012));
      ripple.lookAt(0, 0, 0);
      ripple.userData = { kind: 'ripple', t: (idx % 6) / 6 }; // de-synced per marker
      markerGroup.add(ripple);

      // elevated great-circle arc
      const mid = origin.clone().add(hqVec).multiplyScalar(0.5);
      const lift = 1 + 0.35 + origin.distanceTo(hqVec) * 0.18;
      mid.normalize().multiplyScalar(lift);
      const curve = new THREE.QuadraticBezierCurve3(
        origin.clone().multiplyScalar(1.005),
        mid,
        hqVec.clone().multiplyScalar(1.005)
      );
      const geo = new THREE.BufferGeometry().setFromPoints(curve.getPoints(60));
      const arc = new THREE.Line(geo, new THREE.LineBasicMaterial({ color: 0x5EEAD4, transparent: true, opacity: 0.42 }));
      arc.userData = { phase: Math.random() * Math.PI * 2 };
      arcGroup.add(arc);

      // Comet spark: hard core + trailing glow sprite for a textured "packet"
      const sparkGroup = new THREE.Group();
      const sparkCore = new THREE.Mesh(
        new THREE.SphereGeometry(0.012, 10, 10),
        new THREE.MeshBasicMaterial({ color: 0x5EEAD4 })
      );
      const sparkGlow = new THREE.Sprite(new THREE.SpriteMaterial({
        map: GLOW_TEX, color: 0x5EEAD4,
        blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, opacity: 0.9,
      }));
      sparkGlow.scale.setScalar(0.09);
      sparkGroup.add(sparkCore, sparkGlow);
      sparkGroup.userData = {
        curve, glowMat: sparkGlow.material,
        t: Math.random(), speed: 0.004 + Math.random() * 0.004,
      };
      arcGroup.add(sparkGroup);
      arcs.push(sparkGroup);
    });

    // --- interaction ---
    let dragging = false, lastX = 0, lastY = 0;
    // Initial view: slight tilt + rotated so Europe/Africa face the camera
    let targetY = -0.35, targetX = 0.15, rotY = -0.35, rotX = 0.15;
    let autoRot = !reducedMotion;

    mount.addEventListener('pointerdown', (e) => {
      dragging = true; lastX = e.clientX; lastY = e.clientY;
      autoRot = false;
      mount.setPointerCapture(e.pointerId);
    });
    mount.addEventListener('pointermove', (e) => {
      if (!dragging) return;
      targetY += (e.clientX - lastX) * 0.005;
      targetX += (e.clientY - lastY) * 0.005;
      targetX = Math.max(-0.9, Math.min(0.9, targetX));
      lastX = e.clientX; lastY = e.clientY;
    });
    mount.addEventListener('pointerup',    () => { dragging = false; setTimeout(() => { autoRot = !reducedMotion; }, 3000); });
    mount.addEventListener('pointerleave', () => { dragging = false; });

    // --- resize ---
    function resize() {
      const w = mount.clientWidth;
      if (!w) return;
      renderer.setSize(w, w, false);
      camera.aspect = 1; camera.updateProjectionMatrix();
    }
    window.addEventListener('resize', resize);
    new ResizeObserver(resize).observe(mount);

    // --- animate ---
    const clock = new THREE.Clock();
    function tick() {
      const dt = clock.getDelta();
      const t  = clock.elapsedTime;

      if (autoRot) targetY += dt * 0.12;
      rotY += (targetY - rotY) * 0.08;
      rotX += (targetX - rotX) * 0.08;

      [core, wire, continents, hqGroup, markerGroup, arcGroup].forEach(o => {
        o.rotation.y = rotY; o.rotation.x = rotX;
      });

      if (!reducedMotion) {
        markerGroup.children.forEach(m => {
          const k = m.userData.kind;
          if (k === 'dot') {
            m.scale.setScalar(1 + 0.28 * Math.sin(t * 2.5 + m.userData.phase));
          } else if (k === 'glow') {
            // Breathing halo — size + opacity pulse together, preserving
            // the per-marker base scale (severity-sized).
            const p = (Math.sin(t * 2.2 + m.userData.phase) + 1) / 2;
            m.material.opacity = 0.55 + 0.4 * p;
            const base = m.userData.baseScale || 0.11;
            m.scale.setScalar(base * (1 + 0.35 * p));
          } else if (k === 'ripple') {
            // One ring expanding outward, fading as it grows (radar-ping look).
            m.userData.t = (m.userData.t + dt * 0.55) % 1;
            const p = m.userData.t;
            const s = 1 + p * 2.2;
            m.scale.setScalar(s);
            m.material.opacity = (1 - p) * 0.7;
          }
        });
        arcGroup.children.forEach(obj => {
          if (obj.type === 'Line') {
            obj.material.opacity = 0.26 + 0.32 * (Math.sin(t * 2 + (obj.userData.phase || 0)) + 1) / 2;
          }
        });
        arcs.forEach(sp => {
          sp.userData.t += sp.userData.speed;
          if (sp.userData.t > 1) sp.userData.t = 0;
          sp.position.copy(sp.userData.curve.getPoint(sp.userData.t));
          // Comet fades in/out at the endpoints, peaks mid-flight.
          const near = 1 - Math.abs(sp.userData.t - 0.5) * 2;
          if (sp.userData.glowMat) sp.userData.glowMat.opacity = 0.3 + near * 0.8;
        });
        // HQ core pulse
        hqCore.scale.setScalar(1 + 0.18 * Math.sin(t * 2));
        // HQ glow breathe
        hqGlow.material.opacity = 0.75 + 0.2 * Math.sin(t * 2 + 0.3);
        hqGlow.scale.setScalar(0.18 + 0.03 * Math.sin(t * 2));
        // HQ ripple rings — staggered radar pings
        hqRipples.forEach(r => {
          r.userData.t = (r.userData.t + dt * 0.45) % 1;
          const p = r.userData.t;
          r.scale.setScalar(1 + p * 2.6);
          r.material.opacity = (1 - p) * 0.85;
        });
      }

      renderer.render(scene, camera);
      requestAnimationFrame(tick);
    }
    tick();
  }

  // ---------- Continents: dot cloud masked on Natural Earth texture ----------
  async function buildContinents(mask) {
    // Higher N + 5×5 dilated mask + smaller point → denser, fully-filled
    // continents without bleed into oceans.
    const N = 200000;
    const positions = [];
    for (let i = 0; i < N; i++) {
      const phi = Math.acos(1 - 2 * (i + 0.5) / N);
      const theta = Math.PI * (1 + Math.sqrt(5)) * i;
      const x = -Math.sin(phi) * Math.cos(theta);
      const y =  Math.cos(phi);
      const z =  Math.sin(phi) * Math.sin(theta);
      const lat = 90 - (phi * 180 / Math.PI);
      // ll2vec uses theta_v = (lng+180)*π/180, so lng = theta_deg - 180 (wrapped to [-180, 180])
      const lng = ((theta * 180 / Math.PI - 180) % 360 + 540) % 360 - 180;
      if (isLandAt(mask, lat, lng)) {
        positions.push(x * 1.002, y * 1.002, z * 1.002);
      }
    }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));

    const mat = new THREE.ShaderMaterial({
      uniforms: { uColor: { value: new THREE.Color('#BEF264') } },
      vertexShader: `varying float vAlpha;
        void main(){
          vec4 mv = modelViewMatrix * vec4(position, 1.0);
          // Front hemisphere fully visible; back hemisphere fades out smoothly.
          vAlpha = clamp(-mv.z * 0.6 + 0.35, 0.0, 1.0);
          gl_Position = projectionMatrix * mv;
          // Smaller dot now that N=200k; density carries the silhouette.
          gl_PointSize = 3.3 * (1.8 / -mv.z);
        }`,
      fragmentShader: `uniform vec3 uColor; varying float vAlpha;
        void main(){
          vec2 c = gl_PointCoord - 0.5;
          float d = length(c);
          if (d > 0.5) discard;
          // Soft round dot with anti-aliased edge.
          float edge = smoothstep(0.5, 0.35, d);
          gl_FragColor = vec4(uColor, vAlpha * edge);
        }`,
      transparent: true,
      depthWrite: false,
    });
    return new THREE.Points(geo, mat);
  }

  init();
})();
