// static/js/base.js
document.addEventListener('DOMContentLoaded', function () {
  const sidebar = document.querySelector('.sidebar');
  const overlay = document.getElementById('overlay');
  const mobileMenuBtn = document.getElementById('mobileMenuBtn');

  // ========== DROPDOWNS (soporta múltiples) ==========
  const toggles = Array.from(document.querySelectorAll('.dropdown-toggle'));

  function closeAllDropdowns(exceptToggle = null) {
    toggles.forEach(tg => {
      const menu = tg.nextElementSibling; // asume .dropdown-menu justo después
      if (!menu || !menu.classList.contains('dropdown-menu')) return;

      if (exceptToggle && tg === exceptToggle) return;

      tg.classList.remove('active');
      menu.classList.remove('show');

      const arrow = tg.querySelector('.dropdown-arrow');
      if (arrow) arrow.style.transform = '';
    });
  }

  toggles.forEach(toggle => {
    const menu = toggle.nextElementSibling;
    if (!menu || !menu.classList.contains('dropdown-menu')) return;

    toggle.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();

      // Cierra otros dropdowns
      closeAllDropdowns(toggle);

      // Toggle actual
      toggle.classList.toggle('active');
      menu.classList.toggle('show');

      const arrow = toggle.querySelector('.dropdown-arrow');
      if (arrow) {
        arrow.style.transform = menu.classList.contains('show') ? 'rotate(90deg)' : '';
      }
    });

    // Prevenir que clicks dentro del menú lo cierren
    menu.addEventListener('click', function (e) {
      e.stopPropagation();
    });
  });

  // Cerrar dropdowns al hacer click fuera
  document.addEventListener('click', function () {
    closeAllDropdowns(null);
  });

  // ========== MOBILE MENU ==========
  function toggleMobileMenu() {
    sidebar.classList.toggle('active');
    overlay.classList.toggle('active');

    if (sidebar.classList.contains('active')) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
  }

  function closeMobileMenu() {
    sidebar.classList.remove('active');
    overlay.classList.remove('active');
    document.body.style.overflow = '';
  }

  if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      toggleMobileMenu();
    });
  }

  if (overlay) {
    overlay.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      closeMobileMenu();
    });
  }

  window.addEventListener('resize', function () {
    if (window.innerWidth > 768) {
      closeMobileMenu();
      document.body.style.overflow = '';
    }
  });

  // ========== AUTO-OPEN segun ruta ==========
  const currentPath = window.location.pathname;

  // Auto-abrir Backups
  if (currentPath.includes('/backups') || currentPath.includes('/bk')) {
    const backupsToggle = document.getElementById('backupsDropdown');
    if (backupsToggle) {
      const menu = backupsToggle.nextElementSibling;
      backupsToggle.classList.add('active');
      if (menu && menu.classList.contains('dropdown-menu')) {
        menu.classList.add('show');
      }
      const arrow = backupsToggle.querySelector('.dropdown-arrow');
      if (arrow) arrow.style.transform = 'rotate(90deg)';
    }
  }

  // Auto-abrir Inventario
  if (currentPath.includes('/inventario')) {
    const invToggle = document.getElementById('inventarioDropdown');
    if (invToggle) {
      const menu = invToggle.nextElementSibling;
      invToggle.classList.add('active');
      if (menu && menu.classList.contains('dropdown-menu')) {
        menu.classList.add('show');
      }
      const arrow = invToggle.querySelector('.dropdown-arrow');
      if (arrow) arrow.style.transform = 'rotate(90deg)';
    }
  }

  // Prevenir que clicks en el sidebar lo cierren (mantengo tu comportamiento)
  if (sidebar) {
    sidebar.addEventListener('click', function (e) {
      e.stopPropagation();
    });
  }
});