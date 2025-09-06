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



const goToAgregar = () =>{
    window.location.href = "../html/agregar_aviso.html";
} 

const goToLista = () =>{
    window.location.href = "../html/lista_avisos.html";
} 

const goToEstadisticas = () =>{
    window.location.href = "../html/estadisticas.html";
} 


const agregarBtn = document.getElementById("btn_agregar");
agregarBtn.addEventListener("click", goToAgregar);


const listaBtn = document.getElementById("btn_lista");
listaBtn.addEventListener("click", goToLista);

const estadisticasBtn = document.getElementById("btn_estadisticas");
estadisticasBtn.addEventListener("click", goToEstadisticas);


const cargarUltimosAvisos = () => {
    const tbody = document.querySelector("table tbody");

    const ultimos = avisos.slice(-5);

    ultimos.forEach(av => {
        const fila = document.createElement("tr");
        fila.innerHTML = `
            <td>${av.fecha_publicacion}</td>
            <td>${av.comuna}</td>
            <td>${av.sector}</td>
            <td>${av.cantidad} ${av.tipo}, ${av.edad} ${av.medida}</td>
            <td><img src="${av.fotos[0]}" width="80"></td>
        `;
        tbody.appendChild(fila);
    });
};
document.addEventListener("DOMContentLoaded", () => {
    cargarUltimosAvisos();
});