const tabs = Array.from(document.querySelectorAll("[data-tab]"));
const panels = Array.from(document.querySelectorAll("[data-panel]"));

function selectTab(tabName, { updateHash = true, focus = false } = {}) {
  const nextTab = tabs.find((tab) => tab.dataset.tab === tabName) || tabs[0];

  tabs.forEach((tab) => {
    const active = tab === nextTab;
    tab.classList.toggle("is-active", active);
    tab.setAttribute("aria-selected", String(active));
    tab.tabIndex = active ? 0 : -1;
  });

  panels.forEach((panel) => {
    panel.hidden = panel.dataset.panel !== nextTab.dataset.tab;
  });

  if (updateHash) {
    window.history.replaceState(null, "", `#${nextTab.dataset.tab}`);
  }
  window.scrollTo({ top: 0, behavior: "instant" });
  if (focus) {
    nextTab.focus();
  }
}

tabs.forEach((tab, index) => {
  tab.addEventListener("click", () => selectTab(tab.dataset.tab));
  tab.addEventListener("keydown", (event) => {
    if (!['ArrowLeft', 'ArrowRight'].includes(event.key)) {
      return;
    }
    event.preventDefault();
    const direction = event.key === 'ArrowRight' ? 1 : -1;
    const nextIndex = (index + direction + tabs.length) % tabs.length;
    selectTab(tabs[nextIndex].dataset.tab, { focus: true });
  });
});

document.querySelector(".identity").addEventListener("click", (event) => {
  event.preventDefault();
  selectTab("project");
});

const initialTab = window.location.hash.replace("#", "");
selectTab(initialTab === "about" ? "about" : "project", { updateHash: false });
