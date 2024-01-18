$(document).ready(function(){
    // 일반적으로 Django에서 csrf_token의 추적을 받지 않는 입력창이 임의로 추가되면
    // Django에서 csrf 보안 경고를 날린다. 때문에 새로 추가된 input 박스도
    // csrf의 관리 하에 들어가게 만들어야 한다.

    $('#submit_form').on('click', function(event) {
        event.preventDefault();

        const form = $('#meal_result_form');
        const formData = form.serialize();

        console.log(formData)

        const csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

        $.ajax({
            url: 'http://127.0.0.1:8000/meal/meal_post',
            type: 'POST',
            data: formData + '&csrfmiddlewaretoken=' + csrf_token,
            contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
            processData: false,
            success: function(response) {
                console.log('성공', response)
            },
            error: function (error) {
                console.error('CSRF 토큰 오류 발생', error);
            }
        });
    });
});