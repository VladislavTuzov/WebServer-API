function sendRequest(method, url, body) {
    const headers = {
        "Content-Type": "application/json",
        mode: "no-cors"
    };
    return fetch(url, {
        method: method,
        body: JSON.stringify(body),
        headers: headers
    }).then((response) => {
        if (response.ok) {
            return response.json();
        }
        return response.json().then((error) => {
            const e = new Error("Ошибка запроса");
            e.data = error;
            throw e;
        });
    });
}
let maxScores;
sendRequest('POST', '/control/check_scores', null)
    .then(data => {
        console.log(data)
       if(data.auth) {
           maxScores = Number(data.scores);
           fillScoresBlock(data.scores)
           scoreUseCheck()
           $('#scores-use').click(function () {
               scoreUseCheck()
           })
           $('.input-pay-scores').change(function () {
               let val = Number($(this).val())
               if(val < 0) {
                   $(this).val(0)
               } else if(val > maxScores) {
                   $(this).val(maxScores)
               }

           })
       }
    })


$('.time-select input').click(function () {
    let timeInput = $('.timepicker-block')
    if($(this).hasClass('time-target')) {
       timepickerFill()
        console.log('sassas')
    } else {
        timeInput.html(``)
        console.log('sas')
    }
})

let D = new Date();

let Year = D.getFullYear()
let Month = D.getMonth() + 1
let Day = D.getDate()
let H = D.getHours()
let M = D.getMinutes()

let MonthS;
if(Month < 10) {
    MonthS = `0${Month}`
} else {
    MonthS = Month
}
D.setDate(D.getDate() + 14)

let MaxYear = D.getFullYear()
let MaxMonth = D.getMonth() + 1;
let MaxDay = D.getDate()

let MaxMonthS;
if(MaxMonth < 10) {
    MaxMonthS = `0${MaxMonth}`
} else {
    MaxMonthS = MaxMonth
}

let GoodsData;
let ArrayGoods;
let couponData;
if(Cookies.get('Goods')) {
    GoodsData = Cookies.getJSON('Goods').GoodsData
    ArrayGoods = GoodsData.goods
}
else {
    window.location.href = '/basket';
}
if(Cookies.get('coupon')) {
    couponData = Cookies.getJSON('coupon').coupon;

}

function precentSum(sum, precent) {
    let sumPrecent = (sum/100)*precent
    let result = (sum - sumPrecent).toFixed(2);
    return result;
}

let totalSum

if(couponData && couponData.discount>0){
    totalSum = precentSum(GoodsData.total_sum, couponData.discount);
    console.log(totalSum);
}
else{
    totalSum = GoodsData.total_sum;
}

const total = totalSum

function fillOrderContainer() {
    if(GoodsData) {
        if(ArrayGoods.length > 0) {
            ArrayGoods.forEach((item, index) => {
                $('.container-goods').append(createRowProduct(index, item))
            })
        }
    }
    if(couponData) {
        if(couponData.descript.length > 0) {
            $('.container-goods').append(createRowBonus(couponData.descript))
        }
    }
   setTotalText()
}
fillOrderContainer()
function createRowBonus(description) {
    return `
      <div class="row row-table">
        <div class="col-lg-8">
            <div class="prod-content d-flex">
                <div class="prod-title">
                  ${description}
                </div>
                <div class="prod-count">
                    × 1
                </div>
            </div>
        </div>
        <div class="col-lg-4">
            <div class="prod-price">
               0 ₽
            </div>
        </div>
      </div> 
    `
}
function createRowProduct(index, item) {
    return `
      <div class="row row-table">
        <div class="col-lg-8">
            <div class="prod-content d-flex">
                <div class="prod-title">
                  ${item.title}
                </div>
                <div class="prod-count">
                    × ${item.count}
                </div>
            </div>
        </div>
        <div class="col-lg-4">
            <div class="prod-price">
               ${item.count * item.price} ₽
            </div>
        </div>
      </div> 
`
}
function timepickerFill() {
    $('.timepicker-block').html(`
         <input required  type="datetime-local" id="time_ex"
          name="meeting-time" 
          min="${Year}-${MonthS}-${Day}T${H}:${M}" max="${MaxYear}-${MaxMonthS}-${MaxDay}T22:30">
    `)
}

