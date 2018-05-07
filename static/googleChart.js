<script type="text/javascript">
                // Load google charts
                google.charts.load('current', {'packages': ['corechart']});
                google.charts.setOnLoadCallback(drawChart);

                // Draw the chart and set the chart values
                function drawChart() {
                    var data = google.visualization.arrayToDataTable([
                        ['Estatus', 'Cantidad de compras'],
                        ['Completadas', {{ complete  }}],
                        ['Pendientes', {{ pending }}],
                        ['Sin Enviar', {{ unshipped }}],
                        ['Canceladas', {{ canceled }}]
                    ]);

                    // Optional; add a title and set the width and height of the chart
                    var options = {'title': 'Estatus de Compras', 'width': 400, 'height': 300};

                    // Display the chart inside the <div> element with id="piechart"
                    var chart = new google.visualization.PieChart(document.getElementById('piechart'));
                    chart.draw(data, options);
                }
            </script>