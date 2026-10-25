# ARX wrapper integration / ARX 包装层集成

## 中文

`R5Controller.cpp` 基于固定版本的 ARX R5 ROS2 wrapper，采用 BSD-3-Clause。完整 SDK、共享库、URDF 和消息包按 [setup](../../docs/setup.md) 从上游获取。

本地修改：

1. 发布普通/VR 状态前检查位置、速度、电流数组长度，复制循环按 ROS 消息数组长度运行，修正 `i<=7` 等越界风险。
2. `FollowCmdCallback` 的位置夹爪分支由 `setCatch(msg->joint_pos[6] * 5)` 改为 `setCatch(msg->joint_pos[6])`，用于两台普通夹爪 R5。六轴本来就是 1:1；未改扭矩分支或底层 SDK。
3. 在 `arm_control/package.xml` 增加 `<export><build_type>ament_cmake</build_type></export>`，修复 colcon 将其识别为 ROS1/catkin 的问题。

在新建 workspace 中，用本文件替换 `arx_r5_controller/src/R5Controller.cpp`，重新编译后加载对应的 `install/setup.bash`。初始化与运行方式见[遥操指南](../../docs/teleoperation.md)。

## English

The C++ file derives from the pinned ARX ROS2 wrapper under BSD-3-Clause. Obtain the SDK, shared libraries, URDFs and message packages through [setup](../../docs/setup.md).

Changes bound feedback copies/check short arrays before normal/VR publication and remove the ordinary-gripper position-follow ×5. Six arm joints were already 1:1; torque control and the underlying SDK are unchanged. Separately declare `ament_cmake` in the arm_control package export to fix colcon classification.

Replace `arx_r5_controller/src/R5Controller.cpp` in a new workspace, rebuild and source its `install/setup.bash`. See [teleoperation](../../docs/teleoperation.md) for initialization and startup.
