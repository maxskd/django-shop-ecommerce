var update_buttons = document.getElementsByClassName('update-cart')

for(var i=0; i< update_buttons.length; i++){
    update_buttons[i].addEventListener('click', function(e){
        var bookId = this.dataset.book
        var action = this.dataset.action

        if(user_id){
            updateUserOrder(bookId,action)
        }
        else {
            addCookieItem(bookId, action)
        }

    })
}
/* Add item in cart for anonymous user with cookie */
function addCookieItem(bookId, action){
    if (action == 'add'){
        if (cart[bookId] == undefined){
            cart[bookId] = {'quantity':1}
        }
        else {
            cart[bookId]['quantity'] += 1
        }
    }
    if (action == 'remove'){
        cart[bookId]['quantity'] -= 1

        if (cart[bookId]['quantity'] <= 0){
            delete cart[bookId];
        }
    }
    console.log('Cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}

function updateUserOrder(bookId, action){

    var url = '/shop/update_item/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'bookId': bookId, 'action':action})
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log('Data:', data);
        location.assign("/shop/cart");
    });
}