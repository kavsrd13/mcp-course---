import { App } from "@modelcontextprotocol/ext-apps";

const root = document.querySelector<HTMLElement>("#widget")!;
const app = new App({ name: "Classroom Widgets", version: "1.0.0" });

app.ontoolresult = (result) => {
  const data = result.structuredContent as any;
  if (!data) return;

  if (data.widget === "time") {
    root.innerHTML = `<h2>${data.title}</h2><div class="value">${data.value}</div>`;
  }

  if (data.widget === "weather") {
    root.innerHTML = `
      <h2>${data.title}</h2>
      <div class="value">${data.temperature} C</div>
      <p>Wind: ${data.wind} km/h</p>`;
  }

  if (data.widget === "calendar") {
    const count = new Date(data.year, data.month, 0).getDate();
    const start = new Date(data.year, data.month - 1, 1).getDay();
    const cells = [
      ...Array(start).fill(""),
      ...Array.from({ length: count }, (_, i) => i + 1),
    ];
    root.innerHTML = `
      <h2>${data.title}</h2>
      <div class="days">${cells.map((day) => `<div class="day">${day}</div>`).join("")}</div>`;
  }
};

app.connect();

