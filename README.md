# geiyepa
自动同步twitter的like 及 pixiv 的点赞，并将图片、视频下载到本地，pixiv中的动图会自动拼接为gif
# 使用方法
app.config 含义
## proxy
代理
## mode
type:用于twitter数据同步,第一次运行时要将其设为first,之后改为!first <br>
不在乎之前的数据的完整性的话可以直接设为!first
## mysql
### address 数据库地址
### username 数据库用户名
### 数据库密码
## twitter
### twitter\_id
地址https://api.twitter.com/2/timeline/profile/\*\*\*\*\*\*\*.json 中的数字
## pixiv
### pixiv\_id 用户登陆id
