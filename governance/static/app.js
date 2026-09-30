const state = {
  catalog: null,
  selectedId: null,
  creating: false,
  hash: "",
};

const $ = (id) => document.getElementById(id);

function optionList(select, values, current) {
  const first = select.querySelector("option[value='']");
  select.innerHTML = "";
  if (first) select.appendChild(first);
  for (const value of values) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    select.appendChild(option);
  }
  if (current) select.value = current;
}

function filters() {
  return {
    q: $("q").value.trim().toLowerCase(),
    repo: $("repo").value,
    topic: $("topic").value,
    kind: $("kind").value,
    activation: $("activation").value,
  };
}

function visibleItems() {
  const filter = filters();
  return state.catalog.items.filter((item) => {
    if (filter.repo && item.repo !== filter.repo) return false;
    if (filter.topic && !item.topics.includes(filter.topic)) return false;
    if (filter.kind && item.kind !== filter.kind) return false;
    if (filter.activation && item.activation !== filter.activation) return false;
    if (state.hash && item.content_hash !== state.hash) return false;
    if (!filter.q) return true;
    const haystack = [item.title, item.repo, item.description, item.source_path, ...item.topics]
      .join(" ")
      .toLowerCase();
    return haystack.includes(filter.q);
  });
}

function renderBudgets() {
  const host = $("budgets");
  host.innerHTML = "";
  for (const budget of state.catalog.budgets) {
    const chip = document.createElement("button");
    chip.type = "button";
    chip.className = "budget" + (budget.over_budget ? " over" : "");
    const name = budget.repo.split("/")[1] || budget.repo;
    chip.textContent = `${name} always-on ${budget.always_on_tokens} / ${budget.cap}`;
    chip.title = budget.over_budget
      ? "Always-on text is over the per-repo budget"
      : "Always-on tokens in this repository";
    chip.addEventListener("click", () => {
      $("repo").value = budget.repo;
      state.hash = "";
      render();
    });
    host.appendChild(chip);
  }
}

function renderList() {
  const host = $("list");
  host.innerHTML = "";
  if (state.hash) {
    const clear = document.createElement("li");
    const button = document.createElement("button");
    button.type = "button";
    button.className = "ghost";
    button.textContent = "Clear identical-text filter";
    button.addEventListener("click", () => {
      state.hash = "";
      renderList();
    });
    clear.appendChild(button);
    host.appendChild(clear);
  }
  const items = visibleItems();
  if (!items.length) {
    const empty = document.createElement("li");
    empty.textContent = "Nothing matches these filters.";
    host.appendChild(empty);
    return;
  }
  for (const item of items) {
    const li = document.createElement("li");
    const button = document.createElement("button");
    button.type = "button";
    button.className = "row" + (item.id === state.selectedId ? " active" : "");
    const title = document.createElement("strong");
    title.textContent = item.title;
    const meta = document.createElement("span");
    meta.textContent = `${item.repo.split("/")[1]} · ${item.kind} · ${item.activation} · ${item.tokens} tokens`;
    button.append(title, meta);
    button.addEventListener("click", () => openItem(item.id));
    li.appendChild(button);
    if (item.identical_copies > 1) {
      const copies = document.createElement("button");
      copies.type = "button";
      copies.className = "copy";
      copies.textContent = `Same text in ${item.identical_copies}`;
      copies.addEventListener("click", () => {
        state.hash = item.content_hash;
        renderList();
      });
      li.appendChild(copies);
    }
    host.appendChild(li);
  }
}

function fillSelects() {
  optionList($("repo"), state.catalog.repos, $("repo").value);
  optionList($("topic"), state.catalog.topics, $("topic").value);
  optionList($("kind"), state.catalog.kinds, $("kind").value);
  optionList($("activation"), state.catalog.activations, $("activation").value);
  optionList($("kind-field"), state.catalog.kinds);
  optionList($("activation-field"), state.catalog.activations);
}

function renderBanner() {
  const over = state.catalog.budgets.filter((row) => row.over_budget).map((row) => row.repo.split("/")[1]);
  const budgetNote = over.length
    ? ` Over the ${state.catalog.cap}-token always-on budget: ${over.join(", ")}.`
    : ` Always-on budget is ${state.catalog.cap} tokens per repository.`;
  $("banner").textContent =
    "Archive of public rules, agent files, and automation prompts. Save writes this archive and keeps a version. It does not update the source repository or the live Cursor Automation." +
    budgetNote +
    " " +
    state.catalog.gaps[0];
}

