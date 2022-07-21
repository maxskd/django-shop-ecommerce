let orders = document.getElementsByClassName('card-history');
/* Calculate total price */
for (let i = 0; i < orders.length; i++) {
    books = orders[i].getElementsByClassName('book-info');
    let total_price = 0;
    let total_quantity = 0;
    for (let i = 0; i< books.length; i++){
        quantity = books[i].getElementsByClassName('item-quantity')
        prices = books[i].getElementsByClassName('item-total')
        for(let i = 0; i < quantity.length; i++){
            total_price += parseFloat(prices[i].innerHTML);
            total_quantity += parseInt(quantity[i].innerHTML)
        }
    }
    orders[i].getElementsByClassName('place-for-price')[0].innerHTML = total_price + ',00₸';
    orders[i].getElementsByClassName('place-for-quantity')[0].innerHTML = total_quantity;
}