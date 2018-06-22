8/10/2017 2:57:24 PM 

* [1 Tomcat](#1)
	* [1.1 安装JDK](#1.1)
	* [1.2 安装apache-tomcat](#1.2)
	* [1.3 安装Maven](#1.3)
	* [1.4 安装DayTrader](#1.4)
* [2 Geronimo](#2)
* [3 Mysql](#3)
	* [3.1 安装mysql版本5.6.37](#3.1)
	* [3.2 添加防火墙规则](#3.2)	
	* [3.3 开启允许远程](#3.3)
	* [3.4 远端方式连接测试](#3.4)
	* [3.5 创建本地非root账号](#3.5)
	* [3.6 创建非root账号](#3.6)
	* [3.7 创建库](#3.7)
* [4 Geronimo对接mysql数据库](#4)
	* [4.1 jdbc驱动](#4.1)
	* [4.2 创建库连接](#4.2)	
* [5 部署DayTrader应用](#5)
	* [5.1 部署应用](#5.1)
	* [5.2 初始化应用数据库](#5.2)	
	* [5.3 tomcat部署应用](#5.3)
* [7 关键的启动](#7)
	* [7.1 tomcat启动](#7.1)
	* [7.2 geronimo启动](#7.2)	

<h2 id="1">1 Tomcat</h2>
<h2 id="1.1">1.1 安装JDK</h2>
    mkdir /usr/java;
    cp /home/jdk-6u45-linux-x64.bin /usr/java;
    chmod u+x /usr/java/jdk-6u45-linux-x64.bin;
    cd /usr/java/;
    ./jdk-6u45-linux-x64.bin;

    # vi /etc/profile  在最后加下下面几行export
	cat << EOF >> /etc/profile
	export JAVA_HOME=/usr/java/jdk1.6.0_45
	export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
	export PATH=$PATH:$JAVA_HOME/bin
	EOF
    # reboot
[http://download.oracle.com/otn/java/jdk/6u45-b06/jdk-6u45-linux-x64.bin](http://download.oracle.com/otn/java/jdk/6u45-b06/jdk-6u45-linux-x64.bin)

<h2 id="1.2">1.2 安装apache-tomcat</h2>
    # tar -zxvf /home/apache-tomcat-7.0.79.tar.gz -C /home
    设置用户名密码
    # vi /home/apache-tomcat-7.0.79/conf/tomcat-users.xml  在倒数第二行加上下面几行
    <role rolename="manager-gui"/>
    <role rolename="manager-script"/>
    <role rolename="manager-jmx"/>
    <role rolename="manager-status"/>
    <user username="tomcat" password="710000" roles="manager-gui,manager-script,manager-jmx,manager-status"/>

    #或者直接sed，7表示行号，a\后行插入,i\前行插入，XXX表示内容，中间\n换号
    sed -i '7a\XXX' /home/apache-tomcat-7.0.79/conf/tomcat-users.xml
    # sh /home/apache-tomcat-7.0.79/bin/startup.sh

[http://mirror.jax.hugeserver.com/apache/tomcat/tomcat-7/v7.0.79/bin/apache-tomcat-7.0.79.tar.gz](http://mirror.jax.hugeserver.com/apache/tomcat/tomcat-7/v7.0.79/bin/apache-tomcat-7.0.79.tar.gz)

> 浏览器登录http://IP:8080/

> 注意：要在租户的管理界面上添加安全组规则，放开8080端口（和Mysql的3306端口，windows远程登录3389端口）,0.0.0.0/0,入方向

点击Manager App按钮设置应用，此步骤需要用户名TOMCAT_USER和密码TOMCAT_PASSWD


修改tomcat端口
vi /home/apache-tomcat-7.0.79/conf/server.xml

    <Connector port="9999" protocol="HTTP/1.1"
       connectionTimeout="20000"
       redirectPort="8443" />

<h2 id="1.3">1.3 安装Maven</h2>
> 用于执行mvn命令来安装DayTrader

    # tar -zxvf /home/apache-maven-3.2.3-bin.tar.gz -C /home
    # vi /etc/profile
    修改最后的export PATH=增加:/home/apache-maven-3.2.3/bin
    # reboot

[https://archive.apache.org/dist/maven/maven-3/3.2.3/binaries/apache-maven-3.2.3-bin.tar.gz](https://archive.apache.org/dist/maven/maven-3/3.2.3/binaries/apache-maven-3.2.3-bin.tar.gz)

<h2 id="1.4">1.4 安装DayTrader</h2>
    # yum install zip
    # unzip /home/daytrader-parent-3.0.0.zip -d /home/
    # cd /home/daytrader
    # mvn clean install
    大概15分钟后，看到如下成功
    [INFO] BUILD SUCCESS
    [INFO] ------------------------------------------------------------------------
    [INFO] Total time: 12:22 min
    [INFO] Finished at: 2017-08-08T17:08:05+08:00
    [INFO] Final Memory: 58M/340M
    [INFO] ------------------------------------------------------------------------

[http://svn.apache.org/repos/asf/geronimo/daytrader/tags/daytrader-parent-3.0.0/](http://svn.apache.org/repos/asf/geronimo/daytrader/tags/daytrader-parent-3.0.0/)

坑---mvn在AWS上安装报错：

    [ERROR]   The project org.apache.geronimo.daytrader:daytrader-parent:3.0.0 (/home/daytrader/pom.xml) has 1 error
    [ERROR] Non-resolvable parent POM: Could not transfer artifact org.apache.geronimo.genesis:genesis-java6-flava:pom:2.0 from/to central (https://repo.maven.apache.org/maven2): Connect to repo.maven.apache.org:443 [repo.maven.apache.org/151.101.112.215] failed: Connection timed out and 'parent.relativePath' points at wrong local POM @ line 21, column 13 -> [Help 2]
    org.apache.maven.model.resolution.UnresolvableModelException: Could not transfer artifact org.apache.geronimo.genesis:genesis-java6-flava:pom:2.0 from/to central (https://repo.maven.apache.org/maven2): Connect to repo.maven.apache.org:443 [repo.maven.apache.org/151.101.112.215] failed: Connection timed out
    Caused by: org.apache.maven.wagon.providers.http.httpclient.conn.ConnectTimeoutException: Connect to repo.maven.apache.org:443 [repo.maven.apache.org/151.101.112.215] failed: Connection timed out
    [ERROR] For more information about the errors and possible solutions, please read the following articles:
    [ERROR] [Help 1] http://cwiki.apache.org/confluence/display/MAVEN/ProjectBuildingException
    [ERROR] [Help 2] http://cwiki.apache.org/confluence/display/MAVEN/UnresolvableModelException

修改DNS

    nslookup repo.maven.apache.org
    vi /etc/resolv.conf
    nameserver 8.8.8.8

把daytrader-repository.zip解压到/root/.m2目录下

    mkdir -p /root/.m2/
    unzip /home/daytrader-repository.zip -d /root/.m2/
    cd /home/daytrader;mvn install

<h2 id="2">2 Apache Geronimo v3.0.1 Release</h2>
> 只是为了设置数据库而用（tomcat无法直接重设置数据库。。）

[http://geronimo.apache.org/downloads.html](http://geronimo.apache.org/downloads.html)

<h2 id="2.1">2.1 Linux版</h2>
    # tar -zxvf /home/geronimo-tomcat7-javaee6-3.0.1-bin.tar.gz -C /home
需要安装   [1.1 安装JDK](#1.1)、[1.3 安装Maven](#1.3)、[1.4 安装DayTrader](#1.4)

    # /home/geronimo-tomcat7-javaee6-3.0.1/bin/startup
    使用浏览器登录http://IP:8080/,登陆用户名和密码见changing-the-username-and-password.html中的设置
    # vi /home/geronimo-tomcat7-javaee6-3.0.1/var/security/users.properties  (user1=password1)
    # vi /home/geronimo-tomcat7-javaee6-3.0.1/var/security/groups.properties (admin=user1,user2)

> http://IP:8080/无法访问，查看log中的ERROR日志：

    /home/geronimo-tomcat7-javaee6-3.0.1//var/log/geronimo.log
    /home/geronimo-tomcat7-javaee6-3.0.1/var/log/geronimo.out在初始化中
    Module 12/68 org.apache.geronimo.

[http://geronimo.apache.org/GMOxDOC30/changing-the-username-and-password.html](http://geronimo.apache.org/GMOxDOC30/changing-the-username-and-password.html "设置geronimo登录用户和密码")

<h2 id="3">3 Mysql</h2>
<h2 id="3.1">3.1 安装mysql版本5.6.37</h2>
    # wget https://repo.mysql.com/mysql-community-release-el7-7.noarch.rpm
    # rpm -ivh mysql-community-release-el7-7.noarch.rpm (或者yum localinstall安装)
    # yum install mysql-community-server
    # service mysqld start
    # chown -R mysql:mysql /var/lib/mysql (groupadd mysql;useradd -g mysql mysql)

    首次登陆前，需要设置密码
    # mysql_secure_installation

    # mysql -u root -p

	以下几步不需要,只是记录
    mysql > use mysql;
    mysql > update user set password=password('PASSWORD') where user='USERNAME';
    mysql > GRANT ALL PRIVILEGES ON *.* TO 'USERNAME'@'%' IDENTIFIED BY "PASSWORD";
    mysql > FLUSH PRIVILEGES;
    mysql > quit;
<h2 id="3.2">3.2 添加防火墙规则</h2>
> 性能下降严重，暂时不需要执行

    # iptables -A INPUT -s 192.168.0.0/16 -p tcp -m state --state NEW -m tcp --dport 3306 -j ACCEPT
<h2 id="3.3">3.3 开启允许远程</h2>
    # vi /etc/my.cnf
    port=3306
    bind-address=192.168.0.193
    # skip-networking （注释掉或删除）

    # service mysqld restart
<h2 id="3.4">3.4 远端方式连接测试</h2>
    # mysql -u root -h 192.168.1.15 -p
<h2 id="3.5">3.5 创建本地非root账号</h2>
> 不需要这步，会报错，只是记录

    CREATE USER 'myuser'@'localhost' IDENTIFIED BY 'mypass';
    GRANT ALL ON *.* TO 'myuser'@'localhost';
<h2 id="3.6">3.6 创建非root账号</h2>
    mysql> CREATE USER 'chen'@'%' IDENTIFIED BY 'chen-1234';
    mysql> GRANT ALL ON *.* TO 'chen'@'%';
<h2 id="3.7">3.7 创建库</h2>
    mysql> create database tradedb;
    mysql> use tradedb;
    //授权hdp用户拥有hivemeta数据库的所有权限
    mysql> grant all privileges on *.* to chen@"%" identified by "chen-1234" with grant option;
    mysql> flush privileges;

<h2 id="4">4 Geronimo对接mysql数据库</h2>
<h2 id="4.1">4.1 jdbc驱动</h2>
    1）登录Geronimo界面，点击“Administration”下的“- Console”，页面跳转。
    2）在“Navigator:”选中“高级”选择，选择目录树中的“Resource”目录下的的“JAR仓库”。
    3）在右侧的“添加存档到存储库中”下，“选择文件”浏览选择mysql-connector-java-5.1.43-bin.jar
	4）在右侧的“添加存档到存储库中”下，组输入“mysql”，勾选“Specify other parts”，会自动带出信息

如果是英文版的界面，“Resource”->"Repository"
最终存放到/home/geronimo-tomcat7-javaee6-3.0.1/repository目录下
mysql/mysql-connector-java/5.1.43-bin/mysql-connector-java-5.1.43-bin.jar

[https://downloads.mysql.com/archives/c-j/](https://downloads.mysql.com/archives/c-j/)[老版本]

[https://dev.mysql.com/downloads/connector/j/](https://dev.mysql.com/downloads/connector/j/)[新版本5.1.43]

<h2 id="4.2">4.2 创建库连接</h2>
    1）登录Geronimo界面，点击“Administration”下的“- Console”，页面跳转。
    2）在“Navigator:”选中“普通”选择，选择目录树中的“DateSources”。
    3）在右侧的“数据库连接池”设置界面，选择“使用 Geronimo 数据库连接池向导”，“数据库连接池名称:
    ”输入TradeDataSource，“数据库类型:”下列选择“MySql”。
    4）根据提示设置“连接基本属性”，“数据库名称”输入tradedb
    5）在运行 SQL，下拉选择“jdbc/TradeDataSource”，测试SQL语句select 0;

<h2 id="5">5 部署DayTrader应用</h2>
> 如果用户名trade/trade,数据库名为tradedb，则修改少很多

修改Geronimo节点上的（PC端文件，从浏览器上传）
/home/daytrader/javaee6/plans/target/classes/daytrader-mysql-xa-plan.xml
47行，49行，92-93，95-96，112-113，115-116。
<h2 id="5.1">5.1 部署应用</h2>
    1）登录Geronimo界面，点击“Administration”下的“- Console”，页面跳转。
    2）在“Navigator:”选中“普通”选择，选择目录树中的“Deployer”。
    3）在右侧的“安装应用","归档文件:"浏览选择daytrader-ear-3.0.0.ear；”部署计划“浏览选择daytrader-mysql-xa-plan.xml，点击”安装“。看到“成功启动应用“，表明部署OK

daytrader-ear-3.0.0.ear在daytrader-parent-3.0.0 SVN路径下:

daytrader-parent-3.0.0\javaee6\assemblies\daytrader-ear\target\daytrader-ear-3.0.0.ear

<h2 id="5.2">5.2 初始化应用数据库</h2>
    1）登录Geronimo界面，点击“Administration”下的“- Console”，页面跳转。
    2）在“Navigator:”选中“普通”选择，选择目录树中的“Applications (EAR)”。
    3) 在右侧的“Installed Enterprise Applications (EAR)”界面，选择URL为“/daytrader”，进入http://IP:8080/daytrader/页面
    4）选中”Configuration“标签页，分别进行“Configure DayTrader run-time parameters”，主要设置DayTrader Max Users=1000、Trade Max Quotes=2000；
	“(Re)-create  DayTrader Database Tables and Indexes"和”(Re)-populate  DayTrader Database“
    5）最后选择进入测试页面“Test DayTrader Scenario”

<h2 id="5.3">5.3 tomcat部署应用</h2>
    1）打开tomcat管理界面，进入“Manager App”
    2）在“Tomcat Web Application Manager"界面下，“WAR file to deploy”那里，”选择文件“daytrader-web-jdbc-3.0-M1.war

    可能出现的坑：403 Access Denied
    重新从manager进入再次”选择文件“

    3）最后在Applications列表里，能看到/daytrader-web-jdbc-3.0-M1
    4）在tomcat节点上修改文件
    /home/apache-tomcat-7.0.79/webapps/daytrader-web-jdbc-3.0-M1/META-INF/context.xml:50行
    增加
    <Resource name="jdbc/TradeDataSource" auth="Container" type="javax.sql.DataSource"
           maxActive="100" maxIdle="30" maxWait="10000"
           username="USER" password="PASSWD" driverClassName="com.mysql.jdbc.Driver"
           url="jdbc:mysql://192.168.0.193:3306/tradedb?autoReconnect=true"/>
    注释掉71行， 前<!--，后-->
    5）把mysql-connector-java-5.1.43-bin.jar放到tomcat节点的/home/apache-tomcat-7.0.79/webapps/daytrader-web-jdbc-3.0-M1/WEB-INF/lib下
    # cp /home/mysql-connector-java-5.1.43-bin.jar /home/apache-tomcat-7.0.79/webapps/daytrader-web-jdbc-3.0-M1/WEB-INF/lib/
    6）在Applications列表，/daytrader-web-jdbc-3.0-M1对应的那一行，选择“Reload”
    7）测试应用是否部署OK，http://IP:8080/daytrader-web-jdbc-3.0-M1/scenario

<h2 id="5.4">5.4 tomcat应用session不释放问题</h2>
    vi /home/apache-tomcat-7.0.79/webapps/daytrader-web-jdbc-3.0-M1/WEB-INF/web.xml
    修改session-timeout为1分钟

<h2 id="5.5">5.5 设置数据库链接数</h2>
    vi /etc/my.cnf
    修改max_connections=3000，重启服务
    #检查参数
    mysqladmin -uroot -p variables
    关注max_connections 、max_user_connections、wait_timeout 

<h2 id="6">6 坑记录</h2>
<h2 id="6.1">6.1 mysql密码丢失</h2>
> ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: NO)

    # mysql_secure_installation  根据提示操作即可,可重设密码 

> 老版本

    # /usr/sbin/mysqld stop
    # mysqld_safe --user=mysql --skip-grant-tables --skip-networking &
    # mysql -u root mysql
    mysql> UPDATE user SET Password=PASSWORD('XXX') where USER='root';
    mysql> UPDATE user SET authentication_string=PASSWORD('XXX') where USER='root'; (mysql 5.7版本用这个)
    mysql> FLUSH PRIVILEGES;
    mysql> quit

[http://www.cnblogs.com/qianxiaoruofeng/p/5774104.html](http://www.cnblogs.com/qianxiaoruofeng/p/5774104.html "")
[阿里云CentOS-7.2安装mysql]

[http://blog.csdn.net/qustdjx/article/details/26937325/](http://blog.csdn.net/qustdjx/article/details/26937325/ "")[MySQL远程连接ERROR]

    mysql> show databases;
    mysql> select * from mysql.user;
    设置密码
    # /usr/bin/mysqladmin -u root password 'new-password'
    或者
    # /usr/bin/mysql_secure_installation
    指定路径，重新安装数据库
    # /usr/bin/mysql_install_db --datadir /mnt/xvdb1/mysql/ --user=mysql
<h2 id="6.2">6.2 iptables save报错</h2>
> Centos7执行service iptables save报错

    systemctl stop firewalld 关闭防火墙
    yum install iptables-services 安装或更新服务
    systemctl enable iptables 启动iptables
    systemctl start iptables 打开iptables
    service iptables save

<h2 id="6.3">6.3 部署到SSD</h2>
fdisk新盘，p查看 n新增 p主分区 1分区号 +390G大小 w写分区表

    mkfs -t ext3 -c /dev/vdb1 (检查坏道，超级慢)
	mkfs -t ext3 /dev/vdb1 (比较快)
    mkdir -p /mnt/vdb1/mysql
    mount /dev/vdb1 /mnt/vdb1/mysql

    将数据目录修改为SSD盘的路径,vi /etc/my.cnf
    #datadir=/var/lib/mysql
    datadir=/mnt/vdb1/mysql

    [root@mysql home]# chown mysql:mysql /mnt/vdb1/mysql/

<h2 id="6.4">6.4 tar.gz解压报错</h2>

    # tar -zxvf geronimo-tomcat7-javaee6-3.0.1-bin.tar.gz 
    报下面的错
    gzip: stdin: not in gzip format
    tar: Child returned status 1
    tar: Error is not recoverable: exiting now
    检查文件的格式
    # file geronimo-tomcat7-javaee6-3.0.1-bin.tar.gz 
    geronimo-tomcat7-javaee6-3.0.1-bin.tar.gz: HTML document, ASCII text, with very long lines

> 重新安装数据库

    /usr/bin/mysql_install_db --datadir /mnt/xvdb1/mysql/ --user=mysql

<h2 id="7">7 关键的启动</h2>
<h2 id="7.1">7.1 tomcat启动</h2>
    sh /home/apache-tomcat-7.0.79/bin/startup.sh
<h2 id="7.2">7.2 geronimo启动</h2>
    /home/geronimo-tomcat7-javaee6-3.0.1/bin/startup

<h2 id="8">8 其它</h2>
<h2 id="8.1">8.1 解压缩</h2>
    把文件abc.txt和目录dir1压缩成为yasuo.zip
    ＃ zip -r yasuo.zip abc.txt dir1
    解压缩
    # unzip yasuo.zip

<h2 id="8.1">8.1 测试注意事项</h2>
每次测试前执行

Reset DayTrader (to be done before each run)

<h2 id="8.2">8.2 Jmeter Error率高</h2>
Jmeter老是报socket错误:

java.net.SocketException: No buffer space available (maximum connections reached)

java.net.ConnectException: Connection timed out: connect

    如下报存为reg文件，导入注册表
    Windows Registry Editor Version 5.00
    
    [HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\services\Tcpip\Parameters]
    "MaxUserPort"=dword:0000fffe
    "TCPTimedWaitDelay"=dword:0000001e

[https://stackoverflow.com/questions/10088363/java-net-socketexception-no-buffer-space-available-maximum-connections-reached](https://stackoverflow.com/questions/10088363/java-net-socketexception-no-buffer-space-available-maximum-connections-reached)


<h2 id="8.3">8.3 Jmeter JVM</h2>
    vi /bin/jmeter.bat
    set HEAP=-Xms256m -Xmx256m
    set NEW=-XX:NewSize=128m -XX:MaxNewSize=128m
    改为：
    set HEAP=-Xms256m -Xmx1024m
    set NEW=-XX:NewSize=128m -XX:MaxNewSize=512m

<h2 id="8.4">8.4 内核参数调整</h2>
暂时不需要，只是记录。

    sysctl -w net.ipv4.tcp_mem=786432 1048576 1572864;
    sysctl -w net.ipv4.tcp_wmem=8192 436600 873200;
    sysctl -w net.ipv4.tcp_rmem=32768 436600 873200;
    sysctl -w net.ipv4.tcp_window_scaling=1;
    sysctl -w net.core.netdev_max_syn_backlog=400000;
    sysctl -w net.core.optmem_max=10000000;
    sysctl -w net.core.rmem_default=10000000;
    sysctl -w net.core.rmem_max=10000000;
    sysctl -w net.core.wmem_default=11059200;
    sysctl -w net.core.wmem_max=11059200;
    sysctl -w net.ipv4.tcp_keepalive_time=1800;
    sysctl -w net.ipv4.tcp_keepalive_intvl=30;
    sysctl -w net.ipv4.tcp_keepalive_probes=3;
    sysctl -w net.ipv4.tcp_sack=1;
    sysctl -w net.ipv4.tcp_fack=1;
    sysctl -w net.ipv4.tcp_timestamps=1;
    sysctl -w net.ipv4.tcp_syncookies=1;
    sysctl -w net.ipv4.tcp_tw_reuse=1;
    sysctl -w net.ipv4.tcp_tw_recycle=1
    sysctl -w net.ipv4.tcp_fin_timeout=30;
    sysctl -w net.ipv4.ip_local_port_range=1024 65000;
    sysctl -w net.ipv4.tcp_max_syn_backlog=2048;
    sysctl -p;

<h2 id="9">9 资源采集</h2>
    yum install sysstat

[https://repo.mysql.com/](https://repo.mysql.com/)[mysql的repo]


[https://www.ibm.com/developerworks/cn/cloud/library/1310_xiali_daytrader/](https://www.ibm.com/developerworks/cn/cloud/library/1310_xiali_daytrader/)[自动部署和安装Daytrader应用]

[http://download.h3c.com.cn/download.do?id=2514797](http://download.h3c.com.cn/download.do?id=2514797)[H3C_CAS_JMeter性能测试操作指导书]


<h2 id="10">10 参考文献</h2>
[https://sourceforge.net/projects/hdparm/](https://sourceforge.net/projects/hdparm/) [查看硬盘cache]
