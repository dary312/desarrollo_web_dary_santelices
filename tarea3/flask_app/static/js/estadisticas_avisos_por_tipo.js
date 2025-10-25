async function obtenerDatosTorta(
  url = "http://127.0.0.1:5000/estadisticas/avisos_por_tipo"
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


function procesarDatosTorta(datos) {
  if (!Array.isArray(datos)) {
    console.warn("Expected an array of data; received:", datos);
    return [];
  }

  const nombresBonitos = {
    perro: "Perro",
    gato: "Gato",
  };

  const datosProcesados = datos.map((registro) => {
    const { tipo, cantidad } = registro;

    const tipoNormalizado = String(tipo).toLowerCase();
    const nombre = nombresBonitos[tipoNormalizado] || String(tipo);

    const valor = Number(cantidad) || 0;

    return { name: nombre, y: valor };
  });

  return datosProcesados;
}
async function crearGraficoTorta() {
  try {
    const datos = await obtenerDatosTorta();
    const seriePie = procesarDatosTorta
(datos || []);

    Highcharts.chart('torta', {
      chart: { type: 'pie' },
      title: { text: 'Distribución de avisos por tipo' },
      tooltip: { pointFormat: '<b>{point.percentage:.1f}%</b> ({point.y} avisos)' },

      plotOptions: {
        pie: {
          allowPointSelect: true,
          cursor: 'pointer',
          dataLabels: { enabled: true, format: '{point.name}: {point.y}' },
          showInLegend: true
        }
      },
      series: [{
        name: 'Tipo',
        data: seriePie
      }],
      legend: { enabled: true },
      credits: { enabled: false },
      responsive: {
        rules: [{
          condition: { maxWidth: 500 },
          chartOptions: {
            legend: { layout: 'horizontal', align: 'center', verticalAlign: 'bottom' }
          }
        }]
      }
    });
  } catch (error) {
    console.error("Failed to render the chart:", error);
    document.getElementById('torta').innerHTML =
      '<p style="color:red;">No se pudieron cargar los datos.</p>';
  }
}

crearGraficoTorta();
