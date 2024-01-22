$(document).ready(function () {

    var ctx = document.getElementById('caloriesChart');

    var chart = new Chart(ctx, {
        type: 'bar', // 라인 차트 유형
        data: {
            labels: dates, // x축 레이블로 날짜 사용
            datasets: [{
                label: '칼로리', // 데이터셋의 레이블
                backgroundColor: 'rgba(255, 99, 132, 0.2)', // 그래프 내부 색
                borderColor: 'rgba(255, 99, 132, 1)', // 선 색
                borderWidth: 1,
                data: calories, // y축 데이터로 칼로리 사용
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true // y축을 0부터 시작
                }
            },
            responsive: true,
            maintainAspectRatio: false,
            onClick: function (e) {
                var activePoints = chart.getElementsAtEventForMode(e, 'nearest', { intersect: true }, true);

                if (activePoints.length) {
                    var firstPoint = activePoints[0];
                    var label = chart.data.labels[firstPoint.index];
                    console.log('label ', label)
                    // 새 창에서 상세 정보 페이지
                    window.open('/meal/meal_detail/' + label, '_blank', 'width=800,height=600,top=100,left=100');
                }
            }
        }
    });

})