function render() {
  fillSelects();
  renderBanner();
  renderBudgets();
  renderList();
}

async function loadCatalog() {
  const response = await fetch("/api/catalog");
  state.catalog = await response.json();
  render();
}

function showItem(item) {
  state.creating = false;
  state.selectedId = item.id;
  const summary = state.catalog.items.find((row) => row.id === item.id);
  const copies = summary ? summary.identical_copies : 1;
  $("editor-title").textContent = item.title;
  const source = item.source_url
    ? ` Source: ${item.source_path}.`
    : item.source_path
      ? ` Path: ${item.source_path}.`
      : "";
  $("editor-meta").textContent =
    `${item.tokens} tokens · ${item.kind} · ${item.activation}.${source} Identical copies: ${copies}.`;
  $("title").value = item.title;
  $("repo-field").value = item.repo;
  $("kind-field").value = item.kind;
  $("activation-field").value = item.activation;
  $("topics").value = (item.topics || []).join(", ");
  $("body").value = item.body || "";
  const history = $("history");
  const versions = $("versions");
  versions.innerHTML = "";
  const rows = item.versions || [];
  history.hidden = rows.length === 0;
  for (const version of [...rows].reverse()) {
    const li = document.createElement("li");
    const label = document.createElement("span");
    label.textContent = `${version.saved_at} · ${version.note} · ${version.tokens} tokens`;
    const restore = document.createElement("button");
    restore.type = "button";
    restore.className = "ghost";
    restore.textContent = "Restore";
    restore.addEventListener("click", () => restoreVersion(item.id, version.id));
    li.append(label, restore);
    versions.appendChild(li);
  }
  $("status").textContent = "";
  renderList();
}

async function openItem(id) {
  const response = await fetch("/api/items/" + encodeURIComponent(id));
  if (!response.ok) {
    $("status").textContent = "Could not open that directive.";
    return;
  }
  const item = await response.json();
  const summary = state.catalog.items.find((row) => row.id === id);
  showItem({ ...item, identical_copies: summary ? summary.identical_copies : 1 });
}

function payload() {
  return {
    title: $("title").value,
    repo: $("repo-field").value,
    kind: $("kind-field").value,
    activation: $("activation-field").value,
    topics: $("topics").value,
    body: $("body").value,
  };
}

async function restoreVersion(id, versionId) {
  const response = await fetch(
    `/api/items/${encodeURIComponent(id)}/restore/${encodeURIComponent(versionId)}`,
    { method: "POST" }
  );
  const data = await response.json();
  if (!response.ok) {
    $("status").textContent = data.error || "Restore failed.";
    return;
  }
  await loadCatalog();
  showItem(data);
  $("status").textContent = "Restored " + versionId + ".";
}

$("editor").addEventListener("submit", async (event) => {
  event.preventDefault();
  $("status").textContent = "Saving…";
  const creating = state.creating || !state.selectedId;
  const url = creating ? "/api/items" : "/api/items/" + encodeURIComponent(state.selectedId);
  const response = await fetch(url, {
    method: creating ? "POST" : "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload()),
  });
  const data = await response.json();
  if (!response.ok) {
    $("status").textContent = data.error || "Save failed.";
    return;
  }
  await loadCatalog();
  showItem(data);
  const budget = data.budget;
  const warn = budget && budget.over_budget ? ` ${budget.repo} is over the always-on budget.` : "";
  $("status").textContent = "Saved." + warn;
});

$("new-item").addEventListener("click", () => {
  state.creating = true;
  state.selectedId = null;
  $("editor-title").textContent = "New directive";
  $("editor-meta").textContent = "Skills are the right home for procedures that are not needed on every turn.";
  $("title").value = "";
  $("repo-field").value = $("repo").value || "AlexTouvras/";
  $("kind-field").value = "skill";
  $("activation-field").value = "agent";
  $("topics").value = "";
  $("body").value = "";
  $("history").hidden = true;
  $("status").textContent = "";
  $("title").focus();
});

for (const id of ["q", "repo", "topic", "kind", "activation"]) {
  $(id).addEventListener("input", () => {
    state.hash = "";
    renderList();
  });
}

loadCatalog();
