checkSum()
let slideLenth;
let counter = 0;
let dotSlide;
let arrayPos = [];
hidePrev()
function hidePrev() {
    $('.button-prev').css({
        'visibility:': 'hidden',
        'opacity': '0'
    })
}
function showPrev() {
    $('.button-prev').css({
        'visibility:': 'visible',
        'opacity': '1'
    })
}
function hideNext() {
    $('.button-next').css({
        'visibility:': 'hidden',
        'opacity': '0'
    })
}
function showNext() {
    $('.button-next').css({
        'visibility:': 'visible',
        'opacity': '1'
    })
}
function nextSlide() {
    if(counter < slideLenth - 1) {
        console.log(counter)
        counter++
        showPrev()
        dotSlide.css({'margin-left':`-${100*counter}% `})
        if(counter == slideLenth - 1) {
            hideNext()
        }
    }
}
function prevSlide () {
    if(counter > 0) {
        counter--
        showNext()
        dotSlide.css({'margin-left':`-${100*counter}% `})
        if(counter === 0) {
            hidePrev()
        }
    }
}
$('.button-carousel > i').click(function () {
     dotSlide = $('.carousel-block:first-child')
    slideLenth = $('.carousel-block').length
    if (!$(this).hasClass('button-prev')) {
        nextSlide()
    } else {
        prevSlide()
    }
})

function checkSum() {
    if(GoodsData.total_sum > 100) {
        $('.additional-container').css({
            'display':'block '
        })
        sendRequest('POST', '/control/pos_posit', null )
            .then(data => {
                fillAditional(data)
            })
    }
}
function getRandomInRange(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function fillAditional(items) {
    for (let i = 0; i < 4; i++) {
        let resultRandomId = getRandomInRange(0, items.length - 1)
        if (!arrayPos.filter(prod => prod.id === items[resultRandomId].id)[0] ) {
            arrayPos.push(items[resultRandomId])
        } else {
            i--
        }
    }
    arrayPos.forEach((item, index) => {
        $('.carousel-wrapper').append(createAdditionalItem(item, index))
    })
}
function createAdditionalItem(item, index) {
    return `
     <div class="carousel-block">
        <img height="130" width="200" src="${item.photo}" alt="">
            <div class="carousel-title">
                ${item.name}
            </div>
            <div class="carousel-sum">
                ${item.price} ₽
            </div>
            <div onclick="addToBasket(${index})" class="toBasket">
                В корзину
            </div>
    </div>
    `
}
function addToBasket(obj) {
    console.log(ArrayGoods)
    item = arrayPos[obj]
    const product = {
        id: `a_${item.id}`,
        title: item.name,
        weight: `${item.weight} г`,
        picture: item.photo,
        count: 1,
        price: item.price
    }
    if(!ArrayGoods.filter(it => it.id == `a_${item.id}`)[0]) {
        console.log(product)
        ArrayGoods.push(product)
    } else {
        let i;
        let count;
        ArrayGoods.forEach((value, index) => {
            if (value.id === product.id)  {
                i = index
                count = value.count;
            }
        })
        product.count += count;
        ArrayGoods.splice(i,1,product)
    }
    updateCookie()
    fillBasketContainer()
}

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
