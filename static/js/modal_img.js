$('.close-modal-img').click(function () {
    $('.modal-img').css({'display': 'none'})
})
$('.card__main img').click(function () {
    $('.modal-img img').attr('src', $(this).attr('src'))
 $('.modal-img').css({'display':'flex'})
})
