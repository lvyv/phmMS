# 一、快速开始

1.进入一个干净的目录，确保能在命令行直接运行python的命令为python3.7以上。
```
PS E:\document\source\repos\pytest> python --version
Python 3.9.7
```
2.创建虚拟环境。
```
PS E:\document\source\repos\pytest> python -m venv py397
PS E:\document\source\repos\pytest> . .\py397\Scripts\activate
(py397) PS E:\document\source\repos\pytest>
```
3.下载源码。
```
(py397) PS E:\document\source\repos\pytest> git clone https://github.com/lvyv/phmMS.git
Cloning into 'phmMS'...
remote: Enumerating objects: 108, done.
remote: Counting objects: 100% (108/108), done.
remote: Compressing objects: 100% (68/68), done.
remote: Total 108 (delta 35), reused 103 (delta 30), pack-reused 0 eceiving objects:  77% (84/108), 1.61 MiB | 242.00 KiBReceiving objects:  83% (99/108), 1.61 MiB | 242.00 KiB/s
Receiving objects: 100% (108/108), 1.70 MiB | 217.00 KiB/s, done.
Resolving deltas: 100% (35/35), done.
```
4.安装依赖包。

```
(py397) PS E:\document\source\repos\pytest> cd .\phmMS\
(py397) PS E:\document\source\repos\pytest\phmMS> pip install -r .\requirements.txt
```
5.运行程序。
```
(py397) PS E:\document\source\repos\pytest\phmMS> cd .\tests\
(py397) PS E:\document\source\repos\pytest\phmMS\tests> $Env:PYTHONPATH = "..;../app"
(py397) PS E:\document\source\repos\pytest\phmMS\tests> python test_phmMS.py
INFO: Sat 20 Nov 2021 17:09:09 test_phmMS.py ********************  CASICLOUD AI METER services  ********************
INFO: Sat 20 Nov 2021 17:09:09 test_phmMS.py phmMS tables were created by import statement ['req_history', 'api_token', 'public.xc_equipment'].
INFO: Sat 20 Nov 2021 17:09:09 test_phmMS.py phmMS micro service starting at 0.0.0.0: 29081
INFO: Sat 20 Nov 2021 17:09:10 main.py Worker Thread:  14500     tables ['req_history', 'api_token', 'public.xc_equipment'].
INFO: Sat 20 Nov 2021 17:09:10 main.py Worker Thread:  11488     tables ['req_history', 'api_token', 'public.xc_equipment'].
INFO: Sat 20 Nov 2021 17:09:10 main.py Worker Thread:   9376     tables ['req_history', 'api_token', 'public.xc_equipment'].
```
6.访问地址[https://127.0.0.1:29081/docs](https://127.0.0.1:29081/docs)。
在POST /api/v1/equipment/item/{counts}输入counts值为希望的记录数，比如1000，将在tests目录产生1000行记录。
注意，每次调用接口，将会在原来数据库追加数据。

# 二、设备健康模型调度器开发环境

1.使用pycharm ide打开根目录。

2.在settings中添加python3的环境（可能需要添加各种第三方包）。

3.设置代码目录为app（调度），physics（模型）。

4.添加一个启动项，指向tests目录的test_phmMS.py，test_phmMD.py两个文件为启动入口，分别启动调度微服务和模型微服务。

5.启动mock程序模仿外部资源，比如数据资源集成分系统的各种数据集市api。


# 三、代码静态分析
1.启动sonarqube
2.下载安装sonarscanner（绿色软件需要设置其bin目录到环境变量path；设置conf下的sonar-sonar.host.url=http://192.168.47.144:9119）
3.执行命令
```
sonar-scanner.bat -D"sonar.projectKey=97875a8430eaf4fe582e2c31401d12620eb4dba7" -D"sonar.sources=." -D"sonar.host.url=http://192.168.47.144:9119" -D"sonar.login=97875a8430eaf4fe582e2c31401d12620eb4dba7"
```

# 四、待办事项

1.对于给定的时间窗口，返回soh和扩展值

包含实时计算和历史查询返回两个逻辑。如果startts==0，endts==0，则实时计算；如果startts和endts差是一个区间，则查询历史值。

1.1.实时计算

soh的api调用下发后，计算出soh，并且返回，还要publish到mqtt。

a）计算soh

b）写入数据库（既要写入req表，还要写入equipment表NOK）

c）发送到mqtt

1.2.历史查询（NOK）

不调用模型，直接从数据库的equipment取出历史区间的值。

ts：[]

soh:[]



【注意】实时计算的时候产生的这个指标计算值在后面可以通过一个定时任务，每天算一次，从而得到历史趋势指标值（NOK），需要提供微服务接口。

当前可以先利用/api/v1/equipment/item/{counts}修改得到仿真数据。
