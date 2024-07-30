document.addEventListener('DOMContentLoaded', function () {
  const searchButton = document.querySelector('.search-button');
  searchButton.addEventListener('click', function (event) {
    event.preventDefault();
    const searchQuery = document.querySelector('.search-box').value;
    if (searchQuery) {
      window.location.href = `https://www.google.com/search?q=${searchQuery}`; // for now only
    }
  });
});
