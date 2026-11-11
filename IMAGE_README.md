# Kokoro 配音

文字转中文或美式英文女声，支持调整语速并下载WAV。

## 基本环境

Ubuntu 22.04，Python 3.12，PyTorch 2.8.0，CUDA 12.8。支持CPU或GPU；建议8GB内存起测。语音前端字典另占少量空间。

## 使用方法

创建并启动实例后，直接打开“自定义服务6006”，按页面提示运行任务并下载结果。首次任务需要初始化模型。

- 项目：https://github.com/zw2029181901/autodl-kokoro
- 代码：`/root/autodl-active`
- 模型：`/root/autodl-active/models`，权重已包含，无需再次下载。
- Python：`/root/autodl-active/.venv/bin/python`
- 启动命令：`bash /root/autodl-active/run-service.sh`
- 输出等预留磁盘：2GB

## 环境验证

```bash
/root/autodl-active/.venv/bin/python /root/autodl-active/runtime/doctor.py --project /root/autodl-active --models --http
```

独立导出环境已在RTX3090通过真实HTTP上传、排队、模型推理和下载。之后在无卡模式核对系统盘模型路径、文件大小、软链接、依赖及6006服务；不重复执行完整推理。开机机制沿用U2Net保存镜像新实例验证通过的同一配置，没有为本应用另建客户测试实例。完整记录见 `IMAGE_VALIDATION.json`。

镜像 `autodl-kokoro-20261111`，UUID `image-7765357d0f`，平台体积1.86GB，已就绪。社区审核及公开状态以平台当前状态为准。

模型和依赖许可见 `THIRD_PARTY.md` 与 `licenses`。结果应按实际用途核验。
