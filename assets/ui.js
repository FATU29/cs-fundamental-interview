/*
 * Theme controller. Loaded synchronously in <head> so data-theme is set
 * before first paint (no flash). Choices: auto | light | dark | sepia.
 * "auto" follows the OS (prefers-color-scheme) and reacts to OS changes.
 * Storage access is wrapped in try/catch: file:// and private mode can throw.
 */
(function () {
  "use strict";

  var KEY = "csf-theme";
  var CHOICES = ["auto", "light", "dark", "sepia"];
  var LABELS = { auto: "Tự động", light: "Sáng", dark: "Tối", sepia: "Sepia" };
  var root = document.documentElement;
  var media = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;

  function read() {
    try {
      var v = localStorage.getItem(KEY);
      return CHOICES.indexOf(v) !== -1 ? v : "auto";
    } catch (e) { return "auto"; }
  }

  function write(v) {
    try { localStorage.setItem(KEY, v); } catch (e) { /* ignore: theme still applies for this page */ }
  }

  function apply(choice) {
    var effective = choice === "auto" ? (media && media.matches ? "dark" : "light") : choice;
    root.setAttribute("data-theme", effective);
    root.setAttribute("data-theme-choice", choice);
  }

  apply(read());

  if (media) {
    var onOsChange = function () { if (read() === "auto") apply("auto"); };
    if (media.addEventListener) media.addEventListener("change", onOsChange);
    else if (media.addListener) media.addListener(onOsChange); // old Safari
  }

  document.addEventListener("DOMContentLoaded", function () {
    var select = document.getElementById("theme-select");
    if (!select) return;
    CHOICES.forEach(function (c) {
      var opt = document.createElement("option");
      opt.value = c;
      opt.textContent = LABELS[c];
      select.appendChild(opt);
    });
    select.value = read();
    select.addEventListener("change", function () {
      write(select.value);
      apply(select.value);
    });
  });
})();
