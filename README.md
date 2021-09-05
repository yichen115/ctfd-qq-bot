# ctfd-qq-bot
脚本改自：https://github.com/forever404/CTFd-Bot

主要是配合go-cqhttp实现监控ctfd注册与解答题目并在qq群推送，
根据 https://docs.go-cqhttp.org/ 找一个适合自己服务器的 release 版本，
教程：https://www.yuque.com/hxfqg9/misc/ctfd#B10Ou

如果go-cqhttp启用了access-token要注意改脚本里的的group_api，加上个&access_token=yourtoken

go-cqhttp项目：https://github.com/Mrs4s/go-cqhttp/