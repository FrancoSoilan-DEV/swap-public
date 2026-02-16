document.addEventListener('DOMContentLoaded', function() {
    'use strict';
    
    // ========== ACTUALIZAR ESTADÍSTICAS ==========
    function updateStats() {
        const totalEquipos = document.getElementById('totalEquipos');
        const totalFuncionarios = document.getElementById('totalFuncionarios');
        const equiposCount = document.getElementById('equiposCount');
        const funcionariosCount = document.getElementById('funcionariosCount');
        
        if (totalEquipos) totalEquipos.textContent = window.totalEquipos || 0;
        if (totalFuncionarios) totalFuncionarios.textContent = window.totalFuncionarios || 0;
        if (equiposCount) equiposCount.textContent = window.totalEquipos || 0;
        if (funcionariosCount) funcionariosCount.textContent = window.totalFuncionarios || 0;
    }
    updateStats();
    
    // ========== FILTRO FUNCIONARIOS CON EQUIPO ==========
    const searchEquipos = document.getElementById('searchEquipos');
    const clearSearchEquipos = document.getElementById('clearSearchEquipos');
    const equiposTableBody = document.getElementById('equiposTableBody');
    
    if (searchEquipos) {
        searchEquipos.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase().trim();
            
            // Show/hide clear button
            if (clearSearchEquipos) {
                if (searchTerm.length > 0) {
                    clearSearchEquipos.classList.add('visible');
                } else {
                    clearSearchEquipos.classList.remove('visible');
                }
            }
            
            // Filter rows
            const rows = equiposTableBody.querySelectorAll('tr:not(.empty-row)');
            let visibleCount = 0;
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchTerm) || searchTerm === '') {
                    row.style.display = '';
                    visibleCount++;
                } else {
                    row.style.display = 'none';
                }
            });
            
            // Show empty state if no results
            const emptyRow = equiposTableBody.querySelector('.empty-row');
            if (visibleCount === 0) {
                if (!emptyRow) {
                    const newEmptyRow = document.createElement('tr');
                    newEmptyRow.className = 'empty-row';
                    newEmptyRow.innerHTML = `
                        <td colspan="7">
                            <div class="empty-state">
                                <span class="material-symbols-outlined">search_off</span>
                                <p>No se encontraron resultados para "${searchTerm}"</p>
                            </div>
                        </td>
                    `;
                    equiposTableBody.appendChild(newEmptyRow);
                } else {
                    const emptyCell = emptyRow.querySelector('td div p');
                    if (emptyCell) {
                        emptyCell.textContent = `No se encontraron resultados para "${searchTerm}"`;
                    }
                    emptyRow.style.display = '';
                }
            } else {
                if (emptyRow) {
                    emptyRow.style.display = 'none';
                }
            }
        });
    }
    
    // Clear search
    if (clearSearchEquipos) {
        clearSearchEquipos.addEventListener('click', function() {
            if (searchEquipos) {
                searchEquipos.value = '';
                searchEquipos.dispatchEvent(new Event('input'));
                searchEquipos.focus();
            }
        });
    }
    
    // ========== FILTRO FUNCIONARIOS ==========
    const searchFuncionarios = document.getElementById('searchFuncionarios');
    const clearSearchFuncionarios = document.getElementById('clearSearchFuncionarios');
    const funcionariosTableBody = document.getElementById('funcionariosTableBody');
    
    if (searchFuncionarios) {
        searchFuncionarios.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase().trim();
            
            if (clearSearchFuncionarios) {
                if (searchTerm.length > 0) {
                    clearSearchFuncionarios.classList.add('visible');
                } else {
                    clearSearchFuncionarios.classList.remove('visible');
                }
            }
            
            const rows = funcionariosTableBody.querySelectorAll('tr:not(.empty-row)');
            let visibleCount = 0;
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchTerm) || searchTerm === '') {
                    row.style.display = '';
                    visibleCount++;
                } else {
                    row.style.display = 'none';
                }
            });
            
            const emptyRow = funcionariosTableBody.querySelector('.empty-row');
            if (visibleCount === 0) {
                if (!emptyRow) {
                    const newEmptyRow = document.createElement('tr');
                    newEmptyRow.className = 'empty-row';
                    newEmptyRow.innerHTML = `
                        <td colspan="3">
                            <div class="empty-state">
                                <span class="material-symbols-outlined">search_off</span>
                                <p>No se encontraron resultados para "${searchTerm}"</p>
                            </div>
                        </td>
                    `;
                    funcionariosTableBody.appendChild(newEmptyRow);
                } else {
                    const emptyCell = emptyRow.querySelector('td div p');
                    if (emptyCell) {
                        emptyCell.textContent = `No se encontraron resultados para "${searchTerm}"`;
                    }
                    emptyRow.style.display = '';
                }
            } else {
                if (emptyRow) {
                    emptyRow.style.display = 'none';
                }
            }
        });
    }
    
    if (clearSearchFuncionarios) {
        clearSearchFuncionarios.addEventListener('click', function() {
            if (searchFuncionarios) {
                searchFuncionarios.value = '';
                searchFuncionarios.dispatchEvent(new Event('input'));
                searchFuncionarios.focus();
            }
        });
    }
    
    // ========== VALIDACIÓN DE IP EN TIEMPO REAL ==========
    const ipInput = document.querySelector('input[name="fce_ip"]');
    if (ipInput) {
        ipInput.addEventListener('input', function(e) {
            const ip = this.value;
            const ipRegex = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
            
            // Remove existing error
            const existingError = this.parentNode.querySelector('.ip-error');
            if (existingError) existingError.remove();
            
            if (ip && !ipRegex.test(ip)) {
                this.style.borderColor = '#ef476f';
                
                const errorMsg = document.createElement('div');
                errorMsg.className = 'error-message ip-error';
                errorMsg.style.cssText = 'color: #ef476f; font-size: 11px; margin-top: 4px; display: flex; align-items: center; gap: 4px;';
                errorMsg.innerHTML = '<span class="material-symbols-outlined" style="font-size: 14px;">error</span> Dirección IP no válida';
                this.parentNode.appendChild(errorMsg);
            } else {
                this.style.borderColor = '';
            }
        });
        
        ipInput.addEventListener('blur', function() {
            if (this.value === '') {
                this.style.borderColor = '';
                const existingError = this.parentNode.querySelector('.ip-error');
                if (existingError) existingError.remove();
            }
        });
    }
    
    // ========== MEJORAR SELECTS CON BÚSQUEDA ==========
    const selects = document.querySelectorAll('.form-select');
    selects.forEach(select => {
        if (select.options.length > 5) {
            // Add search input for better UX
            const wrapper = document.createElement('div');
            wrapper.style.position = 'relative';
            select.parentNode.insertBefore(wrapper, select);
            wrapper.appendChild(select);
            
            const searchIcon = document.createElement('span');
            searchIcon.className = 'material-symbols-outlined';
            searchIcon.style.cssText = 'position: absolute; left: 12px; top: 50%; transform: translateY(-50%); font-size: 18px; color: var(--gray-500); pointer-events: none;';
            searchIcon.textContent = 'search';
            wrapper.appendChild(searchIcon);
            
            select.style.paddingLeft = '44px';
        }
    });
    
    // ========== CONFIRMACIÓN ANTES DE ELIMINAR ==========
    const deleteForm = document.querySelector('form .btn-danger');
    if (deleteForm) {
        deleteForm.addEventListener('click', function(e) {
            const select = document.querySelector('select[name="fce_id"]');
            if (select && !select.value) {
                e.preventDefault();
                alert('Por favor, selecciona un registro para desactivar');
                return;
            }
            
            if (!confirm('¿Estás seguro de desactivar este registro? El registro pasará a estado inactivo y no aparecerá en los listados activos.')) {
                e.preventDefault();
            }
        });
    }
    
    // ========== RESPONSIVE TABLE HINT ==========
    function checkTableOverflow() {
        const tables = document.querySelectorAll('.table-responsive');
        tables.forEach(table => {
            if (table.scrollWidth > table.clientWidth) {
                const hint = document.querySelector('.mobile-hint');
                if (hint) hint.style.display = 'flex';
            }
        });
    }
    
    window.addEventListener('load', checkTableOverflow);
    window.addEventListener('resize', checkTableOverflow);
    
    // ========== ANIMACIONES SMOOTH ==========
    // Add ripple effect to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            ripple.className = 'ripple';
            ripple.style.cssText = `
                position: absolute;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.5);
                transform: scale(0);
                animation: ripple 0.6s linear;
                pointer-events: none;
            `;
            
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = `${size}px`;
            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;
            
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
    });
    
    // Add ripple animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
});