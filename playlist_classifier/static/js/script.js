document.getElementById('classifyForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const playlistId = document.getElementById('playlistId').value;
    fetch('/classify', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `playlist_id=${encodeURIComponent(playlistId)}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        let result = '<h3>Classification Result:</h3><ul>';
        data.forEach(song => {
            result += `<li>${song.title} - Mood: ${song.mood}, Genre: ${song.genre}</li>`;
        });
        result += '</ul>';
        document.getElementById('classificationResult').innerHTML = result;
    })
    .catch(error => {
        document.getElementById('classificationResult').innerHTML = `<p class="error">Error: ${error.message}</p>`;
    });
});

document.getElementById('generateForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const mood = document.getElementById('moodSelect').value;
    const genre = document.getElementById('genreSelect').value;
    fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `mood=${encodeURIComponent(mood)}&genre=${encodeURIComponent(genre)}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        let result = '<h3>Generated Playlist:</h3><ul>';
        data.forEach(song => {
            result += `<li>${song.title}</li>`;
        });
        result += '</ul>';
        document.getElementById('generationResult').innerHTML = result;
    })
    .catch(error => {
        document.getElementById('generationResult').innerHTML = `<p class="error">Error: ${error.message}</p>`;
    });
});