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
to /4 the
to pre/4 the
to pre/d^4 the
```
点击搜索按钮，或在输入框中回车，得到查询结果：同时含有to和the的上下文，从to前5个单词到the后5个单词结束。

已知鲁棒性：
+ 命令不完整返回错误码`{"code": -1}`
+ 结果为空返回空列表，显示`No result found`

TODO列表:
+ 实现空格查询的等价

