let slideLenth = ($('.slides > div').length);
let counter = 0;
let dotSlide = $('.slide:first-child')

function nextSlide() {
    if(counter < slideLenth - 1) {
        counter++
        dotSlide.css({'margin-left':`-${100*counter}% `})
    } else {
        dotSlide.css({'margin-left': '0'})
        counter = 0
    }
}
function prevSlide () {
    if(counter > 0) {
        counter--
        dotSlide.css({'margin-left':`-${100*counter}% `})
    } else {
        counter = slideLenth - 1
        dotSlide.css({'margin-left': `-${100*(slideLenth - 1)}%`})
    }
}
$('.slider-btn').click(function () {
    if(!$(this).hasClass('slider-prev')) {
        nextSlide()
    } else {
        prevSlide()
    }
})
setInterval(() => nextSlide() , 7000)
