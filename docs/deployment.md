# VLA deployment / VLA 部署

## 中文

部署分三层：服务器模型推理 → SSH 隧道 → 本机 ROS/原厂 SDK 执行。服务器 HTTP 服务不接触 CAN 或 ROS，默认仅监听 `127.0.0.1:18765`。它没有面向公网的认证，不要改成公网监听。

### 模型侧

将 `runtime/host/deployment_v1/` 放在服务器 `$R5_DEPLOY_ROOT/scripts/`。输入训练 YAML、R5 robot config、归一化统计和目标 HF checkpoint 必须来自同一次训练。`contract.py` 的历史 NORM_SHA 与 4000 步/50 步断言必须有实际来源，不能只为了跑通而改成任意值。

原生模型输出七维绝对目标，预测 50 步、10 次去噪、bf16。2k/4k 模型和真实训练输入一致性检查代码保留在参考目录；若要运行需单独授权/提交，不是本仓库 CI 的一部分。过去真实录制样本上的离线误差不等于独立验证或闭环成功率。

`serve.sbatch` 是历史两小时服务参考，GPU 数 1、nice=0。现场曾另以 48 小时上限申请服务。新环境按实际时限配置并正常排队，不假设始终有空闲卡，也不自动续租。

在原服务验收标志确由当前模型检查产生后，操作员提交服务：

```bash
export R5_DEPLOY_ROOT=/srv/r5/real_robot/r5/deployment/charger_preview
export R5_CHECK_STEP=4000
sbatch --nice=0 --export=ALL \
  --output="$R5_DEPLOY_ROOT/logs/serve-%j.out" \
  --error="$R5_DEPLOY_ROOT/logs/serve-%j.err" \
  "$R5_DEPLOY_ROOT/scripts/serve.sbatch"
```

本机隧道（仅当 SSH 终点与服务在同一节点时直接适用；多节点集群需正确转发到实际执行节点）：

```bash
ssh -o ExitOnForwardFailure=yes -o ServerAliveInterval=30 -N \
  -L 127.0.0.1:8765:127.0.0.1:18765 robot@server.example.invalid
```

### 本机 SDK 与只读预览

停止遥操，确保只有一个从臂控制者。CAN 按遥操章节准备，但模型从臂使用 `normal` 模式和独立命令话题，不再订阅主臂状态。**下面 SDK 启动可使能/回零，由现场手动执行：**

```bash
ROS_DOMAIN_ID=85 ROS_LOCALHOST_ONLY=1 ros2 run arx_r5_controller R5Controller --ros-args \
  -r __node:=r5_model_follower \
  -p arm_can_id:=can1 -p arm_control_type:=normal -p arm_end_type:=0 \
  -p arm_pub_topic_name:=/r5_pair/follower_status \
  -p arm_sub_topic_name:=/r5_model/arm_cmd \
  2>&1 | tee /path/to/current-sdk.log
```

先确认相机及状态已正常发布，再只读预览：

```bash
bash runtime/host/deployment_v1/raw_preview.sh --samples 3
```

该命令不创建运动发布器。不要为了解决预览问题盲目重启 SDK。初始位姿及物品准备由操作员完成；`move_to_demo_start.py`/`return_to_task_start.sh` 含特定示范位形、SDK 二进制偏移和已停用的反馈检查，不作为新机器的通用回位命令。

### 显式执行

现场重新确认准备完成后，操作员在前台手动执行，保持可输入的终端：

```bash
bash runtime/host/deployment_v1/task500.sh \
  --execute --confirm-clear --sdk-log /path/to/current-sdk.log
```

预测 50、执行 50、再观察，最多 500 条目标；动作段内名义 30 Hz，不是 30 Hz 推理。按回车仅表示操作员报告完成，没有自动成功检测。保留每段输入时间、预测、发送记录及人工干预说明，另录 test-only bag。

外层未修改模型目标，但原厂 SDK 内部仍有软件饱和/插值。若源码中反馈速度、跟踪、推理期间位移检查已被注释，就不能宣称它们有效；详见安全文档。停止发布不是急停，最后目标可能继续执行或保持。

## English

Deployment separates GPU inference, an SSH tunnel and the local ROS/vendor-SDK bridge. Bind inference to loopback only; the reference HTTP service has no public-facing authentication. In multi-node clusters, tunnel to the node actually running the service.

Keep checkpoint, training config, robot mapping and normalization from the same run. Historical hashes/step assertions are provenance checks, not arbitrary configuration to bypass. The policy uses bf16, ten denoising steps and 50 absolute seven-dimensional targets. The reference service job requests one GPU at normal priority; adjust its two-hour historical limit explicitly if needed, rather than assuming a reservation remains active.

Stop teleoperation before policy control. Start exactly one follower SDK in `normal` mode with the topic/node bindings shown above; startup may home the arm. Obtain live RGB and follower state, then run the read-only preview before operator-authorized execution. The demonstration-specific return tool is not a generic safe homing tool.

The foreground `task500.sh --execute --confirm-clear --sdk-log ...` command enables motion: 50 targets per fresh observation, maximum 500. Thirty Hz refers to publication inside each segment; inference adds gaps. Enter records operator-reported completion, not automatic task success. Record evaluations separately, preserve command evidence and disclose intervention. SDK saturation/interpolation still applies. Commented-out feedback checks are not active protection, and stopping publication is not an emergency stop.
