$(document).ready(function () {
    const slideList = document.querySelector('.slide_list');
    const slideContents = document.querySelectorAll('.slide_content');
    const slideBtnNext = document.querySelector('.slide_btn_next');
    const slideBtnPrev = document.querySelector('.slide_btn_prev');
    const pagination = document.querySelector('.slide_pagination');
    const slideLen = slideContents.length;
    const slideWidth = 1200; // 슬라이드 너비 조절하려면 여기서
    const slideSpeed = 600; // 슬라이드 넘어가는 속도
    const startNum = 0; // 시작 인덱스
    
    slideList.style.width = slideWidth * (slideLen + 2) + "px";
    
    // 만약 슬라이드가 끝부분에 다다랐다면 복붙
    let firstChild = slideList.firstElementChild;
    let lastChild = slideList.lastElementChild;
    let clonedFirst = firstChild.cloneNode(true);
    let clonedLast = lastChild.cloneNode(true);

    slideList.appendChild(clonedFirst);
    slideList.insertBefore(clonedLast, slideList.firstElementChild);

    // 점 만드는 로직
    let pageChild = '';
    for (var i = 0; i < slideLen; i++) {
    pageChild += '<li class="dot';
    pageChild += (i === startNum) ? ' dot_active' : '';
    pageChild += '" data-index="' + i + '"><a href="#"></a></li>';
    }
    pagination.innerHTML = pageChild;
    const pageDots = document.querySelectorAll('.dot');

    slideList.style.transform = "translate3d(-" + (slideWidth * (startNum + 1)) + "px, 0px, 0px)";

    let curIndex = startNum;
    let curSlide = slideContents[curIndex];
    curSlide.classList.add('slide_active');

    let nextBtns = function() {
        if (curIndex <= slideLen - 1) {
            slideList.style.transition = slideSpeed + "ms";
            slideList.style.transform = "translate3d(-" + (slideWidth * (curIndex + 2)) + "px, 0px, 0px)";
        }
        if (curIndex === slideLen - 1) {
            setTimeout(function() {
            slideList.style.transition = "0ms";
            slideList.style.transform = "translate3d(-" + slideWidth + "px, 0px, 0px)";
            }, slideSpeed);
            curIndex = -1;
        }
        curSlide.classList.remove('slide_active');
        pageDots[(curIndex === -1) ? slideLen - 1 : curIndex].classList.remove('dot_active');
        curSlide = slideContents[++curIndex];
        curSlide.classList.add('slide_active');
        pageDots[curIndex].classList.add('dot_active');
    };

    /* 다음 버튼 */
    slideBtnNext.addEventListener('click', nextBtns);

    /* 이전 버튼 */
    slideBtnPrev.addEventListener('click', function() {
    if (curIndex >= 0) {
        slideList.style.transition = slideSpeed + "ms";
        slideList.style.transform = "translate3d(-" + (slideWidth * curIndex) + "px, 0px, 0px)";
    }
    if (curIndex === 0) {
        setTimeout(function() {
        slideList.style.transition = "0ms";
        slideList.style.transform = "translate3d(-" + (slideWidth * slideLen) + "px, 0px, 0px)";
        }, slideSpeed);
        curIndex = slideLen;
    }
    curSlide.classList.remove('slide_active');
    pageDots[(curIndex === slideLen) ? 0 : curIndex].classList.remove('dot_active');
    curSlide = slideContents[--curIndex];
    curSlide.classList.add('slide_active');
    pageDots[curIndex].classList.add('dot_active');
    });

    /* 아래쪽 점 버튼 */
    let curDot;
    Array.prototype.forEach.call(pageDots, function (dot, i) {
    dot.addEventListener('click', function (e) {
        e.preventDefault();
        curDot = document.querySelector('.dot_active');
        curDot.classList.remove('dot_active');
        
        curDot = this;
        this.classList.add('dot_active');

        curSlide.classList.remove('slide_active');
        curIndex = Number(this.getAttribute('data-index'));
        curSlide = slideContents[curIndex];
        curSlide.classList.add('slide_active');
        slideList.style.transition = slideSpeed + "ms";
        slideList.style.transform = "translate3d(-" + (slideWidth * (curIndex + 1)) + "px, 0px, 0px)";
        });
    });

    let autoSlide;

    function startAutoSlide() {
        autoSlide = setInterval(nextBtns, 7000); // 여기 있는 숫자가 5초 간격으로 움직임
    }

    startAutoSlide();

    slideList.addEventListener('mouseenter', function() {
        clearInterval(autoSlide);
    });

    slideList.addEventListener('mouseleave', function() {
        startAutoSlide();
    });
});