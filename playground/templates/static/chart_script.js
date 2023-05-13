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
type.addEventListener('click', function() {changeType(this.value);})

function changeType(updateType) {       
    chart.config.type = updateType;      
    chart.update();
}

var data1 = document.getElementById('dataOne');
data1.addEventListener('click', function() {changeData(this.value);})

function changeData(updateData) {
    if (updateData == 'income') {
        chart.config.data.labels = ["$10k", "$20k", "$34k", "$50k"];
    }else if (updateData == 'weapon') {
        chart.config.data.labels = ["Guns", "Whip", "Sword", "Knife"];
    }else if (updateData == 'neighborhood') {
        chart.config.data.labels = ["Ellicot City", "Miami", "Leola", "Catonsville"];
    }
    chart.update();
}



