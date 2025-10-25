async function enviarComentario(url, payload) {
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json"
      },
      cache: "no-store",
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    return await response.json();
  } catch (error) {
    console.error("There has been a problem with your fetch operation:", error);
  }
}

function procesarRespuestaComentario(data) {
  if (!data) {
    console.warn("Expected a JSON response; received:", data);
    mostrarErrorComentario("Error inesperado. Intente nuevamente.");
    return;
  }

  if (data.ok === false) {
    const mensaje = Array.isArray(data.errores) && data.errores.length > 0
      ? data.errores.join(" ")
      : "No se pudo enviar el comentario.";
    mostrarErrorComentario(mensaje);
    return;
  }

  if (data.ok === true && data.comentario) {
    ocultarErrorComentario();

    const form = document.getElementById("form_comentario");
    if (form) form.reset();

    const avisoId = document.getElementById("comentario_aviso_id")?.value;
    if (avisoId && typeof cargarComentariosParaAviso === "function") {
      cargarComentariosParaAviso(avisoId);
    }
    alert("¡Comentario agregado con éxito!");
  }
}

function mostrarErrorComentario(mensaje) {
  const errorBox = document.getElementById("form_comentario_error");
  if (!errorBox) return;
  errorBox.textContent = mensaje;
  errorBox.style.display = "block";
}

function ocultarErrorComentario() {
  const errorBox = document.getElementById("form_comentario_error");
  if (!errorBox) return;
  errorBox.textContent = "";
  errorBox.style.display = "none";
}

function inicializarFormularioComentario() {
  const form = document.getElementById("form_comentario");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    const avisoId = document.getElementById("comentario_aviso_id")?.value || "";
    const nombre  = (document.getElementById("c_nombre")?.value || "").trim();
    const texto   = (document.getElementById("c_texto")?.value  || "").trim();

    if (!avisoId) {
      mostrarErrorComentario("No se encontró el aviso asociado.");
      return;
    }

    ocultarErrorComentario();

    const url = `/api/avisos/${avisoId}/comentarios`;
    const payload = { nombre, texto };

    const data = await enviarComentario(url, payload);
    procesarRespuestaComentario(data);
  });
}

document.addEventListener("DOMContentLoaded", inicializarFormularioComentario);
