
## 1.引言
### 1-1.目的
​	编写本需求规格说明书目的是为了以系统建设要求为指导，结合对需求收集，及基本需求的分析汇总，形成调研阶段的分析结果。

​	本文档是对功能模块的基本需求功能特性的描述，用于定义项目范围，明确开发需求，并为后期的分析设计、代码实现和测试提供指导。

1.分析设计，以本需求规格说明书为标准完成总体设计和详细设计；  

2.代码实现，以本需求规格说明书为标准，并结合总体设计、详细设计完成代码编写；  

3.测试，以本需求规格说明书为标准，结合分析设计完成单元测试用例和系统测试用例编写和测试。

### 1-2.背景
​	本次待开发的软件为“Plant VS Zombies(暂定)”。

​	玩家可以在该小游戏中重温经典的塔防策略游戏玩法，合理排布自己的武器来守卫阵地！


### 1-3.定义

| 序号    |  名称   |   定义  |
| --- | --- | --- |
|  1   |  Python   |   Python是一种跨平台的计算机程序设计语言，是一种面向对象的动态类型语言。  |
|  2   |  Pygame   |   Pygame是利用SDL库的写就的游戏库， 是用来开发游戏软件的 Python 程序模块。pygame允许你在 Python 程序中创建功能丰富的游戏和多媒体程序，是一个高可移植性的模块，可以支持多个操作系统，非常适合进行游戏开发。  |

### 1-4.文档范围
​	本需求规格说明书对产品功能模块的功能定义、接口定义、UI设计、以及其他研发约束条件等研发需求做了详细定义。


### 1-5.读者对象
1.项目经理：项目经理可以根据该文档了解产品的预期功能，并据此进行程序设计、项目管理。  

2.设计人员：对需求进行分析，并设计出系统，包括数据库的设计。  

3.开发人员：配合《详细设计说明书》，了解程序功能，进行程序编码设计。  

4.测试人员：根据本文档编写测试用例，并对产品进行功能性测试和非功能性测试。  

5.用户：了解预期产品的功能和性能，并与分析人员一起对整个需求进行讨论和协商。

### 1-6.参考文献
暂无


## 2.项目概述
### 2-1.产品概述
​	基于经典**策略塔防游戏**植物大战僵尸设计的关卡、武器与敌人，重温经典塔防的魅力

​	不断更新**新的关卡**，让玩家始终有所挑战

​	**无尽模式**，看看你可以坚持多久！

​   解锁**玩家技能**，发现新的有趣御敌方法！

### 2-2.产品功能
   游戏本身是很好的娱乐方式，但现在的许多游戏过分强调了竞技性与商业性，使游戏无法使玩家真正放松。
   
   我们要做的就是一款诙谐幽默、轻松写意的游戏。玩游戏的本质应当是快乐！



### 2-3.用户特点
​	本软件面向的主要用户是热爱游戏的玩家群体，其主要特点是希望游戏中含有尽量少的商业元素，单纯享受游戏的快乐。


### 2-4.一般约束
​	进行本软件开发工作的约束条件如下：

​   开发周期短：两个月的开发时间需要开发队合理规划时间，做到多项任务并发。

​   采用的方法与技术有限：鉴于所学知识与编程经验的缺乏，项目团队成员的技术水平不够成熟较低，需要在开发过程中学习编程技术，提高软件开发能力。


### 2-5.假设与依据
​	本项目是否能够成功实施，主要取决于以下的几点：

​   团队成员的积极合作配合，为了项目的开发和实施，要求每个团队成员对个人时间进行合理规划，配合其他成员完成任务。

​   完成该项目的必要知识，包括编程语言的掌握与理解程度，游戏的合理设计等  

​   团队负责人协调各部分开发团队，激励队伍的能力。


## 3.具体需求
​  首先我们以UML类图简单地考量软件中各类的关系  
https://raw.githubusercontent.com/AllenW1998/imgplays/master/UML.png  



### 3-1.功能需求(每个功能下面应配一张游戏里的画面；最后应该整合一个UML类图确定玩家类和系统类的交互)

