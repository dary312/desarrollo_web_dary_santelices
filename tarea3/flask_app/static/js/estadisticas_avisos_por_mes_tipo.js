async function obtenerDatosBarras(
  url = "http://127.0.0.1:5000/estadisticas/avisos_por_mes_tipo"
) {
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
    console.error("Error al obtener los datos:", error);
  }
}

function procesarDatosBarras(datos) {
  if (!Array.isArray(datos)) {
    console.warn("Expected an array of data; received:", datos);
    return { meses: [], perros: [], gatos: [] };
  }

  const meses = datos.map((dato) => dato.mes);
  const cantidadPerros = datos.map((dato) => dato.perro);
  const cantidadGatos = datos.map((dato) => dato.gato);

  return {
    meses,
    perros: cantidadPerros,
    gatos: cantidadGatos,
  };
}


async function crearGraficoBarras() {
  try {
    const datos = await obtenerDatosBarras();
    const { meses, perros, gatos } = procesarDatosBarras(datos || []);

    Highcharts.chart("barra", {
      chart: {
        type: "column",
      },
      title: {
        text: "Avisos por mes y tipo",
      },
      xAxis: {
        categories: meses,
        title: {
          text: "Mes",
        },
        crosshair: true,
      },
      yAxis: {
        min: 0,
        title: {
          text: "Cantidad de avisos",
        },
        allowDecimals: false,
      },
      tooltip: {
        shared: true,
        headerFormat: "<b>{point.key}</b><br/>",
      },
      plotOptions: {
        column: {
          grouping: true,
          shadow: false,
          borderWidth: 0,
        },
      },
      series: [
        {
          name: "Perros",
          data: perros,
          color: "#2E86DE",
        },
        {
          name: "Gatos",
          data: gatos,
          color: "#525151db",
        },
      ],
      credits: { enabled: false },
    });
  } catch (error) {
    console.error("Failed to render the chart:", error);
    document.getElementById("barra").innerHTML =
      '<p style="color:red;">No se pudieron cargar los datos.</p>';
  }
}

crearGraficoBarras();
