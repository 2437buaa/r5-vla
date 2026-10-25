# R5 VLA

**ARX R5 teleoperation → demonstrations → LingBot-VLA training → real-robot deployment.**

**ARX R5 遥操作 → 示范录制 → LingBot-VLA 训练 → 真机部署。**

[中文完整指南](README.zh-CN.md) · [English guide](README.en.md) · [Safety / 安全说明](docs/safety.md) · [Contributing / 协作](CONTRIBUTING.md)

## 中文

奶龙陆战队的 R5 真机工程记录与工具集：两台同型号 R5 一主一从采集示范，两台 Gemini 305 提供腕部和外部 RGB 视角，基于 LingBot-VLA 2.0 独立训练，部署时由模型控制一台从臂。

包含批量 MCAP 录制、人工标签、从臂与双相机时间对齐、数据校验、双视图 MP4 导出、双 GPU 训练参考、远程推理和原厂 SDK 执行桥。默认不录深度；不包含原始示范、视频、权重、密钥或原厂二进制。

这是**私有阶段的开源准备仓库**，不是一键即用的机器人产品。`reference/` 是经过路径脱敏的历史工程快照，保留既有控制逻辑和局限；先生成本地配置，再逐项审查。不要把示例参数、原型保护或一次人工确认的演示当作安全认证。

已记录的实验：71 条人工成功标签示范、24,576 帧、4000 次更新，2000/4000 步导出；一次模型执行发送 6×50 条目标后由操作员确认完成。**无独立实机验证集，无核验后的整体成功率，无全程无人干预认证。** 自采数据与 clean-only 仿真比赛模型分离。

## English

An engineering toolkit and reproducibility record by Team Nailong: collect demonstrations with two identical ARX R5 arms in leader–follower teleoperation, observe the follower with wrist and external Gemini 305 RGB cameras, train a dedicated LingBot-VLA 2.0 policy, and deploy it on one follower arm.

Includes batched MCAP recording, human labels, camera/follower alignment, dataset checks, dual-view MP4 export, two-GPU training references, remote inference and a vendor-SDK execution bridge. Depth recording is off by default. Raw demonstrations, videos, weights, credentials and vendor binaries are excluded.

This is a **private, pre-publication engineering repository**, not a turnkey robot product. `reference/` preserves path-tokenized historical code, including known limitations. Materialize a local configuration and review it before use. Example values, prototype checks and an operator-reported demonstration are not safety certification.

Recorded experiment: 71 human-success-labelled demonstrations, 24,576 aligned frames, 4,000 updates, exports at 2k/4k. One execution sent 6×50 model targets before operator confirmation. **No held-out real-robot validation set, audited overall success rate, or independently verified intervention-free evaluation.** Self-collected data are separate from clean-only simulation competition training.

## Workflow / 流程

| Stage / 阶段 | Guide / 指南 | Code / 代码 |
|---|---|---|
| Host & dependencies / 上位机与依赖 | [Setup](docs/setup.md) | [ARX integration](integrations/arx/README.md) |
| Leader–follower / 主从遥操 | [Teleoperation](docs/teleoperation.md) | [Launch template](reference/host/launch/one_master_one_slave.launch.py.in) |
| Record & export / 录制与导出 | [Recording](docs/recording.md) | [Recorder](reference/host/batch_record.py.in), [MP4 exporter](reference/host/export_dual_view_mp4.py.in) |
| Alignment & labels / 时间对齐与标签 | [Data format](docs/data-format.md) | [Preparation](reference/host/training_v1/prepare.py.in) |
| Train / 训练 | [Training](docs/training.md) | [Trainer](reference/host/training_v1/train.py.in) |
| Deploy / 部署 | [Deployment](docs/deployment.md) | [Policy adapter](reference/host/deployment_v1/adapter.py.in), [Execution bridge](reference/host/deployment_v1/trial50.py.in) |
| Evidence & limits / 证据与边界 | [Provenance](docs/provenance.md) | [Manifest](provenance/source-manifest.json) |

## Start without hardware / 无硬件开始

```bash
git clone https://github.com/2437buaa/r5-vla.git
cd r5-vla
python3 scripts/check_repository.py
python3 -m unittest discover -s tests -v
cp config/site.example.json config/site.local.json
# Edit local paths and device identities; do not commit site.local.json.
# 修改本地路径和设备身份；不要提交 site.local.json。
python3 scripts/materialize.py --config config/site.local.json --output runtime
```

These commands do not launch ROS, cameras, CAN, training, or robot motion. Configuration is not hardware acceptance. / 上述命令不会启动 ROS、相机、CAN、训练或机械臂；配置成功不代表硬件验收。

## License / 许可

Project-authored code and documentation: [Apache-2.0](LICENSE). The attributed ARX wrapper retains [BSD-3-Clause](integrations/arx/LICENSE.ARX). External SDKs, models and datasets retain their own terms; see [third-party notices](THIRD_PARTY_NOTICES.md). Public release remains a separate owner decision.
