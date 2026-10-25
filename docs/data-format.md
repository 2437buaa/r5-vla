# Data contract / 数据契约

## 中文

原始回合目录：

```text
r5_session_.../
  session.json
  episodes/episode_000001/
    episode.json
    raw/qos.yaml
    raw/bag/metadata.yaml
    raw/bag/bag_0.mcap
```

必需话题为两路 `/camera_N/color/image_raw`、`color/camera_info` 和 `/r5_pair/follower_status`；另保留可用的 `/tf_static`。主臂不是训练输入或动作标签来源，不要求记录主臂姿态。`episode.json` 保留任务、人工标签、test-only、收尾状态、消息计数及原始时间。

状态：`[q1, q2, q3, q4, q5, q6, gripper_native]`。六轴单位 rad，夹爪使用 SDK 原生位置值。数组按关节顺序排列，与 CAN 电机 ID 分开定义。电流与速度字段保留原始 SDK 语义；夹爪尚无米制开口标定。

时间对齐：camera_1 header 锚点 → camera_2 唯一、顺序最近邻，误差 ≤16.7 ms → 从臂前后状态跨度 ≤10 ms → 六轴线性插值、夹爪因果前值保持。处理时检查图像间隙、共享区间与 30 Hz 名义时间漂移，并保存对齐 CSV。相机使用 header 时间，机械臂使用 SDK ROS 发布时间；当前未配置硬件同步。

图像：rgb8，848×530 → INTER_AREA →256×256；camera_2 对应 `camera_top`，camera_1 对应 `camera_wrist_left`。

监督：同一回合未来 `t+1…t+50` 的从臂实测位置，采用绝对目标。标签限制在回合内，尾部 padding 在 loss 和统计中排除。模型内部 55 维表示选择六轴索引 0…5 与夹爪索引 28，并维护有效 mask。

归一化由选定训练数据计算，采用分字段 q01/q99 的 `bounds_99_woclip`，通过文件 SHA 与部署绑定。更换训练数据时重新生成统计和绑定。

## English

The directory layout above preserves session/episode metadata, QoS and original MCAPs. Record both RGB streams and camera infos, follower status and available static transforms. Leader pose is not needed by the policy. Preserve task, human labels, test-only flags, shutdown state, counts and original timestamps.

State/action semantics: six absolute joint positions in radians plus native gripper state. Joint order is defined separately from motor IDs. Current/velocity fields retain SDK semantics; gripper width is not calibrated in meters. Align using camera_1 headers, unique sequential nearest camera_2 matches within 16.7 ms, and follower brackets within 10 ms. Interpolate arm positions and causally hold gripper state. Save alignment tables with gap and nominal-clock checks. Robot timestamps are SDK ROS publication times; hardware synchronization is not configured.

Resize RGB to 256² with INTER_AREA, mapping external to top and wrist to wrist-left. Targets are measured follower states at t+1…t+50 within each episode. Mask tail padding and select the seven valid dimensions from the internal 55-D representation.

Compute field-wise q01/q99 normalization from selected training data and bind its SHA to deployment. Regenerate statistics and bindings when the training data changes.
