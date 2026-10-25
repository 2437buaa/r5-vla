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

状态：`[q1, q2, q3, q4, q5, q6, gripper_native]`。六轴单位 rad，夹爪为原厂 SDK 原生值，不是米制开口宽度。数组索引不是 CAN 电机 ID。电流不自动解释为力，速度发布频率不代表硬件采样频率。

时间对齐：camera_1 header 锚点 → camera_2 最近邻且不复用/倒序、误差 ≤16.7 ms → 从臂前后状态跨度 ≤10 ms → 六轴线性插值、夹爪因果前值保持。检查图像间隙、完整共享区间与 30 Hz 名义时间漂移，保留对齐 CSV。相机 header 和 SDK ROS 发布时刻不是已认证的统一硬件时钟。

图像：rgb8，848×530 → INTER_AREA →256×256；camera_2 对应 `camera_top`，camera_1 对应 `camera_wrist_left`。

监督：同一回合未来 `t+1…t+50` 的从臂实测位置，绝对目标、非增量。不是记录到的主臂指令或控制器接收目标。不得跨回合构造标签；尾部 padding 在 loss 和统计中排除。模型内部 55 维表示仅选六轴索引 0…5 和夹爪索引 28，并维护有效 mask。

归一化仅由选定训练数据计算，实际变换采用分字段 q01/q99 的 `bounds_99_woclip` 路线；绑定实际读取内容和 SHA，而不是只看 YAML。新训练必须重新建立归一化与部署绑定，不能照搬历史 hash。

## English

The directory layout above preserves session/episode metadata, QoS and original MCAPs. Record both RGB streams and camera infos, follower status and available static transforms. Leader pose is not needed by the policy. Preserve task, human labels, test-only flags, shutdown state, counts and original timestamps.

State/action semantics: six absolute joint positions in radians plus native gripper state. Indices are not motor IDs; current is not calibrated force. Align using camera_1 headers, unique nearest camera_2 matches within 16.7 ms, and follower brackets within 10 ms; interpolate arm positions and causally hold gripper state. Check gaps and nominal-clock drift and retain alignment tables. These timestamps do not certify a shared hardware acquisition clock.

Resize RGB to 256² with INTER_AREA, consistently mapping external to top and wrist to wrist-left. Targets are future measured follower states at t+1…t+50, not recorded control commands. Never cross episodes; mask padding. Select only the seven valid dimensions from the model's internal 55-D representation.

Compute field-wise q01/q99 normalization from accepted training data and bind its actual content/SHA to deployment. A historical hash must not be reused for a different training run.
