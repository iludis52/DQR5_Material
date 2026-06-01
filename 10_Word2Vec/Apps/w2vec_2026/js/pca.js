/*
 * ============================================================================
 *  w2vec_2026 — Hauptkomponentenanalyse (PCA)
 * ----------------------------------------------------------------------------
 *  Bibliotheksfreie PCA zur 2D-Projektion der Wortvektoren.
 *  Der numerische SVD-Kern (Golub & Reinsch, 1970) wurde aus der Original-App
 *  übernommen und von allen D3-Abhängigkeiten befreit (range/zip/sum/map
 *  durch reines JavaScript ersetzt).
 *
 *  Verwendung:
 *      const model = fitPCA(rows);     // rows: Array von Vektoren (n × d)
 *      const [x, y] = model.project(vec);
 *
 *  Es wird auf die Eingabevektoren "gefittet"; beliebige Vektoren (auch
 *  Ausgabevektoren) lassen sich anschließend auf dieselben Achsen projizieren.
 * ============================================================================
 */

/* --- kleine Matrix-Helfer ------------------------------------------------ */
function _transpose(X) {
  const rows = X.length, cols = X[0].length;
  const T = [];
  for (let j = 0; j < cols; j++) {
    const r = new Array(rows);
    for (let i = 0; i < rows; i++) r[i] = X[i][j];
    T.push(r);
  }
  return T;
}

function _colMeans(X) {
  const rows = X.length, cols = X[0].length;
  const m = new Array(cols).fill(0);
  for (let i = 0; i < rows; i++)
    for (let j = 0; j < cols; j++) m[j] += X[i][j];
  for (let j = 0; j < cols; j++) m[j] /= rows;
  return m;
}

function _dot(a, b) {
  let s = 0;
  for (let i = 0; i < a.length; i++) s += a[i] * b[i];
  return s;
}

function _column(M, k) {
  return M.map(row => row[k]);
}

/*
 * Golub-Reinsch Thin-SVD.  A: m × n mit m >= n.
 * Rückgabe { U (m×n), S (n), V (n×n) } mit A = U · diag(S) · Vᵀ.
 */
