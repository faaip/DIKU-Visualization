function createPieChart(query) {
    var width = 200;
    var height = 200;
    var padding = 10;
    var opacity = .8;
    var opacityHover = 1;
    var otherOpacityOnHover = .8;
    var tooltipMargin = 13;

    var radius = Math.min(width - padding, height - padding) / 2;
    var color = d3.scaleOrdinal(d3.schemeCategory10);

    // document.getElementById("pieSpinner").outerHTML = "";
    $(".loader").remove();
    document.getElementById("piechart").innerHTML = "";
    var data = getCounts(query);

    var totalCount = 0;
    var totalDuration = 0;

    data = $.map(data, function (item, key) {
        var checkBox = document.getElementById(key);
        if (checkBox.checked == false) {
            return null;
        } else {
            totalCount += item.count;
            totalDuration += item.durationHour;
            item.name = key;
        }
        return item;
    });

    console.log(data)

    var svg = d3.select("#piechart")
        .append('svg')
        .attr('class', 'pie')
        .attr('width', width)
        .attr('height', height)


    var g = svg.append('g')
        .attr('transform', 'translate(' + (width / 2) + ',' + (height / 2) + ')');

    var arc = d3.arc()
        .innerRadius(0)
        .outerRadius(radius);

    var pie = d3.pie()
        .value(function (d) {
            return d.durationHour;
        })
        .sort(null);

    var path = g.selectAll('path')
        .data(pie(data))
        .enter()
        .append("g")
        .append('path')
        .attr('d', arc)
        .attr('fill', (d, i) => color(i))
        .style('opacity', opacity)
        .style('stroke', 'white')
        .on("mouseover", function (d) {
            d3.selectAll('path')
                .style("opacity", otherOpacityOnHover);
            d3.select(this)
                .style("opacity", opacityHover);

            let g = d3.select("svg")
                .style("cursor", "pointer")
                .append("g")
                .attr("class", "tooltip")
                .style("opacity", 0);

            g.append("text")
                .attr("class", "name-text")
                .text(`${getActivityString(d.data.name)} ${(d.data.durationHour/totalDuration*100).toFixed(2)} %`)
                .attr('text-anchor', 'middle');

            let text = g.select("text");
            let bbox = text.node().getBBox();
            let padding = 2;
            g.insert("rect", "text")
                .attr("x", bbox.x - padding)
                .attr("y", bbox.y - padding)
                .attr("width", bbox.width + (padding * 2))
                .attr("height", bbox.height + (padding * 2))
                .style("fill", "white")
                .style("opacity", 0.75);
        })
        .on("mousemove", function (d) {
            let mousePosition = d3.mouse(this);
            let x = mousePosition[0] + width / 2;
            let y = mousePosition[1] + height / 2 - tooltipMargin;

            let text = d3.select('.tooltip text');
            let bbox = text.node().getBBox();
            if (x - bbox.width / 2 < 0) {
                x = bbox.width / 2;
            } else if (width - x - bbox.width / 2 < 0) {
                x = width - bbox.width / 2;
            }

            if (y - bbox.height / 2 < 0) {
                y = bbox.height + tooltipMargin * 2;
            } else if (height - y - bbox.height / 2 < 0) {
                y = height - bbox.height / 2;
            }

            d3.select('.tooltip')
                .style("opacity", 1)
                .attr('transform', `translate(${x}, ${y})`);
        })
        .on("mouseout", function (d) {
            d3.select("svg")
                .style("cursor", "none")
                .select(".tooltip").remove();
            d3.selectAll('path')
                .style("opacity", opacity);
        })
        .on("touchstart", function (d) {
            d3.select("svg")
                .style("cursor", "none");
        })
        .each(function (d, i) {
            this._current = i;
        });

    let legend = d3.select("#piechart").append('div')
        .attr('class', 'legend')
        .style('margin-top', '30px');

    let keys = legend.selectAll('.key')
        .data(data)
        .enter().append('div')
        .attr('class', 'key')
        .style('display', 'flex')
        .style('align-items', 'center')
        .style('margin-right', '20px');

    keys.append('div')
        .attr('class', 'symbol')
        .style('height', '10px')
        .style('width', '10px')
        .style('margin', '5px 5px')
        .style('background-color', (d, i) => color(i));

    keys.append('div')
        .attr('class', 'name')
        .text(d => `${getActivityString(d.name)} ${d.durationHour.toFixed(1)}  hours`);

    legend.append('div')
        .attr('class', 'name')
        .style('margin', '5px 5px')
        .text("Total duration: " + parseInt(totalDuration) + " hours");

    keys.exit().remove();
}

function pieLoader() {
    document.getElementById("piechart").innerHTML = "";
    var element = document.createElement('div');
    element.className = 'loader';
    element.id = 'pieSpinner';
    document.getElementById('rightControls').appendChild(element);
}