$(document).ready(function(){
    // 원래 숨겨져있는 #modify_result 항목을 표시하는 기능
    // 이 로직이 굳이 필요할까?
    // $('#deny-button').on('click', function(event) {
    //     $("#modify_result").css('display', 'block');
    // });

    // 팝업 테스트
    // 팝업은 디자인 측면에서 그리 좋지 못한 선택지 같다.
    // 유저 인터페이스 경험에서 많이 안 좋을 것이다.
    // function showSearchPop() {
    //     window.open("meal_index.html", "a", "width=400, height=300, left=100, top=50");
    // };

    // remove_input 클래스가 부여된 버튼을 클릭했을 때
    $('#meal_result_form').on('click', '.remove_input', function(event) {
        var inputBox = $(this).parent(".input_container");
        var input = $(this).prev('input');
        var markerId = input.data('marker-id');
        var searchUl = $(this).next('ul');
        console.log(markerId)
        var marker = $('#' + markerId);
        console.log(marker)
        // 해당 개체의 이전 값 input 태그를 지우고
        // 자기 자신도 지워버린다.
        input.remove();
        marker.remove();
        searchUl.remove();
        inputBox.remove();
        $(this).remove();
    });

    // add_input_box 즉 '입력창 추가' 버튼을 클릭했을 때
    $('#add_input_box').on('click', function(event) {
        const last_box = $('.input_container').last();
        console.log(last_box)

        // input을 하나 만든다
        const add_input = $('<input>', {
            type: 'text',
            name: 'noname',
            class: 'food-input',
            placeholder: '음식 검색',
        });

        // 결과창
        const newResultsContainer = $('<ul>', {
            class: 'search-results',
            style: 'display: none;',
        });

        // input을 없앨 수 있는 버튼
        const remove_btn = $('<button>', {
            class: 'remove_input greenBtn',
            text: '입력창 삭제'
        });

        const newContainer = $('<div>', {
            class: 'input_container'
        }).append(add_input, remove_btn, newResultsContainer);

        if (last_box.length > 0) {
            console.log(newContainer)
            last_box.after(newContainer);

        } else {
            let pBox = $('#not_detected');
            pBox.replaceWith(newContainer);

        }

    });

    $(document).on('input', '.food-input', function(){
        var searchWord = $(this).val();
        // console.log(searchWord)
        var resultContainer = $(this).siblings('.search-results');

        $.ajax({
            url: 'http://127.0.0.1:8000/meal/food_search',
            data: {"searchWord": searchWord},
            dataType: 'json',
            success: function(data){
                // console.log(data)
                resultContainer.empty();

                $.each(data.results, function(index, result) {
                    // console.log(result.food_code)
                    var resultItem = $('<li>' + result.name + " | " + result.maker + '</li>');

                    resultItem.click(function() {
                        var currentInput = $(this).closest('.input_container').find('.food-input');
                        currentInput.attr('name', result.food_code);
                        currentInput.val(result.name);
                    });

                    resultContainer.append(resultItem);
                });
            },
            error: function(error){
                console.error("알 수 없는 에러 발생", error)
            }
        })
    });

    // focus된 input창만 display: block 활성화
    $(document).on('focus', '.food-input', function(){
        $(this).siblings('.search-results').css('display', 'block');
    });

    // 벗어나면 다시 숨김
    $(document).on('click', function(event){
        if (!$(event.target).closest('.search-results').length && !$(event.target).hasClass('food-input')) {
        // if (!$(event.target).closest('.search-results').length) {
            $('.search-results').css('display', 'none');
        }
    });
});