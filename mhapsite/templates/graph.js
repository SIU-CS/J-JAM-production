($document).ready(function() {
    // Load the Visualization API and the corechart package.
    google.charts.load('current', {'packages':['corechart']});

    // Set a callback to run when the Google Visualization API is loaded.
    google.charts.setOnLoadCallback(drawChart);

    // Callback that creates and populates a data table,
    // instantiates the pie chart, passes in the data and
    // draws it.
    function drawChart() {
        // Create the data table.
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Posts');
        data.addColumn('number', 'Happiness');
        data.addRows({{data|safe}});

        var options = {
            'title': 'Mental Health Visual Representation',
            'hAxis': {
                'minValue': 0,
                'maxValue': 1
            }
        };

        // Instantiate and draw our chart, passing in some options.
        var chart = new google.visualization.BarChart(document.getElementById('chart_div'));
        google.visualization.events.addListener(chart, 'select', selectHandler); 

        function selectHandler(e) {
            var postIndex = link[0].row;
            alert(postIndex);
            var slug = data_slugs[postIndex];
            alert(slug);
        }
        chart.draw(data, options);
    }
});
