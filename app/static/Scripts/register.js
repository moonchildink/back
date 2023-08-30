$(function () {
    const btn = $("#submit_btn");
    btn.on('click', async (event) => {
        event.preventDefault();
        let name = $("#inputName").val();
        let email = $("#inputEmail").val();
        let pwd1 = hex_md5($("#inputPassword1").val());
        let pwd2 = hex_md5($("#inputPassword2").val());

        if (name != null) {
            if (email != null) {
                if (pwd1 != null) {
                    if (pwd2 != null && pwd1 === pwd2) {
                        let form = new FormData();
                        form.append('name', name);
                        form.append('mail', email);
                        form.append('password', pwd1);
                        let res;
                        console.log(name,email,pwd1);
                        res = sendRequest('/auth/register/post', "POST",form);
                        console.log(res);
                    }
                }
            }
        }

    })

})