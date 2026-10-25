# Safety and prototype limits / 安全与原型边界

## 中文

本项目是研究原型，不是经过安全认证的机器人控制系统。软件测试、收到 ROS/CAN 数据和模型 loss 均不能认证安全运动。

- 克隆、检查、生成配置不启动硬件；原厂 SDK 启动、遥操与显式执行命令可能立即使能、回零或运动。
- 同一从臂只能有一个控制者。切换遥操/模型前停止旧控制程序，确认实际设备身份及当前姿态。
- 必须现场确认安装牢固、运动区清空、夹爪/物品条件及可实际执行的停机手段。软件退出、Ctrl+C、关闭录像或不再发送目标，不保证 SDK/电机立即停止。
- 原型没有经认证的碰撞检测、自动避障、力限制或急停。软件 joint bounds 不是碰撞安全认证。
- 速度、跟踪、推理期间位移检查曾被现场修改或注释。导出源码保留现状；旧 POLICY 常量、注释、日志中的检查名称并不证明检查仍启用。
- `move_to_demo_start.py` 包含记录姿态和二进制偏移读取，`sdk_online_latch_repro.py` 包含特定 SDK ABI 的离线 ctypes 复现实验；后者不应被当成通用驱动工具。不得在未经审查的新库上替换 hash 后直接运行。
- `trial50.py` 模型输出经验阈值主要记录告警；其返回 `passed` 不是物理安全许可。不要根据文件名或旧报告推断现有保护能力。
- 应先进行静态检查、硬件身份核对、只读观测及现场审查；本仓库 CI 不运行任何硬件模块。

公开或部署前，应由实际执行团队重新审查控制与停机机制；本仓库不对尚未验证的保护作保证。

## English

This research prototype is not a safety-certified robot controller. Software tests, received ROS/CAN frames and model loss do not certify safe motion.

Cloning, static checks and configuration rendering do not start hardware. SDK startup, teleoperation and explicit execution can enable, home or move it. Use exactly one follower controller and verify physical identity and pose before switching control.

An onsite operator must verify mounting, workspace, gripper/object conditions and an effective shutdown procedure. Exiting software, Ctrl+C, stopping recording or ceasing publication does not guarantee immediate stop; the SDK can retain its last target.

There is no certified collision avoidance, force limit or emergency stop. Some feedback/speed/motion-during-inference checks were disabled onsite and remain so in this historical export. Constants, old comments and log labels are not evidence of active guards. Empirical output warnings and `passed` are not physical safety authorization.

Return and ctypes diagnostic tools are tied to a specific pose/SDK ABI. Do not bypass review by changing their hash for a different library. CI only checks source/configuration and never exercises hardware. The operating team must review control and stopping behavior before deployment or public release.
