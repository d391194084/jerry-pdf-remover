# 🚀 快速開始指南 - 3 分鐘上手

## 方案選擇

選擇最適合您的方案：

### 💻 方案 1：GitHub Codespaces（推薦 ⭐）
**完全免費，無需安裝任何東西**

1. 進入 [jerry-pdf-remover 倉庫](https://github.com/yourusername/jerry-pdf-remover)
2. 點擊「Code」→「Codespaces」→「Create codespace on main」
3. 等待 2-3 分鐘環境加載
4. 在終端執行：
   ```bash
   pip install -r requirements.txt
   streamlit run streamlit_app.py
   ```
5. ✅ 完成！應用會自動在瀏覽器中打開

### 💾 方案 2：本地執行
**在您的電腦上運行**

```bash
# 1. 克隆倉庫
git clone https://github.com/yourusername/jerry-pdf-remover.git
cd jerry-pdf-remover

# 2. 建立虛擬環境
python -m venv venv

# 3. 啟用虛擬環境
source venv/bin/activate      # Linux/Mac
# 或
venv\Scripts\activate          # Windows

# 4. 安裝依賴
pip install -r requirements.txt

# 5. 執行應用
streamlit run streamlit_app.py

# 6. 打開瀏覽器
# 自動打開 http://localhost:8501
```

### 🌐 方案 3：線上部署（Streamlit Cloud）
**公開分享給他人**

1. Fork 倉庫到您的 GitHub
2. 訪問 [share.streamlit.io](https://share.streamlit.io)
3. 用 GitHub 帳戶登入
4. 點擊「New app」
5. 選擇倉庫、分支、檔案 (`streamlit_app.py`)
6. 點擊「Deploy」
7. ✅ 完成！獲得公開 URL

---

## 使用應用

1. **上傳 PDF**  
   點擊上傳區域選擇您的 PDF 檔案

2. **自動分析**  
   系統會自動分析 PDF 並推薦最佳方案

3. **選擇方案**
   - 方法 1（快速）- 1-5 秒
   - 方法 2（推薦）- 5-15 秒 ⭐
   - 方法 3（完美）- 20-60 秒

4. **開始移除**  
   點擊「開始移除浮水印」按鈕

5. **下載結果**  
   自動下載清潔後的 PDF

---

## 常見問題

**Q：需要安裝什麼軟體？**  
A：使用 Codespaces 時完全不需要。本地執行只需 Python 3.9+

**Q：支援多大的檔案？**  
A：最大 200MB（可修改）

**Q：隱私安全嗎？**  
A：是的，檔案完全在本地或 Codespaces 上處理，不會上傳第三方

**Q：浮水印移除不乾淨？**  
A：嘗試方法 3（完美效果方案），通常能解決問題

**Q：可以批量處理嗎？**  
A：目前支援逐個檔案，可在 GitHub Issues 提交功能請求

---

## 下一步

- 📖 閱讀 [README.md](README.md) 了解更多功能
- 📚 查看 [DEPLOYMENT-GUIDE.md](DEPLOYMENT-GUIDE.md) 詳細部署指南
- 🐛 報告問題或提出建議
- ⭐ 如果有幫助請給個 Star！

---

**提示：** 第一次執行時下載依賴可能需要 2-3 分鐘，後續執行會更快。
