document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/articles/')
        .then(response => response.json())
        .then(data => {
            const articlesList = document.getElementById('articles-list');
            data.results.forEach(article => {
                const listItem = document.createElement('li');
                listItem.innerHTML = `
                    <a href="/articles/${article.id}/">
                        <h2>${article.title}</h2>
                        <p>Author: ${article.author_username}</p>
                        <p>Average Rating: ${article.average_rating}</p>
                    </a>
                    <hr>
                `;
                articlesList.appendChild(listItem);
            });
        })
        .catch(error => {
            displayError('Error fetching articles.');
        });
});

function displayError(message) {
    const errorBox = document.getElementById('error-box');
    errorBox.innerText = message;
    errorBox.classList.remove('hidden');
}
