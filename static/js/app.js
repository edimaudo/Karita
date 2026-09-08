(() => {
  const root = document.documentElement;
  const savedTheme = localStorage.getItem("karita-theme") || "dark";
  const savedSize = localStorage.getItem("karita-font-size") || "medium";
  root.dataset.theme = savedTheme;
  root.dataset.fontSize = savedSize;

  document.querySelectorAll("[data-font]").forEach(button => {
    button.classList.toggle("active", button.dataset.font === savedSize);
    button.addEventListener("click", () => {
      const size = button.dataset.font;
      root.dataset.fontSize = size;
      localStorage.setItem("karita-font-size", size);
      document.querySelectorAll("[data-font]").forEach(b => b.classList.toggle("active", b === button));
    });
  });

  const themeButton = document.querySelector("[data-theme-toggle]");
  if (themeButton) {
    themeButton.addEventListener("click", () => {
      const theme = root.dataset.theme === "dark" ? "light" : "dark";
      root.dataset.theme = theme;
      localStorage.setItem("karita-theme", theme);
    });
  }
})();
