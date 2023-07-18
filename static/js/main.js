// main.js
const imageUpload = document.getElementById('image-upload');
const imagePreviewContainer = document.getElementById('image-preview-container');
const captureButton = document.getElementById('capture-btn');

captureButton.addEventListener('click', function() {
    if ('mediaDevices' in navigator && 'getUserMedia' in navigator.mediaDevices) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function(stream) {
                const video = document.createElement('video');
                video.srcObject = stream;
                video.autoplay = true;
                video.addEventListener('loadedmetadata', function() {
                    const canvas = document.createElement('canvas');
                    canvas.width = video.videoWidth;
                    canvas.height = video.videoHeight;
                    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
                    const imageUrl = canvas.toDataURL('image/jpeg');
                    displayImagePreview(imageUrl);
                    stream.getTracks().forEach(function(track) {
                        track.stop();
                    });
                });
            })
            .catch(function(error) {
                console.log('Error accessing camera:', error);
            });
    } else {
        console.log('Camera not supported');
    }
});

imageUpload.addEventListener('change', function() {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(event) {
            const imageUrl = event.target.result;
            displayImagePreview(imageUrl);
        };
        reader.readAsDataURL(file);
    } else {
        imagePreviewContainer.innerHTML = '';
    }
});

function displayImagePreview(imageUrl) {
    const imagePreview = document.createElement('img');
    imagePreview.src = imageUrl;
    imagePreviewContainer.innerHTML = '';
    imagePreviewContainer.appendChild(imagePreview);
}
