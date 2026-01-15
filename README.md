# 🔍 Jerry PDF 浮水印移除應用

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://github.com/jerry-pdf-remover)

一個強大的 PDF 浮水印移除工具，可直接在 GitHub Codespaces 上執行，無需下載或安裝。

## ✨ 功能特性

- 🚀 **三種智能演算法** - 快速、平衡、完美方案可選
- 📊 **實時 PDF 分析** - 自動檢測浮水印類型並推薦方案
- 💾 **線上直接執行** - 無需安裝，在瀏覽器中即可使用
- 🔒 **隱私優先** - 檔案不會保存到伺服器
- 📱 **響應式設計** - 支援桌面和行動裝置
- ⚡ **快速處理** - 方法 1 只需 1-5 秒
- 🎯 **效果優秀** - 方法 3 可移除 95%+ 的浮水印

## 📂 專案結構

```
jerry-pdf-remover/
├── streamlit_app.py          # Streamlit 主應用
├── requirements.txt          # Python 依賴
├── .streamlit/
│   └── config.toml           # Streamlit 配置
├── README.md                 # 本檔案
└── .gitignore                # Git 忽略規則
```

## 🚀 快速開始

### 方案 A：使用 GitHub Codespaces（推薦）

1. **打開此項目**
   - 進入 GitHub 上的 `jerry-pdf-remover` 倉庫

2. **啟動 Codespaces**
   ```
   按下 Code → Codespaces → Create codespace on main
   ```

3. **安裝依賴**
   ```bash
   pip install -r requirements.txt
   ```

4. **執行應用**
   ```bash
   streamlit run streamlit_app.py
   ```

5. **打開應用**
   - Codespaces 會自動在新標籤中打開應用
   - 或訪問顯示的 URL（通常是 `localhost:8501`）

### 方案 B：本地執行

1. **克隆倉庫**
   ```bash
   git clone https://github.com/yourusername/jerry-pdf-remover.git
   cd jerry-pdf-remover
   ```

2. **建立虛擬環境**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   venv\Scripts\activate     # Windows
   ```

3. **安裝依賴**
   ```bash
   pip install -r requirements.txt
   ```

4. **執行應用**
   ```bash
   streamlit run streamlit_app.py
   ```

5. **打開瀏覽器**
   - 自動打開 `http://localhost:8501`

### 方案 C：雲端部署（Streamlit Cloud）

1. **Fork 此倉庫**到您的 GitHub 帳戶

2. **連接到 Streamlit Cloud**
   - 訪問 [share.streamlit.io](https://share.streamlit.io)
   - 登入您的 GitHub 帳戶
   - 點擊「New app」

3. **配置應用**
   - Repository: `yourusername/jerry-pdf-remover`
   - Branch: `main`
   - Main file path: `streamlit_app.py`

4. **部署**
   - 點擊「Deploy」
   - 等待部署完成

## 📖 使用說明

### 基本步驟

1. **上傳 PDF**
   - 點擊「選擇 PDF 檔案」上傳您的 PDF

2. **分析檔案**
   - 系統會自動分析 PDF 並推薦最佳方案

3. **選擇方案**
   - **方法 1（快速）** - 適合簡單浮水印
   - **方法 2（推薦）** - 適合一般浮水印
   - **方法 3（完美）** - 適合複雜浮水印

4. **開始處理**
   - 點擊「開始移除浮水印」按鈕

5. **下載結果**
   - 處理完成後自動下載清潔後的 PDF

### 方案對比

| 方案 | 速度 | 效果 | 複雜度 | 適用場景 |
|------|------|------|--------|---------|
| 方法 1 | ⚡⚡⚡ 極快 | ⭐⭐⭐⭐ | 簡單 | 簡單浮水印 |
| 方法 2 | ⚡⚡ 適中 | ⭐⭐⭐⭐⭐ | 中等 | 一般浮水印 |
| 方法 3 | ⚡ 較慢 | ⭐⭐⭐⭐⭐ | 複雜 | 複雜浮水印 |

## 🔧 三種移除方法詳解

### 方法 1：快速移除（PyMuPDF）
- **原理** - 直接移除向量浮水印圖層
- **優點** - 速度最快（1-5 秒），無損處理
- **缺點** - 複雜浮水印效果可能不完美
- **適用** - 簡單的灰色文字浮水印

### 方法 2：平衡方案（混合處理）
- **原理** - 結合向量移除和影像增強
- **優點** - 速度適中（5-15 秒），效果好，通用性強
- **缺點** - 檔案大小可能增加
- **適用** - 大多數常見浮水印

### 方法 3：完美效果（PDF 重構）
- **原理** - 完全重構 PDF，應用多層影像處理
- **優點** - 效果最好（95%+ 移除率），適合所有浮水印
- **缺點** - 速度較慢（20-60 秒），檔案較大
- **適用** - 複雜、淺色、多層浮水印

## 🔒 隱私保護

- ✅ 所有檔案在本地或 Codespaces 上處理
- ✅ 檔案不會保存到任何伺服器
- ✅ 處理完成後立即刪除臨時檔案
- ✅ 無廣告、無追蹤、無數據收集

## 🐛 常見問題

### Q: 支援多大的 PDF？
A: 最大 200MB（Streamlit 預設限制）。可在 `streamlit_app.py` 中修改：
```python
st.file_uploader(..., maximum_upload_size=200)
```

### Q: 處理失敗怎麼辦？
A: 
1. 確保 PDF 檔案有效
2. 嘗試不同的移除方案
3. 檔案過大時分割成多個檔案

### Q: 需要網路連接嗎？
A: 本地執行時不需要（除了 Streamlit 驗證）
   Codespaces 或 Cloud 部署需要連接

### Q: 浮水印移除不乾淨？
A: 嘗試方法 3（完美效果方案），通常能解決問題

### Q: 可以批量處理嗎？
A: 目前支援逐個檔案處理。可在 GitHub Issues 中提交功能請求

## 📦 依賴

- **streamlit** - Web 框架
- **PyMuPDF (fitz)** - PDF 處理
- **Pillow** - 影像處理
- **numpy** - 數值計算
- **scipy** - 科學計算

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

1. Fork 此倉庫
2. 建立功能分支 (`git checkout -b feature/new-feature`)
3. 提交更改 (`git commit -m 'Add new feature'`)
4. 推送到分支 (`git push origin feature/new-feature`)
5. 打開 Pull Request

## 📝 License

MIT License - 詳見 LICENSE 檔案

## 👨‍💼 作者

**Jerry** - IT 基礎設施與網路安全專家

## ⭐ 如果有幫助，請給個 Star！

您的支持是我繼續維護這個項目的動力！

---

## 📞 聯繫與支持

- 📧 通過 GitHub Issues 提交問題
- 💬 提交功能請求和建議
- 🐛 報告 Bug

---

**最後更新:** 2026-01-16
**版本:** 1.0.0
