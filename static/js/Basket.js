let GoodsData;
let ArrayGoods;

let Action = {
    arr: new Array()
}
async function actionCheck  () {
    const data = Action;
    const url = '/control/check_action'
    try {
        const response = await fetch(url, {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json',
                'mode':"no-cors"
            }
        });

        let json = response.json();
        console.log(JSON.stringify(json))
        json.then(data => {
            console.log(data)
            if(data.status === true) {
                if (Cookies.get('test') === undefined) {
                    Cookies.set('test', {data});
                    addActionToGoods(Cookies.getJSON('test').data)
                    console.log('ДОБАВЛЯЕМ')
                }
            }else {
                if(Cookies.get('test')) {
                    removeAction()
                    fillBasketContainer()
                }
            }
        })

    } catch (error) {
        console.error('Ошибка:', error);
    }
}
function hasAction() {
    let res = false;
    let i;
    ArrayGoods.forEach((item, index) => {
        if(item.id == 'action_product') {
           res = true;
           i = index;
        }
    })
    return new Array(res, i);
}
function addActionToGoods(data) {
    if(Cookies.getJSON('test') && !hasAction()[0]) {
        ArrayGoods.push({
            id: 'action_product',
            title: data.name,
            weight: `${data.weight} г`,
            picture: data.photo,
            count: 1,
            price: 0
        })
    }
    updateCookie()
    fillBasketContainer()

}
if(Cookies.get('Goods')) {
    GoodsData = Cookies.getJSON('Goods').GoodsData
    ArrayGoods = GoodsData.goods
    $('.basket-container').css({'display':'flex'})
    $('.total-container').css({'display':'block'})
    actionInit()

}
else {
    $('.basket-container').css({'display':'none'})
    $('.total-container').css({'display':'none'})
}

async function actionSend() {
    if (ArrayGoods.length > 0 && Cookies.get('test') === undefined) {
       await actionCheck()
    }
}

$(document).ready(async function () {
    await actionSend()

})
function removeAction() {
    Cookies.remove('test')
    ArrayGoods.splice(hasAction()[1], 1)
}
function createActionProduct(item) {
    return `<div class="row basket-item" >
      <div class="col-lg-12">
        <div class="product-item">
          <div class="product-content">
            <img src="${item.picture}" alt="" class="product-picture">
            <div class="product-info-text">
              <h2 class="product-title">
                ${item.title}
              </h2>
              <span class="product-weight">
                        ${item.weight}
                </span>
            </div>
          </div>
          <div class="product-dynamic-content">
            <div class="product-action">
             В подарок
            </div>
            <div class="product-bottom d-flex">
              <div class="product-subtotal">
               0 ₽
              </div>
            </div>
          </div>
        </div>
      </div>
      <hr>
    </div>`

}
function actionInit() {
    ArrayGoods.forEach(item => {
        Action.arr.push(Number(item.id.split('_')[1]))
    })
    Action.arr = Action.arr.sort((a, b) => {
        return a-b;
    })
}
function emptyBasket() {
    return `
      <p class="basket-empty-text">
        Ваша корзина пока пуста.
      </p>
      <a href="index.html" class="return-main-page">Вернуться в магазин</a>
    `
}
function setTotal(obj = GoodsData) {
    $('.total-sum > span').text(`${obj.total_sum} ₽`)
}

setTotal()
function createProduct(item, index) {
    return `<div class="row basket-item" >
      <div class="col-lg-12">
        <div class="product-item">
          <div class="product-content">
            <img src="${item.picture}" alt="" class="product-picture">
            <div class="product-info-text">
              <h2 class="product-title">
                ${item.title}
              </h2>
              <span class="product-weight">
                        ${item.weight}
                </span>
            </div>
          </div>
          <div class="product-dynamic-content">
            <div class="product-quantity">
              <button class="quantity-btn" onclick="MinusSubProduct(${index})">
                -
              </button>
              <input readonly type="number" 
                     min="1" name="quantity" value="${item.count}" class="product-sub-quantity">
              <button class="quantity-btn" onclick="AddSubProduct(${index})">
                +
              </button>
            </div>
            <div class="product-bottom d-flex">
              <div class="product-subtotal">
               ${item.count*item.price} ₽
              </div>
              <i onclick="removeProduct(${index})" class="bi bi-trash product-remove"></i>
            </div>
          </div>

        </div>
      </div>
    </div>`
}
function precentSum(sum, precent) {
    let sumPrecent = (sum/100)*precent
    let result = (sum - sumPrecent).toFixed(2);
    return result;
}
function checkCoupon() {

    if(Cookies.getJSON('coupon') !== undefined) {
        let coup = Cookies.getJSON('coupon')

        if(coup.coupon.discount > 0) {
            $('.total-sum > span').css({'text-decoration': 'line-through'})
            $('.total-sum-discount').text(`${precentSum(GoodsData.total_sum, coup.coupon.discount) } ₽`)
        }
        if(coup.coupon.descript.length > 0) {
            $('.bonus-description').css({'display':'block'})
            $('.bonus-description').html(`
            <h4 class="bonus-text">
                 Дополнительный бонус:
                <span>${coup.coupon.descript}</span>
             </h4>
            `)
        }
    }

}

checkCoupon()
function setState(obj = GoodsData) {
    //состояние для desktop версии
    $('.quatity ').text(`${obj.total_count}`)
    $('.mobile-quatity').text(`${obj.total_count}`)
    //состояние для моибильной версии
    $('.goods-sum-text').text(`${obj.total_sum} ₽`)
    $('.mobile-sum').text(`${obj.total_sum} ₽`)

    setTotal()
}
function updateProperties (obj = GoodsData) {
    obj.total_count = obj.goods.reduce((res, i) => res + i.count, 0);
    obj.total_sum = obj.goods.reduce((res, i) =>res + (i.price * i.count), 0)
}
function updateCookie() {
    GoodsData.goods = ArrayGoods;
    updateProperties()
    console.log(GoodsData)
    setState()
    checkCoupon()
    Cookies.set('Goods', {GoodsData}, { expires: 30 });
}
function AddSubProduct (index) {
    ArrayGoods[index].count +=1;
    fillBasketContainer()
    console.log(ArrayGoods)
    updateCookie()
}
function ResetProperties (obj = GoodsData) {
    obj.total_count = 0
    obj.total_sum = 0
}
function removeProduct(index) {
    if(ArrayGoods.length == 1) {
        GoodsData.goods = ArrayGoods;
        Cookies.remove('Goods');
        ResetProperties()
        $('.additional-container').css({'display':'none'})
        $('.total-container').css({'display':'none'})
        $('.basket-container').css({'display':'none'})
        $('.basket-info').html(emptyBasket())
        setState()
    }
    else {
        if(Cookies.get('test')) {
            removeAction()
        }
        ArrayGoods.splice(index, 1)
        updateCookie()
        fillBasketContainer()
    }
}
function MinusSubProduct(index) {
    if(ArrayGoods[index].count > 1)
    ArrayGoods[index].count -=1;
    fillBasketContainer()
    updateCookie()
}
function fillBasketContainer() {
    $('.basket-container').html("")
    $('.basket-info').html("")
    if(GoodsData) {
        if(ArrayGoods.length > 0) {
            ArrayGoods.forEach((item, index) => {
                if(item.id == 'action_product') {
                    $('.basket-container').append(createActionProduct(item))
                } else {
                    $('.basket-container').append(createProduct(item, index))
                }
            })
        }
    }
    else {
        $('.basket-info').html(emptyBasket())
    }
}
fillBasketContainer()
