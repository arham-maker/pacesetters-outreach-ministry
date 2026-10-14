(function () {
  var body = document.body;
  var rootClass = document.documentElement.className + " " + body.className;
  if (/sqs-edit|squarespace-editable|sqs-editing/.test(rootClass)) {
    body.classList.add("pom-editing");
  }

  if (document.querySelector(".pom-page-plain, .pom-page-contact")) {
    body.classList.add("pom-has-plain");
  }

  var toggle = document.querySelector(".pom-menu-toggle");
  var drawer = document.getElementById("pom-drawer");
  if (toggle && drawer) {
    toggle.addEventListener("click", function () {
      var open = drawer.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      body.classList.toggle("pom-nav-open", open);
    });
    drawer.addEventListener("click", function (event) {
      if (event.target.closest("a")) {
        drawer.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
        body.classList.remove("pom-nav-open");
      }
    });
  }

  Array.prototype.forEach.call(document.querySelectorAll("[data-pom-nav]"), function (nav) {
    var cms = nav.querySelector("[data-nav-cms]");
    var fallback = nav.querySelector("[data-nav-fallback]");
    if (cms && fallback && cms.querySelector("a[href]")) {
      fallback.hidden = true;
      nav.classList.add("is-cms-nav");
    }
  });

  Array.prototype.forEach.call(document.querySelectorAll("[data-pom-region]"), function (region) {
    var cms = region.querySelector(".pom-cms");
    if (cms && cms.querySelector(".sqs-block, .sqs-row, .form-wrapper")) {
      region.classList.add("has-cms");
    }
  });

  Array.prototype.forEach.call(document.querySelectorAll("[data-accordion]"), function (list) {
    var items = list.querySelectorAll(".pom-faq-item");
    Array.prototype.forEach.call(items, function (item) {
      var button = item.querySelector(".pom-faq-q");
      var panel = item.querySelector(".pom-faq-a");
      if (!button || !panel) {
        return;
      }
      button.addEventListener("click", function () {
        var willOpen = !item.classList.contains("is-open");
        Array.prototype.forEach.call(items, function (other) {
          other.classList.remove("is-open");
          var otherBtn = other.querySelector(".pom-faq-q");
          if (otherBtn) {
            otherBtn.setAttribute("aria-expanded", "false");
          }
        });
        if (willOpen) {
          item.classList.add("is-open");
          button.setAttribute("aria-expanded", "true");
        }
      });
    });
  });

  Array.prototype.forEach.call(document.querySelectorAll("[data-quotes]"), function (wrap) {
    var quotes = wrap.querySelectorAll(".pom-quote");
    if (!quotes.length) {
      return;
    }
    var index = 0;
    function show(next) {
      index = (next + quotes.length) % quotes.length;
      Array.prototype.forEach.call(quotes, function (quote, i) {
        quote.classList.toggle("is-active", i === index);
      });
    }
    var scope = wrap.parentNode;
    Array.prototype.forEach.call(scope.querySelectorAll("[data-quote]"), function (button) {
      button.addEventListener("click", function () {
        var dir = button.getAttribute("data-quote") === "prev" ? -1 : 1;
        show(index + dir);
      });
    });
  });

  Array.prototype.forEach.call(document.querySelectorAll("[data-filters]"), function (bar) {
    var grid = document.querySelector("[data-product-grid]");
    if (!grid) {
      return;
    }
    bar.addEventListener("click", function (event) {
      var button = event.target.closest("[data-filter]");
      if (!button) {
        return;
      }
      var filter = button.getAttribute("data-filter");
      Array.prototype.forEach.call(bar.querySelectorAll("[data-filter]"), function (tab) {
        tab.classList.toggle("is-active", tab === button);
      });
      Array.prototype.forEach.call(grid.querySelectorAll("[data-category]"), function (card) {
        var category = (card.getAttribute("data-category") || "").toLowerCase();
        var show = filter === "all" || category.indexOf(filter) !== -1;
        card.hidden = !show;
      });
    });
  });

  Array.prototype.forEach.call(document.querySelectorAll("[data-contact-form]"), function (form) {
    form.addEventListener("submit", function (event) {
      if (form.getAttribute("data-live") === "true") {
        return;
      }
      event.preventDefault();
      var note = form.querySelector(".pom-form-note");
      if (note) {
        note.hidden = false;
      }
      form.reset();
    });
  });
})();
