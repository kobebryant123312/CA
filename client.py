import socket
import ssl
import pprint
# 创建了一个 SSL上下文,ssl.PROTOCOL_TLS表示选择客户端和服务器均支持的最高协议版本
context = ssl.SSLContext(ssl.PROTOCOL_TLS)
# 设置模式为CERT_REQUIRED，在此模式下，需要从套接字连接的另一端获取证书；如果未提供证书或验证失败则将引发 SSLError。
context.verify_mode = ssl.CERT_REQUIRED
# 加载一组用于验证服务器证书的CA证书
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
pprint.pprint(ssl_sock.getpeercert())
while True:     # 通过一个死循环不断接收用户输入，并发送给服务器
    inp = input("请输入要发送的信息： ").strip()
    if not inp:     # 防止输入空信息，导致异常退出
        continue
    ssl_sock.sendall(inp.encode())

    if inp == "exit":   # 如果输入的是‘exit’，表示断开连接
        print("结束通信！")
        break

    server_reply = ssl_sock.recv(1024).decode()
    print(server_reply)
s.close()    # 关闭连接
