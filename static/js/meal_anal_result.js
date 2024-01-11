$(document).ready(function(){
    // remove_input 클래스가 부여된 버튼을 클릭했을 때
    $('#meal_result_form').on('click', '.remove_input', function(event) {
        // 해당 개체의 이전 값 input 태그를 지우고
        // 자기 자신도 지워버린다.
        $(this).prev('input').remove();
        $(this).remove();
    });

    // add_input_box 즉 '입력창 추가' 버튼을 클릭했을 때
    $('#add_input_box').on('click', function(event) {
        const last_input = $('#meal_result_form').find(':input:last');

        const add_input = $('<input>', {
            type: 'text',
            name: 'food_info[]'
        });

        const remove_btn = $('<button>', {
            class: 'remove_input',
            text: '입력창 삭제'
        });

        last_input.after(add_input, remove_btn);
    });

    $('#submit_form').on('click', function() {
        const form = $('#meal_result_form');
        const formData = form.serialize();
        const csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

        $.ajax({
            url: 'http://127.0.0.1:8000/meal/meal_to_analyze',
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