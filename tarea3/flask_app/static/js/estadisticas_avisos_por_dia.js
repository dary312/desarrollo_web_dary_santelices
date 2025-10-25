async function obtenerDatosLineas(
  url = "http://127.0.0.1:5000/estadisticas/avisos_por_dia"
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
    console.error(
      "There has been a problem with your fetch operation:",
      error
    );
  }
}

function procesarDatosLineas(datos) {
  if (!Array.isArray(datos)) {
    console.warn("Expected an array of data; received:", datos);
    return [];
  }

  const datosOrdenados = [...datos].sort((a, b) => a.fecha.localeCompare(b.fecha));

  const puntos = datosOrdenados.map((registro) => {
    const { fecha, cantidad } = registro;
    const [year, month, day] = fecha.split("-").map(Number);

    const timestamp = Date.UTC(year, month - 1, day);
    const value = Number(cantidad) || 0;

    return [timestamp, value];
  });

  return puntos;
}

async function crearGraficoLinea() {
  try {
    const datos = await obtenerDatosLineas
  ();
    const serie = procesarDatosLineas(datos || []);

    Highcharts.chart("linea", {
      chart: {
        type: "line",
      },
      title: {
        text: "Avisos de adopción por día",
      },
      xAxis: {
        type: "datetime",
        title: {
          text: "Fecha",
        },
      },
      yAxis: {
        title: {
          text: "Cantidad de avisos",
        },
        allowDecimals: false,
        min: 0,
      },
      tooltip: {
        xDateFormat: "%d/%m/%Y",
        shared: true,
      },
      series: [
        {
          name: "Avisos",
          data: serie,
          color: "#2E86DE",
          lineWidth: 1,
          marker: {
            enabled: true,
            radius: 4,
          },
        },
      ],
      legend: {
        enabled: true,
      },
      credits: { enabled: false },
      responsive: {
        rules: [
          {
            condition: {
              maxWidth: 500,
            },
            chartOptions: {
              legend: {
                layout: "horizontal",
                align: "center",
                verticalAlign: "bottom",
              },
            },
          },
        ],
      },
    });
  } catch (error) {
    console.error("Failed to render the chart:", error);
    document.getElementById("linea").innerHTML =
      '<p style="color:red;">No se pudieron cargar los datos.</p>';
  }
}

crearGraficoLinea();
