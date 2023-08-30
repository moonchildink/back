$(function () {
    const btn = $("#login_btn");
    btn.on('click', async (event) => {

        console.log('点我了');
        event.preventDefault();

        let mail = $("#floatingInput").val();
        let password = $("#floatingPassword").val();
        password = hex_md5(password);
        if(mail!=null && password!=null){
            let form = new FormData();
            form.append('mail', mail);
            form.append('password', password);
            form.append('remeber', true);

            console.log(mail, password);
            let res;
            res = sendRequest('/auth/login/post', 'POST', form);
            res.then(result => {
                console.log(result);
            }).catch(reject => {
                console.log(reject);
            })
            console.log(res);
        }else {
            alert('请输入用户名和密码！');
        }

    });
});