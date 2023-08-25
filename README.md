# E7AS
### Epic 7 Auto Script.

# 脚本不能保证稳定，运行请确保有对应的网络环境


## 支持的功能

- [x] 多账号
- [x] 支持国服与谷歌版
- [x] 推送运行结果（推送文件取自[这里](https://github.com/whyour/qinglong)）
- [x] 刷书签
- [x] 网络异常等待及超时退出（谷歌版）
- [x] 每日签到/活动签到
- [x] 大厅宠物奖励收取
- [x] 每日召唤（人物/宠物）并保存记录
- [x] 圣域收菜
- [x] 讨伐/祭坛/净化深渊/考验殿堂
- [x] 骑士团每日签到奖励/捐赠/每周任务奖励领取/每周购买摩罗戈拉（达成率暂无素材）
- [x] 邮箱奖励领取
- [x] 定期任务奖励收取
- [x] 亚外服看广告
- [x] 竞技场NPC
- [x] 运行时网络不稳定等待甚至退出
- [ ] 领取每日与周任务奖励（很不稳定）



## 配置相关

0. 安装[python3.10+](https://www.python.org/downloads/)，安装时/后添加至环境变量
1. Download zip，解压
2. 进入文件夹，空白处选择“在终端中打开”
3. 输入以下命令并回车，等待依赖安装完成

  `pip install -r requirements.txt`

4. 修改模拟器分辨率为1600*900，打开usb调试并填写config.json
5. 输入以下命令并回车即可启动

  `python main_alpha.py`

定时任务的配置不再赘述
