<?php
// ============================================================
//  Schüler-Chat – Proxy (DeepInfra + Mistral, streaming)
//  ------------------------------------------------------------
//  Diese Datei gehört in DENSELBEN Ordner wie schueler.html.
//  Die API-Keys bleiben ausschließlich hier auf dem Server –
//  der Browser der Schüler bekommt sie nie zu sehen.
//
//  Per FTP hochladen, dann NUR den Konfigurations-Block unten
//  ausfüllen. Am Code darunter muss nichts geändert werden.
// ============================================================


// ╔══════════════════════════════════════════════════════════╗
// ║  KONFIGURATION – NUR HIER ETWAS ÄNDERN                    ║
// ╚══════════════════════════════════════════════════════════╝

// ── 1) Kurs-Passwort ──────────────────────────────────────────
//    Das geben die Schüler im Login-Fenster ein.
//    Pro Kurs/Halbjahr am besten wechseln.
$ACCESS_PASSWORD = '2026arduino';

// ── 2) Anbieter + Keys ────────────────────────────────────────
//    Trage die beiden Keys ein. Die URLs stimmen bereits.
$PROVIDERS = [
    'deepinfra' => [
        'key' => ',
        'url' => 'https://api.deepinfra.com/v1/openai/chat/completions',
    ],
    'mistral'   => [
        'key' => ',
        'url' => 'https://api.eu.mistral.ai/v1/chat/completions',
    ],
    // LM Studio (lokaler Rechner im Schulnetz) braucht keinen Key.
    // IP und Port stehen direkt beim Modell-Eintrag unten.
    'lmstudio'  => [
        'key' => '',
        'url' => '',
    ],
];

// ── 3) Freigegebene Modelle (Whitelist / Dropdown) ────────────
//    'label'    = was der Schüler im Dropdown sieht
//    'id'       = exakte Modell-Kennung, wie die API sie erwartet
//    'provider' = 'deepinfra', 'mistral' oder 'lmstudio'
//
//    Nur bei 'lmstudio' zusätzlich:
//    'ip'       = IP-Adresse des Rechners, auf dem LM Studio läuft
//    'port'     = Port des LM-Studio-Servers (Standard: 1234)
//    'id'       = Modell-Kennung, wie LM Studio sie anzeigt
//                 (Developer-Tab → „API Model Identifier")
//    Nur Textmodelle eintragen – die App schickt ausschließlich Text.
//
//    Zeilen nach Belieben ergänzen, ändern oder löschen.
//    Das Dropdown in der App zieht automatisch nach.
$ALLOWED_MODELS = [
    ['label' => 'DeepSeek-V4.1-Flash', 'id' => 'deepseek-ai/DeepSeek-V4.1-Flash', 'provider' => 'deepinfra'],
    ['label' => 'DeepSeek-V4-Flash-0731', 'id' => 'deepseek-ai/DeepSeek-V4-Flash-0731', 'provider' => 'deepinfra'],
    ['label' => 'zai-org/GLM-5.3-Flash', 'id' => 'zai-org/GLM-5.3-Flash', 'provider' => 'deepinfra'],
    ['label' => 'mistral-large-2512', 'id' => 'mistral-large-2512', 'provider' => 'mistral'],
    ['label' => 'mistral-large-4', 'id' => 'mistral-large-4', 'provider' => 'mistral', 'request_options' => ['reasoning_effort' => 'none'],],
    ['label' => 'LM Studio (lokal)', 'id' => 'qwen/qwen3.8-27b', 'provider' => 'lmstudio', 'ip' => '172.20.0.16', 'port' => 1234],
];

// ── 4) Kostenbremse ───────────────────────────────────────────
//    Deckelt die Antwortlänge – kappt zu große Anfragen.
$MAX_TOKENS_CAP = 2048;

//    Max. Chat-Anfragen pro Browser-Sitzung und Stunde.
$RATE_LIMIT = 40;


// ╔══════════════════════════════════════════════════════════╗
// ║  AB HIER NICHTS MEHR ÄNDERN                               ║
// ╚══════════════════════════════════════════════════════════╝

// Diese Datei wird aus schueler.html im selben Ordner aufgerufen
// (gleiche Herkunft) – deshalb absichtlich KEINE offenen
// CORS-Header. So kann keine fremde Website den Proxy missbrauchen.

$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';

