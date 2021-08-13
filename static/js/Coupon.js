let CouponObj = Cookies.getJSON('coupon')

let open_menu = $('.open-burger');
let close_menu = $('.close-menu')
let menu = $('.mobile-menu')

function ModalPromo(text, color,) {
    $('.modal-promo').css({'display':'flex'})
    $('.text-promo-info').text(text).css({'color':`${color}`})
    $('.promo-info-text').css({'border':`1px solid ${color}`})
}

open_menu.click(function () {
    menu.css({'display':'block'})
})
close_menu.click(function () {
    menu.css({'display':'none'});
})

const url = '/orders/coupon_check';


async function coupon_submit(coupon) {

    const data = { coupons: `${coupon}` };
    try {
        const response = await fetch(url, {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json',
                'mode':"no-cors"
            }
        });
        let json = await response.json();
        let descr = json.description;
        let discount = json.discount;
        let status = json.status;
        if(json.error == 'coupon not found') {
            discount = '';
            descr = '';

            ModalPromo('Такого купона не существует!', 'red')

            $('#discount-promo').text(`${discount}`)
            $('#description-promo').text(`${descr}`)

        }
        else if (!json.error) {
            if(status) {

                ModalPromo('Промокод активирован!', 'green')
                if (discount.length != 0 ) {
                    $('#discount-promo').text(`На заказ действует скидка ${discount}%`)
                }
                else {
                    $('#discount-promo').text(``)
                }
                $('#description-promo').text(`${descr}`)

                await CouponStorage (Number(coupon), descr, Number(discount))



            }
            else {
                ModalPromo('Данный купон уже активирован!', 'red')
                discount = '';
                descr = '';
                $('#discount-promo').text(`${discount}`)
                $('#description-promo').text(`${descr}`)

            }


        }
        //console.log('Успех:', JSON.stringify(json));
    } catch (error) {
        //console.error('Ошибка:', error);

    }
}
async function CouponStorage( code, desc, disc) {
    const coupon = {
        code: Number(code),
        descript: desc,
        discount: Number(disc)
    }
    Cookies.set('coupon', {coupon})
}
async function sendCoupon(input_value) {
    if(input_value.length < 1) {
        discount = '';
        descr = '';
        ModalPromo('Пожалуйста, введите промокод!', 'red')
        $('#discount-promo').text(`${discount}`)
        $('#description-promo').text(`${descr}`)

    }
    else {
        await coupon_submit(input_value)
    }
}
$('.close-modal-promo').click(async function () {
    $('.modal-promo').css({'display':"none"});
    location.reload()
})
//отправка промокода
$('.submit-promo').click(async function (e) {
    e.preventDefault()
    let input_value = document.getElementById('input-promo').value
    if(CouponObj ) {
        ModalPromo('Cначала используйте активированный купон!', 'red')
    }
    else {
        await sendCoupon(input_value)
    }


})
$('.submit-promo-mobile').click(async function (e) {
    e.preventDefault()
    let  input_value = document.getElementById('input-mobile-promo').value
    if(CouponObj) {
        ModalPromo('Cначала используйте активированный купон!', 'red')
    }
    else {
        await sendCoupon(input_value)
    }
})
