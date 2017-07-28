# 解析xml文件生成对应的媒体文件
author：achilles_xushy
## 功能说明：
    1. 解析big xml，将对应的视频文件改名为xml里面对应的名字

** 运行过程中会生成大量的进程，为了防止程序失败，需要设置系统最大打开文件描述符的上限数量 **
    
    1. 修改/etc/security/limit.conf添加一下字段：
        root             soft    nofile          10240
        root             hard    nofile          10240
        修改后保存，断开，重新ssh连接
        
    2. 下载所需的ffprobe，分别为linux跟windows

## 2017-07-26 achilles_xushy
    1. 将初始文件上传到git服务器
    2. 添加开发日志文件
    3. 完成基本的编码工作
    
    
  
