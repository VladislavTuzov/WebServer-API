const comb = {
    sps: [],
    pos: []
}
function sortRang(arr) {
    arr = arr.sort((a, b) => {
        return a-b;
    })
}
$('.btn-sub').click(function () {
    $('.product-select').each(function () {
        comb.sps.push(Number($(this).val()))
    })
    $('.bonus-select').each(function () {
        comb.pos.push(Number($(this).val()))
    })
    sortRang(comb.sps)
    sortRang(comb.pos)
    sendRequest('POST', '/control/add_comb_act', comb)
        .then(res => {
            location.href = '/admins-cont'
        })
        .catch(err => {
            location.href = '/admins-cont'
        })
})
function addList(block, class_) {
    $(block).append(createList(class_))
}
function createListItem(title, id) {
    return `
    <option value="${id}">${title}</option>
    `
}
function fillSelect(items, block) {
    let newItem = $(block).last()
    items.forEach((item)=> {
        newItem.append(createListItem(item.name, item.id))
    })
}
function createList(item) {
    return `
       <div class="row-select d-flex">
            <select class="${item}"></select>
       </div>
    `
}
$('.select-add').click(() => {
    addList('.list-wrapper', 'product-select')
    fillSelect(recievedArray, '.product-select')
})
$('.select-add-bonus').click(() => {
    addList('.result-list-wrapper', 'bonus-select')
    fillSelect(recievedArray, `.bonus-select`)

})
let recievedArray;
sendRequest('POST','/control/pos_posit', null)
    .then((data) => {
        fillSelect(data, `.product-select`)
        fillSelect(data, `.bonus-select`)
        recievedArray = data
    })
    .catch(e => console.log(e))

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
