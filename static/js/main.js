// Auto-dismiss messages
document.querySelectorAll('.message').forEach(msg => {
    setTimeout(() => msg.remove(), 5000);
});

// Active nav link highlight
const currentPath = window.location.pathname;
document.querySelectorAll('.nav-link').forEach(link => {
    if (link.href && link.pathname === currentPath) {
        link.style.color = 'var(--accent)';
    }
});
