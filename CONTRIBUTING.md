# Contributing / 参与协作

## 中文

仓库先保持 private。管理员通过 Settings → Collaborators，以队友 GitHub 用户名邀请；队友接受后克隆仓库。管理页面不是所有人通用的邀请链接，真实邀请绑定指定账号。

建议每项修改新建分支，通过 Pull Request 说明修改、验证方式、是否可能影响硬件运动。不要直接覆盖历史证据或改写共享分支历史。硬件相关改动不得靠 GitHub Actions 自动实机验收。

本地配置放 `config/site.local.json`，生成副本放 `runtime/`，均不提交。原始 bag、图像、视频、权重及带个人/服务器信息的日志默认不提交。控制逻辑变更与路径重构分开提交；如改动参考源文件，需要同步更新来源 manifest 并披露其已不再是原始导出快照。

## English

Keep the repository private initially. Administrators invite specific GitHub usernames in Settings → Collaborators. The management page is not a universal invitation link; actual invitations are account-bound.

Use feature branches and pull requests describing the change, verification and possible motion effects. Preserve evidence and shared history. CI must never perform physical hardware acceptance.

Keep local configuration and rendered runtime untracked. Do not commit raw bags, images, videos, weights or identifying logs by default. Separate control changes from path refactors. If a reference source changes, update its provenance manifest and disclose that it is no longer an unchanged export.
