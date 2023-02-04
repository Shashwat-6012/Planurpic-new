if(localStorage.getItem('cart') == null ){
    var cart = {};
}
else{
    cart = JSON.parse(localStorage.getItem('cart'));
    document.getElementById('Cartno').innerHTML = Object.keys(cart).length;
}


    cart = JSON.parse(localStorage.getItem('cart'));
    
$.ajax({
        url: 'shop/cart',
        type: "POST",
        data: {'cart_id': cart },
        headers: { "X-CSRFToken": $.cookie("csrftoken") },
        dataType: "json",
        success: function (data) {
            console.log(data)
            
        },
        error: function () {
            alert("Some problem on passing data");
        }
        
    });

