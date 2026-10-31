# Yelp 商业数据分析与交互式大屏展示

## 1. 项目简介
本项目为《商业数据分析》期末大作业。基于 Yelp 官方公开数据集，使用纯 Python 技术栈，完成了从“数据合规获取 → 清洗治理 → 商业模型分析（RFM、帕累托、VADER 情感分析、SARIMA 预测） → 可视化复现 → Streamlit 交互式大屏搭建”的端到端商业数据分析流程。

## 2. 数据来源与合规声明
- **数据源名称**：Yelp Open Dataset
- **官方 URL**：https://www.yelp.com/dataset
- **获取方式**：官方提供的一次性下载文件（非爬虫，符合课程白名单要求）
- **获取日期**：2026 年 10 月 【这里改一下具体日期】
- **授权说明**：遵循 Yelp 官方学术用途协议。**因数据协议限制，本仓库未上传原始 JSON 大文件。** 仅保留了抽样清洗后的 500 行数据（位于 `data/clean/` 目录下）。原始数据请自行前往官网下载。

## 3. 环境依赖
在运行本项目前，请确保已安装 Python 3.8+ 环境。
安装依赖包：
```bash
pip install -r requirements.txt

克隆本仓库到本地后，按以下顺序执行：
python scripts/01_data_clean.py
python scripts/02_model_analysis.py
streamlit run app.py
