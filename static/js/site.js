// Opens add / edit / delete forms in the page's <dialog> and submits them without leaving the page.
//
// THE MODAL FLOW, step by step
//   1. Click:  you click a button that has data-modal="<url>" (Add, pencil, bin).
//   2. Fetch:  we ask the server for that URL; it replies with a small piece of HTML (a form).
//   3. Show:   we put that HTML inside the empty <dialog id="modal"> from base.html and open it.
//   4. Submit: when the form is submitted we stop the browser's normal full-page submit and
//              send the data ourselves with fetch().
//   5. Result: status 204 ("saved, nothing to show") -> reload the page so the table is fresh.
//              Anything else (usually the form again, with error messages) -> redraw the dialog.
//
// Plain English: the pop-up never navigates away, so the table behind it stays where it is
// and the user does not lose their place. Technical: progressive enhancement with fetch() +
// the native <dialog> element; no libraries. Django's CSRF token travels inside the form data.

// Wrapped in a function so our variables do not leak into the global scope.
(function () {
  // The one shared dialog. If a page has none (should not happen), do nothing instead of crashing.
  var dialog = document.getElementById("modal");
  if (!dialog) return;

  // Put server-sent HTML in the dialog and open it. The "if" avoids calling showModal() twice
  // (which would throw an error) when we are just redrawing a form that already shows errors.
  function show(html) {
    dialog.innerHTML = html;
    if (!dialog.open) dialog.showModal();
  }

  // One click listener for the whole page (event delegation): it also works for buttons that
  // did not exist at load time, such as the Close buttons inside HTML we inject later.
  document.addEventListener("click", function (e) {
    // closest() walks up from what was clicked, so clicking the icon inside a button still counts.
    var opener = e.target.closest("[data-modal]");
    if (opener) {
      fetch(opener.getAttribute("data-modal")).then(function (r) { return r.text(); }).then(show);
    // Close on any [data-close] button (X / Cancel), or when the click lands on the dimmed
    // backdrop (a click outside the card registers on the <dialog> element itself).
    } else if (e.target.closest("[data-close]") || e.target === dialog) {
      dialog.close();
    }
  });

  // "submit" bubbles up from the form inside the dialog, so one listener here covers every form we load.
  dialog.addEventListener("submit", function (e) {
    // Stop the normal browser submit (which would load a new page) because we send it ourselves below.
    e.preventDefault();
    var form = e.target;
    // FormData collects every input, including the hidden CSRF token Django requires.
    fetch(form.action, { method: "POST", body: new FormData(form) }).then(function (r) {
      // 204 = success: the view saved/deleted and sent no body, so refresh to show the change.
      if (r.status === 204) location.reload();
      // Otherwise the server returned the form again with validation errors; show it.
      else return r.text().then(show);
    });
  });
})();
