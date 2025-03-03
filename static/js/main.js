document.addEventListener('DOMContentLoaded', function() {
    // File size validation
    const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
    
    const imageInputs = document.querySelectorAll('input[type="file"]');
    imageInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file.size > MAX_FILE_SIZE) {
                alert('File size must be less than 5MB');
                e.target.value = '';
            }
        });
    });

    // Message length validation
    const messageInput = document.getElementById('message');
    if (messageInput) {
        messageInput.addEventListener('input', function() {
            const maxLength = 1000;
            if (this.value.length > maxLength) {
                alert(`Message must be less than ${maxLength} characters`);
                this.value = this.value.substring(0, maxLength);
            }
        });
    }

    // Image preview
    const previewImage = (input, previewId) => {
        const preview = document.getElementById(previewId);
        if (preview && input.files && input.files[0]) {
            const reader = new FileReader();
            reader.onload = function(e) {
                preview.src = e.target.result;
                preview.style.display = 'block';
            }
            reader.readAsDataURL(input.files[0]);
        }
    };

    // Add loading indicators
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Processing...';
        });
    });
});