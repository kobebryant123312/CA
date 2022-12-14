[# **Python实现基于OpenSSL的SSL通信**
](https://github.com/kobebryant123312/CA)
### ~~实验原理~~

_openssl 是目前最流行的 SSL 密码库工具，其提供了一个通用、健壮、功能完备的工具套件，用以支持SSL/TLS 协议的实现。openssl在SSL的基础上，另外包含了公钥私钥的生成、摘要生成等各种工具。
例如有些时候我们浏览网站的时候会有一些广告，这些广告什么的不一定是原网站挂上去的，也有可能是中间的运营商在中间篡改了内容导致的，可以使用https技术（一般是基于openssl）来对数据进行加密，保证数据不被篡改。_

SSL协议通信的握手步骤如下：

_第1步：SSL客户机连接至SSL服务器，并要求服务器验证它自身的身份。_

_第2步：服务器通过发送它的数字证书证明其身份。这个交换还可以包括整个证书链，直到某个根证书颁发机构（CA）。通过检查有效日期并确认证书包含可信任CA的数字签名来验证证书的有效性。_

_第3步：服务器发出一个请求，对客户端的证书进行验证，但是由于缺乏公钥体系结构，当今的大多数服务器不进行客户端认证。_

_第4步，协商用于加密的消息加密算法和用于完整性检查的哈希函数，通常由客户端提供它支持的所有算法列表，然后由服务器选择最强大的加密算法。_

_第5步，客户机和服务器通过以下步骤生成会话密钥：
    客户机生成一个随机数，并使用服务器的公钥（从服务器证书中获取）对它加密，以送到服务器上。
    服务器用更加随机的数据（客户机的密钥可用时则使用客户机密钥，否则以明文方式发送数据）响应。_

### ~~实验操作~~ （需要安装openssl)

https://www.openssl.org/source/

_1. 在kali环境下配置openssl证书内容_

先创建 CA 私钥，生成ca.crt；密钥长度为2048位：

    e默认是65537

![Alt](img/img.png)

生成自签名CA证书：

    req X.509证书签发请求(CSR)管理
    
    -new 新的请求
    
    -x509 输出一个X509格式的证书
    
    -days X509证书的有效时间
    
    -key 用于签名待生成的请求证书的私钥文件
    
    -subj 参数指定证书信息，避免在终端逐个输入

![Alt](img/img_1.png)


生成服务器私钥：

![Alt](img/img_3.png)

生成要颁发证书的证书签名请求：

![Alt](img/img_4.png)
    
用第2步创建的 CA 证书给第4步生成的签名请求进行签名，表明该证书请求已被CA信任，得到一个被CA签名过的证书：
   
![Alt](img/img_5.png) 

客户端用CA证书来对服务端被CA签名过的证书来进行认证：

![Alt](img/img_6.png)
    
结果是签名验证成功
    
查看证书具体信息：

    Issuer:
    证书颁发机构CA
    Subject:
    拥有证书的网站信息

![Alt](img/img_7.png)

查看证书里的公钥信息：

![Alt](img/img_8.png)

查看数字签名：

![Alt](img/img_9.png)

_2. 编写代码实现SSL通信_

项目运行环境为python3.9。所需的安装库见requirements.txt文件

直接 pip install -r requirements.txt 即可安装全部依赖库。

对连接的另一方的证书进行验证，客户端必须提供一个 “CA 证书” 文件，即CA机构的公钥，用这个公钥去验证被CA机构的颁发的目标网站的证书，这个证书相当于被CA机构的私钥签名过。

    Server
![Alt](img/img_10.png)

    Client
![Alt](img/img_11.png)

所以如果通过验证，则表明该网站被CA信任，那么客户端就可以相信它。


创建套接字及绑定地址进行监听：

![Alt](img/img_12.png)

客户端返回的 SSL 套接字会绑定上下文、设置以及证书：

![Alt](img/img_13.png)

服务端包装一个现有的 Python socket,并返回一个ssl socket,server_side为true表示为服务器行为，默认为false则表示客户端：

![Alt](img/img_14.png)

服务端接收消息：

![Alt](img/img_16.png)

客户端连接服务器：

![Alt](img/img_15.png)

先打印证书信息：

![Alt](img/img_17.png)

连接上服务器后进行消息传输：

![Alt](img/img_18.png)



**Main.py**

负责整合服务端和客户端的内容，进行封装：
![Alt](img/img_19.png)

实现在main.py调用server和client的所有功能，进行一键通信。

    把所有编写好的py文件和证书放在同一文件夹下

### **~~实验结果~~**

运行server.py首先打开服务端：

![Alt](img/img_20.png)

打开客户端输入发送消息：

![Alt](img/img_21.png)

服务端接收完成：

![Alt](img/img_22.png)

运行main.py

打印出来的证书信息：

![Alt](img/img_23.png)

客户端发送：hello,im,li

服务端接受来自端口54659客户端发来的消息

客户端接收服务端确认收到消息的通知，握手完成。

Exit退出会话。

整个运行的截图如下所示：

![Alt](img/img_2.png)


TODOs:

- [x] 实现了OpenSSL的通信
- [ ] 通信界面可视化




### 作者
作者：蓝昊

学号：202000460101



