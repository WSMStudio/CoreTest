## 核心代码测试阶段
### `Proximity Search`开发阶段

运行以下命令
```shell
python server.py
```
然后访问
```text
localhost:8000
```
在搜索框中分别输入以下命令进行测试
```text
to /1 the
to /2 the
to /3 the
to /4 the
```
点击搜索按钮，或在输入框中回车，得到查询结果：同时含有to和the的上下文，从to前5个单词到the后5个单词结束。

已知鲁棒性：
+ 命令不完整返回错误码`{"code": -1}`
+ 结果为空返回空列表，显示`No result found`

TODO列表:
+ 返回结果按照`docID`折叠
+ 支持同段查询，同句查询
+ 单独实现`Query Parser`
+ 实现无顺序查询
+ 实现空格查询的等价

