# Recording, upload and video / 录制、上传与视频

## 中文

### 双相机

在已加载 ROS 和 workspace 的两个终端启动相机；分别填写真实序列号。配置文件内可开启深度，但批量录制默认只保存 RGB：

```bash
ROS_DOMAIN_ID=85 ROS_LOCALHOST_ONLY=1 ros2 launch orbbec_camera gemini_301_series.launch.py \
  camera_name:=camera_1 serial_number:=YOUR_WRIST_SERIAL device_num:=2 \
  config_file_path:=$(pwd)/runtime/host/config/gemini305_rgbd_30fps.yaml
```

```bash
ROS_DOMAIN_ID=85 ROS_LOCALHOST_ONLY=1 ros2 launch orbbec_camera gemini_301_series.launch.py \
  camera_name:=camera_2 serial_number:=YOUR_EXTERNAL_SERIAL device_num:=2 \
  config_file_path:=$(pwd)/runtime/host/config/gemini305_rgbd_30fps.yaml
```

`camera_1` 为腕部，`camera_2` 为外部。使用 `ros2 run rqt_image_view rqt_image_view` 查看两路 `/camera_N/color/image_raw`，检查视野、848×530 分辨率和约 30 FPS 的到达节拍。两相机使用软件时间戳对齐。

### 批量录制

先用测试模式，不需要移动机械臂：

```bash
bash runtime/host/batch_record.sh --test-only --episodes 3 --max-seconds 20
```

正式录制示例：

```bash
bash runtime/host/batch_record.sh \
  --task "Put the charger in the box" --episodes 30 --max-seconds 60
```

交互流程：回车开始 → 示范 → 回车结束 → 输入 `s` 成功、`f` 失败、`d` 丢弃但保留、`u` 不确定 → 下一条；空闲时 `q` 结束整批。`--episodes` 为本批录制上限。录制与遥操独立运行。

每批结束输出 `SESSION_CLOSED`。失败和丢弃回合保留原始文件，数据选择时按标签排除。相同任务各批次使用一致的指令、相机安装、分辨率和机器人定义。每条覆盖完整任务，环境重置放在录制间隙。

默认目录为工具旁的 `recordings/r5_session_.../`，可通过 `--output-root` 指定数据盘。录制前用 `df -h` 检查空间；raw RGB 占用较大。上传和数据质量检查是独立步骤。

### 上传与校验

`upload_batch.py` 使用配置中的 SSH 目标、服务器目录与 decoder 路径；`--process` 在上传后提交 CPU 校验作业。Linux 上传也可使用 rsync：

```bash
rsync -rt --partial --info=progress2 /path/to/r5_session_example/ \
  robot@server.example.invalid:/srv/r5/real_robot/r5/batches/r5_session_example/
```

每批使用独立的 session 目录，保留原始层级。上传后比较源端和目标端的逐文件 SHA256。

Windows PowerShell 可使用系统 OpenSSH 与 tar，先打包再传：

```powershell
tar -cf r5_session_example.tar -C "D:\R5Recordings" r5_session_example
Get-FileHash .\r5_session_example.tar -Algorithm SHA256
ssh robot@server.example.invalid "mkdir -p /srv/r5/incoming"
scp .\r5_session_example.tar robot@server.example.invalid:/srv/r5/incoming/
ssh robot@server.example.invalid "sha256sum /srv/r5/incoming/r5_session_example.tar"
```

比较两端 SHA，用 `tar -tf` 检查归档使用相对路径且不含 `..`，然后解压到独立目录。本机原件保留至服务器校验及备份完成。

### 评测录像与导出

模型执行时，另开终端，使用 `--test-only`、`--episodes 1` 和所需的 `--max-seconds`，指定独立 `--output-root`。测试录制在训练选择时自动排除。

关闭录制后，在 ROS 环境离线导出，不重放到话题：

```bash
/usr/bin/python3 runtime/host/export_dual_view_mp4.py \
  /path/to/session/episodes/episode_000001/raw/bag \
  --output /path/to/new_export_directory
```

遇到时间戳间隙时，`--allow-timestamp-gaps` 可重复最近帧并添加可视标注。导出同时保存 `frame_timestamps.csv` 和 `export_report.json`。MP4 用于观看，训练对齐直接使用原始 MCAP。

## English

Launch wrist `camera_1` and external `camera_2` using their serial numbers and the pinned Orbbec launch file above. Check views, 848×530 resolution and approximately 30 FPS arrival rates. Views are aligned using software timestamps. The driver can run depth, but recording uses RGB by default.

Run a test-only batch first. Enter starts/stops an episode; label `s/f/d/u`, then continue or quit with `q` while idle. Recording runs independently of teleoperation. Failed/discarded episodes remain on disk and are excluded by labels. Keep task text, camera mounting, robot definition and units consistent, with resets between recordings. Check disk capacity for raw RGB storage.

Upload and data validation are separate from recording. Preserve session directories and compare per-file SHA256 values. Configure the upload script's SSH/server/decoder paths for the site. PowerShell users can tar, hash, scp, compare the server hash and extract into a new directory. Retain local originals until server verification and backup finish.

Use test-only recording for policy evaluations. Export closed bags with the MP4 tool. Optional gap handling repeats and annotates frames; timing tables and reports accompany the video. Training alignment uses original MCAP data.
