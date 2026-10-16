(function () {
  var body = document.body;
  var rootClass = document.documentElement.className + " " + body.className;
  if (/sqs-edit|squarespace-editable|sqs-editing/.test(rootClass)) {
    body.classList.add("pom-editing");
  }

  if (document.querySelector(".pom-page-plain, .pom-page-checkout") || (!document.querySelector(".pom-page, .pom-hero") && !document.querySelector(".pom-page-product"))) {
    body.classList.add("pom-has-plain");
  }
  if (document.querySelector(".pom-page-product, .pom-page-checkout")) {
    body.classList.add("pom-has-plain");
  }

  var path = (window.location.pathname || "").replace(/\/+$/, "") || "/";
  if (
    path === "/cart" ||
    /cart/i.test(body.className) ||
    document.querySelector(".cart-container, .sqs-cart-page, #cart, .empty-message, .cart-empty")
  ) {
    body.classList.add("pom-has-cart");
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
    var fallback = nav.querySelector("[data-nav-fallback]");
    if (fallback) {
      fallback.hidden = false;
    }
  });

  Array.prototype.forEach.call(document.querySelectorAll("[data-pom-region]"), function (region) {
    var cms = region.querySelector(".pom-cms");
    if (cms && cms.querySelector(".sqs-block:not(.sqs-block-spacer), .form-wrapper")) {
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

  Array.prototype.forEach.call(document.querySelectorAll("[data-gallery]"), function (gallery) {
    var slides = gallery.querySelectorAll("[data-slide]");
    var dotsWrap = gallery.querySelector("[data-gallery-dots]");
    var dots = dotsWrap ? dotsWrap.querySelectorAll("[data-dot]") : [];
    if (!slides.length) {
      return;
    }
    var index = 0;
    function show(next) {
      index = (next + slides.length) % slides.length;
      Array.prototype.forEach.call(slides, function (slide, i) {
        slide.classList.toggle("is-active", i === index);
      });
      Array.prototype.forEach.call(dots, function (dot, i) {
        dot.classList.toggle("is-active", i === index);
      });
    }
    var prev = gallery.querySelector("[data-gallery-prev]");
    var next = gallery.querySelector("[data-gallery-next]");
    if (prev) {
      prev.addEventListener("click", function () {
        show(index - 1);
      });
    }
    if (next) {
      next.addEventListener("click", function () {
        show(index + 1);
      });
    }
    Array.prototype.forEach.call(dots, function (dot) {
      dot.addEventListener("click", function () {
        show(parseInt(dot.getAttribute("data-dot"), 10) || 0);
      });
    });
  });

  function money(n) {
    return "$" + Number(n).toFixed(2);
  }

  function pad2(n) {
    return n < 10 ? "0" + n : String(n);
  }

  function syncOrderSummary(page) {
    var productView = page.querySelector("[data-product-view]");
    var orderView = page.querySelector("[data-order-view]");
    if (!orderView) {
      return;
    }
    var qtyInput = productView ? productView.querySelector("[data-qty] input") : null;
    var qty = Math.max(1, parseInt(qtyInput && qtyInput.value, 10) || 1);
    var unit = parseFloat(orderView.getAttribute("data-unit-price") || "0") || 0;
    var ship = parseFloat(orderView.getAttribute("data-shipping") || "4") || 0;
    var sub = unit * qty;
    var total = sub + ship;
    var qtyEl = orderView.querySelector("[data-order-qty]");
    var subEl = orderView.querySelector("[data-order-subtotal]");
    var shipEl = orderView.querySelector("[data-order-shipping]");
    var totalEl = orderView.querySelector("[data-order-total]");
    var payEl = orderView.querySelector("[data-order-pay]");
    if (qtyEl) {
      qtyEl.textContent = "Quantity : " + pad2(qty);
    }
    if (subEl) {
      subEl.textContent = money(sub);
    }
    if (shipEl) {
      shipEl.textContent = money(ship);
    }
    if (totalEl) {
      totalEl.textContent = money(total);
    }
    if (payEl) {
      payEl.textContent = "Pay " + money(total);
    }
  }

  Array.prototype.forEach.call(document.querySelectorAll("[data-product-page]"), function (page) {
    var productView = page.querySelector("[data-product-view]");
    var orderView = page.querySelector("[data-order-view]");
    if (!productView || !orderView) {
      return;
    }
    function showOrder(on) {
      page.classList.toggle("is-ordering", on);
      body.classList.toggle("pom-is-ordering", on);
      if (on) {
        syncOrderSummary(page);
        orderView.hidden = false;
        productView.hidden = true;
        window.scrollTo(0, 0);
        if (window.history && window.history.replaceState) {
          window.history.replaceState(null, "", "#order");
        }
      } else {
        orderView.hidden = true;
        productView.hidden = false;
        if (window.history && window.history.replaceState) {
          window.history.replaceState(null, "", window.location.pathname + window.location.search);
        }
      }
    }
    Array.prototype.forEach.call(page.querySelectorAll("[data-buy-now]"), function (btn) {
      btn.addEventListener("click", function (event) {
        event.preventDefault();
        showOrder(true);
      });
    });
    Array.prototype.forEach.call(page.querySelectorAll("[data-back-product]"), function (btn) {
      btn.addEventListener("click", function (event) {
        event.preventDefault();
        showOrder(false);
      });
    });
    if (window.location.hash === "#order") {
      showOrder(true);
    }
  });

  Array.prototype.forEach.call(document.querySelectorAll("[data-qty]"), function (wrap) {
    var input = wrap.querySelector("input");
    var minus = wrap.querySelector("[data-qty-minus]");
    var plus = wrap.querySelector("[data-qty-plus]");
    if (!input) {
      return;
    }
    function setQty(next) {
      var value = Math.max(1, parseInt(next, 10) || 1);
      input.value = String(value);
      var page = wrap.closest("[data-product-page]");
      if (page) {
        syncOrderSummary(page);
      }
    }
    if (minus) {
      minus.addEventListener("click", function () {
        setQty(parseInt(input.value, 10) - 1);
      });
    }
    if (plus) {
      plus.addEventListener("click", function () {
        setQty(parseInt(input.value, 10) + 1);
      });
    }
  });

  Array.prototype.forEach.call(document.querySelectorAll("[data-checkout-form]"), function (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var error = form.querySelector("[data-checkout-error]");
      if (!form.checkValidity()) {
        if (error) {
          error.hidden = false;
        }
        if (form.reportValidity) {
          form.reportValidity();
        }
        return;
      }
      if (error) {
        error.hidden = true;
      }
      var scope = form.closest("[data-order-view]") || form.closest(".pom-page-checkout") || document;
      var modal = scope.querySelector("[data-order-modal]");
      if (modal) {
        modal.hidden = false;
        body.classList.add("pom-modal-open");
      }
    });
  });

  Array.prototype.forEach.call(document.querySelectorAll("[data-order-modal]"), function (modal) {
    modal.addEventListener("click", function (event) {
      if (event.target === modal || event.target.closest("[data-modal-close]")) {
        modal.hidden = true;
        body.classList.remove("pom-modal-open");
      }
    });
  });
})();
