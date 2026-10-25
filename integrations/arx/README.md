# ARX wrapper integration / ARX 包装层集成

## 中文

`R5Controller.cpp` 来自固定版本的 ARX R5 ROS2 wrapper，保留 BSD-3-Clause 许可，修改在文件头和本节披露。完整 SDK、共享库、URDF、消息包、编译产物不随本项目转载，按 setup 指南从原厂获取。

本地修改：

1. 发布普通/VR 状态前检查位置、速度、电流数组长度，复制循环按 ROS 消息数组长度运行，修正 `i<=7` 等越界风险。
2. `FollowCmdCallback` 的位置夹爪分支由 `setCatch(msg->joint_pos[6] * 5)` 改为 `setCatch(msg->joint_pos[6])`，用于两台普通夹爪 R5。六轴本来就是 1:1；未改扭矩分支或底层 SDK。
3. 单独需要在 `arm_control/package.xml` 增加 `<export><build_type>ament_cmake</build_type></export>`，避免 colcon 误识别为 ROS1/catkin。这是构建元数据修改，不是控制算法。

在新建 workspace 中，将本文件复制替换原厂对应的 `arx_r5_controller/src/R5Controller.cpp`，保留上游原件，重新编译并核对实际加载的 install 路径。不要覆盖运行中的旧安装或把二进制 SHA 作为已完成设备匹配的证明。原型重力补偿、初始化和夹爪语义仍需现场核验。

## English

The attributed C++ file derives from the pinned ARX ROS2 wrapper and retains BSD-3-Clause terms. Obtain full SDKs, shared libraries, URDFs and message packages directly from the vendor; they are not redistributed here.

Changes bound feedback copies/check short arrays before normal/VR publication and remove the ordinary-gripper position-follow ×5. Six arm joints were already 1:1; torque control and the underlying SDK are unchanged. Separately declare `ament_cmake` in the arm_control package export to fix colcon classification.

Apply the wrapper only in a new workspace, preserve originals, rebuild and verify the actual installation loaded. Do not overwrite a running installation. A matching binary hash does not certify hardware compatibility, initialization or gripper behavior.
