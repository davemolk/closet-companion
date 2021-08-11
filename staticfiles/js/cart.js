const updateBtns = document.getElementsByClassName('update-cart')

for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        const productId = this.dataset.product
        const action = this.dataset.action
        console.log('productId:', productId, 'action:', action)
        console.log('user:', user)
        if (user == "AnonymousUser") {
            console.log('not logged in')
        }
        else {
            updateUserOrder(productId, action)
        }
    })
}


function updateUserOrder(productId, action) {
    console.log('User is authenticated, sending data...')
    const url = '/update_item/'

    fetch("/store/update_item/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })
    .then((response) => {
        console.log('hi')
        return response.json();
    })
    .then((data) => {
        console.log('Data:', data)
        location.reload()
    });
}
