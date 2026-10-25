# Training / 训练

## 中文

参考训练从官方 `robbyant/lingbot-vla-v2-6b` 基座独立开始，不从 RoboTwin 后训练权重或仿真比赛 checkpoint 开始。按上游项目安装训练环境并单独下载模型，遵守模型及依赖许可。本仓库不包含权重。MCAP 解码需要 `mcap`、`mcap-ros2-support`，数据构建使用 LeRobot 0.4.3；PyTorch/CUDA/FlashAttention 组合按上游版本与实际 GPU 适配，不能用一个未测试的 pip 清单声称环境已验收。

### 实际实验配置

- 71 条人工成功标签示范、24,576 帧；其余 12 条标签记录和 test-only 排除。
- 全部 71 条用于训练，没有独立验证集。
- 两张 GPU，micro-batch 8/卡，梯度累积 2，global batch 32。
- 全模型微调、FSDP2、混合精度和梯度检查点；非 LoRA。
- AdamW，普通参数组峰值 5e-5，专家组采用上游比例，100 步 warmup、余弦衰减。
- `L1_fm` 动作训练目标；关闭深度与视频辅助教师分支。
- 总计 4000 次参数更新，2000/4000 步保存 DCP 和 HF 导出。

### 文件布局与门控

生成的 `runtime/host/training_v1/` 作为服务器 `$R5_TRAIN_BUNDLE/scripts/`，实际路径与配置一致。`runtime/train-config.yaml` 是脱敏后的真实训练配置，复制到 `TRAIN_CONFIG_TEMPLATE` 所指位置。`common.py` 中的四批 session 仍是历史清单，换批次时需明确修改，不能只改任务名字。

需要的服务器依赖、基座和原始数据准备好后，按以下逻辑逐项执行，而不是盲目一键提交：

1. `verify_base.py "$R5_TRAIN_BUNDLE"` 对比官方 HF LFS 元数据和本地模型分片 SHA；保存 `BASE_VERIFIED.json`。
2. CPU 数据解码、时间对齐及读取检查。`prepare_checked.py` 是实际修复过的读取检查实现，`prepare.py` 保留了较早版本，不能把二者当作相同入口。先审查，再以 CPU 作业执行修正版本。
3. 检查 `CPU_READY.json`、数据清单、padding、实际归一化/逆变换和来源 SHA。通过标志必须由本次真实检查生成，不能从参考记录复制。
4. 查看 `train.sbatch`、IPC 辅助检查和训练脚本需要的环境变量。只有在 CPU/基座/IPC 前置证据满足后，才由操作员通过 Slurm 提交训练。
5. 保存 `CHECKPOINT_READY_STEP_2000.json` 后可单独准备测试，训练继续至 4000。导出完成标记与完整分片文件都需核对。

历史 `check.sbatch` 结尾会调用 `submit_train.py` 自动提交训练；`restart_after_ipc.py` 等工具也会提交作业。这些不是只读检查命令。`submit_train.py` 中旧作业号只是历史元数据，换环境应更新，不能据此推断队列状态。

本仓库保留历史 71/12 计数、2000/4000 步断言以及实验初始姿态绑定，尚未重构成任意数据集/任意步数的通用训练器。修改这些约束时重新审查数据选择、归一化、导出和部署契约。

### 调度原则

`nice=0` 是正常优先级，不主动降权也不插队。CPU 准备无需 GPU，训练请求两卡，推理服务另请求一卡；资源、partition、mem 和时限均由所在集群允许范围确定。不要取消其他用户作业，不要登录节点直接长期占 GPU。日志中 RUNNING 不等于已完成一次参数更新，检查 progress 与 forward/backward 证据。

## English

Start independently from the official base model, not a RoboTwin post-trained or competition checkpoint. Install the pinned upstream training environment and obtain weights separately. The data path uses MCAP decoding and LeRobot 0.4.3. GPU-dependent packages require a tested upstream-compatible stack, not a guessed universal requirements file.

The recorded configuration is 71 demonstrations/24,576 frames, two GPUs, global batch 32, full-model FSDP2 fine-tuning, AdamW, warmup/cosine, L1_fm, RGB-only with auxiliary teachers disabled, 4,000 updates and 2k/4k exports. There is no held-out validation set.

Place rendered scripts in the configured training bundle's `scripts/`; place the rendered real training YAML at `TRAIN_CONFIG_TEMPLATE`. Update historical session lists intentionally. Verify base shard hashes, run the corrected CPU preparation/reader path, inspect fresh CPU acceptance and normalization evidence, satisfy IPC prerequisites, then submit through Slurm. Do not manufacture PASS files.

`prepare_checked.py` contains the later reader fixes; `prepare.py` is historical. Some gate/restart scripts submit training automatically and are not read-only. Hard-coded historical job IDs are metadata, not live dependencies. The reference retains experiment-specific counts and step assertions and is not yet a general dataset trainer.

Keep normal scheduling with `nice=0`; do not cancel unrelated jobs or run long GPU work on login nodes. Validate actual optimizer progress and checkpoint completeness rather than treating allocation as training acceptance.
