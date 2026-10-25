# VLA deployment / VLA 部署

## 中文

部署分三层：服务器模型推理 → SSH 隧道 → 本机 ROS/原厂 SDK 执行。HTTP 服务监听 `127.0.0.1:18765`，通过 SSH 转发访问，不提供认证。

### 模型侧

将 `runtime/host/deployment_v1/` 放在服务器 `$R5_DEPLOY_ROOT/scripts/`。部署加载同次训练的 YAML、R5 robot config、归一化统计和 HF checkpoint。`contract.py` 配置归一化 SHA、checkpoint 步数与预测长度。

推理使用 bf16、10 次去噪，输出 50 步七维绝对目标。`prepare.py` 检查训练/部署输入一致性，`offline.py` 对 2k/4k checkpoint 进行录制样本推理。

`serve.sbatch` 默认申请 1 张 GPU，`nice=0`，时限 2 小时。服务时长通过 `#SBATCH --time` 调整。

模型检查生成 `OFFLINE_COMPLETE.json` 后，提交服务：

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

停止遥操后，将从臂切换到 `normal` 模式，订阅独立的模型命令话题。SDK 启动会使能并可能回零：

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

`raw_preview.sh` 读取实时观测并保存预测，不发布控制目标。`move_to_demo_start.py` 和 `return_to_task_start.sh` 使用本次示范初始位形及固定 SDK 二进制布局，适配说明见[安全说明](safety.md)。

### 执行任务

机械臂、物品和工作区准备就绪后，在交互终端运行：

```bash
bash runtime/host/deployment_v1/task500.sh \
  --execute --confirm-clear --sdk-log /path/to/current-sdk.log
```

每次预测并执行 50 条目标，再取新观测，上限 500 条。段内按名义 30 Hz 发布，段间包含推理等待。按回车结束并标记完成；程序未实现自动成功检测。测试录像使用单独的 test-only bag。

执行桥传递原始模型目标，SDK 内部进行软件饱和与插值。当前反馈检查状态见[安全说明](safety.md)。停止发布后，SDK 可能继续执行或保持最后目标。

## English

Deployment separates GPU inference, an SSH tunnel and the local ROS/vendor-SDK bridge. The HTTP service binds to loopback without authentication. In multi-node clusters, forward the tunnel to the execution node.

Load checkpoint, training config, robot mapping and normalization from the same run. Configure their bindings in `contract.py`. Inference uses bf16, ten denoising steps and 50 seven-dimensional absolute targets. The service job requests one GPU with `nice=0` and a two-hour default time limit, configurable through `#SBATCH --time`.

Stop teleoperation and start the follower SDK in `normal` mode with the bindings above. Startup can home the arm. Once RGB and follower state are available, `raw_preview.sh` saves predictions without publishing targets. Return tools use this experiment's initial pose and a fixed SDK layout.

Run `task500.sh --execute --confirm-clear --sdk-log ...` in an interactive terminal after preparing the robot and workspace. Each fresh observation produces 50 targets, with a 500-target maximum. Thirty Hz applies within each segment; inference adds gaps. Enter ends the run and records completion. Evaluations use separate test-only recordings. SDK saturation/interpolation applies, and the SDK can retain its last target after publication stops. See [safety](safety.md) for current feedback checks.
