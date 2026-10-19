/*
 * Markdown reader: reader.html?p=<Folder>/<slug>
 * - The .md is loaded through a generated <Folder>/<slug>.md.js (tools/build-md.js),
 *   because fetch() of local files is blocked on file://.
 * - Only paths listed in registry.js are accepted, so ?p= cannot load arbitrary scripts.
 * - marked parses, DOMPurify sanitizes, Mermaid (vendored, loaded only when needed)
 *   renders ```mermaid blocks. No network access.
 */
(function () {
  "use strict";

  var R = window.REGISTRY || { topics: [], articles: [] };
  var root = document.getElementById("md-root");

  function fail(msg) {
    root.textContent = "";
    var p = document.createElement("p");
    p.className = "empty";
    p.textContent = msg;
    root.appendChild(p);
  }

  function enc(folder) { return encodeURIComponent(folder); }

  // Resolve ?p= against the registry.
  var p = new URLSearchParams(location.search).get("p") || "";
  var cut = p.lastIndexOf("/");
  var folder = p.slice(0, cut), slug = p.slice(cut + 1);
  var topic = R.topics.filter(function (t) { return t.folder === folder; })[0];
  var article = topic && R.articles.filter(function (a) {
    return a.topic === topic.id && a.slug === slug;
  })[0];
  if (!article) { fail("Không tìm thấy bài viết trong registry.js: " + p); return; }

  var base = enc(folder) + "/";
  document.title = article.title + " (Markdown) | CS Fundamentals";
  document.getElementById("crumb-topic").textContent = topic.title;
  document.getElementById("crumb-topic").href = base + "index.html";
  document.getElementById("crumb-title").textContent = article.title;
  document.getElementById("link-topic").href = base + "index.html";

  var key = folder + "/" + slug;
  var s = document.createElement("script");
  s.src = base + enc(slug) + ".md.js";
  s.onload = function () {
    var md = window.MD_SOURCES && window.MD_SOURCES[key];
    if (typeof md !== "string") { fail("File .md.js không chứa nội dung. Chạy: node tools/build-md.js"); return; }
    render(md);
  };
  s.onerror = function () { fail("Chưa có " + slug + ".md.js. Chạy: node tools/build-md.js"); };
  document.body.appendChild(s);

  // Relative links in the .md are relative to the topic folder; the reader lives at root.
  function fixUrl(u, isLink) {
    if (!u || /^([a-z][a-z0-9+.-]*:|#|\/)/i.test(u)) return u;
    var m = isLink && u.match(/^([a-z0-9-]+)\.(md|html)(#.*)?$/i);
    if (m && m[2].toLowerCase() === "md") {
      return "reader.html?p=" + encodeURIComponent(folder + "/" + m[1]) + (m[3] || "");
    }
    return base + u;
  }

  function render(md) {
    var html = window.marked.parse(md, { gfm: true, headerIds: true, mangle: false });
    var clean = window.DOMPurify.sanitize(html, { USE_PROFILES: { html: true } });
    root.innerHTML = clean;

    root.querySelectorAll("a[href]").forEach(function (a) {
      a.setAttribute("href", fixUrl(a.getAttribute("href"), true));
    });
    root.querySelectorAll("img[src]").forEach(function (img) {
      img.setAttribute("src", fixUrl(img.getAttribute("src"), false));
      img.setAttribute("loading", "lazy");
    });
    // Wide tables scroll horizontally on mobile, same as HTML articles.
    root.querySelectorAll("table").forEach(function (t) {
      var w = document.createElement("div");
      w.className = "table-wrap";
      t.parentNode.insertBefore(w, t);
      w.appendChild(t);
    });
    if (location.hash) {
      var target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
      if (target) target.scrollIntoView();
    }

    var blocks = root.querySelectorAll("pre > code.language-mermaid");
    if (blocks.length) loadMermaid(blocks);
  }

  function loadMermaid(blocks) {
    var nodes = [];
    blocks.forEach(function (code) {
      var fig = document.createElement("figure");
      fig.className = "diagram-fig";
      var frame = document.createElement("div");
      frame.className = "diagram-frame mermaid";
      frame.textContent = code.textContent;
      fig.appendChild(frame);
      code.parentNode.replaceWith(fig);
      nodes.push(frame);
    });
    var s = document.createElement("script");
    s.src = "assets/vendor/mermaid.min.js";
    s.onload = function () {
      // Diagram frame is always white, so the default (light) Mermaid theme fits every site theme.
      window.mermaid.initialize({ startOnLoad: false, securityLevel: "strict", theme: "default" });
      window.mermaid.run({ nodes: nodes }).catch(function (e) {
        console.error("Mermaid render error", e);
      });
    };
    document.body.appendChild(s);
  }
})();
