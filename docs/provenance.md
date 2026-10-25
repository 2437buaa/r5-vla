# Experiment record / 实验记录

## 中文

任务：`Put the charger in the box`。一台 R5 执行充电器抓取入盒，两台 Gemini 305 提供腕部与外部视角。

`provenance/source-manifest.json` 记录原文件和模板的 SHA256。模板中的路径、设备序列号和服务器配置由本地 site 文件填入。训练实现包括 `prepare_checked.py`，训练参数见 `reference/train-config.yaml.in`。

固定依赖：

| Dependency | Revision |
|---|---|
| ARX R5 | `e87d09c11edb65f6ae672abc7a41fe2277a2f12f` |
| OrbbecSDK_ROS2 | `c153462518ad674650bafa4464fda72c27ab797a` |
| LingBot-VLA code | `be969b8fd117fb70550c5d4bf4bc328211b5b1b6` |
| Base model | `robbyant/lingbot-vla-v2-6b`; exact shard metadata in the reference verifier |

训练使用 71 条人工标记成功的示范，共 24,576 帧。两 GPU 训练 4000 次更新，在 2000/4000 步导出。全部示范用于训练，未设置独立验证集。

本次归一化 SHA256：`3f275d6a06931b34c790d8d9784ad57bc13e21b24d9059674bbc0aeb9803d022`。

SDK 库 SHA256：`30239795532e0d440842405f02092c85f95b5f4b0813c2bdf95b22d89960fa18`。

一次模型测试记录发送 6 段、共 300 条目标，随后由操作员结束运行并标记完成。当前测试未实现自动成功判定，未统计整体成功率或单独记录干预率。

评测录制单独保存，不参与训练。双视图 MP4 从 MCAP 导出，包含视图拼接、时间标注和 30 FPS 选帧；跨越时间戳间隙时重复最近帧并标注。

## English

Task: `Put the charger in the box`. One R5 performs the task, with wrist and external Gemini 305 views.

The source manifest records original/template hashes. Local site configuration supplies paths, device identities and server settings. Training uses `prepare_checked.py` and the configuration in `reference/train-config.yaml.in`.

Training uses 71 human-success-labelled demonstrations and 24,576 aligned frames, two GPUs and 4,000 updates, with exports at 2k/4k. All demonstrations are used for training; there is no held-out validation set. Normalization and SDK hashes are listed above.

One policy test sent six segments totaling 300 targets before the operator ended the run and marked completion. Automatic success detection, aggregate success rate and a separate intervention-rate evaluation are not implemented. Evaluation recordings are excluded from training. Dual-view MP4s combine views, timestamps and 30 FPS frame selection; timestamp gaps use annotated repeated frames.
