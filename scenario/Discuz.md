http://blog.csdn.net/dreamstone_xiaoqw/article/details/77745363

* [1 安装mysql](#1)
	* [1.1 安装mysql版本5.6.37](#1.1)
	* [1.2 修改mysql数据库路径](#1.2)
	* [1.3 使用内网](#1.3)
	* [1.4 卸载mysql](#1.4)
	* [1.5 常见问题解决](#1.5)
* [2 安装Apache组件](#2)
* [3 安装PHP](#3)
* [4 安装并配置Discuz](#4)
	* [4.1 安装Discuz](#4.1)
	* [4.2 配置Discuz](#4.2)	


<h2 id="1">1 安装mysql</h2>
<h2 id="1.1">1.1 安装mysql版本5.6.38</h2>

    wget https://repo.mysql.com/mysql-community-release-el7-7.noarch.rpm
    rpm -ivh mysql-community-release-el7-7.noarch.rpm
    yum install mysql-community-server -y
    service mysqld start
    chkconfig mysqld on
     (rpm -ivh也可以使用yum localinstall安装)
    # chown -R mysql:mysql /var/lib/mysql (groupadd mysql;useradd -g mysql mysql)

    首次设置密码
    # mysql_secure_installation

	重置密码

    # mysql -u root -p
    mysql -u root -p  --socket=/mnt/mysql/mysql.sock

<h2 id="1.2">1.2 修改mysql数据库路径</h2>
    
    echo -e "n\np\n1\n\n\nw\n" | fdisk /dev/vdb
    mkfs.ext4 /dev/vdb1
    mkdir -p /mnt/mysql
    mount /dev/vdb1 /mnt/mysql
    echo /dev/vdb1 '/mnt/mysql ext4    defaults    0  0' >> /etc/fstab
    chown mysql:mysql /mnt/mysql/
    /usr/bin/mysql_install_db --user=mysql --datadir=/mnt/mysql/
    上面不需要指定--basedir=/usr/
    
    vi /etc/my.cnf
    datadir=/mnt/mysql
    
    或者手工操作：
    # cp -pr /var/lib/mysql/ /mnt/vdb1/mysql/
    # vi /etc/my.cnf
    # datadir=/var/lib/mysql 换成 datadir=/mnt/mysql/
   
    修改数据库最大连接数量（参考http://blog.51cto.com/12927979/2047537）
    max_connections=1000
    ulimit -n
    vi /usr/lib/systemd/system/mysqld.service,增加
    LimitNOFILE=65535
    LimitNPROC=65535
    $ systemctl daemon-reload
    $ systemctl restart mysql.service

    配置文件修改无效？(下面只是临时生效，进程重启失效)
    show variables like "max_connections";
    show variables like "%process%";
    set GLOBAL max_connections=1000;
    FLUSH PRIVILEGES;
    show databases;
    
    修改确认检查
    # ps -ef | grep mysql

[mysql压力测试工具tpcc-mysql安装测试使用](http://blog.csdn.net/laiyijian/article/details/70332409)

<h2 id="1.3">1.3 使用内网，开启远程</h2>

    默认配置模板cat /usr/share/mysql/my-default.cnf
    # vi /etc/my.cnf
    port=3306
    bind-address=192.168.0.193
    # skip-networking （注释掉或删除）

    # service mysqld restart
    # mysql -u root -p
    mysql>use mysql;
    mysql>update user set host = '%' where user = 'root';  (关键步骤)
    mysql>select host, user from user;
    mysql>FLUSH PRIVILEGES;

<h2 id="1.4">1.4 卸载mysql</h2>

    # rpm -qa | grep -i mysql
    php-mysql-5.4.16-42.el7.x86_64
    mysql-community-client-5.6.38-2.el7.x86_64
    
    # rpm -e mysql-community-client-5.6.38-2.el7.x86_64
    # chkconfig --del mysql
    # whereis mysql
    # rm -rf /usr/lib64/mysql
    
<h2 id="1.5">1.5 mysql常见问题解决</h2>

https://opms.jcloud.com/archives/3203

更改mysql数据存放到数据盘
https://blog.csdn.net/song_csdn1550/article/details/52222906

<h2 id="2">2 安装Apache组件</h2>

    yum install httpd -y
    service httpd start
    chkconfig httpd on

cat /etc/httpd/conf/httpd.conf |grep -v '#'

默认值DocumentRoot "/var/www/html"（后面PHP用/var/www/html）

修改Apache网站根目录/var/www/html为/mnt/html

    mkdir -p /mnt/html
    chmod -R 755 /mnt/html
    service httpd restart
https://blog.csdn.net/oyudabajiao/article/details/79777755

默认开启长连接
cat /usr/share/doc/httpd-2.4.6/httpd-default.conf |grep KeepAliveTimeout

    KeepAlive On （长连接 or 一个连接/请求）
    MaxKeepAliveRequests 100  (0不限，最大HTTP请求数/TCP连接)
    KeepAliveTimeout 5 （等待下一个来着同一客户端、同一个连接请求的超时时间）

Tcp的链接与断开比http请求的链接和断开，需要消耗掉更多的内存资源和时间。 

[Apache中KeepAlive](https://yq.aliyun.com/articles/35187)

<h2 id="3">3 安装PHP</h2>
<font color=red size=5 face=“黑体”>字体颜色</font>

    ```cpp,monokai(设置背景黑色，)
<table><tr><td bgcolor=#FFFFFF>
	
    yum install php php-fpm php-mysql -y
    service php-fpm start
    netstat -nlpt | grep php-fpm
    chkconfig php-fpm on
</td></tr></table>

<h2 id="4">4 安装并配置Discuz</h2>
<h2 id="4.1">4.1 下载Discuz</h2>

    wget http://download.comsenz.com/DiscuzX/3.2/Discuz_X3.2_SC_UTF8.zip
    mkdir -p /home/Discuz
    unzip Discuz_X3.2_SC_UTF8.zip -d /home/Discuz
<h2 id="4.2">4.2 安装Discuz</h2>

    cp -r /home/Discuz/upload/* /var/www/html/
    chmod -R 777 /var/www/html
    service httpd restart
<h2 id="4.3">4.3 配置Discuz</h2>

    管理员配置页面
    http://<IP 地址>/install
    
    论坛登录页面
    http://<IP 地址>/forum.php
    
    管理员登录页面
    http://<IP 地址>/admin.php?frames=yes&action=index

    关键配置文件
    /var/www/html/config/config_global.php
<h2 id="4.4">4.4 重装Discuz</h2>

    rm -rf /var/www/html/data/install.lock
    如果重装页面出不来，再拷贝一份
    cp /home/Discuz/upload/install/index.php /var/www/html/install/
    service php-fpm restart

<h2 id="4.5">4.5 Discuz自动化配置</h2>

右上角可以直接输入配置关键字快速搜索
<h2 id="4.5.1">4.5.1 关闭注册验证码(must)</h2>
    登陆管理界面后台，上面倒数第6个sheet选项页，"防灌水"->左边的“验证设置”->"验证码设置"
    “注册时启用验证码”
    “登陆时启用验证码”
    “发表信息时启用验证码”
    勾选，“不启用”


<h2 id="4.5.2">4.5.2 两次发表时间间隔(must)</h2>
    在Discuz后台，上面倒数第6个sheet选项页，防灌水-用户设置->两次发表时间间隔(秒):


<h2 id="4.5.3">4.5.3 ”您目前处于见习期间“XX分钟内不能发帖的问题(must)</h2>    
    http://<IP 地址>/admin.php?
    顶部的“首页”->"全局“，左边的“注册与访问控制”，选择“访问控制”页面设置“新手见习期限(分钟)”为0

<h2 id="4.5.4">4.5.4 ”帖子中不显示图片附件(must)</h2> 
    “全局”->上传设置->“论坛附件”->“帖子中显示图片附件 ”

<h2 id="4.5.5">4.5.5 ”密码错误次数过多(建议)</h2> 
密码错误次数过多，请 15 分钟后重新登录
修改source/function/function_member.php
$return = (!$login || (TIMESTAMP - $login['lastupdate'] > 900)) ? 5 : max(0, 5 - $login['count'])
将900秒（15分钟）修改为你想要的秒数即可，其中5代表尝试密码次数

<h2 id="4.5.6">4.5.6 ”同IP注册限制(当IP被限制时才需要配置)</h2> 
限时注册IP注册间隔限制(小时)：修改为0

用户处于限时注册的 IP 列表中的 IP 地址时，同一 IP 在本时间间隔内将只能注册一个帐号

<h2 id="4.5.7">4.5.7 设置上传附件的大小(must)</h2>
用户 » 用户组  [+]，编辑用户组 - 新手上路，论坛相关（附件相关），论坛最大附件尺寸
PS：如果不改，只能上传小于1000K的文件

    vi /etc/php.ini
    upload_max_filesize = 2M
    service php-fpm restart
    service httpd restart


上传后台控制代码
vi /home/upload/source/class/forum/forum_upload.php
1、需要php允许上传附件的大小
    vi /etc/php.ini
    upload_max_filesize = 2M
    service php-fpm restart
    service httpd restart

2、修改论坛支持的附件大小

    用户 » 用户组  [+]，编辑用户组 - 新手上路，论坛相关（附件相关），论坛最大附件尺寸

3、修改论坛支持的附件类型

    后台 论坛 板块 编辑  帖子相关   允许附件类型(小写):（附件类型）

<h2 id="4.6">4.6 ”附件上传到对象存储</h2>
<h2 id="4.6.1">4.6.1 ”后台配置</h2>
    
    将阿里的扩展框架内source文件夹下的文件按照对应目录上传至Discuz根目录的source文件夹下！ 
    也就是： 
    把“本文附件-扩展框架”里边的source/class/class_core.php，上传覆盖“网站根目录”下的source/class/class_core.php文件

    /var/www/html/source/class/class_core.php
    /var/www/html/config/config_global.php
    到config_global.php添加如下配置信息： 
     
    // ---------------------------  CONFIG EXTENT --------------------------- // 
    $_config['extend']['storage']['curstorage']= 'aliyun'; 
     
    $_config['extend']['storage']['aliyun']['access_id']= '你的access_id '; 
    $_config['extend']['storage']['aliyun']['access_key']= '你的access_key '; 
    $_config['extend']['storage']['aliyun']['access_host']=  'http://你的bucket名称.oss-cn-hangzhou.aliyuncs.com/'; 
    $_config['extend']['storage']['aliyun']['bucket']= '你的bucket名称'; 

<h2 id="4.6.2">4.6.2 Discuz配置</h2>
在Discuz后台，全局——上传设置——远程附件，开启远程附件，“设置远程访问url”为你设置的二级域名。
然后保存，更新缓存，设置完毕！ 

参考

[如何把Discuz!论坛的文件保存在华为云对象存储](http://jingyan.baidu.com/article/425e69e6071b83be15fc1604.html)

[华为对象存储托管Discuz!论坛图片和附件good](http://forum.huaweicloud.com/forum.php?mod=viewthread&tid=275&extra=page%3D1)

[Discuz实现阿里云oss云存储（扩展框架）](https://bbs.aliyun.com/read/239257.html)

[Discuz插件中心](http://addon.discuz.com/index.php?view=plugins&f_order=lastupdate)

[《从零开始学写discuz插件》教程](http://www.myele.net/thread-14650-1-1.html)


<h2 id="4.6.5">4.6.5 清理用户</h2>

    mysql -u root -p
    show databases;
    use ultrax;
    show tables;
    select * from pre_common_member;（DZ的用户表）
    select * from pre_ucenter_members;（UC的用户表）
    select * from pre_forum_post;(发帖的表)
    select * from pre_common_member_profile;（用户个人信息表）
    
    具体的sql语句是如下：
    DELETE FROM `pre_common_member` WHERE `uid` not in(1,2,3) LIMIT 1000;
    意思是一次性删除出了UID是1，2，3的1000条会员信息。

    DELETE FROM `pre_ucenter_members` WHERE `uid` not in(1,2,3) LIMIT 1000;
    温馨提示：1,2,3 换成不需要删除的ID即可。
    
    清理用户
    DELETE FROM `pre_common_member` WHERE `uid` not in(1);
    DELETE FROM `pre_ucenter_members` WHERE `uid` not in(1);
    清理所有帖子
    DELETE FROM `pre_forum_post` WHERE `pid` not in(-1);

由于用户相关表太多，使用下面得到需要清理的SQL命令，复制出来，1把执行。
    切换到information_schema表下执行
    select concat('delete * from ',table_name,';') from tables where table_name like 'pre_common_member%';

删除后为了防止网站有缓存，还需要登陆论坛的后台点击工具更新下整站缓存即可全部搞定。
控制界面 » 工具 » 更新缓存

<h2 id="4.6.6">4.6.6 清理帖子</h2>

    清理所有帖子
    DELETE FROM `pre_forum_post` WHERE `pid` not in(-1);
    DELETE FROM `pre_forum_thread` WHERE `tid` not in(-1);

    清理附件
    select concat('delete * from ',table_name,';') from tables where table_name like 'from pre_forum_attachment%';

delete * from pre_forum_attachment;
delete * from pre_forum_attachment_0;
delete * from pre_forum_attachment_1;
delete * from pre_forum_attachment_2;
delete * from pre_forum_attachment_3;
delete * from pre_forum_attachment_4;
delete * from pre_forum_attachment_5;
delete * from pre_forum_attachment_6;
delete * from pre_forum_attachment_7;
delete * from pre_forum_attachment_8;
delete * from pre_forum_attachment_9;

批量删帖仅用于删除违规帖子使用，如您需要批量删除历史旧帖，请使用批量主题管理功能。
后台 » 内容 » 论坛 » 论坛批量删帖

<font color=red size=3 face=“黑体”>内容 » 论坛主题管理</font>

手工删除后，需要执行
内容 » 主题回收站 » 清理


<h2 id="4.6.6">4.6.6 取消"您需要登录才可以下载或查看附件"</h2>
第二步：进入后台之后，依次选择“用户-->用户组-->系统用户组”，找到“游客”用户组，点击后面的“编辑”按钮；

进入编辑页面后，在上面的“论坛相关”下拉菜单中选择“附件相关”选项；


<h2 id="4.6.8">4.6.8 本地附件保存位置</h2>
默认为 /var/www/html/data/attachment/forum 服务器路径, 属性 777, 必须为 web 可访问到的目录, 结尾不加 “/”, 相对目录务必以 ”./” 开头

<h2 id="4.6.9">4.6.9 Jmeter请求消息中文乱码</h2>
修改jmeter.properties改为
sampleresult.default.encoding=utf-8

同时在jmeter的“HTTP请求”中，设置Content encoding编码格式为utf-8

<h2 id="4.6.10">4.6.10 Jmeter上传附件</h2>
Advanced里面的implementation要选择java

<h2 id="4.6.11">4.6.11 Jmeter参数无法传递</h2>
${__time(/1000,)函数不要用太多(中文注释也不要用太多)，导致参数无法传递了



<h2 id="4.6.12">4.6.12 Discuz下载附件返回404</h2>
1、检查下data附件目录权限是否为777可读写，data下相应目录也根据安装教程设置对应目前权限；
2、后台--全局--上传设置--基本设置--本地附件保存位置 是否正确；
3、后台--全局--上传设置--远程附件--启用远程附件: 选择“否”



<h2 id="4.8">4.8 Discuz对接对象存储</h2>
<h2 id="4.8.1">4.8.1 安装S3fs</h2>
    yum install automake fuse fuse-devel gcc-c++ git libcurl-devel libxml2-devel make openssl-devel -y
    git clone https://github.com/s3fs-fuse/s3fs-fuse.git
    cd s3fs-fuse
    ./autogen.sh
    ./configure
    make
    make install

	配置对象存储的AK和SK
	AK:SK
	echo 你的AK:你的SK > /etc/passwd-s3fs
	chmod 600 /etc/passwd-s3fs

    挂载
    HEC：s3fs 你的桶名 /mnt/s3fs -o url=http://obs.myhwclouds.com -o passwd_file=/etc/passwd-s3fs
    内网DNS：vi /etc/resolv.conf
    #nameserver 114.114.114.114
    #nameserver 114.114.115.115
    nameserver 100.125.1.250

    AWS：s3fs pp-c00363800 /mnt/s3fs -o url=http://s3.ap-southeast-1.amazonaws.com -o passwd_file=/etc/passwd-s3fs
    调试时可在上面的命令加上-d -d -f -o f2 -o curldbg

	阿里：
	s3fs pp-c00363800 /mnt/s3fs -o url=http://s3.ap-southeast-1.amazonaws.com -o passwd_file=/etc/passwd-s3fs
    s3fs挂载完就会自动卸载，阿里不支持
	https://help.aliyun.com/document_detail/32196.html?spm=5176.doc31952.6.1042.QDLp6U

    卸载
	umount /mnt/s3fs

[AWS-URL](http://docs.aws.amazon.com/zh_cn/general/latest/gr/rande.html#s3_region)

[利用S3fs在Amazon EC2 Linux实例上挂载S3存储桶](https://aws.amazon.com/cn/blogs/china/s3fs-amazon-ec2-linux/)

<h2 id="4.8.2">4.8.2 部署FTP---vsftpd</h2>
	# yum check-update
    # yum install vsftpd -y
    # vi /etc/vsftpd/vsftpd.conf
    local_root=/mnt（表示使用本地用户登录到ftp时的默认目录,不建议直接写/mnt/s3fs ）
	anonymous_enable=NO
    userlist_enable=NO
	userlist_deny=NO
	chroot_local_user=YES
	allow_writeable_chroot=YES
     
    白名单/etc/vsftpd/user_list增加用户名root
    黑名单/etc/vsftpd/ftpusers删除用户名root
    # chmod -R 777 /mnt/s3fs
    # systemctl restart vsftpd.service
	# chkconfig vsftpd on
    
    不建议使用obs-ftpuser，很多问题
    # useradd obs-ftpuser -s /sbin/nologin
    # passwd obs-ftpuser
	

    以下不需要
    # useradd -d /home/www -m obs-ftpuser -s /sbin/nologin
    # cd /home/www
    # chmod -R 777 *
	# passwd obs-ftpuser
    测试使用FileZilla登录,根据返回的错误码定位
    ftp://43.254.3.61/

[参考](http://blog.csdn.net/qq_25663723/article/details/53308507)

<h2 id="4.8.3">4.8.3 修改桶策略</h2>
为了让桶中的文件可以让用户直接访问到，需要修改桶策略！！
通用策略--->公共读

OBS控制台，选择桶--->权限--->桶策略，obsdiscuz改为自己的桶名（此桶中的图片即可被所有用户访问）
效果：Allow
被授权用户：*
资源：arn:aws:s3:::pp-c00363800/*
动作: GetObject

    {
	    "Version":"2012-10-17",
	    "Statement":[
	        {
	            "Sid":"AddPerm",
	            "Effect":"Allow",
	            "Principal":{
	                "AWS":[
	                    "*"
	                ]
	            },
	            "Action":[
	                "s3:GetObject"
	            ],
	            "Resource":[
	                "arn:aws:s3:::pp-c00363800/*"
	            ]
	        }
	    ]
    }

阿里云的策略

	{
	    "Version": "1",
	    "Statement":
	    [{
	        "Effect": "Allow",
	        "Action": ["oss:List*", "oss:Get*"],
	        "Resource": ["acs:oss:*:*:pp-chen", "acs:oss:*:*:pp-chen/*"],
	        "Condition":
	        {
	            "IpAddress":
	            {
	                "acs:SourceIp": "172.31.96.26"
	            }
	        }
	    }]
	}
<h2 id="4.8.3">4.8.3 论坛配置使用远端附件</h2>
管理中心，全局，上传设置，远程附件
    启用远程附件: 是
    FTP 服务器地址: 127.0.0.1
    FTP 帐号: root
    FTP 密码: xxxx
	远程附件目录: ./s3fs
    连接测试:
    远程访问 URL: 
    HEC: http://obs.myhwclouds.com/pp-c00363800 (pp-c00363800为桶名)
         或者http://obs.cn-north-1.myhwclouds.com/pp-c00363800
    AWS: http://s3.ap-southeast-1.amazonaws.com
    阿里云：http://pp-chen.vpc100-oss-cn-qingdao.aliyuncs.com

${__urlencode('$download-aid'))}

使用Badboy录制消息体
[BadboyInstaller](http://www.51testing.com/html/79/n-854279.html)

[官方原版](https://badboy.en.softonic.com/)

[JMeter 测试Web登录](http://blog.csdn.net/zbwork000/article/details/12613611)

[第十一讲、jmeter性能测试实战-web程序](http://blog.csdn.net/aisemi/article/details/55272457)


[JMeter实现多用户并发功能测试 - 抽奖系统实战经验](http://blog.csdn.net/wuxuehong0306/article/details/49902989)

[Discuz! 交流与讨论](http://www.discuz.net/forum.php?gid=1)

Access denied for user 'root'@'localhost' (using password: YES)

access denied的原因有如下可能：
1）mysql的服务器停止
2）用户的端口号或者IP导致  
3）mysql的配置文件错误----my.ini等文件
4）root用户的密码错误

using password的原因有如下可能：
1)错误的密码

vi /etc/my.cnf
在[mysqld]后添加skip-grant-tables（使用 set password for设置密码无效，且此后登录无需键入密码）
systemctl restart mysqld.service
