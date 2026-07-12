from flask import Flask, request, jsonify, render_template_string
import requests
import re

app = Flask(__name__)

# HTML with YouTube Hidden Player integrated for background music
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes">
<title>𓆩𝕊̷7̷𝕃̷ 𝕄̷𝔸̷ℍ̷𝔻̷𝕀̷𓆪 LONG BIO</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
body { background: #050508; color: #e2e8f0; overflow-x: hidden; min-height: 100vh; }
canvas { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 0; pointer-events: none; opacity: 0.35; }

.container { position: relative; z-index: 1; max-width: 520px; margin: 0 auto; padding: 24px 16px 40px; }

/* Header Styling */
h1 { text-align: center; color: #00ffc3; text-shadow: 0 0 20px rgba(0, 255, 195, 0.6); font-size: 1.8rem; margin: 15px 0 8px; letter-spacing: 1px; font-weight: 800; }
.subtitle { text-align: center; margin-bottom: 20px; }
.api-badge { display: inline-block; background: rgba(0, 255, 195, 0.1); color: #00ffc3; padding: 6px 16px; border-radius: 30px; font-size: 0.8rem; border: 1px solid rgba(0, 255, 195, 0.3); font-weight: 600; box-shadow: 0 0 15px rgba(0, 255, 195, 0.1); }

/* Links Styling */
.links { display: flex; justify-content: center; gap: 12px; margin-bottom: 24px; flex-wrap: wrap; }
.links a { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); color: #e2e8f0; padding: 8px 16px; border-radius: 16px; text-decoration: none; font-size: 0.85rem; font-weight: 600; display: flex; align-items: center; gap: 8px; transition: all 0.3s ease; }
.links a i { color: #00ffc3; }
.links a:hover { background: rgba(0, 255, 195, 0.08); border-color: #00ffc3; transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0, 255, 195, 0.1); }

/* Card Styling */
.card { background: rgba(13, 17, 28, 0.75); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border-radius: 24px; padding: 22px; margin-bottom: 20px; border: 1px solid rgba(255, 255, 255, 0.06); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1); transition: border 0.3s ease; }
.card:hover { border-color: rgba(0, 255, 195, 0.2); }
.card h3 { font-size: 1rem; color: #0099ff; margin-bottom: 14px; display: flex; align-items: center; gap: 8px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }

/* Form Controls */
textarea { width: 100%; height: 120px; border-radius: 16px; background: #070913; border: 1px solid rgba(255, 255, 255, 0.1); color: #fff; padding: 14px; font-size: 15px; resize: none; font-family: 'Courier New', Courier, monospace; transition: all 0.3s ease; outline: none; }
textarea:focus { border-color: #00ffc3; box-shadow: 0 0 15px rgba(0, 255, 195, 0.15); }

.preview { margin-top: 14px; padding: 14px; background: #070913; border-radius: 16px; border: 1px dashed rgba(0, 255, 195, 0.3); min-height: 65px; font-size: 15px; word-wrap: break-word; color: #cbd5e1; }

/* Buttons & Formatting */
.format-group { display: flex; flex-wrap: wrap; gap: 8px; }
.format-btn { flex: 1; min-width: 80px; background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 10px; font-weight: 600; color: #cbd5e1; cursor: pointer; font-size: 13px; transition: all 0.2s ease; }
.format-btn:hover { background: #00ffc3; color: #000; font-weight: 700; border-color: #00ffc3; transform: scale(1.03); }

/* Color Ribbon */
.colors-ribbon { display: grid; grid-template-columns: repeat(8, 1fr); gap: 8px; margin-top: 5px; max-height: 140px; overflow-y: auto; padding-right: 4px; }
.colors-ribbon::-webkit-scrollbar { width: 4px; }
.colors-ribbon::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }
.c-dot { height: 32px; border-radius: 10px; cursor: pointer; border: 1px solid rgba(0,0,0,0.3); transition: transform 0.2s ease, box-shadow 0.2s ease; }
.c-dot:hover { transform: scale(1.15) translateY(-2px); box-shadow: 0 5px 10px rgba(0,0,0,0.5); z-index: 2; }

/* Inputs and Custom Dropdowns */
input, select { width: 100%; padding: 14px 18px; margin-top: 12px; border-radius: 16px; background: #070913; border: 1px solid rgba(255, 255, 255, 0.1); color: #fff; font-size: 14px; outline: none; transition: all 0.3s ease; -webkit-appearance: none; appearance: none; }
select { background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10' fill='%2300ffc3'><polygon points='0,0 10,0 5,5'/></svg>"); background-repeat: no-repeat; background-position: right 18px center; padding-right: 40px; }
input:focus, select:focus { border-color: #0099ff; box-shadow: 0 0 15px rgba(0, 153, 255, 0.15); }

/* Input Group with Button */
.input-btn-group { display: flex; gap: 8px; align-items: flex-end; width: 100%; }
.input-btn-group input { flex: 1; }
.get-token-btn { background: rgba(0, 255, 195, 0.1); border: 1px solid rgba(0, 255, 195, 0.4); color: #00ffc3; padding: 14px 16px; border-radius: 16px; font-weight: 600; cursor: pointer; font-size: 13px; height: 48px; margin-top: 12px; display: flex; align-items: center; justify-content: center; gap: 6px; white-space: nowrap; transition: all 0.2s ease; }
.get-token-btn:hover { background: #00ffc3; color: #050508; border-color: #00ffc3; font-weight: 700; box-shadow: 0 0 15px rgba(0, 255, 195, 0.3); }

/* Action Button */
button#submitBtn { background: linear-gradient(90deg, #00ffc3, #0099ff); border: none; border-radius: 16px; padding: 14px; font-weight: 700; color: #050508; cursor: pointer; font-size: 15px; letter-spacing: 0.5px; transition: all 0.3s ease; box-shadow: 0 4px 20px rgba(0, 255, 195, 0.25); }
button#submitBtn:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 6px 25px rgba(0, 255, 195, 0.4); opacity: 0.95; }
button#submitBtn:disabled { background: #1e293b; color: #64748b; cursor: not-allowed; box-shadow: none; border: 1px solid rgba(255,255,255,0.05); }

/* Overlay Notifications */
#overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(5, 5, 8, 0.95); backdrop-filter: blur(25px); -webkit-backdrop-filter: blur(25px); z-index: 1000; display: flex; flex-direction: column; justify-content: center; align-items: center; opacity: 0; visibility: hidden; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
#overlay.active { opacity: 1; visibility: visible; }
.res-icon { font-size: 80px; margin-bottom: 20px; scale: 0.7; transition: transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
#overlay.active .res-icon { scale: 1; }
.res-title { font-size: 26px; font-weight: 800; letter-spacing: 1px; }
.res-body { text-align: center; padding: 24px; max-width: 90%; color: #94a3b8; font-size: 15px; }
.success .res-icon { color: #00ffc3; text-shadow: 0 0 30px rgba(0,255,195,0.4); }
.error .res-icon { color: #ff4757; text-shadow: 0 0 30px rgba(255,71,87,0.4); }

/* ===== CAPTCHA STYLES ===== */
#captchaOverlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(4, 5, 10, 0.98); backdrop-filter: blur(25px); -webkit-backdrop-filter: blur(25px); z-index: 2000; display: flex; justify-content: center; align-items: center; padding: 20px; }
#captchaOverlay.hidden { display: none; }
.captcha-box { background: rgba(13, 17, 28, 0.9); border-radius: 28px; padding: 35px 25px; max-width: 420px; width: 100%; border: 1px solid rgba(0, 255, 195, 0.2); box-shadow: 0 20px 50px rgba(0,0,0,0.6); text-align: center; }
.captcha-box .robot-icon { font-size: 55px; margin-bottom: 12px; }
.captcha-box h2 { color: #fff; font-size: 1.4rem; font-weight: 700; margin-bottom: 6px; }
.captcha-box .sub-text { color: #64748b; font-size: 0.85rem; margin-bottom: 24px; }
.captcha-slider-container { background: #070913; border-radius: 20px; padding: 4px; border: 1px solid rgba(255,255,255,0.08); position: relative; margin: 20px 0; display: flex; align-items: center; height: 56px; user-select: none; -webkit-user-select: none; touch-action: none; }
.captcha-slider-track { flex: 1; height: 100%; border-radius: 16px; position: relative; overflow: hidden; }
.captcha-slider-fill { height: 100%; width: 0%; background: linear-gradient(90deg, #00ffc3, #0099ff); border-radius: 16px; position: absolute; left: 0; top: 0; }
.captcha-slider-thumb { width: 48px; height: 48px; border-radius: 14px; background: #fff; position: absolute; top: 50%; transform: translateY(-50%); left: 4px; box-shadow: 0 4px 15px rgba(0, 255, 195, 0.3); display: flex; align-items: center; justify-content: center; font-size: 18px; color: #000; z-index: 2; cursor: grab; }
.captcha-progress-text { position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); font-size: 0.85rem; color: rgba(255,255,255,0.4); z-index: 1; font-weight: 600; pointer-events: none; }
.captcha-status { margin-top: 15px; font-size: 0.9rem; color: #94a3b8; min-height: 24px; }
.captcha-status.verified { color: #00ffc3; font-weight: bold; }
.captcha-refresh { background: transparent; border: 1px solid rgba(255,255,255,0.1); color: #64748b; padding: 8px 18px; border-radius: 12px; font-size: 0.8rem; cursor: pointer; margin-top: 12px; transition: all 0.2s; }
.captcha-refresh:hover { border-color: #00ffc3; color: #00ffc3; }

/* Hidden YouTube Player Wrapper */
#yt-player-container { position: fixed; width: 1px; height: 1px; left: -10px; top: -10px; opacity: 0; pointer-events: none; }
</style>
</head>
<body>

<!-- Hidden Area for YouTube Iframe -->
<div id="yt-player-container">
    <div id="yt-audio-player"></div>
</div>

<!-- ===== CAPTCHA OVERLAY ===== -->
<div id="captchaOverlay">
    <div class="captcha-box">
        <div class="robot-icon">🤖</div>
        <h2>Security Verification</h2>
        <p class="sub-text">Slide the bar to verify you are a human helper.</p>
        
        <div class="captcha-slider-container" id="sliderContainer">
            <div class="captcha-slider-track">
                <div class="captcha-slider-fill" id="sliderFill"></div>
                <span class="captcha-progress-text" id="progressText">Slide to unlock</span>
            </div>
            <div class="captcha-slider-thumb" id="sliderThumb">
                <i class="fas fa-chevron-right"></i>
            </div>
        </div>
        <div class="captcha-status" id="captchaStatus">👉 Drag the slider to the right</div>
        <button class="captcha-refresh" onclick="resetCaptcha()">⟳ Refresh</button>
    </div>
</div>

<!-- ===== RESULT OVERLAY ===== -->
<div id="overlay">
    <i id="res-icon" class="fas fa-check-circle res-icon"></i>
    <div id="res-title" class="res-title"></div>
    <div id="res-body" class="res-body"></div>
</div>

<canvas id="matrix"></canvas>

<div class="container">
    <h1>𓆩𝕊̷7̷𝕃̷ 𝕄̷𝔸̷ℍ̷𝔻̷𝕀̷𓆪 LONG BIO</h1>
    <div class="subtitle">
        <span class="api-badge">⚡ Powered by 𓆩𝕊̷7̷𝕃̷ 𝕄̷𝔸̷ℍ̷𝔻̷𝕀̷𓆪</span>
    </div>
    
    <div class="links">
        <a href="https://t.me/Xxm0t" target="_blank"><i class="fas fa-user-shield"></i> Owner</a>
        <a href="https://t.me/mf5rt1" target="_blank"><i class="fas fa-bullhorn"></i> Channel</a>
        <a href="https://t.me/AsaadYT2012" target="_blank"><i class="fas fa-user-friends"></i> Friend</a>
    </div>

    <!-- 1. TEXT GRADIENT COLORS -->
    <div class="card">
        <h3><i class="fas fa-palette"></i> Text Gradient Colors</h3>
        <div class="colors-ribbon" id="colorRibbon"></div>
    </div>

    <!-- 2. FORMATTING TOOLS -->
    <div class="card">
        <h3><i class="fas fa-font"></i> Formatting Tools</h3>
        <div class="format-group">
            <button class="format-btn" onclick="insertSimple('[b]')"><b>Bold</b></button>
            <button class="format-btn" onclick="insertSimple('[i]')"><i>Italic</i></button>
            <button class="format-btn" onclick="insertSimple('[c]')">Curve</button>
            <button class="format-btn" onclick="insertSimple('[u]')"><u>Underline</u></button>
            <button class="format-btn" onclick="insertSimple('[s]')"><kbd>Strike</kbd></button>
        </div>
    </div>
    
    <!-- 3. BIO EDITOR -->
    <div class="card">
        <h3><i class="fas fa-pen-nib"></i> Bio Editor</h3>
        <textarea id="bio" placeholder="Type or paste your bio description here..."></textarea>
        <div id="charCount" style="text-align:right; font-size:12px; margin-top:6px; color:#64748b;">0 / 250</div>
        <div class="preview" id="preview">Live Preview Area</div>
    </div>

    <!-- 4. AUTHENTICATION & SERVER -->
    <div class="card">
        <h3><i class="fas fa-key"></i> Authentication & Server</h3>
        <select id="method" onchange="togglePassword()">
            <option value="jwt">JWT Token (Direct Link)</option>
            <option value="uid">UID & Password (Login)</option>
            <option value="access">Access Token</option>
            <option value="eat">EAT Token</option>
        </select>
        <select id="serverSelect">
            <option value="ME">🇸🇦 ME - Middle East (MENA)</option>
            <option value="IND">🇮🇳 IND - India</option>
            <option value="BD">🇧🇩 BD - Bangladesh</option>
            <option value="SG">🇸🇬 SG - Singapore</option>
            <option value="BR">🇧🇷 BR - Brazil</option>
            <option value="US">🇺🇸 US - USA</option>
            <option value="EU">🇪🇺 EU - Europe</option>
        </select>
        
        <div class="input-btn-group">
            <input id="token" placeholder="Enter Account Token / UID string" autocomplete="off">
            <button type="button" class="get-token-btn" onclick="window.open('https://ticket.kiosgamer.co.id/', '_blank')">
                <i class="fas fa-external-link-alt"></i> جلب EAT توكن
            </button>
        </div>
        
        <input id="password" placeholder="Account Password" type="password" style="display:none;">
        <button id="submitBtn" onclick="handleSubmit()" style="width:100%; margin-top:16px;" disabled>🔒 Verify First</button>
    </div>
</div>

<!-- Load YouTube Iframe Player API -->
<script src="https://www.youtube.com/iframe_api"></script>

<script>
// ========== YOUTUBE BACKGROUND AUDIO ==========
let player;
function onYouTubeIframeAPIReady() {
    player = new YT.Player('yt-audio-player', {
        height: '1',
        width: '1',
        videoId: 'fY_t3wFX6q8', // Your requested YouTube Video ID
        playerVars: {
            'autoplay': 1,
            'loop': 1,
            'playlist': 'fY_t3wFX6q8',
            'controls': 0,
            'showinfo': 0,
            'modestbranding': 1,
            'enablejsapi': 1
        },
        events: {
            'onReady': onPlayerReady
        }
    });
}

function onPlayerReady(event) {
    // Try to autoplay, will be unmuted upon user interaction
    event.target.playVideo();
}

// Force audio to play/unmute on user interaction to bypass browser blocks
function triggerAudioPlay() {
    if (player && typeof player.playVideo === 'function') {
        player.playVideo();
        if (typeof player.unMute === 'function') {
            player.unMute();
        }
    }
}

// Listen for first touch/click on page just in case
document.addEventListener('click', triggerAudioPlay, { once: true });
document.addEventListener('touchstart', triggerAudioPlay, { once: true });

// ========== MATRIX BACKGROUND ==========
const canvas = document.getElementById("matrix");
const ctx = canvas.getContext("2d");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
const letters = "S7L01S7L";
const fontSize = 14;
const columns = canvas.width / fontSize;
const drops = [];
for (let i = 0; i < columns; i++) drops[i] = 1;
function drawMatrix() {
    ctx.fillStyle = "rgba(5, 5, 8, 0.06)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "#00ffc3";
    ctx.font = fontSize + "px monospace";
    for (let i = 0; i < drops.length; i++) {
        let text = letters[Math.floor(Math.random() * letters.length)];
        ctx.fillText(text, i * fontSize, drops[i] * fontSize);
        if (drops[i] * fontSize > canvas.height && Math.random() > 0.98) drops[i] = 0;
        drops[i]++;
    }
    requestAnimationFrame(drawMatrix);
}
drawMatrix();

// ========== UTILITY FUNCTIONS ==========
function showResult(type, title, html) {
    const ov = document.getElementById('overlay');
    ov.className = type + " active";
    document.getElementById('res-icon').className = type === 'success' ? "fas fa-check-circle res-icon" : "fas fa-times-circle res-icon";
    document.getElementById('res-title').innerText = title;
    document.getElementById('res-body').innerHTML = html;
    setTimeout(() => { ov.className = ""; }, 5000);
}

function insertSimple(tag) {
    let bio = document.getElementById("bio");
    let start = bio.selectionStart;
    let end = bio.selectionEnd;
    let text = bio.value;
    let newText = text.substring(0, start) + tag + text.substring(end);
    bio.value = newText;
    bio.focus();
    bio.setSelectionRange(start + tag.length, start + tag.length);
    updatePreview();
}

function insertColor(color) {
    insertSimple('[' + color + ']');
}

function togglePassword() {
    let m = document.getElementById("method").value;
    let pwdField = document.getElementById("password");
    pwdField.style.display = (m === "uid") ? "block" : "none";
}

let lastValidBio = "";
function updatePreview() {
    let bio = document.getElementById("bio");
    if (bio.value.length > 250) {
        bio.value = lastValidBio;
        return;
    }
    lastValidBio = bio.value;
    document.getElementById("charCount").innerText = bio.value.length + " / 250";
    let raw = bio.value;
    let text = raw.replace(/[&<>]/g, function(m) {
        if (m === '&') return '&amp;';
        if (m === '<') return '&lt;';
        if (m === '>') return '&gt;';
        return m;
    });
    let result = '';
    let i = 0;
    let currentColor = null;
    let currentBold = false, currentItalic = false, currentCurve = false, currentUnderline = false, currentStrike = false;
    
    function applyCurrent() {
        let style = '';
        if (currentColor) style += `color:#${currentColor};`;
        if (currentBold) style += `font-weight:bold;`;
        if (currentItalic) style += `font-style:italic;`;
        if (currentCurve) style += `font-style:italic;`;
        if (currentUnderline) style += `text-decoration:underline;`;
        if (currentStrike) style += `text-decoration:line-through;`;
        if (style) return `<span style="${style}">`;
        return '';
    }
    
    let buffer = '';
    while (i < text.length) {
        if (text[i] === '[') {
            if (buffer) {
                let open = applyCurrent();
                result += open + buffer + (open ? '</span>' : '');
                buffer = '';
            }
            let endIdx = text.indexOf(']', i);
            if (endIdx === -1) {
                buffer += text[i];
                i++;
                continue;
            }
            let tag = text.substring(i+1, endIdx);
            i = endIdx + 1;
            if (/^[0-9A-Fa-f]{6}$/.test(tag)) {
                currentColor = tag;
            } else if (tag === 'b') {
                currentBold = !currentBold;
            } else if (tag === 'i') {
                currentItalic = !currentItalic;
            } else if (tag === 'c') {
                currentCurve = !currentCurve;
            } else if (tag === 'u') {
                currentUnderline = !currentUnderline;
            } else if (tag === 's') {
                currentStrike = !currentStrike;
            } else {
                buffer += '[' + tag + ']';
            }
        } else {
            buffer += text[i];
            i++;
        }
    }
    if (buffer) {
        let open = applyCurrent();
        result += open + buffer + (open ? '</span>' : '');
    }
    document.getElementById("preview").innerHTML = result || "Live Preview Area";
}

// ========== COLOR RIBBON ==========
const colors = ["#FF0000","#DC143C","#B22222","#8B0000","#FA8072","#FF7F50","#FF8C00","#FFA500","#FFD700","#FFFF00","#F0E68C","#98FB98","#00FF00","#32CD32","#00FF7F","#008000","#2E8B57","#556B2F","#808000","#40E0D0","#00FFFF","#00BFFF","#1E90FF","#4682B4","#0000FF","#0000CD","#00008B","#191970","#8A2BE2","#9370DB","#800080","#4B0082","#FF00FF","#EE82EE","#DA70D6","#FF1493","#FF69B4","#FFC0CB","#D2B48C","#D2691E","#A0522D","#8B4513","#FFFFFF","#C0C0C0","#A9A9A9","#808080","#696969","#2F4F4F","#000000"];
const ribbon = document.getElementById("colorRibbon");
colors.forEach(col => {
    let dot = document.createElement("div");
    dot.className = "c-dot";
    dot.style.backgroundColor = col;
    dot.onclick = () => insertColor(col.substring(1));
    ribbon.appendChild(dot);
});

document.getElementById("bio").addEventListener("input", updatePreview);
updatePreview();

// ========== SMART CAPTCHA ==========
let captchaVerified = false;
let isDragging = false;
let startX = 0;
let thumbLeft = 4;

const sliderContainer = document.getElementById('sliderContainer');
const sliderThumb = document.getElementById('sliderThumb');
const sliderFill = document.getElementById('sliderFill');
const progressText = document.getElementById('progressText');
const captchaStatus = document.getElementById('captchaStatus');
const captchaOverlay = document.getElementById('captchaOverlay');
const submitBtn = document.getElementById('submitBtn');

function getMaxLeft() {
    return sliderContainer.offsetWidth - sliderThumb.offsetWidth - 8;
}

function updateSlider(x) {
    const maxLeft = getMaxLeft();
    let left = Math.max(0, Math.min(x, maxLeft));
    const percent = (left / maxLeft) * 100;
    
    sliderThumb.style.left = (left + 4) + 'px';
    sliderFill.style.width = percent + '%';
    progressText.textContent = Math.round(percent) + '%';
    
    return left;
}

function handleStart(clientX) {
    const rect = sliderContainer.getBoundingClientRect();
    isDragging = true;
    startX = clientX - rect.left - sliderThumb.offsetWidth / 2;
    const currentLeft = parseFloat(sliderThumb.style.left) || 4;
    thumbLeft = currentLeft - 4;
    
    sliderThumb.style.transition = 'none';
    sliderFill.style.transition = 'none';
    captchaStatus.textContent = '🔓 Keep sliding...';
    triggerAudioPlay(); // Trigger music on captcha touch/drag start
}

function handleMove(clientX) {
    if (!isDragging) return;
    
    const rect = sliderContainer.getBoundingClientRect();
    const maxLeft = getMaxLeft();
    let newLeft = clientX - rect.left - sliderThumb.offsetWidth / 2;
    newLeft = Math.max(0, Math.min(newLeft, maxLeft));
    
    updateSlider(newLeft);
    
    if (newLeft >= maxLeft - 2) {
        isDragging = false;
        captchaVerified = true;
        captchaStatus.textContent = '✅ Verified Successfully!';
        captchaStatus.className = 'captcha-status verified';
        progressText.textContent = 'Verified';
        sliderThumb.style.background = '#00ffc3';
        sliderThumb.innerHTML = '<i class="fas fa-check"></i>';
        
        submitBtn.disabled = false;
        submitBtn.textContent = '🚀 UPDATE BIO';
        triggerAudioPlay(); // Double safety play check
        
        setTimeout(() => {
            captchaOverlay.classList.add('hidden');
        }, 500);
    }
}

function handleEnd() {
    if (isDragging) {
        isDragging = false;
        const maxLeft = getMaxLeft();
        const currentLeft = parseFloat(sliderThumb.style.left) || 4;
        
        if (currentLeft - 4 < maxLeft - 15) {
            sliderThumb.style.transition = 'left 0.3s ease';
            sliderFill.style.transition = 'width 0.3s ease';
            sliderThumb.style.left = '4px';
            sliderFill.style.width = '0%';
            progressText.textContent = 'Slide to unlock';
            captchaStatus.textContent = '👉 Drag to the end to verify';
        }
    }
}

sliderContainer.addEventListener('mousedown', (e) => { e.preventDefault(); handleStart(e.clientX); });
document.addEventListener('mousemove', (e) => { if (isDragging) handleMove(e.clientX); });
document.addEventListener('mouseup', handleEnd);

sliderContainer.addEventListener('touchstart', (e) => { e.preventDefault(); handleStart(e.touches[0].clientX); }, { passive: false });
document.addEventListener('touchmove', (e) => { if (isDragging) handleMove(e.touches[0].clientX); }, { passive: false });
document.addEventListener('touchend', handleEnd);

function resetCaptcha() {
    captchaVerified = false;
    isDragging = false;
    sliderThumb.style.transition = 'left 0.3s ease';
    sliderFill.style.transition = 'width 0.3s ease';
    sliderThumb.style.left = '4px';
    sliderFill.style.width = '0%';
    progressText.textContent = 'Slide to unlock';
    captchaStatus.textContent = '🔄 Verification reset';
    captchaStatus.className = 'captcha-status';
    sliderThumb.style.background = '#fff';
    sliderThumb.innerHTML = '<i class="fas fa-chevron-right"></i>';
    captchaOverlay.classList.remove('hidden');
    submitBtn.disabled = true;
    submitBtn.textContent = '🔒 Verify First';
}

// ========== MAIN SUBMIT HANDLER ==========
async function handleSubmit() {
    if (!captchaVerified) { resetCaptcha(); return; }
    await updateBio();
}

async function updateBio() {
    let method = document.getElementById("method").value;
    let token = document.getElementById("token").value.trim();
    let bio = document.getElementById("bio").value;
    let password = document.getElementById("password").value.trim();
    let server = document.getElementById("serverSelect").value;
    let btn = document.getElementById("submitBtn");
    
    if (!token) { alert("Token required!"); return; }
    if (!bio) { alert("Bio is required!"); return; }
    
    let body = { token, bio, server, method };
    if (method === "uid") {
        if (!password) { alert("Password required!"); return; }
        body.password = password;
    }
    
    let original = btn.innerText;
    btn.innerText = "⏳ Processing...";
    btn.disabled = true;
    
    try {
        let res = await fetch("/api/update", {
            method: "POST",
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify(body)
        });
        let data = await res.json();
        
        if (data.status === "success") {
            showResult('success', '✅ SUCCESS!', `
                <div style="text-align:center; padding:5px;">
                    <div><strong>🆔 UID:</strong> ${data.uid || 'N/A'}</div>
                    <div><strong>👤 Nickname:</strong> ${data.name || 'N/A'}</div>
                    <div style="margin-top:10px; color:#00ffc3;">${data.message || 'Updated!'}</div>
                </div>
            `);
            document.getElementById("token").value = "";
            document.getElementById("password").value = "";
            document.getElementById("bio").value = "";
            updatePreview();
        } else {
            showResult('error', '❌ FAILED', data.message || 'Unknown error');
        }
    } catch(e) {
        showResult('error', '⚠️ ERROR', e.message);
    } finally {
        btn.innerText = original;
        btn.disabled = false;
    }
}

window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});
</script>
</body>
</html>
"""

API_BASE_URL = "https://drogon-bio-api.vercel.app/bio"

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/update', methods=['POST'])
def update_bio():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "Missing JSON body"}), 400

        method = data.get('method', 'jwt')
        bio = data.get('bio', '').strip()
        server = data.get('server', 'IND')
        token = data.get('token', '').strip()
        password = data.get('password', '').strip()

        if not bio:
            return jsonify({"status": "error", "message": "Bio is required"}), 400
        if not token:
            return jsonify({"status": "error", "message": "Token/UID is required"}), 400

        params = {"bio": bio, "region": server}

        if method == 'uid':
            if not password:
                return jsonify({"status": "error", "message": "Password required"}), 400
            params['uid'] = token
            params['pass'] = password
        elif method == 'jwt':
            params['jwt'] = token
        elif method == 'eat':
            params['eat'] = token
        elif method == 'access':
            params['access'] = token

        response = requests.get(API_BASE_URL, params=params, timeout=30)
        response.raise_for_status()
        api_data = response.json()

        result = {
            "status": "success" if api_data.get('success') else "error",
            "message": api_data.get('status', 'Bio updated'),
            "uid": api_data.get('uid'),
            "name": api_data.get('name'),
        }

        if not api_data.get('success', False):
            result["status"] = "error"
            result["message"] = api_data.get('status', 'API failure')

        return jsonify(result)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
        <h2>Security Verification</h2>
        <p class="sub-text">Slide the bar to verify you are a human helper.</p>
        
        <div class="captcha-slider-container" id="sliderContainer">
            <div class="captcha-slider-track">
                <div class="captcha-slider-fill" id="sliderFill"></div>
                <span class="captcha-progress-text" id="progressText">Slide to unlock</span>
            </div>
            <div class="captcha-slider-thumb" id="sliderThumb">
                <i class="fas fa-chevron-right"></i>
            </div>
        </div>
        <div class="captcha-status" id="captchaStatus">👉 Drag the slider to the right</div>
        <button class="captcha-refresh" onclick="resetCaptcha()">⟳ Refresh</button>
    </div>
</div>

<!-- ===== RESULT OVERLAY ===== -->
<div id="overlay">
    <i id="res-icon" class="fas fa-check-circle res-icon"></i>
    <div id="res-title" class="res-title"></div>
    <div id="res-body" class="res-body"></div>
</div>

<canvas id="matrix"></canvas>

<div class="container">
    <h1>𓆩𝕊̷7̷𝕃̷ 𝕄̷𝔸̷ℍ̷𝔻̷𝕀̷𓆪 LONG BIO</h1>
    <div class="subtitle">
        <span class="api-badge">⚡ Powered by 𓆩𝕊̷7̷𝕃̷ 𝕄̷𝔸̷ℍ̷𝔻̷𝕀̷𓆪</span>
    </div>
    
    <div class="links">
        <a href="https://t.me/Xxm0t" target="_blank"><i class="fas fa-user-shield"></i> Owner</a>
        <a href="https://t.me/mf5rt1" target="_blank"><i class="fas fa-bullhorn"></i> Channel</a>
        <a href="https://t.me/AsaadYT2012" target="_blank"><i class="fas fa-user-friends"></i> Friend</a>
    </div>

    <!-- 1. TEXT GRADIENT COLORS -->
    <div class="card">
        <h3><i class="fas fa-palette"></i> Text Gradient Colors</h3>
        <div class="colors-ribbon" id="colorRibbon"></div>
    </div>

    <!-- 2. FORMATTING TOOLS -->
    <div class="card">
        <h3><i class="fas fa-font"></i> Formatting Tools</h3>
        <div class="format-group">
            <button class="format-btn" onclick="insertSimple('[b]')"><b>Bold</b></button>
            <button class="format-btn" onclick="insertSimple('[i]')"><i>Italic</i></button>
            <button class="format-btn" onclick="insertSimple('[c]')">Curve</button>
            <button class="format-btn" onclick="insertSimple('[u]')"><u>Underline</u></button>
            <button class="format-btn" onclick="insertSimple('[s]')"><kbd>Strike</kbd></button>
        </div>
    </div>
    
    <!-- 3. BIO EDITOR -->
    <div class="card">
        <h3><i class="fas fa-pen-nib"></i> Bio Editor</h3>
        <textarea id="bio" placeholder="Type or paste your bio description here..."></textarea>
        <div id="charCount" style="text-align:right; font-size:12px; margin-top:6px; color:#64748b;">0 / 250</div>
        <div class="preview" id="preview">Live Preview Area</div>
    </div>

    <!-- 4. AUTHENTICATION & SERVER -->
    <div class="card">
        <h3><i class="fas fa-key"></i> Authentication & Server</h3>
        <select id="method" onchange="togglePassword()">
            <option value="jwt">JWT Token (Direct Link)</option>
            <option value="uid">UID & Password (Login)</option>
            <option value="access">Access Token</option>
            <option value="eat">EAT Token</option>
        </select>
        <select id="serverSelect">
            <option value="ME">🇸🇦 ME - Middle East (MENA)</option>
            <option value="IND">🇮🇳 IND - India</option>
            <option value="BD">🇧🇩 BD - Bangladesh</option>
            <option value="SG">🇸🇬 SG - Singapore</option>
            <option value="BR">🇧🇷 BR - Brazil</option>
            <option value="US">🇺🇸 US - USA</option>
            <option value="EU">🇪🇺 EU - Europe</option>
        </select>
        
        <!-- Input Group: Token field + Get EAT Token button -->
        <div class="input-btn-group">
            <input id="token" placeholder="Enter Account Token / UID string" autocomplete="off">
            <button type="button" class="get-token-btn" onclick="window.open('https://ticket.kiosgamer.co.id/', '_blank')">
                <i class="fas fa-external-link-alt"></i> جلب EAT توكن
            </button>
        </div>
        
        <input id="password" placeholder="Account Password" type="password" style="display:none;">
        <button id="submitBtn" onclick="handleSubmit()" style="width:100%; margin-top:16px;" disabled>🔒 Verify First</button>
    </div>
</div>

<script>
// ========== MATRIX BACKGROUND ==========
const canvas = document.getElementById("matrix");
const ctx = canvas.getContext("2d");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
const letters = "S7L01S7L";
const fontSize = 14;
const columns = canvas.width / fontSize;
const drops = [];
for (let i = 0; i < columns; i++) drops[i] = 1;
function drawMatrix() {
    ctx.fillStyle = "rgba(5, 5, 8, 0.06)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "#00ffc3";
    ctx.font = fontSize + "px monospace";
    for (let i = 0; i < drops.length; i++) {
        let text = letters[Math.floor(Math.random() * letters.length)];
        ctx.fillText(text, i * fontSize, drops[i] * fontSize);
        if (drops[i] * fontSize > canvas.height && Math.random() > 0.98) drops[i] = 0;
        drops[i]++;
    }
    requestAnimationFrame(drawMatrix);
}
drawMatrix();

// ========== UTILITY FUNCTIONS ==========
function showResult(type, title, html) {
    const ov = document.getElementById('overlay');
    ov.className = type + " active";
    document.getElementById('res-icon').className = type === 'success' ? "fas fa-check-circle res-icon" : "fas fa-times-circle res-icon";
    document.getElementById('res-title').innerText = title;
    document.getElementById('res-body').innerHTML = html;
    setTimeout(() => { ov.className = ""; }, 5000);
}

function insertSimple(tag) {
    let bio = document.getElementById("bio");
    let start = bio.selectionStart;
    let end = bio.selectionEnd;
    let text = bio.value;
    let newText = text.substring(0, start) + tag + text.substring(end);
    bio.value = newText;
    bio.focus();
    bio.setSelectionRange(start + tag.length, start + tag.length);
    updatePreview();
}

function insertColor(color) {
    insertSimple('[' + color + ']');
}

function togglePassword() {
    let m = document.getElementById("method").value;
    let pwdField = document.getElementById("password");
    pwdField.style.display = (m === "uid") ? "block" : "none";
}

let lastValidBio = "";
function updatePreview() {
    let bio = document.getElementById("bio");
    if (bio.value.length > 250) {
        bio.value = lastValidBio;
        return;
    }
    lastValidBio = bio.value;
    document.getElementById("charCount").innerText = bio.value.length + " / 250";
    let raw = bio.value;
    let text = raw.replace(/[&<>]/g, function(m) {
        if (m === '&') return '&amp;';
        if (m === '<') return '&lt;';
        if (m === '>') return '&gt;';
        return m;
    });
    let result = '';
    let i = 0;
    let currentColor = null;
    let currentBold = false, currentItalic = false, currentCurve = false, currentUnderline = false, currentStrike = false;
    
    function applyCurrent() {
        let style = '';
        if (currentColor) style += `color:#${currentColor};`;
        if (currentBold) style += `font-weight:bold;`;
        if (currentItalic) style += `font-style:italic;`;
        if (currentCurve) style += `font-style:italic;`;
        if (currentUnderline) style += `text-decoration:underline;`;
        if (currentStrike) style += `text-decoration:line-through;`;
        if (style) return `<span style="${style}">`;
        return '';
    }
    
    let buffer = '';
    while (i < text.length) {
        if (text[i] === '[') {
            if (buffer) {
                let open = applyCurrent();
                result += open + buffer + (open ? '</span>' : '');
                buffer = '';
            }
            let endIdx = text.indexOf(']', i);
            if (endIdx === -1) {
                buffer += text[i];
                i++;
                continue;
            }
            let tag = text.substring(i+1, endIdx);
            i = endIdx + 1;
            if (/^[0-9A-Fa-f]{6}$/.test(tag)) {
                currentColor = tag;
            } else if (tag === 'b') {
                currentBold = !currentBold;
            } else if (tag === 'i') {
                currentItalic = !currentItalic;
            } else if (tag === 'c') {
                currentCurve = !currentCurve;
            } else if (tag === 'u') {
                currentUnderline = !currentUnderline;
            } else if (tag === 's') {
                currentStrike = !currentStrike;
            } else {
                buffer += '[' + tag + ']';
            }
        } else {
            buffer += text[i];
            i++;
        }
    }
    if (buffer) {
        let open = applyCurrent();
        result += open + buffer + (open ? '</span>' : '');
    }
    document.getElementById("preview").innerHTML = result || "Live Preview Area";
}

// ========== COLOR RIBBON ==========
const colors = ["#FF0000","#DC143C","#B22222","#8B0000","#FA8072","#FF7F50","#FF8C00","#FFA500","#FFD700","#FFFF00","#F0E68C","#98FB98","#00FF00","#32CD32","#00FF7F","#008000","#2E8B57","#556B2F","#808000","#40E0D0","#00FFFF","#00BFFF","#1E90FF","#4682B4","#0000FF","#0000CD","#00008B","#191970","#8A2BE2","#9370DB","#800080","#4B0082","#FF00FF","#EE82EE","#DA70D6","#FF1493","#FF69B4","#FFC0CB","#D2B48C","#D2691E","#A0522D","#8B4513","#FFFFFF","#C0C0C0","#A9A9A9","#808080","#696969","#2F4F4F","#000000"];
const ribbon = document.getElementById("colorRibbon");
colors.forEach(col => {
    let dot = document.createElement("div");
    dot.className = "c-dot";
    dot.style.backgroundColor = col;
    dot.onclick = () => insertColor(col.substring(1));
    ribbon.appendChild(dot);
});

document.getElementById("bio").addEventListener("input", updatePreview);
updatePreview();

// ========== SMART CAPTCHA ==========
let captchaVerified = false;
let isDragging = false;
let startX = 0;
let thumbLeft = 4;

const sliderContainer = document.getElementById('sliderContainer');
const sliderThumb = document.getElementById('sliderThumb');
const sliderFill = document.getElementById('sliderFill');
const progressText = document.getElementById('progressText');
const captchaStatus = document.getElementById('captchaStatus');
const captchaOverlay = document.getElementById('captchaOverlay');
const submitBtn = document.getElementById('submitBtn');

function getMaxLeft() {
    return sliderContainer.offsetWidth - sliderThumb.offsetWidth - 8;
}

function updateSlider(x) {
    const maxLeft = getMaxLeft();
    let left = Math.max(0, Math.min(x, maxLeft));
    const percent = (left / maxLeft) * 100;
    
    sliderThumb.style.left = (left + 4) + 'px';
    sliderFill.style.width = percent + '%';
    progressText.textContent = Math.round(percent) + '%';
    
    return left;
}

function handleStart(clientX) {
    const rect = sliderContainer.getBoundingClientRect();
    isDragging = true;
    startX = clientX - rect.left - sliderThumb.offsetWidth / 2;
    const currentLeft = parseFloat(sliderThumb.style.left) || 4;
    thumbLeft = currentLeft - 4;
    
    sliderThumb.style.transition = 'none';
    sliderFill.style.transition = 'none';
    captchaStatus.textContent = '🔓 Keep sliding...';
}

function handleMove(clientX) {
    if (!isDragging) return;
    
    const rect = sliderContainer.getBoundingClientRect();
    const maxLeft = getMaxLeft();
    let newLeft = clientX - rect.left - sliderThumb.offsetWidth / 2;
    newLeft = Math.max(0, Math.min(newLeft, maxLeft));
    
    updateSlider(newLeft);
    
    if (newLeft >= maxLeft - 2) {
        isDragging = false;
        captchaVerified = true;
        captchaStatus.textContent = '✅ Verified Successfully!';
        captchaStatus.className = 'captcha-status verified';
        progressText.textContent = 'Verified';
        sliderThumb.style.background = '#00ffc3';
        sliderThumb.innerHTML = '<i class="fas fa-check"></i>';
        
        submitBtn.disabled = false;
        submitBtn.textContent = '🚀 UPDATE BIO';
        
        setTimeout(() => {
            captchaOverlay.classList.add('hidden');
        }, 500);
    }
}

function handleEnd() {
    if (isDragging) {
        isDragging = false;
        const maxLeft = getMaxLeft();
        const currentLeft = parseFloat(sliderThumb.style.left) || 4;
        
        if (currentLeft - 4 < maxLeft - 15) {
            sliderThumb.style.transition = 'left 0.3s ease';
            sliderFill.style.transition = 'width 0.3s ease';
            sliderThumb.style.left = '4px';
            sliderFill.style.width = '0%';
            progressText.textContent = 'Slide to unlock';
            captchaStatus.textContent = '👉 Drag to the end to verify';
        }
    }
}

sliderContainer.addEventListener('mousedown', (e) => { e.preventDefault(); handleStart(e.clientX); });
document.addEventListener('mousemove', (e) => { if (isDragging) handleMove(e.clientX); });
document.addEventListener('mouseup', handleEnd);

sliderContainer.addEventListener('touchstart', (e) => { e.preventDefault(); handleStart(e.touches[0].clientX); }, { passive: false });
document.addEventListener('touchmove', (e) => { if (isDragging) handleMove(e.touches[0].clientX); }, { passive: false });
document.addEventListener('touchend', handleEnd);

function resetCaptcha() {
    captchaVerified = false;
    isDragging = false;
    sliderThumb.style.transition = 'left 0.3s ease';
    sliderFill.style.transition = 'width 0.3s ease';
    sliderThumb.style.left = '4px';
    sliderFill.style.width = '0%';
    progressText.textContent = 'Slide to unlock';
    captchaStatus.textContent = '🔄 Verification reset';
    captchaStatus.className = 'captcha-status';
    sliderThumb.style.background = '#fff';
    sliderThumb.innerHTML = '<i class="fas fa-chevron-right"></i>';
    captchaOverlay.classList.remove('hidden');
    submitBtn.disabled = true;
    submitBtn.textContent = '🔒 Verify First';
}

// ========== MAIN SUBMIT HANDLER ==========
async function handleSubmit() {
    if (!captchaVerified) { resetCaptcha(); return; }
    await updateBio();
}

async function updateBio() {
    let method = document.getElementById("method").value;
    let token = document.getElementById("token").value.trim();
    let bio = document.getElementById("bio").value;
    let password = document.getElementById("password").value.trim();
    let server = document.getElementById("serverSelect").value;
    let btn = document.getElementById("submitBtn");
    
    if (!token) { alert("Token required!"); return; }
    if (!bio) { alert("Bio is required!"); return; }
    
    let body = { token, bio, server, method };
    if (method === "uid") {
        if (!password) { alert("Password required!"); return; }
        body.password = password;
    }
    
    let original = btn.innerText;
    btn.innerText = "⏳ Processing...";
    btn.disabled = true;
    
    try {
        let res = await fetch("/api/update", {
            method: "POST",
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify(body)
        });
        let data = await res.json();
        
        if (data.status === "success") {
            showResult('success', '✅ SUCCESS!', `
                <div style="text-align:center; padding:5px;">
                    <div><strong>🆔 UID:</strong> ${data.uid || 'N/A'}</div>
                    <div><strong>👤 Nickname:</strong> ${data.name || 'N/A'}</div>
                    <div style="margin-top:10px; color:#00ffc3;">${data.message || 'Updated!'}</div>
                </div>
            `);
            document.getElementById("token").value = "";
            document.getElementById("password").value = "";
            document.getElementById("bio").value = "";
            updatePreview();
        } else {
            showResult('error', '❌ FAILED', data.message || 'Unknown error');
        }
    } catch(e) {
        showResult('error', '⚠️ ERROR', e.message);
    } finally {
        btn.innerText = original;
        btn.disabled = false;
    }
}

window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});
</script>
</body>
</html>
"""

API_BASE_URL = "https://drogon-bio-api.vercel.app/bio"

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/update', methods=['POST'])
def update_bio():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "Missing JSON body"}), 400

        method = data.get('method', 'jwt')
        bio = data.get('bio', '').strip()
        server = data.get('server', 'IND')
        token = data.get('token', '').strip()
        password = data.get('password', '').strip()

        if not bio:
            return jsonify({"status": "error", "message": "Bio is required"}), 400
        if not token:
            return jsonify({"status": "error", "message": "Token/UID is required"}), 400

        params = {"bio": bio, "region": server}

        if method == 'uid':
            if not password:
                return jsonify({"status": "error", "message": "Password required"}), 400
            params['uid'] = token
            params['pass'] = password
        elif method == 'jwt':
            params['jwt'] = token
        elif method == 'eat':
            params['eat'] = token
        elif method == 'access':
            params['access'] = token

        response = requests.get(API_BASE_URL, params=params, timeout=30)
        response.raise_for_status()
        api_data = response.json()

        result = {
            "status": "success" if api_data.get('success') else "error",
            "message": api_data.get('status', 'Bio updated'),
            "uid": api_data.get('uid'),
            "name": api_data.get('name'),
        }

        if not api_data.get('success', False):
            result["status"] = "error"
            result["message"] = api_data.get('status', 'API failure')

        return jsonify(result)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
