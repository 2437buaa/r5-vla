# Training / 训练

## 中文

训练从 `robbyant/lingbot-vla-v2-6b` 基座开始。训练环境采用固定版本的 LingBot-VLA 上游依赖，MCAP 解码使用 `mcap` 和 `mcap-ros2-support`，数据构建使用 LeRobot 0.4.3。PyTorch、CUDA 和 FlashAttention 的版本按 GPU 与上游要求配置。

### 实验配置

- 71 条人工成功标签示范、24,576 帧；其余 12 条标签记录和 test-only 排除。
- 全部 71 条用于训练，没有独立验证集。
- 两张 GPU，micro-batch 8/卡，梯度累积 2，global batch 32。
- 全模型微调、FSDP2、混合精度和梯度检查点；非 LoRA。
- AdamW，普通参数组峰值 5e-5，专家组采用上游比例，100 步 warmup、余弦衰减。
- `L1_fm` 动作训练目标；关闭深度与视频辅助教师分支。
- 总计 4000 次参数更新，2000/4000 步保存 DCP 和 HF 导出。

### 文件布局与启动流程

将 `runtime/host/training_v1/` 部署至服务器 `$R5_TRAIN_BUNDLE/scripts/`，将 `runtime/train-config.yaml` 放在 `TRAIN_CONFIG_TEMPLATE` 指定位置。数据批次由 `common.py` 的 `SESSIONS` 配置。

准备流程：

1. `verify_base.py "$R5_TRAIN_BUNDLE"` 对比官方 HF LFS 元数据和本地模型分片 SHA；保存 `BASE_VERIFIED.json`。
2. 使用 `prepare_checked.py` 完成 CPU 数据解码、对齐及读取检查；`prepare.py` 为较早实现。
3. 数据准备输出 `CPU_READY.json`、数据清单、padding 检查结果、归一化统计和文件 SHA。
4. 配置 `train.sbatch` 和 IPC 检查所需环境变量，前置检查通过后提交训练。
5. 2000 步导出后生成 `CHECKPOINT_READY_STEP_2000.json`，训练继续到 4000 步。

`check.sbatch` 结尾调用 `submit_train.py` 自动提交训练，`restart_after_ipc.py` 提供重启入口。`submit_train.py` 中的作业元数据按当前运行更新。

脚本包含本次实验的 71/12 条数据计数和 2000/4000 步设置。适配新实验时同步更新数据选择、归一化、导出和部署配置。

### Slurm 资源

CPU 准备不请求 GPU，训练使用两张卡，推理服务使用一张卡，默认 `nice=0`。partition、内存和时限在各 sbatch 文件中配置。训练进度保存在 `output/progress/`，首步前反向结果保存在 `output/forward_backward_pass/`。

## English

Training starts from `robbyant/lingbot-vla-v2-6b` with the pinned upstream environment. Data preparation uses MCAP decoding and LeRobot 0.4.3. Configure PyTorch, CUDA and FlashAttention for the GPU and upstream requirements.

The recorded configuration is 71 demonstrations/24,576 frames, two GPUs, global batch 32, full-model FSDP2 fine-tuning, AdamW, warmup/cosine, L1_fm, RGB-only with auxiliary teachers disabled, 4,000 updates and 2k/4k exports. There is no held-out validation set.

Place rendered training scripts in `$R5_TRAIN_BUNDLE/scripts/` and the training YAML at `TRAIN_CONFIG_TEMPLATE`. Configure sessions in `common.py`. Verify base shard hashes, run `prepare_checked.py` for CPU preparation, complete the IPC checks and submit through Slurm.

`prepare_checked.py` contains the updated reader implementation; `prepare.py` is an earlier version. `check.sbatch` submits training automatically, and `restart_after_ipc.py` provides a restart entry point. Update job metadata, episode counts and step settings when adapting the experiment.

CPU preparation requests no GPU, training requests two GPUs and inference requests one, with `nice=0`. Configure partition, memory and time limits in the sbatch files. Progress is written to `output/progress/`; the first forward/backward result is stored in `output/forward_backward_pass/`.
