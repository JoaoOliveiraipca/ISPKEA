
$("#commentForm").submit(function(e){
   e.preventDefault();

    $.ajax({
        data: $(this).serialize(),

        method: $(this).attr("method"),

        url: $(this).attr("action"),

        dataType: "json",

        success : function(response){
            console.log("comment saved")

            if (response.bool== True){


            }
        }
    })
})

// add to cart

$(".add-to-cart-btn").on("click", function(){
   
    let this_val = $(this)
    let index = this_val.attr("data-index")

    let quantity = $(".product-quantity-" + index).val()
    let product_title = $(".product-title-" + index).val()
    let product_id = $(".product-id-" + index).val()
    let product_price = $(".current-product-price-" + index).text()
    let product_pid = $(".product-pid-" + index).val()
    let product_image =$(".product-image-" + index).val()

    console.log("Quantity:", quantity);
    console.log("Id:", product_id);
    console.log("Pid:", product_pid);
    console.log("Title:", product_title);
    console.log("Image:", product_image);
    console.log("Price:", product_price);
    console.log("This is:", this_val);

    $.ajax({
        url:'/add-to-cart',
        data:{
            'id':product_id,
            'pid':product_pid,
            'image':product_image,
            'qty':quantity,
            'title':product_title,
            'price':product_price
        },
        dataType:'json',
        beforeSend:function(){
            console.log("adding to cart....");
        },
        success:function(response){
            this_val.html("✓")
            console.log("added product to cart");
            $(".cart-items-count").text(response.totalcartItems)
        }
    });
})


$(".delete-product").on("click", function(){

    let product_id = $(this).attr("data-product")
    let this_val = $(this)

    console.log("P_ID:", product_id);

    $.ajax({
        url: "/delete-from-cart",
        data: {
            "id": product_id
        },
        dataType: "json",
        beforeSend:function(){
            this_val.hide()
        },
        success: function(response){
            this_val.show()
            $(".cart-items-count").text(response.totalcartitems)
            $("#cart-list").html(response.data)
        }
    })
})

$(".update-product").on("click", function(){

    let product_id = $(this).attr("data-product")
    let this_val = $(this)
    let product_qty = $(".product-qty-" + product_id ).val()

    console.log("P_ID:", product_id);
    console.log("qty:",product_qty);

    $.ajax({
        url: "/update-cart",
        data: {
            "id": product_id,
            "qty": product_qty
        },
        dataType: "json",
        beforeSend:function(){
            this_val.hide()
        },
        success: function(response){
            this_val.show()
            $(".cart-items-count").text(response.totalcartitems)
            $("#cart-list").html(response.data)
        }
    })
  
})    