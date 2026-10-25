# Hardware safety / 硬件安全

## 中文

### 启动与停止

- SDK 启动可能使能、回零或进入跟随。启动前固定两臂、清空运动区，并准备从运动区外可操作的物理停机手段。
- 同一从臂只运行一个控制器；切换遥操与模型前停止旧控制程序。
- 退出程序、Ctrl+C 或停止发布目标后，SDK 可能继续执行或保持最后目标。录制程序不控制机械臂停机。
- 当前系统不提供碰撞检测、自动避障、标定后的力限制或安全认证急停。

### 当前实现

- `trial50.py` 的模型输出经验阈值主要作为日志告警。反馈速度、跟踪误差和推理期间位移的部分检查已注释。
- 软件关节限位与插值由原厂 SDK 处理。
- `move_to_demo_start.py` 绑定本次示范初始姿态和固定 SDK 二进制偏移；`sdk_online_latch_repro.py` 绑定特定 ABI。更换 SDK 需重新适配二进制布局和接口。
- 自动测试仅覆盖静态代码与配置生成，不连接硬件。

## English

### Startup and shutdown

- SDK startup can enable, home or start following. Secure both arms, clear the workspace and provide a physical stopping method accessible from outside the motion area.
- Run one controller per follower. Stop the previous controller before switching between teleoperation and policy control.
- After program exit, Ctrl+C or stopped publication, the SDK can continue toward or hold its last target. Recording does not stop the robot.
- The current system has no collision detection, obstacle avoidance, calibrated force limits or safety-certified emergency stop.

### Implementation

- Empirical model-output thresholds in `trial50.py` mainly produce warnings. Some feedback-speed, tracking-error and motion-during-inference checks are commented out.
- The vendor SDK handles software joint limits and interpolation.
- Return and diagnostic tools depend on this experiment's start pose, SDK binary layout and ABI. A different SDK requires renewed interface/layout adaptation.
- Automated tests check source and configuration only, without hardware access.
