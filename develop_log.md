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
    
## 2017-07-31 achilles_xushy
    1. 根据需求修改代码
    2. 目标文件结构 column--program_name--|--image--image.jpg
                                      --|--media--*.ts
                                      --|--xml--*.json, *.xml
    3. 设置json文件内容
    4. 完成基础代码的编写
    5. 完成图片下载与xml生成代码的编写
    6. 将下载的png转换成jpg
    
## 2017-08-11 achilles_xushy
    1. 联合调试代码
    2. 初步完成测试，还没有在服务器上测试
    3. 修复win下解析视频文件出错问题，主要是文件名及路径中含有空格
    4. 修复linux下解析视频文件出错问题，主要是文件名及路径中含有空格
    5. 如果节目名包含日期，按照预定的格式修改文件名
    6. revise AmendXML.py line 388 for i_d in now_json_dict['episodes']
    7. 修改中国大陆在zone中为空的情况 
  

