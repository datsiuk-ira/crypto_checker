document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('cryptoChart').getContext('2d');
    ctx.canvas.width = 1000;
    ctx.canvas.height = 430;

    const candlestickData = historicalData.map(d => ({
        x: new Date(d[0]).getTime(),
        o: parseFloat(d[1]), // Open price
        h: parseFloat(d[2]), // High price
        l: parseFloat(d[3]), // Low price
        c: parseFloat(d[4])  // Close price
    }));

    const arimaPrediction = arimaData.map(d => ({
        x: new Date(d.timestamp).getTime(),
        y: parseFloat(d.forecast)
    }));

    const cryptoChart = new Chart(ctx, {
        type: 'candlestick',
        data: {
            datasets: [
                {
                    label: "Обрана криптопара",
                    data: candlestickData,
                    color: {
                        up: '#42f584',
                        down: '#f75464',
                        unchanged: '#999',
                    },
                },
                {
                    label: "Прогноз моделі ARIMA",
                    data: arimaPrediction,
                    type: 'line',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 2,
                    pointRadius: 0,
                    fill: false,
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'minute',
                        tooltipFormat: 'll HH:mm',
                        displayFormats: {
                            minute: 'HH:mm'
                        }
                    },
                    title: {
                        display: true,
                        text: 'Час'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Ціна (USDT)'
                    }
                }
            },
            plugins: {
                tooltip: {
                    mode: 'nearest',
                    intersect: false,
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleFont: {
                        weight: 'bold'
                    },
                    bodySpacing: 5,
                    padding: 15,
                    displayColors: false,
                    callbacks: {
                        title: function(tooltipItems) {
                            const date = new Date(tooltipItems[0].parsed.x);
                            return `Date: ${date.toLocaleString()}`;
                        },
                        label: function(context) {
                            if (context.dataset.label === "BTC/USDT") {
                                const { o, h, l, c } = context.raw;
                                return [`Open: ${o.toFixed(2)}`, `High: ${h.toFixed(2)}`, `Low: ${l.toFixed(2)}`, `Close: ${c.toFixed(2)}`];
                            } else {
                                return `ARIMA Prediction: ${context.raw.y.toFixed(2)}`;
                            }
                        }
                    }
                },
                legend: {
                    display: true,
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Свічковий графік аналізу',
                    font: {
                        size: 24
                    },
                    padding: 20
                }
            }
        }
    });
});
