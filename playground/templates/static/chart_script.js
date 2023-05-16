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

// Dynamically updating the chart type
var type = document.getElementById('type');
type.addEventListener('change', function() {changeType(this.value);})

function changeType(updateType) {    
    chart.config.type = updateType;      
    chart.update();
}

var data1 = document.getElementById('dataOne');
data1.addEventListener('change', function() {changeData(this.value);})

function changeData(updateData) {
    if (updateData == 'income') {
        chart.data.labels = ["$10k", "$20k", "$30k", "$40k"];
    }else if (updateData == 'weapon') {
        fetch('/get_crime_data?param1=' + updateData)
            .then(response => response.json())
            .then(weaponData => {
                chart.data.labels = weaponData.weaponLabels;
                chart.data.datasets[0].data = weaponData.weaponCounts;
                chart.update();
            })
            .catch(error => console.error(error));
    }else if (updateData == 'neighborhood') {
        fetch('/get_crime_data?param1=' + updateData)
            .then(response => response.json())
            .then(weaponData => {
                chart.data.labels = weaponData.weaponLabels;
                chart.data.datasets[0].data = weaponData.weaponCounts;
                chart.update();
            })
            .catch(error => console.error(error));
    }
    chart.update();
}




