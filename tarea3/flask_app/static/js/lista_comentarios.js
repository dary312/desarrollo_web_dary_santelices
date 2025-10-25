async function obtenerComentarios(url) {
  try {
    const response = await fetch(url, {
      method: "GET",
      headers: { "Accept": "application/json" },
      cache: "no-store"
    });

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return await response.json();
  } catch (error) {
    console.error("Error al obtener comentarios:", error);
  }
}

function renderComentariosLista(data) {
  const cont = document.getElementById("comentarios_list");
  if (!cont) return;

  cont.innerHTML = "";

  if (!data || data.ok === false) {
    cont.innerHTML = '<p class="muted">No se pudieron cargar los comentarios.</p>';
    return;
  }

  const comentarios = Array.isArray(data.comentarios) ? data.comentarios : [];
  if (comentarios.length === 0) {
    cont.innerHTML = '<p class="muted">Aún no hay comentarios.</p>';
    return;
  }

  const frag = document.createDocumentFragment();

  comentarios.forEach((c) => {
    const card = document.createElement("div");
    card.className = "comentario_item";
    card.innerHTML = `
      <div class="comentario_header">
        <strong class="comentario_nombre">${c.html?.nombre || ""}</strong>
        <span class="comentario_fecha">${c.fecha || ""}</span>
      </div>
      <p class="comentario_texto">${c.html?.texto || ""}</p>
    `;
    frag.appendChild(card);
  });

  cont.appendChild(frag);
}

function cargarComentariosParaAviso(avisoId) {
  const form = document.getElementById("form_comentario");
  if (form) form.reset();

  const errorBox = document.getElementById("form_comentario_error");
  if (errorBox) { errorBox.textContent = ""; errorBox.style.display = "none"; }

  const url = `/api/avisos/${avisoId}/comentarios`;
  obtenerComentarios(url).then(renderComentariosLista);
}

window.cargarComentariosParaAviso = cargarComentariosParaAviso;
