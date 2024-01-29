$(document).ready(function () {
    $("#predict-form").submit(function (e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/fitness_grade/female_adult_predict_ajax/',
            data: $(this).serialize(),

            success: function (response) {
                console.log(response.class_name);
                $("#prediction_result").text("예측 결과: " + response.class_name);
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
});