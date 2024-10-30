
function checkPackage(name){
    name = name.toLowerCase()
    var object = [];
    if (name == "stocks"){
        object = [200, 499]
    }
    else if (name == "basic"){
        object = [500, 4999]
    }
    else if (name == "standard"){
        object = [5000, 9999]
    }
    else if (name == "starter"){
        object = [10000, 49999]
    }
    else if (name == "intermediate"){
        object = [50000, 99999]
    }
    else if (name == "premium"){
        object = [100000, 499999]
    }
    else if (name == "advance"){
        object = [500000, 999999]
    }
    else if (name == "ambassador 1"){
        object = [1000000, 4999999]
    }
    else if (name == "ambassador 2"){
        object = [5000000, 500000000]
    }
    return object

}


$(document).ready(function(){
    const package_name = $("#package_name").text()
    var package_range = checkPackage(package_name)
    console.log(package_range)
    
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