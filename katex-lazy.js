// Lazy KaTeX renderer - only renders math formulas when they scroll into view
// Replaces the default renderMathInElement(document.body) which blocks the main thread
(function(){
  var DELIMITERS = [
    {left:'$$', right:'$$', display:true},
    {left:'$', right:'$', display:false}
  ];

  // Wait for KaTeX + auto-render to be available
  function waitForKaTeX(cb) {
    if (window.renderMathInElement) { cb(); return; }
    var t = setInterval(function(){
      if (window.renderMathInElement) { clearInterval(t); cb(); }
    }, 50);
  }

  waitForKaTeX(function(){
    // Collect all text nodes containing $ delimiters, group by parent element
    var sections = document.querySelectorAll('.card, .fb, .ex, .sol, .tip, .warn, .note, .exam, h2, h3, p, li, td, th, div');
    var mathElements = [];
    var rendered = new WeakSet();

    // Find elements that contain math (have $ in their text)
    sections.forEach(function(el){
      if (el.textContent.indexOf('$') !== -1 && !el.closest('.nav-bar')) {
        mathElements.push(el);
      }
    });

    // Deduplicate: only keep outermost containers
    var filtered = [];
    mathElements.forEach(function(el){
      var dominated = false;
      for (var i = 0; i < mathElements.length; i++) {
        if (mathElements[i] !== el && mathElements[i].contains(el)) {
          dominated = true; break;
        }
      }
      if (!dominated) filtered.push(el);
    });
    mathElements = filtered;

    function renderEl(el) {
      if (rendered.has(el)) return;
      rendered.add(el);
      try {
        renderMathInElement(el, {
          delimiters: DELIMITERS,
          throwOnError: false
        });
      } catch(e) {}
    }

    // Render above-the-fold content immediately (first 8 elements)
    var immediate = mathElements.splice(0, 8);
    immediate.forEach(renderEl);

    // Use IntersectionObserver for the rest
    if (mathElements.length === 0) return;

    if ('IntersectionObserver' in window) {
      var observer = new IntersectionObserver(function(entries){
        entries.forEach(function(entry){
          if (entry.isIntersecting) {
            renderEl(entry.target);
            observer.unobserve(entry.target);
          }
        });
      }, { rootMargin: '300px 0px' }); // render 300px before visible

      mathElements.forEach(function(el){ observer.observe(el); });
    } else {
      // Fallback: render all in chunks via requestIdleCallback or setTimeout
      var idx = 0;
      function renderChunk() {
        var end = Math.min(idx + 5, mathElements.length);
        for (; idx < end; idx++) renderEl(mathElements[idx]);
        if (idx < mathElements.length) {
          (window.requestIdleCallback || setTimeout)(renderChunk, 16);
        }
      }
      renderChunk();
    }
  });
})();
