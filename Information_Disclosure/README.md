# IDscan



check Information_Disclosure
用于检查信息泄露
Welcome all friends to mention more suggestions for improvement
欢迎各位朋友多提改进意见



## environment

python 3.x

pip install requests threadpool



## Catalog
- SVN
	- IDscan.py
		- threadpool
		- http/https
		- random User-Agent
	- url_list.txt
		- Fill in the detected content |将被检测内容填入其中
	- README.md
	



## url_list.txt Example

**if you scan network segment|如果你想扫描网段**

```
192.168.0.0-192.168.0.255
192.167.36.24-192.168.39.255
```

**if you want to scan special port | 如果你想扫描特殊端口**

```192.168.0.1:8081```

**if you wang to scan website url| 如果你想扫描网站地址**

```
http://www.baidu.com
https://www.baidu.com
http://www.baidu.com:81
```




## Support

| type             | explanation        |
| ---------------- | ------------------ |
| /.svn/entries    | SVN信息泄露        |
| /.git/config     | Git信息泄露        |
| /.DS_Store       | DS_Store文件泄露   |
| /WEB-INF/web.xml | 初始化工程配置信息 |
| /crossdomin.xml  | 跨域策略文件       |
| /icons/          | 目录遍历路径       |
| ...              | ...                |



