/*
 * Renders navigation from window.REGISTRY (see /registry.js).
 * Works on file:// because it uses no fetch(). DOM is built with textContent
 * only, so registry strings are never interpreted as HTML.
 *
 * <body data-page="home">                     -> topic cards
 * <body data-page="topic" data-topic="os">    -> article list of one topic
 */
(function () {
  "use strict";

  var R = window.REGISTRY || { topics: [], articles: [] };
  var body = document.body;
  var page = body.getAttribute("data-page");
  var base = body.getAttribute("data-base") || ""; // "" at root, "../" in topic folders

  function el(tag, attrs, text) {
    var node = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) { node.setAttribute(k, attrs[k]); });
    if (text != null) node.textContent = text;
    return node;
  }

  function topicById(id) {
    return R.topics.filter(function (t) { return t.id === id; })[0];
  }

  // Folder names contain spaces and "-", so encode each path segment.
  function topicHref(t) { return base + encodeURIComponent(t.folder) + "/index.html"; }
  // Markdown is rendered by reader.html (marked + vendored Mermaid), not shown raw.
  function readerHref(t, a) {
    return base + "reader.html?p=" + encodeURIComponent(t.folder + "/" + a.slug);
  }

  function articlesOf(topicId) {
    return R.articles.filter(function (a) { return a.topic === topicId; });
  }

  function topicCard(t) {
    var n = articlesOf(t.id).length;
    var card = el("a", { "class": "card", href: topicHref(t) });
    card.appendChild(el("h2", {}, t.title));
    card.appendChild(el("p", {}, t.desc));
    card.appendChild(cardFoot(n + " bài viết", "Xem chủ đề"));
    return card;
  }

  // Footer pinned to the card bottom: left = meta text, right = call to action.
  function cardFoot(left, cta) {
    var foot = el("div", { "class": "card-foot" });
    foot.appendChild(el("span", {}, left));
    foot.appendChild(el("span", { "class": "card-cta", "aria-hidden": "true" }, cta + " \u2192"));
    return foot;
  }

  function articleCard(a, showTopic) {
    var t = topicById(a.topic);
    if (!t) return null;
    // The whole card is one link, so there is a single tab stop per article.
    var card = el("a", { "class": "card", href: readerHref(t, a) });
    if (showTopic) card.appendChild(el("span", { "class": "badge" }, t.title));
    card.appendChild(el("h3", {}, a.title));
    if (a.summary) card.appendChild(el("p", {}, a.summary));
    card.appendChild(cardFoot(a.date || "", "Đọc"));
    return card;
  }

  function fill(container, nodes, emptyMsg) {
    container.textContent = "";
    var real = nodes.filter(Boolean);
    if (!real.length) {
      container.appendChild(el("div", { "class": "empty" }, emptyMsg));
      return;
    }
    real.forEach(function (n) { container.appendChild(n); });
  }

  function renderHome() {
    var topicsBox = document.getElementById("topics");
    var search = document.getElementById("search");

    // A topic matches if its own text or any of its articles' title/summary matches.
    function draw() {
      var q = (search.value || "").trim().toLowerCase();
      var topics = R.topics.filter(function (t) {
        if (!q) return true;
        if ((t.title + " " + t.desc).toLowerCase().indexOf(q) !== -1) return true;
        return articlesOf(t.id).some(function (a) {
          return (a.title + " " + (a.summary || "")).toLowerCase().indexOf(q) !== -1;
        });
      });
      fill(topicsBox, topics.map(topicCard), "Không có chủ đề khớp từ khóa.");
    }
    search.addEventListener("input", draw);
    draw();
  }

  function renderTopic() {
    var t = topicById(body.getAttribute("data-topic"));
    var box = document.getElementById("articles");
    if (!t) { fill(box, [], "Không tìm thấy chủ đề trong registry.js."); return; }
    document.title = t.title + " | CS Fundamentals";
    document.getElementById("topic-title").textContent = t.title;
    document.getElementById("topic-desc").textContent = t.desc;
    fill(box, articlesOf(t.id).map(function (a) { return articleCard(a, false); }),
      "Chưa có bài viết nào trong chủ đề này.");
  }

  if (page === "home") renderHome();
  else if (page === "topic") renderTopic();
})();