function _svd(A) {
  let prec = Math.pow(2, -52);
  const tolerance = 1.e-64 / prec;
  const itmax = 50;
  let c = 0, i = 0, j = 0, k = 0, l = 0;

  const u = A.map(row => row.slice(0));
  const m = u.length;
  const n = u[0].length;

  if (m < n) throw new Error('SVD: benötigt mehr Zeilen als Spalten');

  const e = new Array(n).fill(0);
  const q = new Array(n).fill(0);
  const v = [];
  for (i = 0; i < n; i++) v.push(new Array(n).fill(0));

  function pythag(a, b) {
    a = Math.abs(a); b = Math.abs(b);
    if (a > b) return a * Math.sqrt(1.0 + (b * b / a / a));
    if (b === 0) return a;
    return b * Math.sqrt(1.0 + (a * a / b / b));
  }

  let f = 0, g = 0, h = 0, x = 0, y = 0, z = 0, s = 0;

  for (i = 0; i < n; i++) {
    e[i] = g; s = 0.0; l = i + 1;
    for (j = i; j < m; j++) s += (u[j][i] * u[j][i]);
    if (s <= tolerance) { g = 0.0; }
    else {
      f = u[i][i];
      g = Math.sqrt(s);
      if (f >= 0.0) g = -g;
      h = f * g - s;
      u[i][i] = f - g;
      for (j = l; j < n; j++) {
        s = 0.0;
        for (k = i; k < m; k++) s += u[k][i] * u[k][j];
        f = s / h;
        for (k = i; k < m; k++) u[k][j] += f * u[k][i];
      }
    }
    q[i] = g; s = 0.0;
    for (j = l; j < n; j++) s = s + u[i][j] * u[i][j];
    if (s <= tolerance) { g = 0.0; }
    else {
      f = u[i][i + 1];
      g = Math.sqrt(s);
      if (f >= 0.0) g = -g;
      h = f * g - s;
      u[i][i + 1] = f - g;
      for (j = l; j < n; j++) e[j] = u[i][j] / h;
      for (j = l; j < m; j++) {
        s = 0.0;
        for (k = l; k < n; k++) s += (u[j][k] * u[i][k]);
        for (k = l; k < n; k++) u[j][k] += s * e[k];
      }
    }
    y = Math.abs(q[i]) + Math.abs(e[i]);
    if (y > x) x = y;
  }

  for (i = n - 1; i !== -1; i += -1) {
    if (g !== 0.0) {
      h = g * u[i][i + 1];
      for (j = l; j < n; j++) v[j][i] = u[i][j] / h;
      for (j = l; j < n; j++) {
        s = 0.0;
        for (k = l; k < n; k++) s += u[i][k] * v[k][j];
        for (k = l; k < n; k++) v[k][j] += (s * v[k][i]);
      }
    }
    for (j = l; j < n; j++) { v[i][j] = 0; v[j][i] = 0; }
    v[i][i] = 1; g = e[i]; l = i;
  }

  for (i = n - 1; i !== -1; i += -1) {
    l = i + 1; g = q[i];
    for (j = l; j < n; j++) u[i][j] = 0;
    if (g !== 0.0) {
      h = u[i][i] * g;
      for (j = l; j < n; j++) {
        s = 0.0;
        for (k = l; k < m; k++) s += u[k][i] * u[k][j];
        f = s / h;
        for (k = i; k < m; k++) u[k][j] += f * u[k][i];
      }
      for (j = i; j < m; j++) u[j][i] = u[j][i] / g;
    } else {
      for (j = i; j < m; j++) u[j][i] = 0;
    }
    u[i][i] += 1;
  }

  prec = prec * x;
  for (k = n - 1; k !== -1; k += -1) {
    for (let iteration = 0; iteration < itmax; iteration++) {
      let test_convergence = false;
      for (l = k; l !== -1; l += -1) {
        if (Math.abs(e[l]) <= prec) { test_convergence = true; break; }
        if (Math.abs(q[l - 1]) <= prec) break;
      }
      if (!test_convergence) {
        c = 0.0; s = 1.0;
        const l1 = l - 1;
        for (i = l; i < k + 1; i++) {
          f = s * e[i];
          e[i] = c * e[i];
          if (Math.abs(f) <= prec) break;
          g = q[i];
          h = pythag(f, g);
          q[i] = h; c = g / h; s = -f / h;
          for (j = 0; j < m; j++) {
            y = u[j][l1]; z = u[j][i];
            u[j][l1] = y * c + (z * s);
            u[j][i] = -y * s + (z * c);
          }
        }
      }
      z = q[k];
      if (l === k) {
        if (z < 0.0) {
          q[k] = -z;
          for (j = 0; j < n; j++) v[j][k] = -v[j][k];
        }
        break;
      }
      // Verschiebung aus der unteren 2×2-Untermatrix
      x = q[l]; y = q[k - 1]; g = e[k - 1]; h = e[k];
      f = ((y - z) * (y + z) + (g - h) * (g + h)) / (2.0 * h * y);
      g = pythag(f, 1.0);
      if (f < 0.0) f = ((x - z) * (x + z) + h * (y / (f - g) - h)) / x;
      else f = ((x - z) * (x + z) + h * (y / (f + g) - h)) / x;
      c = 1.0; s = 1.0;
      for (i = l + 1; i < k + 1; i++) {
        g = e[i]; y = q[i]; h = s * g; g = c * g;
        z = pythag(f, h);
        e[i - 1] = z; c = f / z; s = h / z;
        f = x * c + g * s; g = -x * s + g * c; h = y * s; y = y * c;
        for (j = 0; j < n; j++) {
          x = v[j][i - 1]; z = v[j][i];
          v[j][i - 1] = x * c + z * s;
          v[j][i] = -x * s + z * c;
        }
        z = pythag(f, h);
        q[i - 1] = z; c = f / z; s = h / z;
        f = c * g + s * y; x = -s * g + c * y;
        for (j = 0; j < m; j++) {
          y = u[j][i - 1]; z = u[j][i];
          u[j][i - 1] = y * c + z * s;
          u[j][i] = -y * s + z * c;
        }
      }
      e[l] = 0.0; e[k] = f; q[k] = x;
    }
  }

  for (i = 0; i < q.length; i++) if (q[i] < prec) q[i] = 0;

  // Eigenwerte (Singulärwerte) sortieren
  for (i = 0; i < n; i++) {
    for (j = i - 1; j >= 0; j--) {
      if (q[j] < q[i]) {
        c = q[j]; q[j] = q[i]; q[i] = c;
        for (k = 0; k < u.length; k++) { const t = u[k][i]; u[k][i] = u[k][j]; u[k][j] = t; }
        for (k = 0; k < v.length; k++) { const t = v[k][i]; v[k][i] = v[k][j]; v[k][j] = t; }
        i = j;
      }
    }
  }
  return { U: u, S: q, V: v };
}

/*
 * Passt ein PCA-Modell an die Zeilen (Vektoren) an.
 * Zentriert die Daten und ermittelt die ersten beiden Hauptachsen.
 * Robust auch dann, wenn es weniger Vektoren als Dimensionen gibt
 * (dann wird die SVD auf der transponierten, zentrierten Matrix gebildet).
 *
 * Rückgabe: { project(vec) -> [pc0, pc1] }
 */
function fitPCA(rows) {
  const n = rows.length;
  const d = rows[0].length;
  const mean = _colMeans(rows);
  const centered = rows.map(r => r.map((val, j) => val - mean[j]));

  let axis0, axis1;
  if (n >= d) {
    const { V } = _svd(centered);     // V: d × d, Spalten sind die Hauptachsen
    axis0 = _column(V, 0);
    axis1 = _column(V, 1);
  } else {
    const { U } = _svd(_transpose(centered));  // U: d × n, Spalten sind die Hauptachsen
    axis0 = _column(U, 0);
    axis1 = _column(U, 1);
  }

  return {
    project(vec) {
      const c = vec.map((val, j) => val - mean[j]);
      return [_dot(c, axis0), _dot(c, axis1)];
    },
  };
}
