# R5 VLA 中文指南

[English](README.en.md) · [项目首页](README.md)

## 概览

本项目整理了 ARX R5 从遥操、数据采集到 LingBot-VLA 真机部署的完整工程流程。采集是两台机械臂一主一从；模型任务只有一台执行臂。相机为从臂腕部和外部固定 Gemini 305。Ubuntu 22.04、ROS 2 Humble、系统 Python 3.10 用于硬件侧，训练及推理使用独立服务器环境。

工程代码位于 `reference/host/*.in`。`scripts/materialize.py` 根据本地配置替换路径和设备身份，生成 `runtime/` 运行目录。本地配置与运行产物均在 `.gitignore` 中。

## 使用流程

1. [安装依赖](docs/setup.md)：ROS 2、原厂 SDK、相机驱动及训练环境。
2. 配置 `config/site.local.json`，生成本地运行目录。
3. [启动遥操](docs/teleoperation.md)：主臂 `can0`，从臂 `can1`，普通夹爪采用 1:1 映射。
4. [录制示范](docs/recording.md)：启动双相机，完成 test-only 测试后批量采集并标注回合。
5. [处理数据](docs/data-format.md)：校验消息、时间戳和标签，完成双视角与从臂状态对齐。
6. [训练模型](docs/training.md)：服务器完成数据准备、基座校验及双 GPU 训练。
7. [部署策略](docs/deployment.md)：启动推理服务，建立 SSH 隧道，进行只读预览和模型执行。
8. 独立录制测试回合，导出双视图 MP4。

硬件启动与控制模式切换见[安全说明](docs/safety.md)。

## 实验配置

任务为 `Put the charger in the box`。四批正式记录中选取 71 条人工标注成功示范，共 24,576 帧；全部用于训练，没有独立验证集。独立从官方 `robbyant/lingbot-vla-v2-6b` 基座开始，两张 GPU，global batch 32，训练 4000 次更新，2000/4000 步分别保存。

部署输入为双 RGB、从臂六轴绝对位置与夹爪原生值、任务文本。模型输出未来 50 条七维绝对目标，每段按名义 30 Hz 发布，执行完再重新观察；推理等待会打断连续发布节拍。500 是目标条数上限，不是 500 个闭环推理回合。

一次测试记录发送 300 条模型目标，由操作员按回车结束并标记完成。当前没有自动成功判定或完整的成功率统计，详见[实验记录](docs/provenance.md)。

## 适配新环境

- 训练脚本包含该实验的 session 清单、71/12 条数据计数及 2000/4000 步设置。更换数据集时一并更新。
- 部分执行和归位工具绑定特定 SDK SHA、二进制布局及示范初始姿态。
- 速度、跟踪等反馈检查的当前状态见[安全说明](docs/safety.md)。
