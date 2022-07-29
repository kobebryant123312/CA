import socket
import ssl
ip_port = ('127.0.0.1', 9999)
# 创建了一个 SSL上下文,ssl.PROTOCOL_TLS表示选择客户端和服务器均支持的最高协议版本
context = ssl.SSLContext(ssl.PROTOCOL_TLS)
# 加载一个私钥及对应的证书
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

sk = socket.socket()            # 创建套接字
sk.bind(ip_port)                # 绑定服务地址
sk.listen(5)                    # 监听连接请求

print('启动socket服务，等待客户端连接...')

connect_sock, address = sk.accept()     # 等待连接，此处自动阻塞
# 包装一个现有的 Python socket,并返回一个ssl socket,server_side为true表示为服务器行为，默认为false则表示客户端
ssl_connect_sock = context.wrap_socket(connect_sock, server_side=True)
while True:     # 一个死循环，直到客户端发送‘exit’的信号，才关闭连接
    client_data = ssl_connect_sock.recv(1024).decode()      # 接收信息
    if client_data == "exit":       # 判断是否退出连接
        sk.close()  # 关闭连接
        exit("通信结束")
    print("来自%s的客户端向你发来信息：%s" % (address, client_data))
    ssl_connect_sock.sendall('服务器已经收到你的信息'.encode())    # 回馈信息给客户端
