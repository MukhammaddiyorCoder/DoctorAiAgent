/*!
 * Doctor AI Agent - Embeddable Chat Widget
 *
 * Usage:
 *   <script
 *     src="https://yourdomain.com/widget/chat-widget.js"
 *     data-clinic="dr-karimov"
 *     data-color="#3B82F6"
 *     data-position="bottom-right"
 *     data-api="https://yourdomain.com/api/v1"
 *     data-ws="wss://yourdomain.com">
 *   </script>
 */
(function () {
  "use strict";

  var currentScript =
    document.currentScript ||
    (function () {
      var scripts = document.getElementsByTagName("script");
      return scripts[scripts.length - 1];
    })();

  var CLINIC = currentScript.getAttribute("data-clinic");
  if (!CLINIC) {
    console.error("[doctor-ai-widget] data-clinic attribute is required");
    return;
  }
  var COLOR = currentScript.getAttribute("data-color") || "#3B82F6";
  var POSITION = currentScript.getAttribute("data-position") || "bottom-right";
  var API_URL =
    currentScript.getAttribute("data-api") ||
    location.origin.replace(/:\d+$/, "") + ":8000/api/v1";
  var WS_URL =
    currentScript.getAttribute("data-ws") ||
    (location.protocol === "https:" ? "wss://" : "ws://") +
      location.hostname +
      ":8000";

  var STORAGE_KEY = "doctor-ai-widget:" + CLINIC;
  var sessionKey =
    localStorage.getItem(STORAGE_KEY) ||
    "s_" +
      Date.now().toString(36) +
      "_" +
      Math.random().toString(36).slice(2, 10);
  localStorage.setItem(STORAGE_KEY, sessionKey);

  // -------- Styles --------
  var style = document.createElement("style");
  style.textContent = [
    ".dai-btn{position:fixed;width:60px;height:60px;border-radius:50%;border:0;color:#fff;font-size:28px;cursor:pointer;box-shadow:0 6px 20px rgba(0,0,0,.2);z-index:2147483646;display:flex;align-items:center;justify-content:center;transition:transform .15s}",
    ".dai-btn:hover{transform:scale(1.05)}",
    ".dai-panel{position:fixed;width:360px;max-width:calc(100vw - 32px);height:520px;max-height:calc(100vh - 32px);background:#fff;border-radius:16px;box-shadow:0 12px 32px rgba(0,0,0,.25);display:flex;flex-direction:column;overflow:hidden;z-index:2147483647;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif}",
    ".dai-header{padding:14px 16px;color:#fff;display:flex;align-items:center;justify-content:space-between;font-weight:600}",
    ".dai-close{background:transparent;border:0;color:#fff;font-size:22px;cursor:pointer;line-height:1}",
    ".dai-messages{flex:1;padding:12px;overflow-y:auto;background:#f7f7f8;display:flex;flex-direction:column;gap:8px}",
    ".dai-msg{max-width:80%;padding:8px 12px;border-radius:12px;font-size:14px;line-height:1.4;white-space:pre-wrap;word-wrap:break-word}",
    ".dai-msg.user{align-self:flex-end;background:" + COLOR + ";color:#fff;border-bottom-right-radius:4px}",
    ".dai-msg.bot{align-self:flex-start;background:#fff;border:1px solid #e5e7eb;color:#111;border-bottom-left-radius:4px}",
    ".dai-msg.system{align-self:center;background:transparent;color:#6b7280;font-size:12px;border:0}",
    ".dai-input-row{display:flex;padding:10px;gap:8px;border-top:1px solid #e5e7eb;background:#fff}",
    ".dai-input{flex:1;padding:9px 12px;border:1px solid #d1d5db;border-radius:8px;font-size:14px;outline:none}",
    ".dai-input:focus{border-color:" + COLOR + "}",
    ".dai-send{padding:9px 14px;border:0;border-radius:8px;color:#fff;background:" + COLOR + ";cursor:pointer;font-weight:500}",
    ".dai-send:disabled{opacity:.6;cursor:not-allowed}",
  ].join("");
  document.head.appendChild(style);

  function positionCSS(el, side) {
    el.style[side === "bottom-right" ? "right" : "left"] = "20px";
    el.style.bottom = "20px";
    if (side === "bottom-left") el.style.left = "20px";
  }

  // -------- Toggle button --------
  var btn = document.createElement("button");
  btn.className = "dai-btn";
  btn.style.backgroundColor = COLOR;
  btn.innerHTML = "💬";
  btn.setAttribute("aria-label", "Chat");
  positionCSS(btn, POSITION);
  document.body.appendChild(btn);

  // -------- Panel --------
  var panel = document.createElement("div");
  panel.className = "dai-panel";
  panel.style.display = "none";
  positionCSS(panel, POSITION);
  panel.style.bottom = "96px";
  panel.innerHTML =
    '<div class="dai-header" style="background:' + COLOR + ';">' +
    '<span>Assistant</span>' +
    '<button class="dai-close" aria-label="Close">×</button>' +
    '</div>' +
    '<div class="dai-messages" id="dai-messages"></div>' +
    '<div class="dai-input-row">' +
    '<input class="dai-input" id="dai-input" placeholder="Xabar yozing..." />' +
    '<button class="dai-send" id="dai-send">Yuborish</button>' +
    '</div>';
  document.body.appendChild(panel);

  var messagesEl = panel.querySelector("#dai-messages");
  var inputEl = panel.querySelector("#dai-input");
  var sendBtn = panel.querySelector("#dai-send");
  var closeBtn = panel.querySelector(".dai-close");

  function addMessage(text, role) {
    var div = document.createElement("div");
    div.className = "dai-msg " + role;
    div.textContent = text;
    messagesEl.appendChild(div);
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  // -------- Transport: try WebSocket first, fall back to REST --------
  var socket = null;
  var useSocket = false;

  function initSocket() {
    try {
      socket = new WebSocket(WS_URL + "/ws/chat/" + CLINIC + "/");
      socket.onopen = function () {
        useSocket = true;
      };
      socket.onmessage = function (ev) {
        try {
          var data = JSON.parse(ev.data);
          if (data.type === "assistant") {
            addMessage(data.text, "bot");
            setLoading(false);
          } else if (data.type === "system") {
            addMessage(data.text, "system");
          }
        } catch (e) {
          // ignore
        }
      };
      socket.onerror = function () {
        useSocket = false;
      };
      socket.onclose = function () {
        useSocket = false;
      };
    } catch (e) {
      useSocket = false;
    }
  }

  function setLoading(loading) {
    sendBtn.disabled = loading;
    inputEl.disabled = loading;
    sendBtn.textContent = loading ? "..." : "Yuborish";
  }

  function sendViaRest(text) {
    setLoading(true);
    fetch(API_URL + "/ai/chat/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        clinic_slug: CLINIC,
        session_key: sessionKey,
        message: text,
      }),
    })
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        addMessage(data.reply || "...", "bot");
      })
      .catch(function () {
        addMessage("Xatolik yuz berdi. Keyinroq urinib ko'ring.", "bot");
      })
      .finally(function () {
        setLoading(false);
      });
  }

  function sendMessage() {
    var text = (inputEl.value || "").trim();
    if (!text) return;
    addMessage(text, "user");
    inputEl.value = "";

    if (useSocket && socket && socket.readyState === WebSocket.OPEN) {
      setLoading(true);
      socket.send(
        JSON.stringify({
          type: "message",
          text: text,
          session_key: sessionKey,
        }),
      );
    } else {
      sendViaRest(text);
    }
  }

  btn.addEventListener("click", function () {
    var hidden = panel.style.display === "none";
    panel.style.display = hidden ? "flex" : "none";
    if (hidden && !socket) initSocket();
  });
  closeBtn.addEventListener("click", function () {
    panel.style.display = "none";
  });
  sendBtn.addEventListener("click", sendMessage);
  inputEl.addEventListener("keydown", function (e) {
    if (e.key === "Enter") sendMessage();
  });
})();
