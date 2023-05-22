// Create a chart with dummy data for preview on visual_option.html
var ctx = document.getElementById('myChart')
const chart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green'],
        datasets: [{
            label: 'Inner legend Labels',
            backgroundColor: ['pink', 'grey', 'purple', 'red'],
            borderColor: ['orange', 'cyan', 'lightblue', 'bloodorange'],
            data: [15, 10, 7, 5, 13, 9],
            borderWidth: 1
        }]
    },
    option: {scales: {y: {beginAtZero: true}}}
});

// Dynamically updating the chart type for the preview chart on visual_option.html
var type = document.getElementById('chart-type');
type.addEventListener('change', function() {changeType(this.value);})

function changeType(updateType) {    
    chart.config.type = updateType;      
    chart.update();
}

// initializing the data
const CRIME_DATA = ['description', 'crimecode', 'neighborhood', 'weapon'];
const NEIGHBORHOOD_DATA = ['hfai', 'median_income'];

// Dynamically updating the chart data and label for the preview chart on visual_option.html
var data1 = document.getElementById('chart-data');
data1.addEventListener('change', function() {changeData(this.value);})

function changeData(updateData) {
    if (CRIME_DATA.includes(updateData)) {
        fetch('/get_crime_data?param1=' + updateData)
            .then(response => response.json())
            .then(displayData => {
                chart.data.labels = displayData.dataLabels;
                chart.data.datasets[0].label = updateData;
                chart.data.datasets[0].data = displayData.dataCounts;
                chart.update();
            })
            .catch(error => console.error(error));
    } else if (NEIGHBORHOOD_DATA.includes(updateData)){
        fetch ('/get_neighborhood_data?param1=' + updateData)
            .then(response => response.json())
            .then(displayData => {
                chart.data.labels = displayData.dataLabels;
                chart.data.datasets[0].label = updateData;
                chart.data.datasets[0].data = displayData.dataCounts;
                chart.update();
            })
            .catch(error => console.error(error));
    }
}

// This event listener prevent the adding the default option select from sending a post request to the main page
document.addEventListener('DOMContentLoaded', function() {
    var chartTypeSelect = document.getElementById('chart-type');
    var chartDataSelect = document.getElementById('chart-data');
    var addButton = document.querySelector('.add-chart-button button');

    addButton.addEventListener('click', function(event) {
        if (chartTypeSelect.value === 'Choose a Chart Type' || chartDataSelect.value === 'Choose Chart Datas') {
            event.preventDefault(); // Prevent the form from submitting
            alert('Please select a valid chart type and chart data.');
        }
    });
});
