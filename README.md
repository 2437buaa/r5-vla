# R5 VLA

**ARX R5 teleoperation → demonstrations → LingBot-VLA training → real-robot deployment.**

**ARX R5 遥操作 → 示范录制 → LingBot-VLA 训练 → 真机部署。**

[中文完整指南](README.zh-CN.md) · [English guide](README.en.md) · [Safety / 安全说明](docs/safety.md) · [Contributing / 协作](CONTRIBUTING.md)

## 中文

R5 VLA 提供 ARX R5 从遥操作、示范采集到模型训练与真机部署的完整流程。两台 R5 采用主从方式采集数据，两台 Gemini 305 提供腕部和外部 RGB 视角，LingBot-VLA 2.0 策略控制一台从臂执行任务。

功能包括批量 MCAP 录制、回合标注、双相机与从臂状态对齐、数据校验、双视图 MP4 导出、双 GPU 训练、远程推理和原厂 SDK 控制接口。默认使用 RGB，不录制深度。

代码模板位于 `reference/`，通过本地配置生成 `runtime/` 运行目录。模型权重、原始示范和 SDK 二进制单独获取。

充电器入盒实验使用 71 条示范、24,576 帧，训练 4000 次更新，在 2000/4000 步导出模型。部署采用预测 50 步、执行 50 步、重新观察的方式，动作段内按 30 Hz 发布目标。实验配置和测试记录见[实验记录](docs/provenance.md)。

## English

R5 VLA covers ARX R5 teleoperation, demonstration collection, model training and real-robot deployment. Two R5 arms collect leader–follower demonstrations, two Gemini 305 cameras provide wrist and external RGB views, and a LingBot-VLA 2.0 policy controls one follower arm.

Features include batched MCAP recording, episode labels, camera/follower alignment, dataset checks, dual-view MP4 export, two-GPU training, remote inference and a vendor-SDK control interface. RGB is used by default; depth recording is disabled.

Source templates live in `reference/`; local configuration generates the `runtime/` directory. Model weights, raw demonstrations and SDK binaries are obtained separately.

The charger-in-box experiment uses 71 demonstrations, 24,576 aligned frames and 4,000 updates, with exports at 2k/4k. Deployment predicts and executes 50 targets before observing again, publishing at 30 Hz within each segment. See the [experiment record](docs/provenance.md) for configuration and test details.

## Workflow / 流程

| Stage / 阶段 | Guide / 指南 | Code / 代码 |
|---|---|---|
| Host & dependencies / 上位机与依赖 | [Setup](docs/setup.md) | [ARX integration](integrations/arx/README.md) |
| Leader–follower / 主从遥操 | [Teleoperation](docs/teleoperation.md) | [Launch template](reference/host/launch/one_master_one_slave.launch.py.in) |
| Record & export / 录制与导出 | [Recording](docs/recording.md) | [Recorder](reference/host/batch_record.py.in), [MP4 exporter](reference/host/export_dual_view_mp4.py.in) |
| Alignment & labels / 时间对齐与标签 | [Data format](docs/data-format.md) | [Preparation](reference/host/training_v1/prepare.py.in) |
| Train / 训练 | [Training](docs/training.md) | [Trainer](reference/host/training_v1/train.py.in) |
| Deploy / 部署 | [Deployment](docs/deployment.md) | [Policy adapter](reference/host/deployment_v1/adapter.py.in), [Execution bridge](reference/host/deployment_v1/trial50.py.in) |
| Experiment record / 实验记录 | [Provenance](docs/provenance.md) | [Manifest](provenance/source-manifest.json) |

## Quick start / 快速开始

```bash
git clone https://github.com/2437buaa/r5-vla.git
cd r5-vla
python3 scripts/check_repository.py
python3 -m unittest discover -s tests -v
cp config/site.example.json config/site.local.json
# Set local paths and adapter serial numbers in config/site.local.json.
# 在 config/site.local.json 中填写路径和适配器序列号。
python3 scripts/materialize.py --config config/site.local.json --output runtime
```

Next: [setup](docs/setup.md) → [teleoperation](docs/teleoperation.md) → [recording](docs/recording.md) → [training](docs/training.md) → [deployment](docs/deployment.md).

## License / 许可

Code and documentation: [Apache-2.0](LICENSE). The ARX wrapper uses [BSD-3-Clause](integrations/arx/LICENSE.ARX). See [third-party notices](THIRD_PARTY_NOTICES.md) for dependencies.
