
function checkPackage(name){
    name = name.toLowerCase()
    var object = [];
    if (name == "stocks"){
        object = [100, 5000000]
    }
    else if (name == "trade bonds"){
        object = [200, 5000000]
    }
    else if (name == "real estate"){
        object = [1000, 5000000]
    }
    else if (name == "gold and silver"){
        object = [500, 5000000]
    }
    else if (name == "bitcoin and cryptocurrencies"){
        object = [100, 5000000]
    }
    else if (name == "oil and gas"){
        object = [500, 5000000]
    }
    else if (name == "ai and web3"){
        object = [1000, 5000000]
    }
    return object

}


$(document).ready(function(){
    const plan_name = $("#plan_name").text()
    var package_range = checkPackage(plan_name)
    console.log("package range ", package_range)
    
    $("#payment_form").validate({
        errorClass: "is-invalid",
        errorElement: "em",
        errorElementClass: "invalid-feedback",
        validClass: "is-valid",
        rules:{
            amount:{
                required: true,
                range: package_range
            },
            payment_type:{
                required: true
            },
            confirm_payment: {
                required: true
            }
        },
        messages:{
            amount:{
                required: "This field is required",
                // range: "Check the plan range at the side"
            },
            payment_type:{
                required: "Select a payment type"
            },
            confirm_payment: {
                required: "Please Confirm your payment"
            }
        }
    })
})