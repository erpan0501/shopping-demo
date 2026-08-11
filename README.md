# Java 商城项目（本地演示整理版）

## 直接演示

双击根目录的 `启动.command`，或在终端执行 `./启动.command`，会同时启动商城端 Vue（8081）、管理端 Vue（8082）和 Java 后端（8090）。停止时执行 `./关闭.command`；日志保存在 `.run/`。

只启动不依赖外部基础设施的本地演示服务：

```bash
mvn -pl shopping_demo spring-boot:run
```

打开 `http://localhost:8081` 进入商城端，`http://localhost:8082` 进入管理端。Java 后端端口为 `8090`。

## 原有微服务

原有商品、用户、订单、搜索、秒杀、支付、客服等 Maven 模块保留在仓库中，用于后续继续接入 Nacos、MySQL、Redis、RocketMQ、Elasticsearch 等基础设施。本地演示阶段不自动启动这些模块。

全量源码现在使用中性的 `com.localdemo` 包名；如需仅验证编译，可执行：

```bash
mvn -DskipTests package
```
