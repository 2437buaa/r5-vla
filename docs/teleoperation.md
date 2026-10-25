# Teleoperation / 主从遥操作

## 中文

本节包含会改变硬件状态的命令，**仅供现场操作员手动执行**。SDK 启动可能使能、回零并启动重力补偿或跟随；确认固定、工作区、夹爪空载和可用的现场停机方式。不靠“试动一下”识别主从设备。

1. 核对 `/dev/serial/by-id/` 中的两个适配器，将主臂绑定 `can0`、从臂绑定 `can1`。本项目仅保留已审查的 CANable2 SLCAN 固件路径，不能套用于任意 USB-CAN。
2. 所有 SDK 停止时，在两个终端分别运行下列 CAN 会话，并保持终端打开。工具要求目标接口不存在且没有 SDK 运行，不会自动清理现有会话。

```bash
sudo /usr/bin/python3 runtime/host/open_sdk_can.py --arm master
```

```bash
sudo /usr/bin/python3 runtime/host/open_sdk_can.py --arm follower
```

请求的总线速率为 1 Mbps。没有被动帧不等于总线故障；某些电机需要 SDK 初始化后才反馈。配置适配器不是电机健康验收。

3. 在新的终端进入 ROS 环境。以下路径示例需替换为自己的路径：

```bash
source /opt/ros/humble/setup.bash
source /home/robot/r5_teleop_ws/install/setup.bash
export ROS_DOMAIN_ID=85 ROS_LOCALHOST_ONLY=1
```

4. 确认已使用本仓库披露的普通夹爪 1:1 wrapper，且两臂接近匹配的初始化位形。在独立终端先启动从臂，稳定后启动主臂；双方稳定前不要拖动或操作夹爪：

```bash
ros2 launch runtime/host/launch/one_master_one_slave.launch.py \
  enable_master:=false enable_follower:=true
```

```bash
ros2 launch runtime/host/launch/one_master_one_slave.launch.py \
  enable_master:=true enable_follower:=false
```

主臂采用 `remote_master`，从臂采用 `remote_slave`，普通夹爪 `arm_end_type=0`。六轴原本为 1:1；本地修改仅去掉位置夹爪跟随的 ×5，不代表完成零位、行程、符号或夹持力标定。模板 YAML 的旧 ×5 注释描述旧原厂二进制，须以实际构建 wrapper 为准。

只读观察：

```bash
ROS_DOMAIN_ID=85 ros2 topic echo /r5_pair/follower_status --once
/usr/bin/python3 runtime/host/check_dual_can_feedback.py
```

ROS 消息数量不等于电机新鲜采样数量。先正常停止 SDK，再退出 CAN 会话；不可把 Ctrl+C 当作经认证的急停。录制工具不停止遥操。

## English

These are operator-run hardware commands. SDK startup can enable/home a robot and enter gravity compensation or following. Verify physical setup and shutdown procedures before running them.

Bind adapters by stable identity, not tty order: leader `can0`, follower `can1`. With SDKs stopped, run each CAN session in its own terminal. The reference assumes a reviewed CANable2 SLCAN firmware family at 1 Mbps; it is not a universal adapter driver.

Source ROS and the built workspace, use domain 85 and localhost-only DDS. With the documented ordinary-gripper 1:1 wrapper, prepare matching initialization poses; start the follower, then leader after stabilization. Do not manipulate either arm until both are stable. Six arm joints are already 1:1; removing the gripper ×5 does not calibrate zero, travel, direction or force.

Read-only ROS/CAN observations are communication evidence, not safety or fresh-motor-sample certification. Stop SDKs normally before closing CAN sessions. Ctrl+C and stopping recording are not guaranteed robot stops.
