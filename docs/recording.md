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

`camera_1` 是腕部，`camera_2` 是外部，不要中途交换。使用 `ros2 run rqt_image_view rqt_image_view` 查看两路 `/camera_N/color/image_raw`；分别核实视野、无遮挡、848×530 和约 30 FPS。`ros2 topic hz` 测到的是订阅到达节拍，不是曝光同步证明。

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

交互流程：回车开始 → 示范 → 回车结束 → 输入 `s` 成功、`f` 失败、`d` 丢弃但保留、`u` 不确定 → 下一条；空闲时 `q` 结束整批。条数是本批上限，不保证有效成功条数。停止录制不会停止机械臂或遥操。

每条结束核实 bag 已正常关闭，最终看到 `SESSION_CLOSED`。失败或不要的条目保留原始文件及标签，训练选择时排除，不靠手工删除/重编号。统一任务文字、相机位置、分辨率、机器人定义及单位；每条完整展示任务，重置动作尽量不混入任务段。提前用 `df -h` 核查磁盘，raw RGB bag 可能很大。

默认目录为生成工具旁 `recordings/r5_session_.../`，可通过 `--output-root` 改到专用数据盘。录制不自动上传。人工 success 不代表数据已通过训练验收。

### 上传与校验

`upload_batch.py` 是原现场环境的参考：需要配置自己的 SSH 目标和服务器目录，审查其 decoder/template 路径；不会自动删除数据。`--process` 会提交 CPU 校验作业，不应未经查看就使用。普通 Linux 上传可先使用：

```bash
rsync -rt --partial --info=progress2 /path/to/r5_session_example/ \
  robot@server.example.invalid:/srv/r5/real_robot/r5/batches/r5_session_example/
```

目标必须是同一个 session，避免覆盖其他批次；保留目录层级，对全部文件做 SHA256 校验后再处理，不能用“rsync 退出 0”代替源/目标逐文件核验。

Windows PowerShell 可使用系统 OpenSSH 与 tar，先打包再传：

```powershell
tar -cf r5_session_example.tar -C "D:\R5Recordings" r5_session_example
Get-FileHash .\r5_session_example.tar -Algorithm SHA256
ssh robot@server.example.invalid "mkdir -p /srv/r5/incoming"
scp .\r5_session_example.tar robot@server.example.invalid:/srv/r5/incoming/
ssh robot@server.example.invalid "sha256sum /srv/r5/incoming/r5_session_example.tar"
```

人工比较两端 SHA 一致；检查 `tar -tf` 内容没有绝对路径或 `..`，再解到新建的独立目录。上传私钥或密码不是本流程的一部分。不要删除本机原件直到服务器原始文件和备份均确认。

### 评测录像与导出

模型执行时，另开终端录制 `--test-only`、`--episodes 1`、适当 `--max-seconds`，指定独立 `--output-root`；该录制不要混入训练。

关闭录制后，在 ROS 环境离线导出，不重放到话题：

```bash
/usr/bin/python3 runtime/host/export_dual_view_mp4.py \
  /path/to/session/episodes/episode_000001/raw/bag \
  --output /path/to/new_export_directory
```

若导出明确报告时间戳间隙，先保留报告；确需观看副本时，`--allow-timestamp-gaps` 会重复最近帧并可视标注。不能将这种导出作为训练时间对齐通过。保留 `frame_timestamps.csv`、`export_report.json` 和原始 MCAP。

## English

Launch wrist `camera_1` and external `camera_2` using their serial numbers and the pinned Orbbec launch file above. Check views, resolution and frame arrival rates independently. Identical FPS is not synchronized exposure. Depth may run in the camera driver but is not recorded by default.

Run a test-only batch first. For demonstrations, Enter starts/stops an episode; label `s/f/d/u`, then continue or quit with `q` while idle. Recording does not command or stop the robot. Preserve rejected episodes and labels; do not renumber to hide failures. Keep task text, camera mounting, robot definition and units consistent, and check disk capacity.

No automatic upload occurs. Upload closed sessions, preserve directory structure and verify every file with SHA256. The historical upload script requires site-specific review. PowerShell users can tar, hash, scp and compare the server hash before safely extracting into a new directory. Never upload credentials.

Use test-only recording for policy evaluations. Export closed bags with the read-only MP4 tool; it creates a viewing derivative, never a ROS replay. Explicit gap handling repeats and annotates frames. Preserve originals and timing reports; an export is not training acceptance.
