# Public-release checklist / 转公开前检查

## 中文

- [ ] 所有共同作者同意代码/文档的公开和许可；原始数据、视频中涉及的人、设备及场所另行取得授权。
- [ ] 扫描全部 Git 历史而不只是最新文件；无凭据、内网地址、私人序列号或个人目录。
- [ ] 外部依赖保留来源和许可；无误归属原厂代码、模型、SDK 二进制。
- [ ] 本地 site 配置、录制、权重和运行日志不在提交中。
- [ ] 上游获取、编译、配置生成及只读工具由另一台干净机器复核。
- [ ] 重新审查并记录所有硬件控制保护与停机行为；已注释的检查不冒称有效。
- [ ] 演示说明披露人工启动、停止、干预和成功判断；无未经核验的成功率。
- [ ] 新数据集重新建立选择、时间对齐、标签、归一化与部署绑定；未直接套用历史常量。
- [ ] 仓库所有者明确决定由 private 转 public；不由脚本自动转换。

## English

- [ ] Obtain contributor agreement and separate rights for any data/video/site/person disclosure.
- [ ] Scan all Git history, not just the latest files, for credentials and identifying configuration.
- [ ] Retain upstream attribution/licenses; do not relicense vendor binaries, weights or datasets.
- [ ] Keep local configuration, raw recordings, weights and runtime logs out of commits.
- [ ] Recheck source acquisition, build, configuration and read-only tools on a clean machine.
- [ ] Review actual hardware guards and stopping behavior; do not claim disabled checks are active.
- [ ] Disclose operator actions/intervention and success criteria; no unaudited success rates.
- [ ] Rebuild selection, alignment, targets, normalization and deployment bindings for new datasets.
- [ ] Make visibility public only through an explicit owner decision, never automatically.
