(function () {
  'use strict';

  /* Склад: клік по інгредієнту підсвічує його шар на схемі */
  var stack = document.getElementById('stack');
  var buttons = document.querySelectorAll('.ing-btn');

  function pick(btn) {
    var key = btn.getAttribute('data-layer');
    buttons.forEach(function (b) {
      b.setAttribute('aria-pressed', b === btn ? 'true' : 'false');
    });
    stack.querySelectorAll('.layer').forEach(function (layer) {
      layer.classList.toggle('on', layer.getAttribute('data-layer') === key);
    });
  }

  if (stack && buttons.length) {
    buttons.forEach(function (btn) {
      btn.addEventListener('click', function () { pick(btn); });
      btn.addEventListener('mouseenter', function () { pick(btn); });
    });
    pick(document.querySelector('.ing-btn[aria-pressed="true"]') || buttons[0]);
    stack.classList.add('has');
  }

  /* Форма: показуємо відповідь на сторінці (дані нікуди не надсилаються) */
  var form = document.querySelector('.form');
  var status = document.getElementById('form-status');

  if (form && status) {
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }
      status.textContent = 'Дякуємо! Питання прийнято. Це демо-сайт, тому дані нікуди не надсилаються.';
      status.hidden = false;
      form.reset();
    });
  }
})();
