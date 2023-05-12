var ctx = document.getElementById('myChart')

const chart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
            label: 'Second set',
            backgroundColor: ['pink', 'grey', 'purple', 'red'],
            borderColor: ['orange', 'cyan', 'lightblue', 'bloodorange'],
            data: [15, 10, 7, 5, 13, 9],
            borderWidth: 1
        }]
    },
    option: {scales: {y: {beginAtZero: true}}}
});

var type = document.getElementById('type')
type.addEventListener('click', function() {changeType(this.value);})

// Takes in the type from html then change the chart according to that type
function changeType(updateType) {
    chart.config.type = updateType;
    chart.update();
}

