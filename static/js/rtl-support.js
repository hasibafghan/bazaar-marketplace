document.addEventListener('DOMContentLoaded', function () {
  var html = document.documentElement;
  if (html.dir === 'rtl') {
    html.classList.add('rtl');
    html.classList.remove('ltr');
  } else {
    html.classList.add('ltr');
    html.classList.remove('rtl');
  }
});
