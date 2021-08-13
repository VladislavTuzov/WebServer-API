let Goods;
if (Cookies.get('Goods')) Goods = Cookies.getJSON('Goods').GoodsData;

if(Goods) {
    $('.quatity ').text(`${Goods.total_count}`);
    $('.mobile-quatity').text(`${Goods.total_count}`);

    //state for mobile
    $('.goods-sum-text').text(`${Goods.total_sum} ₽`);
    $('.mobile-sum').text(`${Goods.total_sum} ₽`);
}
console.log(Goods)