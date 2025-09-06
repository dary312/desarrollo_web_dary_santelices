let maximoFotosExtra = 4;
let contadorFotos = 0;

const contenedorFotos = document.getElementById("contenedor_fotos");

const crearInputFoto = () => {

  if (contadorFotos >= maximoFotosExtra) return;

  const divFoto = document.createElement("div");
  divFoto.className = "foto-input";

  const input = document.createElement("input");
  input.type = "file";
  input.id = `foto_${contadorFotos}`;
  input.accept = "image/*";

  contadorFotos++;
  
  divFoto.appendChild(input);
  contenedorFotos.appendChild(divFoto);

};

let agregarFoto = document.getElementById("agregar_foto");
agregarFoto.addEventListener("click", crearInputFoto);