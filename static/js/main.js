document.addEventListener('DOMContentLoaded', function () {
    // 1. Sidebar Toggler
    const sidebarCollapse = document.getElementById('sidebarCollapse');
    const sidebar = document.getElementById('sidebar');
    
    if (sidebarCollapse && sidebar) {
        sidebarCollapse.addEventListener('click', function () {
            sidebar.classList.toggle('active');
        });
    }

    // 2. Dark / Light Mode Switcher
    const themeToggleBtn = document.getElementById('theme-toggle');
    const htmlElement = document.documentElement;
    
    // Check saved theme or system preference
    const savedTheme = localStorage.getItem('theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // Default to dark mode if no setting is saved (premium dark-mode design first)
    if (savedTheme) {
        htmlElement.setAttribute('data-theme', savedTheme);
        updateThemeToggleIcon(savedTheme);
    } else {
        const defaultTheme = 'dark'; // Dark theme first
        htmlElement.setAttribute('data-theme', defaultTheme);
        updateThemeToggleIcon(defaultTheme);
    }
    
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', function () {
            const currentTheme = htmlElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            htmlElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeToggleIcon(newTheme);
            
            // Dispatch custom event for Chart.js updates if required
            window.dispatchEvent(new Event('themeChanged'));
        });
    }
    
    function updateThemeToggleIcon(theme) {
        if (!themeToggleBtn) return;
        const icon = themeToggleBtn.querySelector('i');
        if (!icon) return;
        
        if (theme === 'dark') {
            icon.className = 'fas fa-sun text-warning';
            themeToggleBtn.setAttribute('title', 'Switch to Light Mode');
        } else {
            icon.className = 'fas fa-moon text-primary';
            themeToggleBtn.setAttribute('title', 'Switch to Dark Mode');
        }
    }

    // 3. Auto-hide Alerts/Toasts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            // Smoothly fade out using bootstrap transition or custom opacity
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(function () {
                alert.remove();
            }, 500);
        }, 5000);
    });

    // 4. Show/Hide Password Toggle Injection
    const passwordFields = document.querySelectorAll('input[type="password"]');
    passwordFields.forEach(function (field) {
        // Find or create input group container
        let inputGroup = field.closest('.input-group');
        if (!inputGroup) {
            // Standalone password input (e.g. registration loop)
            inputGroup = document.createElement('div');
            inputGroup.className = 'input-group';
            field.parentNode.insertBefore(inputGroup, field);
            inputGroup.appendChild(field);
        }
        
        // Add border end override class to input
        field.classList.add('border-end-0');
        
        // Create toggle button
        const toggleBtn = document.createElement('button');
        toggleBtn.type = 'button';
        toggleBtn.className = 'btn toggle-password-btn';
        toggleBtn.innerHTML = '<i class="fa-solid fa-eye"></i>';
        toggleBtn.setAttribute('aria-label', 'Toggle password visibility');
        
        // Append to group
        inputGroup.appendChild(toggleBtn);
        
        // Toggle visibility click handler
        toggleBtn.addEventListener('click', function () {
            const icon = toggleBtn.querySelector('i');
            if (field.type === 'password') {
                field.type = 'text';
                icon.className = 'fa-solid fa-eye-slash';
            } else {
                field.type = 'password';
                icon.className = 'fa-solid fa-eye';
            }
        });
    });
});

