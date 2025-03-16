// Form validation and submission handling
document.addEventListener('DOMContentLoaded', function() {
    // Show loading spinner during form submission
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const spinner = this.querySelector('.loading-spinner');
            if (spinner) {
                spinner.style.display = 'inline-block';
            }
        });
    });

    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Handle allergen selection in profile
    const allergenSelect = document.getElementById('allergens');
    if (allergenSelect) {
        allergenSelect.addEventListener('change', function() {
            const selectedOptions = Array.from(this.selectedOptions);
            const selectedCount = document.getElementById('selected-count');
            if (selectedCount) {
                selectedCount.textContent = selectedOptions.length;
            }
        });
    }

    // Real-time search input validation
    const searchInput = document.querySelector('input[type="search"]');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const submitBtn = document.querySelector('button[type="submit"]');
            submitBtn.disabled = this.value.trim().length === 0;
        });
    }
});
