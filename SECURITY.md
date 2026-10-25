# Security / 安全信息

## Inference service / 推理服务

The inference service binds to `127.0.0.1` and uses SSH forwarding for remote access. The HTTP API has no authentication and is intended for loopback access only.

推理服务绑定 `127.0.0.1`，远程连接使用 SSH 隧道。HTTP API 无认证，仅用于回环访问。

## Local configuration / 本地配置

Credentials stay in the local SSH configuration. Site configuration, recordings, models and runtime logs are excluded from Git. Report security issues privately to the repository maintainer.

连接凭据由本地 SSH 配置管理。site 配置、录制、模型和运行日志不纳入 Git。安全问题请私下联系仓库维护者。
