document.addEventListener('DOMContentLoaded', function () {
    const articleId = document.getElementById('article-id').value;

    fetch(`/api/articles/${articleId}/`)
        .then(response => response.json())
        .then(article => {
            document.getElementById('article-title').innerText = article.title;
            document.getElementById('article-content').innerText = article.content;
            document.getElementById('article-rating').innerText = 'rated ' + article.average_rating + " / 5";
        })
        .catch(error => {
            displayError('Error fetching article details.' + error);
        });

    const ratingForm = document.getElementById('rating-form');
    ratingForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const formData = new FormData(ratingForm);
        fetch('/api/ratings/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            },
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.created) {
                    alert('Rating submitted successfully.');
                } else {
                    alert('Rating updated successfully.');
                }
                window.location.reload();
            })
            .catch(error => {
                displayError('An error occurred while submitting the rating.');
            });
    });
});

function displayError(message) {
    const errorBox = document.getElementById('error-box');
    errorBox.innerText = message;
    errorBox.classList.remove('hidden');
}
