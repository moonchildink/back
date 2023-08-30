$(function () {
    // 发起当前用户信息请求
    sendRequest('/info', 'GET').then(result => {
        console.log(result);

    }).catch(error => {
        console.log(error);
    })

})