function sendRequest(url,method,data){
    return new Promise((resolve,reject)=>{
        $.ajax({
            url:url,
            method:method,
            data:data,
            processData:false,
            contentType:false,
            success:resolve,
            error:reject
        });
    });
}

function getRequest(url,method){
    return new Promise((resolve, reject)=>{
        $.ajax({
            url:url,
            method:method
        })
    })
}