**主菜单**

​	打开游戏后，点击“新的游戏”，跳转到创建存档界面；点击“继续游戏”，跳转到选择存档界面，选择存档后跳转到“选择关卡”界面；点击“无尽模式”，直接进入游戏画面；点击“退出游戏”，关闭程序回到桌面；点击左上方的“技能树”，可以查看已解锁的技能；




**创建存档界面**

​	进入该界面后，在“存档名字”输入框填入存档名字，点击保存按钮进行保存。如果现有的存档已经有三个，弹出提示“需要删掉一个存档！”




**选择关卡界面**

​	点击界面中的关卡，可直接进入对应关卡游戏画面




**游戏画面**

​	中间的空地是玩家布置防御措施的地方，敌人将从画面右部不断袭来；画面上方的条形栏是可以选择的防御措施；点击画面右上角的“小铲子”可以进入撤销防御措施模式；画面下部的条形栏是当前可以释放的技能；



**布置防御**

​	用鼠标将上方条形栏中的防御措施拖动到空地处即可在对应空地上建立；



**撤销防御**

​	点击画面右上角的“小铲子”可以进入撤销防御措施模式，点击对应的防御措施可以将其撤销；



**释放技能**

​	将下方条形栏中的技能用鼠标拖动到画面中即可在对应位置释放技能




**暂停游戏**

​	点击画面右上角的暂停标志，可将游戏暂停；




**保存游戏**

​	在完成一个关卡后，系统将自动保存当前进度；









### 3-2.外部接口需求
#### 用户接口
​	无特殊需求


#### 硬件接口
​	无特殊需求


#### 软件接口
​	操作系统：WIndows 7.0及以上

​	数据库：MYSQL*

​	开发工具：Python 3.0上


#### 通信接口
​	暂不支持联网


### 3-3.性能需求

1. 存档名字按照规定的数据格式输入，否则系统提示错误并要求重新输入。  

2. 游戏界面中，鼠标点击的延迟不应超过0.5s。  

3. 要求数据库有很好的更新能力。  

4. 能够适应迭代开发。




## 4.属性
### 4-1.可用性
1. 易操作，易理解。界面设计简洁易用。  

2. 稳定性：游戏会更新增加玩家技能、新的关卡等，不断修复bug，使系统更加稳定。  

3. 操作完成时有统一规范的提示信息。例如删除存档时，系统可提示警示框“您确认删除吗？”，玩家点击确认后，系统才执行删除操作，删除后可直接返回相关页面。



### 4-2.可维护性
1. 保留系统对应的版本的源代码，并在每次更新后撰写日志。

2. 代码应当有清晰易懂的注释，有清晰的系统结构，命名规范，界面规范。  

3. 程序应有清晰易懂的提示和帮助信息的错误信息可以帮助用户排除错误，正确运行程序。  

4. 项目启动后，需要执行完整的系统配置管理。 维护配置仍然需要在项目结束之前不断更新系统配置信息。 根据模块，将系统分为配置项，并记录系统的各项维护工作，以备将来检查。

### 4-3.验证验收标准
#### 文档验收标准
1. 项目开发计划  

2. 软件需求说明书  

3. 各阶段项目开发进度汇总报告  

4. 项目总结报告

#### 软件验收标准
Setup安装包


#### 界面验收标准

|  序号   |  名称   |  描述   |
| --- | --- | --- |
|   1  |   主菜单  | 待添加……    |
|   2  | 创建存档    |     |
|  3   |   选择存档  |     |
|  4  |   选择关卡  |     |
|   5 |   无尽模式  |     |
|  6   |  技能树   |     |
|  7  |   游戏画面  |     |

#### 功能验收标准

|   序号  |   名称  |    描述 |
| --- | --- | --- |
|   1  |  创建存档   |  待添加……   |
|    2 |  选择关卡   |     |
|   3  |   布置防御  |     |
|    4 |   撤销防御  |     |
|  5   |   使用技能  |     |
|  6   |  暂停游戏   |     |
|   7  |保存游戏     |     |

#### 其他验收标准

