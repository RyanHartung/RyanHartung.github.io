document.querySelectorAll("[data-cv-view]").forEach((button) => {
  button.addEventListener("click", () => {
    const panel = document.getElementById(button.getAttribute("aria-controls"));
    if (!panel) {
      console.error(`CV view panel not found: ${button.getAttribute("aria-controls")}`);
      return;
    }

    const shouldShow = panel.hidden;
    document.querySelectorAll("[data-cv-panel]").forEach((cvPanel) => {
      cvPanel.hidden = true;
    });
    document.querySelectorAll("[data-cv-view]").forEach((viewButton) => {
      viewButton.setAttribute("aria-pressed", "false");
    });

    if (shouldShow) {
      panel.hidden = false;
      button.setAttribute("aria-pressed", "true");
    }
  });
});
