document.addEventListener('DOMContentLoaded', function() {
    'use strict';
    
    // ========== ACTUALIZAR ESTADÍSTICAS ==========
    const totalBackups = document.getElementById('totalBackups');
    if (totalBackups) totalBackups.textContent = window.totalBackups || 0;
    
    // ========== FILTRO DE BACKUPS ==========
    const searchInput = document.getElementById('searchBackups');
    const clearButton = document.getElementById('clearSearchBackups');
    const tableBody = document.getElementById('backupsTableBody');
    
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase().trim();
            
            // Mostrar/ocultar botón de limpiar
            if (clearButton) {
                if (searchTerm.length > 0) {
                    clearButton.classList.add('visible');
                } else {
                    clearButton.classList.remove('visible');
                }
            }
            
            // Filtrar filas
            const rows = tableBody.querySelectorAll('tr:not(.empty-row)');
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
            
            // Mostrar estado vacío si no hay resultados
            const emptyRow = tableBody.querySelector('.empty-row');
            if (visibleCount === 0) {
                if (!emptyRow) {
                    const newEmptyRow = document.createElement('tr');
                    newEmptyRow.className = 'empty-row';
                    newEmptyRow.innerHTML = `
                        <td colspan="5">
                            <div class="empty-state">
                                <span class="material-symbols-outlined">search_off</span>
                                <p>No se encontraron resultados para "${searchTerm}"</p>
                            </div>
                        </td>
                    `;
                    tableBody.appendChild(newEmptyRow);
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
    
    // Limpiar búsqueda
    if (clearButton) {
        clearButton.addEventListener('click', function() {
            if (searchInput) {
                searchInput.value = '';
                searchInput.dispatchEvent(new Event('input'));
                searchInput.focus();
            }
        });
    }
    
    // ========== CONFIRMACIÓN ANTES DE ELIMINAR ==========
    const deleteForm = document.querySelector('.form-card.danger form');
    const deleteButton = deleteForm?.querySelector('.btn-danger');
    
    if (deleteButton) {
        deleteButton.addEventListener('click', function(e) {
            const select = deleteForm.querySelector('select[name="bk_id"]');
            if (select && !select.value) {
                e.preventDefault();
                alert('Por favor, selecciona un backup para desactivar');
                return;
            }
        });
    }
    
    // ========== MEJORAR SELECT CON BÚSQUEDA ==========
    const selects = document.querySelectorAll('.form-select');
    selects.forEach(select => {
        if (select.options.length > 5) {
            select.style.backgroundPosition = 'right 16px center';
        }
    });
    
    // ========== TOOLTIPS PARA PAGINACIÓN ==========
    const pageBtns = document.querySelectorAll('.page-btn[title]');
    pageBtns.forEach(btn => {
        btn.addEventListener('mouseenter', function(e) {
            const title = this.getAttribute('title');
            if (title) {
                this.setAttribute('data-title', title);
            }
        });
    });
});