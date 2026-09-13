# 曼城学院模型资产

原始目录中的 6 个模型文件完整备份，合计 **16,278,749,490 字节（约 16.28 GB）**。

大型文件以无损 ZIP 压缩分卷保存在本仓库的 [Releases](https://github.com/Calix-L/manchester-institute-assets/releases/tag/assets-2026-09-13) 中。Git 仓库保存资产清单、SHA-256 校验值和还原脚本。仅运行 `git clone` 或下载 GitHub 自动生成的 Source code ZIP 不会下载模型文件。

| 文件 | 原始大小（字节） |
| --- | ---: |
| 曼城学院.blend | 1,321,962,816 |
| 曼城学院.mtl | 214,648 |
| 曼城学院.obj | 14,406,443,718 |
| 曼城学院内部结构.fbx | 350,099,260 |
| 曼城学院外部.fbx | 100,016,140 |
| 曼城学院外部结构.fbx | 100,012,908 |

## 下载和还原

需要 Python 3，以及已登录并有本私有仓库访问权限的 GitHub CLI。请在至少有 30 GB 可用空间的目录操作。

```powershell
gh repo clone Calix-L/manchester-institute-assets
cd manchester-institute-assets
gh release download assets-2026-09-13 --repo Calix-L/manchester-institute-assets --pattern "manchester-institute-assets.zip.*" --dir downloads
python restore_assets.py --parts-dir downloads --output-dir assets
```

也可以从 Releases 页面手动下载全部 `.zip.001`、`.zip.002` 等分卷，放入 `downloads` 目录后执行还原脚本。分卷必须齐全。

脚本会校验每个分卷，按顺序拼接 ZIP，然后逐文件解压并验证原始 SHA-256。原文件名和内容保留；现有内容不同的文件不会被覆盖。还原结果位于 `assets` 目录。

`assets-manifest.json` 包含原文件、压缩包和各分卷的精确大小及校验值。

## 备份范围

本版本备份上述 6 个文件，未修改模型内容，也未检查模型引用的外部纹理是否齐全。ZIP 分卷仅用于传输；编辑模型前需先还原。
