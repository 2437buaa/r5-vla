# Third-party notices / 第三方声明

This repository does not claim ownership of upstream robot SDKs, models, datasets or dependencies. Project-authored glue and documentation use Apache-2.0; attributed vendor derivatives retain their own license.

本仓库不主张拥有上游机器人 SDK、模型、数据集或依赖。项目自编集成代码与文档使用 Apache-2.0；注明来源的原厂衍生文件保持其原许可。

| Component / 组件 | Source / 来源 | Treatment / 处理 |
|---|---|---|
| ARX R5 ROS wrapper | https://github.com/ARXroboticsX/R5 | One modified C++ wrapper included under BSD-3-Clause, license and changes retained; full SDK/binaries excluded. / 仅转载已注明修改的包装层，保留 BSD；不含完整 SDK 或二进制。 |
| LingBot-VLA 2.0 | https://github.com/robbyant/lingbot-vla-v2 | Apache-2.0 upstream code dependency; obtain separately. Small trainer source anchors appear in integration code; upstream remains attributed. / 上游代码独立获取，训练集成含少量源码锚点，保留归属。 |
| Official base weights | https://huggingface.co/robbyant/lingbot-vla-v2-6b | Not redistributed; follow model card and applicable weight terms. / 不转载，按模型自身条款获取。 |
| OrbbecSDK_ROS2 | https://github.com/orbbec/OrbbecSDK_ROS2 | Not vendored; upstream source and bundled SDK retain their own notices. / 不打包，源码和 SDK 遵守各自声明。 |
| LeRobot | https://github.com/huggingface/lerobot | Data-library dependency, not vendored. / 数据处理依赖，不转载其实现。 |
| ROS 2 / MCAP / OpenCV / PyTorch | Respective upstream projects / 各自上游 | Installed separately and governed by their own licenses. / 单独安装，遵守各自许可。 |

Author attribution is not endorsement. Before public release, recheck contributor rights and terms for any added code/data. Copying a model hash or naming a vendor is not permission to redistribute weights or binary SDKs.

注明来源不代表原厂背书。公开前复核新增内容的作者权利及许可；模型 hash 或厂商名称不构成转载权重/SDK 的授权。
