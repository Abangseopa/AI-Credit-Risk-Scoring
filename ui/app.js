// Change this if your API runs elsewhere (e.g. Supabase Edge URL)
const API_BASE = (window.API_BASE || "").replace(/\/+$/,"") || "";

const form = document.getElementById("infoForm");
const loading = document.getElementById("loading");
const result = document.getElementById("result");
const scoreEl = document.getElementById("score");
const rationaleEl = document.getElementById("rationale");
const factorsEl = document.getElementById("factors");
const runAgain = document.getElementById("runAgain");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  result.classList.add("hidden");
  loading.classList.remove("hidden");

  // Basic metadata from the form; backend will read demo_payload.json
  const payload = Object.fromEntries(new FormData(form).entries());

  try {
    // 1) get score
    const sRes = await fetch(`${API_BASE}/score`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    if (!sRes.ok) throw new Error("Score request failed");
    const scoreData = await sRes.json();

    // 2) get factors
    const fRes = await fetch(`${API_BASE}/factors`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
    if (!fRes.ok) throw new Error("Factors request failed");
    const factors = await fRes.json();

    // Render
    scoreEl.textContent = Math.round(scoreData.score ?? 0);
    rationaleEl.textContent = scoreData.rationale || "AI assessment based on cash-flow features and alternative data.";
    factorsEl.innerHTML = "";
    (factors.items || []).forEach(f => {
      const pct = Math.max(0, Math.min(100, Math.round(f.score)));
      const node = document.createElement("div");
      node.className = "factor";
      node.innerHTML = `
        <h4>${f.name} <span class="muted">(${pct}/100)</span></h4>
        <div class="bar"><div class="fill" style="width:${pct}%;"></div></div>
        <p class="muted" style="margin:6px 0 0">${f.note || ""}</p>
      `;
      factorsEl.appendChild(node);
    });
  } catch (err) {
    alert(err.message || "Something went wrong.");
  } finally {
    loading.classList.add("hidden");
    result.classList.remove("hidden");
  }
});

runAgain.addEventListener("click", () => {
  result.classList.add("hidden");
  window.scrollTo({ top: 0, behavior: "smooth" });
});
