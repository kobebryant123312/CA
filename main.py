import threading
import socket
import ssl
import pprint

def client():
    # 创建了一个 SSL上下文,ssl.PROTOCOL_TLS表示选择客户端和服务器均支持的最高协议版本
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    # 设置模式为CERT_REQUIRED，在此模式下，需要从套接字连接的另一端获取证书；如果未提供证书或验证失败则将引发 SSLError。
    context.verify_mode = ssl.CERT_REQUIRED
    # 加载一组用于验证其他对等方证书的CA证书
    context.load_verify_locations("ca.crt")
    # 设置端口
    ip_port = ('127.0.0.1', 9999)
    # 创建套接字
    s = socket.socket()
    # 包装一个现有的 Python 套接字 sock 并返回一个 SSLContext.sslsocket_class 的实例 (默认为 SSLSocket)。
    # 返回的 SSL 套接字会绑定上下文、设置以及证书
    ssl_sock = context.wrap_socket(s, server_hostname='127.0.0.1')

    # 连接服务器
    ssl_sock.connect(ip_port)
    # 输出证书信息
    print('#客户端消息#：客户端成功验证服务端证书，已成功连接，服务端证书信息如下')
    pprint.pprint(ssl_sock.getpeercert())
    while True:  # 通过一个死循环不断接收用户输入，并发送给服务器
        inp = input("#客户端消息#：请输入要发送的信息： ").strip()
        if not inp:  # 防止输入空信息，导致异常退出
            continue
        ssl_sock.sendall(inp.encode())
        if inp == "exit":  # 如果输入的是‘exit’，表示断开连接
            print("#客户端消息#：结束通信！")
            break

        server_reply = ssl_sock.recv(1024).decode()
        print("#客户端消息#：来自%s的服务端向你发来信息：%s" % (ip_port, server_reply))
    s.close()  # 关闭连接


def server():
    ip_port = ('127.0.0.1', 9999)
    # 创建了一个 SSL上下文,ssl.PROTOCOL_TLS表示选择客户端和服务器均支持的最高协议版本
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    # 加载一个私钥及对应的证书
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    sk = socket.socket()  # 创建套接字
    sk.bind(ip_port)  # 绑定服务地址
    sk.listen(5)  # 监听连接请求

    print('#服务端消息#：启动socket服务，等待客户端连接...')

    connect_sock, address = sk.accept()  # 等待连接，此处自动阻塞
    # 包装一个现有的 Python socket,并返回一个ssl socket,server_side为true表示为服务器行为，默认为false则表示客户端
    ssl_connect_sock = context.wrap_socket(connect_sock, server_side=True)
    while True:  # 一个死循环，直到客户端发送‘exit’的信号，才关闭连接
        client_data = ssl_connect_sock.recv(1024).decode()  # 接收信息
        # print(client_data)
        if client_data == "exit":  # 判断是否退出连接
            sk.close()  # 关闭连接
            print("#服务端消息#：客户端已结束通信！")
            exit("通信结束")
        print("#服务端消息#：来自%s的客户端向你发来信息：%s" % (address, client_data))
        ssl_connect_sock.sendall('服务器已经收到你的信息'.encode())  # 回馈信息给客户端


thread_server = threading.Thread(target=server)
thread_client = threading.Thread(target=client)
thread_server.start()
thread_client.start()
thread_server.join()
thread_client.join()
print("退出主线程")