// ── Kleiner Helfer: JSON-Fehler im OpenAI-Stil zurückgeben ────
function json_error($code, $message) {
    http_response_code($code);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode(['error' => ['message' => $message]]);
    exit;
}

// ── LM Studio: URL aus IP + Port eines Modell-Eintrags bauen ──
//    Liefert '' bei ungültiger Angabe. Toleriert http:// und /.
function lmstudio_url($entry) {
    $ip   = trim((string)($entry['ip'] ?? ''));
    $ip   = preg_replace('#^https?://#i', '', $ip);
    $ip   = rtrim($ip, '/');
    $port = (int)($entry['port'] ?? 1234);
    if ($ip === '' || $port < 1 || $port > 65535) return '';
    if (strpos($ip, ':') !== false) $ip = '[' . $ip . ']';   // IPv6-Adresse
    return 'http://' . $ip . ':' . $port . '/v1/chat/completions';
}

// ── Passwort aus dem Header X-Access-Key lesen ────────────────
function access_key_from_request() {
    if (isset($_SERVER['HTTP_X_ACCESS_KEY'])) {
        return $_SERVER['HTTP_X_ACCESS_KEY'];
    }
    if (function_exists('getallheaders')) {
        foreach (getallheaders() as $k => $v) {
            if (strtolower($k) === 'x-access-key') return $v;
        }
    }
    return '';
}

// ── Passwortprüfung (für GET und POST) ────────────────────────
$provided = access_key_from_request();
if (!is_string($ACCESS_PASSWORD) || $ACCESS_PASSWORD === '' ||
    $ACCESS_PASSWORD === 'HIER_KURS_PASSWORT_EINTRAGEN') {
    json_error(500, 'Server ist noch nicht fertig eingerichtet (kein Passwort gesetzt).');
}
if (!hash_equals($ACCESS_PASSWORD, (string)$provided)) {
    json_error(401, 'Passwort falsch.');
}

// ── GET: Modell-Liste fürs Dropdown ───────────────────────────
//    Gibt bewusst nur label + id zurück – Provider/Keys bleiben hier.
if ($method === 'GET') {
    header('Content-Type: application/json; charset=utf-8');
    //    LM-Studio-Modelle bekommen zusätzlich ihre lokale Adresse:
    //    Der Browser im Schulnetz spricht LM Studio direkt an, weil
    //    dieser Server im Internet die private IP nicht erreichen kann.
    $out = array_map(function ($m) {
        $o = ['label' => $m['label'], 'id' => $m['id']];
        if (($m['provider'] ?? '') === 'lmstudio') {
            $url = lmstudio_url($m);
            if ($url !== '') $o['local'] = $url;
        }
        return $o;
    }, $ALLOWED_MODELS);
    echo json_encode(['models' => $out]);
    exit;
}

// ── Ab hier nur noch POST (Chat) ──────────────────────────────
if ($method !== 'POST') {
    json_error(405, 'Nur GET oder POST erlaubt.');
}

// ── Rate Limiting pro Browser-Sitzung ─────────────────────────
//    Weiches Limit gegen versehentliche Dauerlast. Der harte
//    Kostenschutz sind Modell-Whitelist + max_tokens-Deckel.
session_start();
$now = time();
if (!isset($_SESSION['rl']) || ($now - $_SESSION['rl']['start']) > 3600) {
    $_SESSION['rl'] = ['count' => 0, 'start' => $now];
}
$_SESSION['rl']['count']++;
if ($_SESSION['rl']['count'] > $RATE_LIMIT) {
    json_error(429, 'Zu viele Anfragen in dieser Stunde. Bitte kurz warten.');
}

// ── Request-Body lesen und prüfen ─────────────────────────────
$raw  = file_get_contents('php://input');
$data = json_decode($raw, true);

if (!is_array($data) || !isset($data['model'], $data['messages'])) {
    json_error(400, 'Ungültige Anfrage.');
}

// ── Modell gegen Whitelist prüfen und Provider bestimmen ──────
$entry = null;
foreach ($ALLOWED_MODELS as $m) {
    if ($m['id'] === $data['model']) { $entry = $m; break; }
}
if ($entry === null) {
    json_error(400, 'Dieses Modell ist nicht freigegeben.');
}

$prov    = $PROVIDERS[$entry['provider']] ?? null;
$isLocal = ($entry['provider'] === 'lmstudio');

