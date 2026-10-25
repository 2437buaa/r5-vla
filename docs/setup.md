# Setup / 环境准备

## 中文

环境：Ubuntu 22.04 x86_64、ROS 2 Humble、系统 Python 3.10。按 [ROS 官方 Humble 安装说明](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html)安装 ROS，然后安装依赖：

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

KDL 使用 `ros-humble-orocos-kdl-vendor`。ROS 节点使用系统 Python，与 Conda 训练环境分开。

### 固定源码

获取固定版本的依赖：

```bash
git clone https://github.com/ARXroboticsX/R5.git vendor/R5
git -C vendor/R5 checkout --detach e87d09c11edb65f6ae672abc7a41fe2277a2f12f
git clone https://github.com/orbbec/OrbbecSDK_ROS2.git vendor/OrbbecSDK_ROS2
git -C vendor/OrbbecSDK_ROS2 checkout --detach c153462518ad674650bafa4464fda72c27ab797a
git clone https://github.com/robbyant/lingbot-vla-v2.git vendor/lingbot-vla-v2
git -C vendor/lingbot-vla-v2 checkout --detach be969b8fd117fb70550c5d4bf4bc328211b5b1b6
```

将 R5 上游 `ROS2/R5_ws/src/ARX_R5_ros2_V7/arx_r5_controller`、`ROS2/R5_ws/src/arxmsgros2/arm_control`、`ROS2/R5_ws/src/arxmsgros2/arx5_arm_msg` 和 Orbbec 源码放入 ROS workspace 的 `src/`。

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

USB 访问通过设备组权限配置；两台相机使用 USB3 接口。构建完成后，在新终端加载 workspace。

### 配置与生成副本

复制 `config/site.example.json` 为 `config/site.local.json`，填写 ASCII 路径及两个 CAN 适配器序列号。路径使用无空格格式。

```bash
python3 scripts/materialize.py --config config/site.local.json --output runtime
```

运行文件在 `runtime/host/`，训练 YAML 在 `runtime/train-config.yaml`。生成器拒绝覆盖已有目录。服务器端文件按 site 配置中的路径部署。

## English

The platform is Ubuntu 22.04 x86_64, ROS 2 Humble and system Python 3.10. Install ROS and the dependencies above. ROS nodes use system Python, separate from the Conda training environment. KDL uses `ros-humble-orocos-kdl-vendor`.

Fetch the pinned revisions and assemble the workspace from the three R5 ROS packages and the Orbbec checkout. Apply the ARX wrapper/build-metadata changes, check dependencies with rosdep and build. Configure USB access through device-group permissions and connect both cameras over USB3.

Set paths and adapter identities in the local site file, using ASCII paths without spaces. Materialization writes `runtime/host/` and `runtime/train-config.yaml` and refuses an existing output directory. Deploy server files at the configured paths. Supply camera serial numbers to the camera launch commands.