$(function(){
    $("#tel").mask("+7(999) 999-9999");
});
$('#agree').click(function () {
    checkAcceptAgree()
})
checkAcceptAgree()
function checkAcceptAgree() {
    if(!$('#agree').prop('checked')) {
        $('.submit_order').css({'background':'rgba(203, 90, 90, 0.83)'})
    }
    else {
        $('.submit_order').css({'background':'rgba(205, 15, 15, 0.83)'})
    }
}
$('.submit_order').click(async function (e) {
    if ($('#agree').prop('checked')) {
        // Cookies.remove('Goods');
        const request = {
            name: $('#name').val(),
            phone : $('#tel').val(),
            address: $('#address').val(),
            goods: ArrayGoods,
            email: $('#email').val(),
            order_note: $('#order-note').val(),
            time_pin: '',
            applied_coupons: '',
            scores: 0

        }
        if(request.name.length > 0 && request.phone.length > 0 && request.address.length > 0) {
            $('input[type=radio]').each(function () {
                if($(this).prop('checked')) {
                   let field_val = $(this).val()

                   switch ($(this).attr('name')) {
                       case 'delivery_method':
                           request.delivery_method = field_val
                           break;
                       case 'execution_time':
                           request.execution_time = field_val
                           if(request.execution_time == 'at_time') {
                               request.time_pin = $('#time_ex').val()
                           }
                           break;
                       case 'payment_method':
                           request.payment_method = field_val
                           break;
                   }
                }
            })
            if(couponData) {
                request.applied_coupons = couponData.code;
            }
            request.sum = GoodsData.total_sum
            request.count = GoodsData.total_count

            if($(Number($('.input-pay-scores').val())> 0)) {
                request.scores = Number($('.input-pay-scores').val())
            }

            if(request.execution_time == 'at_time') {
                if(request.time_pin != "") {
                    e.preventDefault()
                    await sendOrder(request)
                }
            }
            else {
                e.preventDefault()
                await sendOrder(request)
            }
        }
        else {
            console.log('Required fields is not fill')
        }
    }
    else {
        e.preventDefault()
    }
})
function deleteCookies() {
    Cookies.remove('coupon')
    Cookies.remove('Goods')
    Cookies.remove('test')
}
async function sendOrder(obj) {
     const url = '/orders/no_auth'
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'mode':"no-cors"
            },
            body: JSON.stringify(obj)
        });
        let json = await response.json();
        deleteCookies()
        location.reload()
    }
    catch (e) {
        console.log(e)
    }
}
function setTotalText() {

    $('.total-sum').text(`${totalSum} ₽`)
}
let deliverySumFirst = 100;
let deliverySumSecond = 150;

$('.delivery-select ').click(function () {
    checkDelivery()
})
setDelivery()

checkDelivery()
function checkDelivery() {
    if(total < 600) {
        if($('#f_paid').prop('checked')){
            if(couponData) {
                // console.log(totalSum);
                totalSum = Number(total) + Number(deliverySumFirst);
                // console.log(totalSum);
            }
            else if (!couponData){
                totalSum = Number(total) + Number(deliverySumFirst);
            }
        }
        else {
            // console.log('totalSum');
            if(couponData) {
                totalSum = Number(total) + Number(deliverySumSecond);
            }
            else if (!couponData){
                totalSum = Number(total) + Number(deliverySumSecond);
            }
        }
    }
    // console.log(totalSum);
    setTotalText()
}
function setDelivery() {
    $('.row-delivery > div > .delivery-select').html(``)

    if(totalSum >= 600 && totalSum < 700) {
        $('.row-delivery > div > .delivery-select').html(`
            <div>
                <input type="radio" id="first_delivery" name="delivery_method" value="free_600" checked="checked">
                <label for="first_delivery">Бесплатно по Индустр., Зашекснинском., Заягорбском., Северному р-нам от 600 руб.</label>
            </div>

        `)
    } else if (totalSum < 600) {
        $('.row-delivery > div > .delivery-select').html(`
            <div>
                <input  type="radio" id="f_paid" name="delivery_method" value="paid_100" checked="checked">
                <label class="paid_inp" for="f_paid">Платная доставка по Индустриальному р-ну (100 руб).</label>
            </div>

            <div>
                <input type="radio" id="sec_paid" name="delivery_method" value="paid_150">
                <label class="paid_inp" for="sec_paid">Платная доставка по остальным р-нам (150 руб).</label>
            </div>
        `)
    } else {
        $('.row-delivery > div > .delivery-select').html(`
            <div>
                <input type="radio" id="first_delivery" name="delivery_method" value="free_600" checked="checked">
                <label for="first_delivery">Бесплатно по Индустр., Зашекснинском., Заягорбском., Северному р-нам от 600 руб.</label>
            </div>

            <div>
                <input type="radio" id="sec_delivery" name="delivery_method" value="free_700">
                <label for="sec_delivery">Бесплатно по Ирдоматке, Городищу, завод (до проходной) от 700 руб.</label>
            </div>
            `
        )
    }
}


function scoreUseCheck() {
    if($('#scores-use').prop('checked')) {
        $('.input-pay-scores').css({'display':'block'})
    } else {
        $('.input-pay-scores').css({'display':'none'})
    }
}
/*scores use*/

function scoresBlockHtml(scores) {
    return `
      <div class="title-form">
        Баллы
     </div>
    <div class="bonus_block-act">
         <span>
            <input id="scores-use" type="checkbox" name="agreement" class="check__box">

            <label class="label_scores" for="scores-use">
                Использовать баллы
            </label>
        </span>
        <div class="scores-wrapper">
            <input class="input-pay-scores" type="number" min="1" placeholder="0">
            <div class="count-scores">
                Баллы: <span>${scores}</span>
            </div>
        </div>
    </div>`
    
}
function fillScoresBlock(scores) {
    $('.bonus_pay').html(scoresBlockHtml(scores))
}
