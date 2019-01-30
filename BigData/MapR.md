* [安装MapRPS](#1)
* [测试内存](#2)
* [测试本地盘](#3)
* [测试网络](#4)
   * [iperf带宽](#4.1)
   * [rpctest传输速率](#4.2)
* [ClusterShell集群管理](#5)
<h2 id="1">安装MapRPS</h2>
    yum install wget -y
    wget https://github.com/MapRPS/cluster-validation/archive/master.zip
    unzip master.zip

<h2 id="2">测试内存</h2>

只关注Triad的结果

    for i in `seq 1 10`
    do
      #sh memory-test.sh | grep -e ^Func -e ^Triad | tee ./result/memory-test$i.log
      sh memory-test.sh  | tee ./result/memory-test$i.log
    done

内存时延

    ./lat_mem_rd 1 16

<h2 id="3">测试本地盘</h2>

    --BLOCK-COMMENT--的注释必须去掉，否则报错
    ./disk-test.sh: line 228: warning: here-document at line 152 delimited by end-of-file (wanted `--BLOCK-COMMENT--')
    ./disk-test.sh: line 229: syntax error: unexpected end of file
    
    sh disk-test.sh
    #--destroy时会执行iozone
    sh disk-test.sh --destroy
    sh summIOzone.sh

实际命令

pre-install/iozone -I -r 1M -s 4G -k 10 -+n -i 0 -i 1 -i 2 -f /dev/sdb


<h2 id="4">测试网络</h2>

建立互信

    vi /root/host.list
    sh network-test.sh | tee network-test.log

<h2 id="4.1">iperf带宽</h2>

    ./iperf -s
    iperf -c 192.168.0.106 -t 30 -P1

numa方式

    #numanode0="0-11,24-35"
    #numanode1="12-23,36-47"
    taskset $numanode0 $iperfbin -s > /dev/null
    或
    taskset $numanode1 $iperfbin -s -p $port2 >/dev/null

<h2 id="4.2">rpctest传输速率</h2>

    ./rpctest -server
    ./rpctest -client -b 32 5000 IP

<h2 id="5">ClusterShell集群管理</h2>

    yum install clustershell
    vi /etc/clustershell/groups.d/local.cfg
    all: 192.168.0.229,192.168.0.51

运维利器-ClusterShell集群管理

https://blog.csdn.net/fanren224/article/details/73320749