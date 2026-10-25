# Security / 安全信息

Do not post secrets, network addresses or unredacted recordings in issues. Report suspected credential exposure privately to the repository owner; rotate the credential, then review history. Deleting a file from the latest commit does not remove it from history.

不要在 Issue 中发布密钥、内网地址或未经脱敏的录制。发现凭据泄漏应私下联系仓库所有者，先轮换凭据再检查历史。仅删除最新版本文件不能消除 Git 历史中的泄漏。

Model inference binds to loopback and is accessed through SSH forwarding. Do not expose the unauthenticated reference HTTP service on a public interface. Robot startup and motion require a local operator; stopping a Python process is not a certified emergency stop.

模型推理服务只绑定回环地址，通过 SSH 隧道访问。不要将参考代码中无认证的 HTTP 服务公开到网络。硬件启动与运动需要现场操作员，退出 Python 不等于可靠急停。
