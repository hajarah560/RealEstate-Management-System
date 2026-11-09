// Opens add / edit / delete forms in the page's <dialog> and submits them without leaving the page.
(function () {
  var dialog = document.getElementById("modal");
  if (!dialog) return;

  function show(html) {
    dialog.innerHTML = html;
    if (!dialog.open) dialog.showModal();
  }

  document.addEventListener("click", function (e) {
    var opener = e.target.closest("[data-modal]");
    if (opener) {
      fetch(opener.getAttribute("data-modal")).then(function (r) { return r.text(); }).then(show);
    } else if (e.target.closest("[data-close]") || e.target === dialog) {
      dialog.close();
    }
  });

  dialog.addEventListener("submit", function (e) {
    e.preventDefault();
    var form = e.target;
    fetch(form.action, { method: "POST", body: new FormData(form) }).then(function (r) {
      if (r.status === 204) location.reload();
      else return r.text().then(show);
    });
  });
})();
