document.addEventListener("DOMContentLoaded", () => {
  // -----------------------------
  // Tabs (Programación / Guardar)
  // -----------------------------
  function initTabs(scope) {
    const buttons = Array.from(document.querySelectorAll(`[data-tab-btn="${scope}"]`));
    const panels = Array.from(document.querySelectorAll(`[data-tab-panel="${scope}"]`));

    if (!buttons.length || !panels.length) return;

    function setActive(day) {
      buttons.forEach(btn => {
        const isActive = btn.dataset.day === day;
        btn.classList.toggle("is-active", isActive);
        btn.setAttribute("aria-selected", String(isActive));
      });

      panels.forEach(p => {
        const isActive = p.dataset.day === day;
        p.classList.toggle("is-active", isActive);
      });
    }

    // Default: primer día con contenido > 0, si no, primer tab
    let defaultDay = buttons[0].dataset.day;

    for (const btn of buttons) {
      const countEl = btn.querySelector(".day-tab__count");
      const n = countEl ? parseInt((countEl.textContent || "0").trim(), 10) : 0;
      if (n > 0) { defaultDay = btn.dataset.day; break; }
    }

    setActive(defaultDay);

    buttons.forEach(btn => {
      btn.addEventListener("click", () => setActive(btn.dataset.day));
    });
  }

  // -----------------------------
  // Contadores reales para "Guardar hechos"
  // (cuenta checkboxes por panel)
  // -----------------------------
  function refreshSaveTabCounts() {
    const savePanels = Array.from(document.querySelectorAll('[data-tab-panel="save"]'));
    if (!savePanels.length) return;

    savePanels.forEach(panel => {
      const day = panel.dataset.day;
      // items reales listos para guardar en ese día
      const checks = panel.querySelectorAll('input[name="backups_realizados"]');
      const n = checks.length;

      const badge = document.querySelector(`[data-save-count="${CSS.escape(day)}"]`);
      if (badge) badge.textContent = String(n);

      // también actualiza el .day-tab__count si no usa data-save-count
      const tabBtn = document.querySelector(`[data-tab-btn="save"][data-day="${CSS.escape(day)}"]`);
      if (tabBtn) {
        const countEl = tabBtn.querySelector(".day-tab__count");
        if (countEl && !countEl.hasAttribute("data-save-count")) {
          countEl.textContent = String(n);
        }
      }
    });
  }

  // Iniciar
  refreshSaveTabCounts();
  initTabs("prog");
  initTabs("save");

  // -----------------------------------------
  // Guardar hechos: seleccionar/deseleccionar
  // Solo opera sobre el panel activo (save)
  // -----------------------------------------
  const btnToggleAll = document.getElementById("btnToggleAll");
  const btnGuardar = document.getElementById("btnGuardar");
  const guardarForm = document.getElementById("guardarForm");

  function getActiveSavePanel() {
    return document.querySelector('[data-tab-panel="save"].is-active');
  }

  function getActiveChecks() {
    const panel = getActiveSavePanel();
    if (!panel) return [];
    return Array.from(panel.querySelectorAll('input[name="backups_realizados"]'));
  }

  if (btnToggleAll) {
    btnToggleAll.addEventListener("click", () => {
      const checks = getActiveChecks();
      if (!checks.length) return;

      const allChecked = checks.every(c => c.checked);
      checks.forEach(c => (c.checked = !allChecked));

      btnToggleAll.innerHTML = allChecked
        ? `<span class="material-symbols-outlined">select_check_box</span> Seleccionar todo`
        : `<span class="material-symbols-outlined">check_box</span> Deseleccionar todo`;
    });
  }

  if (btnGuardar && guardarForm) {
    btnGuardar.addEventListener("click", (e) => {
      const checks = getActiveChecks();
      const selected = checks.filter(c => c.checked);

      if (selected.length === 0) {
        e.preventDefault();
        alert("No hay backups seleccionados para guardar en el día actual.");
        return;
      }

      if (!confirm(`¿Guardar ${selected.length} backup(s) como hechos? (No duplicará dentro de la semana)`)) {
        e.preventDefault();
      }
    });

    // Al cambiar de tab en "save", resetea texto del toggle
    document.querySelectorAll('[data-tab-btn="save"]').forEach(btn => {
      btn.addEventListener("click", () => {
        if (btnToggleAll) {
          btnToggleAll.innerHTML = `<span class="material-symbols-outlined">select_check_box</span> Seleccionar todo`;
        }
      });
    });
  }

  // -----------------------------
  // Botón "Detalle del día"
  // -----------------------------
  document.querySelectorAll("[data-detail-btn]").forEach(btn => {
    btn.addEventListener("click", () => {
      const panel = btn.closest(".day-panel");
      if (!panel) return;
      const table = panel.querySelector(".table");
      if (!table) return;
      table.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });
});
