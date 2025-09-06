const avisos = [
  {
    fecha_publicacion: "2025-04-05 10:00",
    region: "Metropolitana",
    comuna: "Santiago",
    sector: "Centro",
    nombre: "Ana Pérez",
    email: "ana@example.com",
    telefono: "+569.12345678",
    contacto: "Instagram: @adopciones_santiago",
    tipo: "Gato",
    cantidad: 1,
    edad: 2,
    medida: "Años",
    fecha_entrega: "2025-04-10 12:00",
    descripcion: "Gatita muy cariñosa y tranquila, esterilizada y con vacunas al día. Ideal para departamento.",
    fotos: ["../fotos/1.png", "../fotos/2.png"]
  },
  {
    fecha_publicacion: "2025-04-06 14:30",
    region: "Metropolitana",
    comuna: "Providencia",
    sector: "Barrio Italia",
    nombre: "Juan Soto",
    email: "juan@example.com",
    telefono: "+569.87654321",
    contacto: "Twitter: @perros_provi",
    tipo: "Perro",
    cantidad: 1,
    edad: 8,
    medida: "Meses",
    fecha_entrega: "2025-04-11 17:00",
    descripcion: "Cachorro mestizo muy juguetón y sociable, necesita espacio para correr. Vacunas al día.",
    fotos: ["../fotos/3.png"]
  },
  {
    fecha_publicacion: "2025-04-07 09:15",
    region: "Metropolitana",
    comuna: "Ñuñoa",
    sector: "Villa Frei",
    nombre: "Laura Campos",
    email: "laura@example.com",
    telefono: "+569.11112222",
    contacto: "Instagram: @adopta_nunoa",
    tipo: "Gato",
    cantidad: 2,
    edad: 6,
    medida: "Meses",
    fecha_entrega: "2025-04-12 13:30",
    descripcion: "Dos gatitos hermanos muy juguetones y curiosos, se entregan juntos. Ya comen solitos.",
    fotos: ["../fotos/4.png", "../fotos/5.png"]
  },
  {
    fecha_publicacion: "2025-04-09 11:20",
    region: "Metropolitana",
    comuna: "Las Condes",
    sector: "El Golf",
    nombre: "María López",
    email: "maria@example.com",
    telefono: "+569.55556666",
    contacto: "Twitter: @adopta_lc",
    tipo: "Gato",
    cantidad: 1,
    edad: 1,
    medida: "Años",
    fecha_entrega: "2025-04-14 16:00",
    descripcion: "Gato joven muy curioso y juguetón, acostumbrado a estar en interiores. Esterilizado.",
    fotos: ["../fotos/7.png"]
  },
  {
    fecha_publicacion: "2025-04-10 08:50",
    region: "Valparaíso",
    comuna: "Viña del Mar",
    sector: "Reñaca",
    nombre: "Pedro González",
    email: "pedro@example.com",
    telefono: "+569.77778888",
    contacto: "Instagram: @adopcionesvina",
    tipo: "Perro",
    cantidad: 1,
    edad: 5,
    medida: "Años",
    fecha_entrega: "2025-04-15 11:00",
    descripcion: "Perro grande muy protector y noble, ideal para casa con patio. Tiene chip y vacunas al día.",
    fotos: ["../fotos/8.png", "../fotos/9.png"]
  }
];



  
const cargarListado = () => {
    const tbody = document.getElementById("tabla_avisos");
    avisos.forEach((av, index) => {
      const fila = document.createElement("tr");
      fila.innerHTML = `
          <td>${av.fecha_publicacion}</td>
          <td>${av.fecha_entrega}</td>
          <td>${av.comuna}</td>
          <td>${av.sector}</td>
          <td>${av.cantidad} ${av.tipo}, ${av.edad} ${av.medida}</td>
          <td>${av.nombre}</td>
          <td>${av.fotos.length}</td>
      `;
      fila.addEventListener("click",() => mostrarDetalle(index));
      tbody.appendChild(fila);
    });
}

const ampliarFoto = (src) => {
  const modal = document.createElement("div");
  modal.style.position = "fixed";
  modal.style.top = "0";
  modal.style.left = "0";
  modal.style.width = "100%";
  modal.style.height = "100%";
  modal.style.backgroundColor = "rgba(0,0,0,0.7)";
  modal.style.display = "flex";
  modal.style.justifyContent = "center";
  modal.style.alignItems = "center";
  modal.style.zIndex = "1000";
  modal.style.cursor = "pointer";


  const img = document.createElement("img");
  img.src = src;
  img.width = 800;
  img.height = 600;


  modal.addEventListener("click", () => {
    document.body.removeChild(modal);
  });

  modal.appendChild(img);
  document.body.appendChild(modal);
};

const mostrarDetalle = (index) => {
  const av = avisos[index];
  document.getElementById("detalle_fecha_publicacion").textContent = av.fecha_publicacion;
  document.getElementById("detalle_region").textContent = av.region;
  document.getElementById("detalle_comuna").textContent = av.comuna;
  document.getElementById("detalle_sector").textContent = av.sector;
  document.getElementById("detalle_nombre").textContent = av.nombre;
  document.getElementById("detalle_email").textContent = av.email;
  document.getElementById("detalle_telefono").textContent = av.telefono;
  document.getElementById("detalle_contacto").textContent = av.contacto;
  document.getElementById("detalle_animales").textContent = `${av.cantidad} ${av.tipo}, ${av.edad} ${av.medida}`;
  document.getElementById("detalle_fecha").textContent = av.fecha_entrega;
  document.getElementById("detalle_descripcion").textContent = av.descripcion;


  const fotosDiv = document.getElementById("detalle_fotos");
  fotosDiv.innerHTML = "";
  av.fotos.forEach(foto => {
    const img = document.createElement("img");
    img.src = foto;
    img.width = 320;
    img.height = 240;
    img.style.cursor = "pointer";
    img.addEventListener("click", () => ampliarFoto(foto));
    fotosDiv.appendChild(img);
  });

  document.getElementById("listado").style.display = "none";
  document.getElementById("detalle").style.display = "block";
  document.getElementById("boton_portada").style.display = "none";
}

const mostrarListado = () => {
  document.getElementById("detalle").style.display = "none";
  document.getElementById("listado").style.display = "block";
  document.getElementById("boton_portada").style.display = "block";
} 


document.addEventListener("DOMContentLoaded", cargarListado);

document.getElementById("portada_button").addEventListener("click", function() {
    window.location.href = "../html/portada.html";
});