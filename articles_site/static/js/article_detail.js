document.addEventListener('DOMContentLoaded', function () {
    const articleId = document.getElementById('article-id').value;

    fetch(`/api/articles/${articleId}/`)
        .then(response => response.json())
        .then(article => {
            document.getElementById('article-title').innerText = article.title;
            document.getElementById('article-content').innerText = article.content;
            document.getElementById('article-rating').innerText = 'rated ' + article.average_rating + " / 5";

            // Fetch user's rating for the article
            fetch(`/api/get_rating/?article_id=${articleId}`)
                .then(response => {
                    if (response.status === 200) {
                        return response.json();
                    } else if (response.status === 404) {
                        document.getElementById('rating').value = '';
                    } else {
                        throw new Error('Error fetching user rating.');
                    }
                })
                .then(ratingData => {
                    if (ratingData) {
                        document.getElementById('rating').value = ratingData.rating;
                    }

                    // Enable or disable the submit button after fetching is complete
                    const ratingForm = document.getElementById('rating-form');
                    const submitButton = ratingForm.querySelector('button[type="submit"]');

                    if (document.getElementById('rating').value === "") {
                        submitButton.disabled = true;
                    }

                    setTimeout(() => {
                        submitButton.disabled = false;
                    }, 30000);  // 30 seconds delay
                })
                .catch(error => {
                    displayError('Error fetching user rating: ' + error.message);
                });
        })
        .catch(error => {
            displayError('Error fetching article details: ' + error.message);
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
            .then(response => {
                if (response.status === 200 || response.status === 201) {
                    return response.json();
                } else {
                    return response.text().then(text => {
                        throw new Error(`Failed to submit rating. Response: ${text}`);
                    });
                }
            })
            .then(data => {
                alert('Rating submitted successfully.');
                window.location.reload();
            })
            .catch(error => {
                displayError('An error occurred while submitting the rating: ' + error.message);
            });
    });

    function displayError(message) {
        const errorBox = document.getElementById('error-box');
        errorBox.innerText = message;
        errorBox.classList.remove('hidden');
    }
});
