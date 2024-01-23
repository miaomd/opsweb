# 下载vscode-server

1. 获取vscode的commit_id

   帮助（help）→关于（about）→提交（commit）

2. 将${commit_id}替换成commit_id，下载获取vscode-server-linux-x64.tar.gz

   [下载链接]: https://update.code.visualstudio.com/commit:${commit_id}/server-linux-x64/stabl

3. 以下已1.85.1版本为例，commit_id=0ee08df0cf4527e40edc9aa28f4b5bd38bbff2b2

# 其他包下载

[下载网址]: https://marketplace.visualstudio.com/vscode

- Chinese (Simplified) 
- Python
- Remote - SSH
- Remote - Tunnels
- Remote Development
- Remote Explorer
- WSL

# 安装vscode-server

- 将**vscode-server-linux-x64.tar.gz**上传到Linux服务器，并解压获得**vscode-server-linux-x64**

- 将**vscode-server-linux-x64**下的所有文件复制到以下路径

  ```
  /root/.vscode-server/bin/0ee08df0cf4527e40edc9aa28f4b5bd38bbff2b2
  ```

  ps：该路径为vscode自动创建，如果没有可以手动创建，也可以先安装Remote连接服务器后自动创建

- 修改文件权限

  ```
  cd /root/.vscode-server/bin/0ee08df0cf4527e40edc9aa28f4b5bd38bbff2b2
  chmod -R 777 . 
  ```

# 安装其他包

- vscode→扩展→扩展框右上角三个点→从VSIX安装→选择已下载的安装包

# 设置免密登录

## 获取客户端公私钥

- 客户端（Windows）打开命令行
- 输入**ssh-keygen**然后一路回车
- 从界面展示的存储路径中，找到公私钥

## 服务器配置公钥

- 将公钥id_rsa.pub 上传到服务器（Linux）

- 将公钥写入到服务器的**authorized_keys**

  ```shell
  cat id_rsa.pub >> ~/.ssh/authorized_keys
  ```

  ps:如果**.ssh**不存在，则使用以下命令创建

  ```
  mkdir ~/.ssh
  ```

- 查看公钥是否写入成功

  ```shell
  vim ~/.ssh/authorized_keys
  ```

## vscode引用私钥

- 点击，左下角（打开远程主机）

- 中间顶部弹出框，选择配置ssh主机

- 选择默认的第一个（因为创建时选择的这个）

- 修改配置文件，添加**IdentityFile**指向本地的私钥

  ```
  Host web
    HostName 10.16.83.239
    User root
    ForwardAgent yes
    IdentityFile C:\Users\M\Desktop\公私钥\id_rsa
    
  ps：
  Host	链接名，可以自定义
  HostName	远程主机ip或域名
  User	远程主机登录的用户名
  ForwardAgent	系统自带，默认就好
  IdentityFile	指向本地的ssh私钥
  ```

- 保存退出即可

# 远程debug

- 找到用户机（Windows）上安装的Python插件

  一般路径：C:\Users\本机用户名\.vscode\extensions\ms-python.python-2023.23.13541005

- 将找到的插件文件夹复制到服务器（Linux）上

  /root/.vscode-server/bin/0ee08df0cf4527e40edc9aa28f4b5bd38bbff2b2/extensions/

- vscode远程连接到服务器

- 点击左侧，运行和调试→自定义运行和调试

- 点击，中间弹出框中的“Django启动和调试”

- 可以开始打断点进行调试了

- 项目启动后地址

  ```
  http://127.0.0.1:8000
  ```

  