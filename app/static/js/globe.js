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
    const px = Math.min(mask.width  - 1, Math.max(0, Math.floor(u * mask.width)));
    const py = Math.min(mask.height - 1, Math.max(0, Math.floor(v * mask.height)));
    const idx = (py * mask.width + px) * 4;
    return mask.data[idx] > 90;
  }

  // ---------- Scene ----------
  async function init() {
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

    // --- HQ marker ---
    const hqGroup = new THREE.Group();
    const hqCore = new THREE.Mesh(
      new THREE.SphereGeometry(0.018, 16, 16),
      new THREE.MeshBasicMaterial({ color: 0xBEF264 })
    );
    hqCore.position.copy(hqVec.clone().multiplyScalar(1.01));
    hqGroup.add(hqCore);
    const hqRing = new THREE.Mesh(
      new THREE.RingGeometry(0.022, 0.028, 32),
      new THREE.MeshBasicMaterial({ color: 0xBEF264, side: THREE.DoubleSide, transparent: true, opacity: 0.8 })
    );
    hqRing.position.copy(hqVec.clone().multiplyScalar(1.012));
    hqRing.lookAt(0, 0, 0);
    hqGroup.add(hqRing);
    scene.add(hqGroup);

    // --- threat markers + arcs ---
    const markerGroup = new THREE.Group();
    const arcGroup = new THREE.Group();
    const arcs = [];
    scene.add(markerGroup, arcGroup);

    threats.forEach((t) => {
      const origin = ll2vec(t.lat, t.lng);
      const sev = t.count > 200 ? 'high' : t.count > 100 ? 'med' : 'low';
      const color = sev === 'high' ? 0xfca5a5 : sev === 'med' ? 0xfbbf24 : 0x5EEAD4;

      const dot = new THREE.Mesh(
        new THREE.SphereGeometry(0.013, 12, 12),
        new THREE.MeshBasicMaterial({ color })
      );
      dot.position.copy(origin.clone().multiplyScalar(1.01));
      dot.userData = { base: 0.013, phase: Math.random() * Math.PI * 2 };
      markerGroup.add(dot);

      const halo = new THREE.Mesh(
        new THREE.RingGeometry(0.02, 0.028, 24),
        new THREE.MeshBasicMaterial({ color, side: THREE.DoubleSide, transparent: true, opacity: 0.45 })
      );
      halo.position.copy(origin.clone().multiplyScalar(1.011));
      halo.lookAt(0, 0, 0);
      halo.userData = { phase: Math.random() * Math.PI * 2 };
      markerGroup.add(halo);

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

      const spark = new THREE.Mesh(
        new THREE.SphereGeometry(0.011, 10, 10),
        new THREE.MeshBasicMaterial({ color: 0x5EEAD4, transparent: true, opacity: 0.9 })
      );
      spark.userData = { curve, t: Math.random(), speed: 0.004 + Math.random() * 0.004 };
      arcGroup.add(spark);
      arcs.push(spark);
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
          if (m.userData.base) {
            m.scale.setScalar(1 + 0.35 * Math.sin(t * 2.5 + m.userData.phase));
          } else {
            const p = (Math.sin(t * 2.2 + (m.userData.phase || 0)) + 1) / 2;
            m.material.opacity = 0.25 + 0.5 * p;
            m.scale.setScalar(1 + p * 0.6);
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
          const near = 1 - Math.abs(sp.userData.t - 0.5) * 2;
          sp.material.opacity = 0.3 + near * 0.7;
        });
        hqRing.scale.setScalar(1 + 0.25 * Math.sin(t * 2));
        hqRing.material.opacity = 0.55 + 0.35 * Math.sin(t * 2 + 0.3);
      }

      renderer.render(scene, camera);
      requestAnimationFrame(tick);
    }
    tick();
  }

  // ---------- Continents: dot cloud masked on Natural Earth texture ----------
  async function buildContinents(mask) {
    const N = 60000;
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
          vAlpha = clamp(-mv.z * 0.4 + 0.08, 0.0, 1.0);
          gl_Position = projectionMatrix * mv;
          gl_PointSize = 2.2 * (1.6 / -mv.z);
        }`,
      fragmentShader: `uniform vec3 uColor; varying float vAlpha;
        void main(){
          vec2 c = gl_PointCoord - 0.5;
          if (length(c) > 0.5) discard;
          gl_FragColor = vec4(uColor, vAlpha);
        }`,
      transparent: true,
      depthWrite: false,
    });
    return new THREE.Points(geo, mat);
  }

  init();
})();
