let  GoodsData;
//функция записи значений в html блоки
function setState(obj = GoodsData) {
    //состояние для desktop версии
    $('.quatity ').text(`${obj.total_count}`)
    $('.mobile-quatity').text(`${obj.total_count}`)
    //состояние для моибильной версии
    $('.goods-sum-text').text(`${obj.total_sum} ₽`)
    $('.mobile-sum').text(`${obj.total_sum} ₽`)

}
function updateProperties (obj = GoodsData) {
    obj.total_count = obj.goods.reduce((res, i) => res + i.count, 0);
    obj.total_sum = obj.goods.reduce((res, i) =>res + (i.price * i.count), 0)
}
if(Cookies.get('Goods') !== undefined){
    GoodsData = Cookies.getJSON('Goods').GoodsData
    setState(GoodsData)
}
console.log(GoodsData)
//Состояние кол-ва выбираемого товара
$('.colvo').click(function () {
    let parent_id = $($(this).parents()[3]).attr('id') // ID товара, с которым есть взаимодейсвтие
    console.log($(this).parents()[3])

    if($(this).hasClass('plus')) {
        $(`#i_${parent_id} `).val(Number($(`#i_${parent_id}`).val()) + 1) // Увеличить кол-во товара
    }
    else {
        if (Number($(`#i_${parent_id}`).val()) > 1) {
            $(`#i_${parent_id} `).val(Number($(`#i_${parent_id}`).val()) - 1) // Уменьшить кол-во товара
        }
    }
})
$('.btn__card').click(function () {
    let parent_id = $($(this).parents()[2]).attr('id') // ID товара, с которым есть взаимодейсвтие
    console.log($(this).parents()[2])
    //Текущий объект
    const product = {
        id: parent_id,
        title: $(`.title_${parent_id}`).text(),
        weight: $(`.weight_${parent_id}`).text(),
        count: Number($(`#i_${parent_id}`).val()) ,
        price: Number($(`.price_${parent_id}`).text().split(' ')[0]),
        picture: $(`#picture_${parent_id}`).attr('src')
    }
    //Если куки уже есть
    if(GoodsData !== undefined) {
        // Перезапись данных объекта, если он уже существует
        if(GoodsData.goods.filter(prod => prod.id === product.id)[0] ) {
            let i;
            let count;
            GoodsData.goods.forEach((value, index) => {
                if (value.id === product.id)  {
                    i = index
                    count = value.count;
                }
            })
            product.count += count;
            GoodsData.goods.splice(i,1,product)
        }
        else {
            GoodsData.goods.push(product)
        }
    }
    else {
        //Создание чистого массива, в котором будут находиться объекты товаров
        GoodsData = {
            goods: []
        }
        GoodsData.goods.push(product)
    }
    updateProperties()
    Cookies.set('Goods', {GoodsData}, { expires: 30 });
    setState(GoodsData)
})
