let chart = function (data1, data2, parent) {
    const margin = {
        top: 20,
        right: 30,
        bottom: 30,
        left: 40,
    };

    const width = 500 - margin.left - margin.right;
    const height = 500 - margin.top - margin.bottom;

    const x = d3.scale.ordinal()
        .rangeRoundBands([0, width], .1)
        .domain(function(d) {
            let ret = [];
            for (let i = 0; i < d.length; i++) {
                ret.push(i);
            }

            return ret;
        }(data1));

    const y = d3.scale.linear()
        .domain([0, Math.max(d3.max(data1), d3.max(data2))])
        .range([height, 0]);

    const xAxis = d3.svg.axis()
        .scale(x)
        .orient('bottom');

    const yAxis = d3.svg.axis()
        .scale(y)
        .orient('left');

    d3.select(parent).select('svg').remove();

    let chart = d3.select(parent).append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left}, ${margin.top})`);

    chart.append('g')
        .attr('class', 'axis xaxis')
        .attr('transform', `translate(0, ${height})`)
        .call(xAxis);

    chart.append('g')
        .attr('class', 'axis yaxis')
        .call(yAxis);

    let bar = chart.selectAll('.bar1')
        .data(data1)
        .enter();

    bar.append('rect')
        .attr('class', 'bar bar1')
        .attr('x', (d, i) => x(i))
        .attr('y', (d) => y(d))
        .attr('height', (d) => height - y(d))
        .attr('width', x.rangeBand() / 2);

    bar = chart.selectAll('.bar2')
        .data(data2)
        .enter();

    bar.append('rect')
        .attr('class', 'bar bar2')
        .attr('x', (d, i) => (x(i) + x.rangeBand() / 2))
        .attr('y', (d) => y(d))
        .attr('height', (d) => height - y(d))
        .attr('width', x.rangeBand() / 2);
};
