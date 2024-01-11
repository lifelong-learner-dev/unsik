$(document).ready(function(){
    $('#meal_result_form').on('click', '.remove_input', function(event) {
        const inputContainer = $(event.target).parent();

        const csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

        $.ajax({
            url: 'http://127.0.0.1:8000/meal/meal_to_analyze',
            type: 'POST',
            data: {
                csrfmiddlewaretoken: csrf_token,
            },
            success: function(response) {
                inputContainer.remove();
            },
            error: function (error) {
                console.error('CSRF 토큰 오류 발생', error);
            }
        });
    });

    $('#add_input_box').on('click', function(event) {
        const last_input = $('#meal_result_form').find(':input:last');

        const add_input = $('<input>', {
            type: 'text',
            name: 'food_info'
        });

        const remove_btn = $('<button>', {
            class: 'remove_input',
            text: '입력창 삭제'
        });

        last_input.after(add_input, remove_btn);
    });
});