if ($isLocal) {
    // LM Studio: nur erreichbar, wenn dieser Proxy selbst im Schulnetz läuft
    $url = lmstudio_url($entry);
    if ($url === '') {
        json_error(500, 'Für dieses LM-Studio-Modell sind IP oder Port nicht korrekt eingetragen.');
    }
    $prov = ['key' => $prov['key'] ?? '', 'url' => $url];
} elseif (!$prov || empty($prov['key']) || strpos($prov['key'], 'HIER_') === 0) {
    json_error(500, 'Für dieses Modell ist serverseitig kein gültiger Key hinterlegt.');
}

// ── Modellspezifische Zusatz-Parameter (request_options) ──────
//    z. B. 'reasoning_effort' => 'none' – überschreiben Client-Werte.
if (!empty($entry['request_options']) && is_array($entry['request_options'])) {
    $data = array_merge($data, $entry['request_options']);
}

// ── Kostenbremse + Streaming erzwingen ────────────────────────
$req = (isset($data['max_tokens']) && is_numeric($data['max_tokens']))
     ? (int)$data['max_tokens'] : $MAX_TOKENS_CAP;
$data['max_tokens'] = max(1, min($req, $MAX_TOKENS_CAP));
$data['stream']     = true;

// ── Vor dem Streamen: Puffer aus, Session-Sperre lösen ────────
@ini_set('zlib.output_compression', '0');
while (ob_get_level() > 0) { ob_end_clean(); }
ob_implicit_flush(true);
session_write_close();   // sonst blockieren parallele Anfragen desselben Schülers

// ── Anfrage an den Anbieter weiterleiten und Chunks durchreichen ──
$upstreamStatus = 0;
$headersSent    = false;

$httpHeaders = [
    'Content-Type: application/json',
    'Accept: text/event-stream',
];
if (!empty($prov['key'])) {
    $httpHeaders[] = 'Authorization: Bearer ' . $prov['key'];   // Key bleibt serverseitig
}

$ch = curl_init($prov['url']);
curl_setopt_array($ch, [
    CURLOPT_POST       => true,
    CURLOPT_POSTFIELDS => json_encode($data),
    CURLOPT_HTTPHEADER => $httpHeaders,
    // Lokale Modelle sind langsamer und laden beim ersten Aufruf erst
    CURLOPT_CONNECTTIMEOUT => $isLocal ? 5 : 15,
    CURLOPT_TIMEOUT        => $isLocal ? 300 : 120,

    // Upstream-Statuscode abgreifen, bevor der Body kommt
    CURLOPT_HEADERFUNCTION => function ($ch, $header) use (&$upstreamStatus) {
        if (preg_match('#^HTTP/\S+\s+(\d+)#', $header, $mm)) {
            $upstreamStatus = (int)$mm[1];
        }
        return strlen($header);
    },

    // Jeden Chunk sofort an den Browser weiterreichen
    CURLOPT_WRITEFUNCTION => function ($ch, $chunk) use (&$upstreamStatus, &$headersSent) {
        if (!$headersSent) {
            // Header erst jetzt setzen – jetzt kennen wir den Upstream-Status.
            if ($upstreamStatus >= 200 && $upstreamStatus < 300) {
                header('Content-Type: text/event-stream; charset=utf-8');
                header('Cache-Control: no-cache');
                header('X-Accel-Buffering: no');   // nginx: Puffern aus
            } else {
                // Fehlerantwort des Anbieters unverändert mit echtem Status durchreichen
                http_response_code($upstreamStatus ?: 502);
                header('Content-Type: application/json; charset=utf-8');
            }
            $headersSent = true;
        }
        echo $chunk;
        flush();
        return strlen($chunk);
    },
]);

curl_exec($ch);
$curlErr = curl_error($ch);
curl_close($ch);

// Es kam nie ein Chunk zurück → Anbieter nicht erreichbar
if (!$headersSent) {
    http_response_code(502);
    header('Content-Type: application/json; charset=utf-8');
    $msg = $isLocal
        ? 'LM Studio nicht erreichbar – ist der Server gestartet und im Netzwerk freigegeben?'
        : 'Anbieter nicht erreichbar';
    echo json_encode(['error' => ['message' =>
        $msg . ($curlErr ? ' (' . $curlErr . ')' : '') . '.']]);
}
