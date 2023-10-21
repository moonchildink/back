# Flask后端

- Date:2023-09-01
- Author:moonchild

## Blog相关接口

所有POST访问要求的接口，要求以Form形式携带参数，在uniapp之中的实现也就是：添加请求头参数：`header:{'Content-Type':'application/x-www-form-urlencoded'}`。

下面给出例子：

```javascript
uni.request({
		url: 'http://118.89.112.228:8000/auth/user',
		data: {
			'token': token
		},
		method: 'POST',
		header: {
			'Content-Type': 'application/x-www-form-urlencoded'
		},
		dataType: 'json'
	}).then((res)=>{
		//...
	});
```



1.   远程服务器地址以及端口：118.89.112.228:8000
2.   发布新帖子：'post/new'，POST，返回json格式字符串。参数：
     1.   'token'：Json web tokens，在用户登录时传送到客户端，并且存储到了uniapp的缓存之中
     2.   'title'：标题
     3.   'content'：文章内容
3.   通过ID获取文章：'post/id'，GET方法，返回json格式字符串。id参数在发布帖子之后返回。
4.   获取文章：'post/get_post'，POST方法，返回json格式字符，要求参数：
     1.   'id'
5.   获取某一用户的文章：'post/my_post'，POST，要求参数：
     1.   当前用户的token
6.   搜索文章：'post/search'，POST方法，要求参数：
     1.   'key_word'：搜索的关键字
7.   删除指定文章：'post/delete'，POST方法，要求参数：
     1.   'post_id'
8.   删除指定文章：'post/<id>'，DELETE方法，参数在请求URL中写明。举例：`http://118.89.112.228:8000/post/<id>`
9.   获取所有POST相关接口：'/post/'，GET方法





### 头像、图片相关接口

-   在注册时添加头像。avatar参数可以为空，也就是使用默认头像。

![image-20231021211227520](https://cdn.jsdelivr.net/gh/moonchildink/image@main/imgs/image-20231021211227520.png)

![image-20231021211233880](https://cdn.jsdelivr.net/gh/moonchildink/image@main/imgs/image-20231021211233880.png)

-   获取当前用户的头像，GET/POST方法

![image-20231021211553581](https://cdn.jsdelivr.net/gh/moonchildink/image@main/imgs/image-20231021211553581.png)

-   通过文件路径获取头像，GET方法

![image-20231021211921068](https://cdn.jsdelivr.net/gh/moonchildink/image@main/imgs/image-20231021211921068.png)



