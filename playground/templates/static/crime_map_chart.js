function addChart(canvasId, chartType, chartData) {
    var chartLabelList = [];
    var chartDataList = [];
    fetch('/get_crime_data?param1=' + chartData)
        .then(response => response.json())
        .then(displayData => {
            chartLabelList = displayData.dataLabels;
            chartDataList = displayData.dataCounts;

            var ctx = document.getElementById(canvasId);
            var chart = new Chart(ctx, {
                type: chartType,
                data: {
                    labels: chartLabelList,
                    datasets: [{
                        label: 'Inner legend Labels',
                        backgroundColor: ['pink', 'grey', 'purple', 'red'],
                        borderColor: ['orange', 'cyan', 'lightblue', 'bloodorange'],
                        data: chartDataList,
                        borderWidth: 1
                    }]
                },
                options: {scales: {y: {beginAtZero: true}}}
            });
        })
        .catch(error => console.error(error));
};
