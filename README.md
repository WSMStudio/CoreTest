## 核心代码测试阶段
### `Proximity Search`开发阶段

运行以下命令
```shell
python tests.py
```
然后访问
```text
localhost:8000
```
在搜索框中输入
```text
and pre/2 obtained
```
点击搜索按钮，得到查询结果：同时含有and和obtained的上下文，从and前5个单词到obtained后5个单词结束。

已知BUG：
+ `and pre/1 the`查不到结果，算法有问题