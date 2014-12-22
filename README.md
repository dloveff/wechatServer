wechatServer
============

微信公众账号后台台,使用tornado编写,可以直接部署到sinaAppEngine上.

首先感谢[lordking的微信公众账号测试平台](https://github.com/lordking/wxtest)的代码,让我能领略到python这门语言的灵活性.这次的代码结构大部分是参考lordking的,对某些逻辑做了简化.

##配置讲解

这里对handler的加载以及关键字回复等做了配置化处理,配置的文件格式为yaml.

配置文件有两个,在config目录下:

 - web.yaml
 - msg.yaml

web.yaml记录tornado的handler与url的映射.
msg.yaml记录不同的message对应的不同的响应方式.


###网页配置举例

```
urlPatterns:
- handler: wxplatform.web.WXInterfaceHandler.WXInterfaceHandler
  url: /

- handler: wxplatform.web.AlvinTestHandler.TestHandler
  url: /test

- handler: wxplatform.web.AlvinTestHandler.TokenHandle
  url: /token
```

###消息配置举例

对微信服务端发来的消息分类如下:

接收的普通消息

 - receive_text 文本
 - receive_image 图片
 - receive_video 视频

接收事件消息

 - event_subscribe 关注
 - event_unsubscribe 取消关注
 - event_scan 扫描二维码
 - event_location 上报地理位置
 - event_click 点击菜单拉取消息时的事件推送
 - event_view  点击菜单跳转链接时的事件推送
 - event_templatesendjobfinish 模板消息发送状态事件

接收语音识别消息

 - recognition_voice 语音消息以及语音识别消息


```
msg_handler:
  receive_text:
    "1": #关键字
      classes: wxplatform.MessageManage.TextMessageHandler#处理类
      content: hello 1 #返回的内容
    "2":#关键字
      classes: wxplatform.MessageManage.NewsMessageHandler
      content:
          - title: hello 1 #图文消息的标题
            description: just a test 1 #图文消息的描述
            picUrl: http://www.xx.com/tongtong.jpg #图文消息的图片链接
            url: http://www.google.com #图文消息的跳转链接
          - title: hello 2
            description: just a test 2
            picUrl: http://www.xx.com/tongtong.jpg
            url: http://www.google.com
```

消息的配置内容的层次为: 消息类型->关键字->处理类+内容

接下来:

 - 增加对微信菜单项的管理
 - 增加对数据处理后数据库的操作
 - 增加后台用户权限管理
