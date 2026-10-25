# Provenance / 来源与实验记录

## 中文

整理日期：2026-10-25，北京时间。此仓库从原工程白名单导出，不携带原工作区 Git 历史、账号配置、日志、原始数据、视频或模型权重。原运行目录未被迁移或修改。

源码来源见 `provenance/source-manifest.json`：每项记录原文件 SHA256 和脱敏模板 SHA256。脱敏仅替换路径、设备序列号与服务器身份，不重新实现控制逻辑。服务器上实际使用的训练脚本（含 `prepare_checked.py`）与实际 `train.yaml` 已补齐，不只依赖本机较早副本。

固定依赖：

| Dependency | Revision |
|---|---|
| ARX R5 | `e87d09c11edb65f6ae672abc7a41fe2277a2f12f` |
| OrbbecSDK_ROS2 | `c153462518ad674650bafa4464fda72c27ab797a` |
| LingBot-VLA code | `be969b8fd117fb70550c5d4bf4bc328211b5b1b6` |
| Base model | `robbyant/lingbot-vla-v2-6b`; exact shard metadata in the reference verifier |

示范任务 `Put the charger in the box`；71 条人工成功标签、24,576 帧；两 GPU 训练 4000 次更新，无独立验证集。一次现场模型日志记录 300 条目标、操作员报告完成、未自动验证成功。不是整体 100% 成功或无人干预认证。

历史归一化 SHA256：`3f275d6a06931b34c790d8d9784ad57bc13e21b24d9059674bbc0aeb9803d022`。特定原厂 SDK 库 SHA256：`30239795532e0d440842405f02092c85f95b5f4b0813c2bdf95b22d89960fa18`。这些指纹不是文件下载地址，也不授权绕过新环境验收。

原始视频和 bag 不在本仓库发布。双视图 MP4 涉及拼接、标注、编码与时间网格选帧；源时间戳间隙可导致显式标注的重复帧，不称作未经处理原片。视频文件之间对应关系及全程人工干预声明需另行核验。

自采实机数据与 clean-only RoboTwin 仿真比赛分开管理；不以此仓库宣称比赛合规认证或官方真机成绩。

## English

Prepared on 2026-10-25 (Asia/Shanghai). This allowlisted export excludes original Git history, account settings, logs, raw data, videos and weights. Original runtime directories are unchanged.

The manifest stores original and tokenized source hashes. Export changes paths/device/site identity only, not control logic. Actual server training scripts, including `prepare_checked.py`, and the real training YAML are included as sanitized references.

The dependency revisions above and historical normalization/SDK hashes support traceability, not download entitlement or acceptance of a different environment. The recorded experiment is 71 demonstrations, 24,576 frames, two-GPU 4k training and one operator-reported 300-target execution, without independent validation or an audited success rate.

MP4 exports are processed viewing derivatives. Keep raw evidence and independently check video/run correspondence and intervention claims. This real-robot project is separate from clean-only simulation training and does not assert official competition compliance or scores.
