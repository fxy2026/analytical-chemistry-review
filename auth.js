// === Auth Guard + User Bar (Analytical Chemistry) ===
(function() {
  var user = localStorage.getItem('achem_user');
  var userData = null;
  try { userData = user ? JSON.parse(user) : null; } catch(e) { userData = null; }
  if (!userData || !userData.username) { window.location.href = 'login.html'; return; }

  function injectUserBar() {
    var bar = document.createElement('div');
    bar.id = 'user-bar';
    bar.innerHTML = '<span class="user-info">&#x1F9EA; ' + escapeHtml(userData.username) + '</span>'
      + '<a href="index.html" class="user-btn">&#x1F4DA; 目录</a>'
      + '<button class="user-btn" id="logoutBtn">退出</button>';
    document.body.insertBefore(bar, document.body.firstChild);

    var style = document.createElement('style');
    style.textContent = '#user-bar{position:fixed;top:0;left:0;right:0;z-index:9998;background:linear-gradient(135deg,#1a5276,#2980b9);color:#fff;padding:6px 16px;font-size:.82em;display:flex;align-items:center;gap:12px;box-shadow:0 2px 8px rgba(0,0,0,.15);}'
      + '#user-bar .user-info{font-weight:600;margin-right:auto;}'
      + '#user-bar .user-btn{color:#fff;background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.3);padding:3px 10px;border-radius:4px;cursor:pointer;text-decoration:none;font-size:.9em;font-family:inherit;transition:background .15s;}'
      + '#user-bar .user-btn:hover{background:rgba(255,255,255,.25);}'
      + 'body{padding-top:38px !important;}'
      + '.nav-bar{top:38px !important;}'
      + '#floating-toc{top:98px !important;}'
      + '#reading-progress-top{top:38px !important;}';
    document.head.appendChild(style);

    document.getElementById('logoutBtn').addEventListener('click', function() {
      localStorage.removeItem('achem_user');
      window.location.href = 'login.html';
    });
  }

  function escapeHtml(str) {
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectUserBar);
  } else { injectUserBar(); }

  window.achemUser = userData.username;
})();
