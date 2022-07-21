let book_quantity = document.getElementsByClassName('item-quantity');
let book_price = document.getElementsByClassName('item-price');
let total_price = 0;
/* Calculate Price so that there is no more request to the DB */
for (let i = 0; i < book_price.length; i++) {
    total_price += parseFloat(book_price[i].innerHTML) * parseFloat(book_quantity[i].innerHTML)
}
document.getElementById('total-price').innerHTML = total_price + ',00₸'