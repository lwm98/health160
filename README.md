# health160

> 2021-11-22：鉴于大家提出的各式问题，刚刚试着约了一下其他有号科目，第一次也[报错](https://github.com/lwm98/health160/issues/6#issuecomment-975028164)，自动重试第二次成功。所以建议各位在自己本地运行的时候，先试下能不能成功约别的有号科目（成功预约后再取消，但是注意**一个月不能取消超过三次！**）

> 2021-11-01：如有问题，可以在issue提，我会尽量抽空总结

> 2021-10-28：运行main.py 出现fake-useragent报错的问题，已解决，详情参考下方记录

## 💡 特别声明:

* 本仓库发布的`health160`项目中涉及的任何脚本，仅用于测试和学习研究，禁止用于商业用途，不能保证其合法性，准确性，完整性和有效性，请根据情况自行判断。

* 请勿将`health160`项目的任何内容用于商业或非法目的，否则后果自负。

* 本项目遵循`GPL-3.0 License`协议，如果本特别声明与`GPL-3.0 License`协议有冲突之处，以本特别声明为准。

>  您使用或者复制了本仓库且本人制作的任何代码或项目，则视为`已接受`此声明，请仔细阅读

> 您在本声明未发出之时点使用或者复制了本仓库且本人制作的任何代码或项目且此时还在使用，则视为`已接受`此声明，请仔细阅读



## 🌱 功能

- 自动预约

- 自动挂号

- 自动抢号



## :art: 改进

- 更正部分网络请求参数及部分请求流程使该脚本正常运作

- 更改控制台输出

- 输出日志文件



## ⚡️ 运行环境



-  [Python 3](https://www.python.org/)



## :whale: 第三方库



- 需要使用到的库已经放在requirements.txt，使用pip安装的可以使用指令  

```
pip install -r requirements.txt
```

- 如果国内安装第三方库比较慢，可以使用以下指令进行清华源加速（不推荐）

```
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```


## 🖖 使用教程

1. 右上角给本项目点个star :star: ，拉取本项目代码

   `git clone https://github.com/lwm98/health160.git`

2. 安装python环境，详情参考[菜鸟教程](https://www.runoob.com/python/python-install.html) 章节python安装

3. 使用pip命令安装所需库

   `pip install -r requirements.txt`

4. 运行main.py

   `python main.py`

5. 按照控制台提示进行抢号挂号，等待好消息吧！

## :bomb: 记录

- 问题已汇总至issues置顶

- 出现较多的问题： fake_useragent.errors.FakeUserAgentError: Maximum amount of retries reached

  原因： 由于DB无法获得在线的useragent的文件

  解决办法：缓存useragent的文件到本地，不用它的自动获取。详情参考 https://www.freesion.com/article/37461287842/

  注：文件已经上传到本repo中，直接把它复制粘贴到临时文件夹中即可（查看临时文件夹位置可以参考上述链接，文件main.py中已加上，运行复制即可）。

## :sparkles: 感谢

##### 非常感谢原作者[@pengpan](https://github.com/pengpan)提供的初代代码及思路 https://github.com/pengpan/91160 



## :pencil: 写在最后

##### 本人改进该脚本的初衷，就是为了给女朋友抢hpv九价的疫苗，因为人工手动抢除了运气极好，否则根本不现实，特意在github浏览，并发现[@pengpan](https://github.com/pengpan)提供的逻辑清晰的初代代码，但由于很久没有维护，故并没有顺利跑通。在多次测试并经本人一番更改网络请求参数及部分流程操作后，大功告成。

##### 同时，本人是真的十分讨厌黄牛奸商，故该脚本开源但禁止商业使用，望理解

觉得该项目有用，就点个star :star: 吧！

以下是本人的成功截图，祝各位好运！


![Snipaste_2021-10-14_11-41-51](https://user-images.githubusercontent.com/48340898/137247678-4dcc34d5-422e-4aec-949d-d6bc48616379.png)
![image](https://user-images.githubusercontent.com/48340898/137247727-bae5648a-e30e-4995-92d0-da17a668e647.png)

peace & love
