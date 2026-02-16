document.addEventListener("DOMContentLoaded", () => {
  const selectAll = document.getElementById("select-all");
  const rowChecks = Array.from(document.querySelectorAll(".row-check"));
  const deleteBtn = document.getElementById("delete-selected");

  const updateDeleteState = () => {
    const anyChecked = rowChecks.some(cb => cb.checked);
    if (deleteBtn) deleteBtn.disabled = !anyChecked;
  };

  if (selectAll) {
    selectAll.addEventListener("change", () => {
      rowChecks.forEach(cb => (cb.checked = selectAll.checked));
      selectAll.indeterminate = false;
      updateDeleteState();
    });
  }

  rowChecks.forEach(cb => {
    cb.addEventListener("change", () => {
      if (selectAll) {
        const allChecked = rowChecks.length > 0 && rowChecks.every(x => x.checked);
        const noneChecked = rowChecks.every(x => !x.checked);
        selectAll.checked = allChecked;
        selectAll.indeterminate = !allChecked && !noneChecked;
      }
      updateDeleteState();
    });
  });

  if (deleteBtn) {
    deleteBtn.addEventListener("click", (e) => {
      const count = rowChecks.filter(cb => cb.checked).length;
      if (!count) return;
      if (!confirm(`¿Eliminar ${count} registro(s) de backups hechos?`)) e.preventDefault();
    });
  }

  updateDeleteState();
});