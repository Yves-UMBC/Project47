function addChart(canvasId, chartType, chartCrimeData) {
    var chartLabel = [];
    var chartData = [];
    fetch('/get_crime_data?param1=' + chartCrimeData)
        .then(response => response.json())
        .then(displayData => {
            chartLabel = displayData.dataLabels;
            chartData = displayData.dataCounts;

            var ctx = document.getElementById(canvasId);
            var chart = new Chart(ctx, {
                type: chartType,
                data: {
                    labels: chartLabel,
                    datasets: [{
                        label: 'Inner legend Labels',
                        backgroundColor: ['pink', 'grey', 'purple', 'red'],
                        borderColor: ['orange', 'cyan', 'lightblue', 'bloodorange'],
                        data: chartData,
                        borderWidth: 1
                    }]
                },
                options: {scales: {y: {beginAtZero: true}}}
            });
        })
        .catch(error => console.error(error));
}