# 📚 Jerry PDF 浮水印移除 - 完整部署指南

## 目錄
1. [GitHub Codespaces 部署](#github-codespaces-部署推薦)
2. [本地執行](#本地執行)
3. [Streamlit Cloud 部署](#streamlit-cloud-部署)
4. [故障排除](#故障排除)

---

## GitHub Codespaces 部署（推薦 ⭐）

### 為什麼選擇 Codespaces？
- ✅ 無需安裝任何軟體
- ✅ 完全免費（每月 60 小時免費額度）
- ✅ 在瀏覽器中直接運行
- ✅ 自動環境配置
- ✅ 支援即時協作

### 步驟 1：進入 GitHub
1. 訪問 [GitHub jerry-pdf-remover 倉庫](https://github.com/yourusername/jerry-pdf-remover)
2. 確保已登入您的 GitHub 帳戶

### 步驟 2：啟動 Codespaces
1. 點擊綠色「Code」按鈕
   ```
   ▼ Code
   ```
2. 選擇「Codespaces」標籤
3. 點擊「Create codespace on main」
4. 等待環境載入（約 2-3 分鐘）

### 步驟 3：安裝依賴
在終端執行：
```bash
pip install -r requirements.txt
```

### 步驟 4：啟動應用
```bash
streamlit run streamlit_app.py
```

### 步驟 5：打開應用
- 瀏覽器會自動打開應用
- 或點擊終端中顯示的 URL
- 通常是：`https://[random-id].github.dev`

### 使用 Codespaces 的提示
- 💡 環境在 30 分鐘無操作後會自動關閉
- 💡 關閉標籤頁不會刪除 Codespace，可重新打開
- 💡 Codespace 已包含所有必要的 Python 版本
- 💡 在 `.devcontainer` 中可自訂開發環境

---

## 本地執行

### 系統要求
- Python 3.9 或更新版本
- pip（Python 套件管理器）
- 2GB 可用硬碟空間

### 步驟 1：克隆倉庫
```bash
# 使用 HTTPS
git clone https://github.com/yourusername/jerry-pdf-remover.git
cd jerry-pdf-remover

# 或使用 SSH
git clone git@github.com:yourusername/jerry-pdf-remover.git
cd jerry-pdf-remover
```

### 步驟 2：建立虛擬環境
建議為每個項目建立獨立的虛擬環境：

**Linux / macOS：**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows：**
```bash
python -m venv venv
venv\Scripts\activate
```

### 步驟 3：安裝依賴
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 步驟 4：驗證安裝
```bash
python -c "import streamlit; print(f'Streamlit {streamlit.__version__}')"
python -c "import fitz; print('PyMuPDF installed')"
```

### 步驟 5：啟動應用
```bash
streamlit run streamlit_app.py
```

### 步驟 6：打開瀏覽器
- 自動打開 `http://localhost:8501`
- 如果沒有自動打開，手動訪問上述地址

### 停止應用
在終端按 `Ctrl + C`

---

## Streamlit Cloud 部署

### 優點
- 🌐 公開網址，可分享給他人
- 🚀 自動化部署
- 💾 免費託管
- 📊 應用統計

### 步驟 1：Fork 倉庫
1. 訪問原始倉庫
2. 點擊「Fork」按鈕
3. 選擇您的帳戶

### 步驟 2：登錄 Streamlit Cloud
1. 訪問 [share.streamlit.io](https://share.streamlit.io)
2. 點擊「Sign up」或「Login」
3. 使用 GitHub 帳戶登入

### 步驟 3：部署應用
1. 點擊「New app」
2. 填入以下信息：
   - **Repository**: `yourusername/jerry-pdf-remover`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`

3. 點擊「Deploy」

### 步驟 4：等待部署完成
- 應用會自動部署
- 顯示 URL 如：`https://jerry-pdf-remover.streamlit.app`
- 部署通常需要 2-3 分鐘

### 管理 Streamlit Cloud 應用
- 查看應用日誌：點擊右上角「☰」→「View logs」
- 刪除應用：點擊「☰」→「Settings」→「Delete app」
- 分享應用：複製 URL 分享給他人

---

## 故障排除

### 問題 1：PyMuPDF 安裝失敗

**症狀：** 
```
ERROR: Could not build wheels for PyMuPDF
```

**解決方案：**
```bash
# 在 Windows 上，可能需要 Visual C++ Build Tools
# 或使用預編譯的 wheel：
pip install --upgrade pip wheel setuptools
pip install PyMuPDF==1.23.8

# 如果仍然失敗，嘗試：
pip install pymupdf  # 小寫名稱
```

### 問題 2：Streamlit 找不到應用

**症狀：**
```
ValueError: Could not find the module at 'streamlit_app.py'
```

**解決方案：**
- 確保檔案名稱正確：`streamlit_app.py`
- 確保在項目根目錄執行命令
- 檢查 `ls` 或 `dir` 命令確認檔案存在

### 問題 3：終端打不開 Streamlit

**症狀：**
```
Streamlit requires raw mode. Press 'y' to continue...
```

**解決方案：**
```bash
# 使用此命令代替：
streamlit run streamlit_app.py --logger.level=debug
```

### 問題 4：記憶體不足

**症狀：** 處理大檔案時應用崩潰

**解決方案：**
```bash
# 設定記憶體限制
streamlit run streamlit_app.py --maxUploadSize=200
```

### 問題 5：GPU 加速（可選）

如果您有 NVIDIA GPU，可加速影像處理：

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 問題 6：Python 版本不兼容

**檢查 Python 版本：**
```bash
python --version  # 應為 3.9 或以上
```

**如果版本過舊：**
- Windows：從 [python.org](https://www.python.org) 下載最新版本
- macOS：使用 Homebrew：`brew install python@3.11`
- Linux：使用套件管理器：`sudo apt install python3.11`

### 問題 7：Codespaces 時間限制

**症狀：** Codespace 在 30 分鐘後自動停止

**解決方案：**
1. 右下角找到 Codespace 標籤
2. 點擊「...」→「Codespaces」→「Change retention period」
3. 選擇更長的時間（最多 28 天）

### 問題 8：檔案大小限制

**症狀：** 提示檔案太大

**解決方案：**
在 `streamlit_app.py` 中修改：
```python
# 將此行改為更大的值（MB）
st.file_uploader(..., maximum_upload_size=500)  # 500 MB
```

---

## 性能最佳化

### 對於 Codespaces：
```bash
# 使用更少的記憶體
streamlit run streamlit_app.py --client.maxMessageSize=10
```

### 對於本地：
```bash
# 使用多線程
export OMP_NUM_THREADS=4
streamlit run streamlit_app.py
```

### 對於 Streamlit Cloud：
在 `.streamlit/config.toml` 中添加：
```toml
[client]
maxMessageSize = 200  # MB
```

---

## 更新應用

### 更新本地版本：
```bash
cd jerry-pdf-remover
git pull origin main
pip install -r requirements.txt --upgrade
```

### 自動更新 Codespaces：
```bash
git pull origin main && pip install -r requirements.txt --upgrade
streamlit run streamlit_app.py
```

---

## 常見配置

### 改變 Streamlit 主題
編輯 `.streamlit/config.toml`：
```toml
[theme]
primaryColor = "#0284c7"
backgroundColor = "#0f172a"
secondaryBackgroundColor = "#1e293b"
textColor = "#f1f5f9"
```

### 改變 Streamlit 埠
```bash
streamlit run streamlit_app.py --server.port=8080
```

### 禁用 Streamlit 分析
```bash
streamlit run streamlit_app.py --logger.level=error
```

---

## 獲取幫助

1. 📖 查看 [Streamlit 文檔](https://docs.streamlit.io)
2. 🐛 在 GitHub Issues 提交問題
3. 💬 開始討論（GitHub Discussions）
4. 📧 聯繫維護者

---

## 下一步

- 📚 閱讀 [README.md](README.md) 了解功能
- 🔧 探索 `streamlit_app.py` 源代碼
- 🚀 在 Streamlit Cloud 部署您的版本
- 💡 提交改進建議

---

**更新時間：** 2026-01-16  
**作者：** Jerry  
**License：** MIT
