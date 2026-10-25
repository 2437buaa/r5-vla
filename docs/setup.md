# Setup / 环境准备

## 中文

参考平台为 Ubuntu 22.04 x86_64、ROS 2 Humble、系统 Python 3.10。先按 [ROS 官方 Humble 安装说明](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html)安装 ROS；不要让 Conda Python 替代 ROS 的系统 Python。以下是依赖清单，不是已经执行的安装记录：

```bash
sudo apt-get update
sudo apt-get install --no-remove \
  ros-humble-desktop python3-colcon-common-extensions python3-rosdep \
  build-essential cmake git can-utils iproute2 usbutils v4l-utils rsync ffmpeg \
  libeigen3-dev liborocos-kdl-dev libusb-1.0-0-dev libgflags-dev libgoogle-glog-dev \
  libdw-dev libssl-dev nlohmann-json3-dev libyaml-cpp-dev libopencv-dev \
  ros-humble-kdl-parser ros-humble-orocos-kdl-vendor ros-humble-urdf \
  ros-humble-cv-bridge ros-humble-image-transport-plugins \
  ros-humble-camera-info-manager ros-humble-diagnostic-updater \
  ros-humble-tf2-sensor-msgs ros-humble-xacro ros-humble-robot-state-publisher \
  ros-humble-rosbag2 ros-humble-rosbag2-storage-mcap \
  python3-numpy python3-opencv python3-yaml python3-h5py python3-psutil
```

注意 KDL 的 ROS 包名是 `ros-humble-orocos-kdl-vendor`，不是 `ros-humble-orocos-kdl`。不配置免密 sudo，不覆盖 `.bashrc`，不更新固件，不默认执行相机厂家会删除其他规则的 udev 脚本。

### 固定源码

在自己选择的 vendor 目录手动获取依赖；仓库不包含这些完整源码或二进制：

```bash
git clone https://github.com/ARXroboticsX/R5.git vendor/R5
git -C vendor/R5 checkout --detach e87d09c11edb65f6ae672abc7a41fe2277a2f12f
git clone https://github.com/orbbec/OrbbecSDK_ROS2.git vendor/OrbbecSDK_ROS2
git -C vendor/OrbbecSDK_ROS2 checkout --detach c153462518ad674650bafa4464fda72c27ab797a
git clone https://github.com/robbyant/lingbot-vla-v2.git vendor/lingbot-vla-v2
git -C vendor/lingbot-vla-v2 checkout --detach be969b8fd117fb70550c5d4bf4bc328211b5b1b6
```

将 R5 上游 `ROS2/R5_ws/src/ARX_R5_ros2_V7/arx_r5_controller`、`ROS2/R5_ws/src/arxmsgros2/arm_control`、`ROS2/R5_ws/src/arxmsgros2/arx5_arm_msg` 和 Orbbec 源码放入独立 ROS workspace 的 `src/`。只在新工作区操作，保留原件。

按 [ARX 集成说明](../integrations/arx/README.md)采用修正后的 ROS wrapper，补齐 `arm_control/package.xml` 的 `ament_cmake` build type。依赖通过 `rosdep check` 核对后编译：

```bash
source /opt/ros/humble/setup.bash
cd /home/robot/r5_teleop_ws
export CMAKE_BUILD_PARALLEL_LEVEL=2 MAKEFLAGS=-j2
colcon build --executor sequential \
  --packages-up-to arm_control arx5_arm_msg arx_r5_controller orbbec_camera orbbec_description \
  --cmake-args -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF \
  -DPython3_EXECUTABLE=/usr/bin/python3 -DPYTHON_EXECUTABLE=/usr/bin/python3 \
  -DINSTALL_UDEV_RULES=OFF
```

这里只构建软件，不启动节点。USB 权限应按实际 PID、设备归属与组权限配置，避免全设备 `0666`。两台相机使用 USB3 接口；确认电源和带宽。

### 配置与生成副本

复制 `config/site.example.json` 为 `config/site.local.json`，填写自己的 ASCII 路径及两个 CAN 适配器序列号。生成器要求显式填写序列号且拒绝 shell/Python 注入字符；生成行为不证明身份正确。

```bash
python3 scripts/materialize.py --config config/site.local.json --output runtime
```

生成文件在 `runtime/host/`；训练 YAML 在 `runtime/train-config.yaml`。不要直接运行 `.in` 模板。若输出已存在，工具拒绝覆盖；重新生成时选择新目录。上传到服务器后，配置里的服务器路径必须与实际复制位置一致。

## English

The reference platform is Ubuntu 22.04 x86_64, ROS 2 Humble and system Python 3.10. Install ROS using its official instructions, then the dependency list above. Keep ROS separate from Conda. The correct ROS KDL package is `ros-humble-orocos-kdl-vendor`.

Fetch the exact upstream revisions above. Assemble a dedicated workspace from the three R5 ROS packages and the Orbbec checkout; retain originals. Apply the documented ARX wrapper/build-metadata changes, check dependencies with rosdep, then build without starting nodes. Review USB permissions per device; do not indiscriminately grant world-write access or run scripts that remove unrelated udev rules.

Copy the site example into a local, untracked configuration and set paths and adapter identities. Materialization creates source files only, refuses overwrite and does not establish hardware acceptance. Server paths must match the eventual server layout. Camera serial numbers are supplied manually to camera launch commands, not inferred from USB enumeration order.
