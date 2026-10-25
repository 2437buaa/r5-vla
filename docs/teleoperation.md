# Teleoperation / 主从遥操作

## 中文

主臂使用原厂重力补偿模式，从臂跟随六轴与夹爪。SDK 启动可能使能和回零；启动前固定两臂、清空工作区，夹爪保持空载。

1. 使用 `/dev/serial/by-id/` 中的适配器身份，将主臂绑定 `can0`、从臂绑定 `can1`。适配器为 CANable2，使用 SLCAN 固件。
2. 所有 SDK 停止后，在两个终端分别启动 CAN 会话并保持终端打开。工具要求目标接口尚未创建。

```bash
sudo /usr/bin/python3 runtime/host/open_sdk_can.py --arm master
```

```bash
sudo /usr/bin/python3 runtime/host/open_sdk_can.py --arm follower
```

总线速率为 1 Mbps，电机反馈可能在 SDK 初始化后开始。

3. 在新的终端进入 ROS 环境。以下路径示例需替换为自己的路径：

```bash
source /opt/ros/humble/setup.bash
source /home/robot/r5_teleop_ws/install/setup.bash
export ROS_DOMAIN_ID=85 ROS_LOCALHOST_ONLY=1
```

4. 使用普通夹爪 1:1 wrapper，将两臂准备在接近匹配的初始化位形。先启动从臂，稳定后在另一终端启动主臂；双方稳定后开始拖动：

```bash
ros2 launch runtime/host/launch/one_master_one_slave.launch.py \
  enable_master:=false enable_follower:=true
```

```bash
ros2 launch runtime/host/launch/one_master_one_slave.launch.py \
  enable_master:=true enable_follower:=false
```

主臂模式为 `remote_master`，从臂为 `remote_slave`，普通夹爪 `arm_end_type=0`。六轴为 1:1；修改后的 wrapper 去掉了位置夹爪跟随的 ×5。模板 YAML 中的 ×5 注释对应原厂未修改版本。

只读观察：

```bash
ROS_DOMAIN_ID=85 ros2 topic echo /r5_pair/follower_status --once
/usr/bin/python3 runtime/host/check_dual_can_feedback.py
```

结束时先停止 SDK，再退出 CAN 会话。SDK 的目标保持与停机行为见[安全说明](safety.md)。

## English

The leader uses vendor gravity compensation; the follower tracks arm joints and gripper. SDK startup can enable/home the arms. Secure both arms, clear the workspace and keep grippers unloaded before startup.

Bind adapters by stable identity: leader `can0`, follower `can1`. With SDKs stopped and interfaces not yet created, run each CAN session in its own terminal. The adapter is CANable2 with SLCAN firmware at 1 Mbps.

Source ROS and the workspace, using domain 85 and localhost-only DDS. Prepare matching initialization poses; start the follower, then the leader after stabilization. Begin dragging once both are stable. The modified wrapper uses 1:1 arm and ordinary-gripper mapping; the YAML ×5 comment describes the original vendor implementation.

Stop SDKs before closing CAN sessions. See [safety](safety.md) for target-holding and stopping behavior.
