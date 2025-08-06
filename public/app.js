
async function fetchStatus() {
  const res = await fetch("/api/status");
  const data = await res.json();
  document.getElementById("status-box").innerText = `结构: ${data.structure}, 打分: ${data.score}, 操作: ${data.action}`;
  const tbody = document.getElementById("trades-body");
  tbody.innerHTML = "";
  data.trades.forEach(t => {
    const row = `<tr><td>${t.time}</td><td>${t.direction}</td><td>${t.score}</td><td>${t.hit}</td><td>${t.profit}</td></tr>`;
    tbody.innerHTML += row;
  });
  const ctx = document.getElementById("winrate-chart").getContext("2d");
  new Chart(ctx, {
    type: "line",
    data: {
      labels: data.winrate_history.map((_, i) => i + 1),
      datasets: [{
        label: "胜率变化(%)",
        data: data.winrate_history
      }]
    }
  });
}
fetchStatus();
