# Contributing / 参与协作

## 中文

本地配置使用 `config/site.local.json`，运行目录为 `runtime/`。两者以及数据、模型和日志均由 `.gitignore` 排除。

文档和代码检查：

```bash
python3 scripts/check_repository.py
python3 -m unittest discover -s tests -v
```

`provenance/source-manifest.json` 记录参考文件的 SHA256。修改参考源文件时同步更新对应条目。CI 执行静态检查和配置生成测试。

## English

Local configuration uses `config/site.local.json`; generated files live in `runtime/`. Both are Git-ignored, along with data, models and logs.

Run the checks above before submitting changes. `provenance/source-manifest.json` records reference-file SHA256 values; update the corresponding entries when reference sources change. CI runs static checks and configuration-rendering tests.
