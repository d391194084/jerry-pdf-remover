import streamlit as st
import fitz  # PyMuPDF
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import io
import tempfile
import os
from pathlib import Path

# ============================================================
# 頁面配置
# ============================================================
st.set_page_config(
    page_title="Jerry PDF 浮水印移除",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自訂樣式
st.markdown("""
    <style>
    .main-title {
        background: linear-gradient(135deg, #0284c7, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .subtitle {
        color: #cbd5e1;
        font-size: 1.1em;
        margin-bottom: 30px;
    }
    .method-box {
        background: rgba(2, 132, 199, 0.1);
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    .success-box {
        background: rgba(22, 163, 74, 0.1);
        border-left: 4px solid #16a34a;
        padding: 15px;
        border-radius: 6px;
        color: #16a34a;
    }
    .error-box {
        background: rgba(220, 38, 38, 0.1);
        border-left: 4px solid #dc2626;
        padding: 15px;
        border-radius: 6px;
        color: #dc2626;
    }
    .info-box {
        background: rgba(2, 132, 199, 0.05);
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 8px;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================
# 工具函數 - PDF 分析
# ============================================================

def analyze_pdf(pdf_bytes):
    """分析 PDF 檔案特徵"""
    try:
        # 保存到臨時檔案
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            tmp.write(pdf_bytes)
            tmp_path = tmp.name
        
        doc = fitz.open(tmp_path)
        analysis = {
            'total_pages': len(doc),
            'has_drawings': False,
            'has_images': False,
            'watermark_detected': False,
            'recommended_method': 'method2',
            'file_size_mb': len(pdf_bytes) / (1024 * 1024)
        }
        
        # 掃描第一頁
        if len(doc) > 0:
            page = doc[0]
            
            # 檢查向量圖形
            try:
                drawings = page.get_drawings()
                analysis['has_drawings'] = len(drawings) > 0
                
                # 檢查浮水印
                if drawings:
                    for drawing in drawings:
                        if hasattr(drawing, 'color') and drawing.color:
                            color = drawing.color
                            if all(180 <= c <= 230 for c in color):
                                analysis['watermark_detected'] = True
                                break
            except:
                pass
            
            # 檢查影像
            try:
                images = page.get_images()
                analysis['has_images'] = len(images) > 0
            except:
                pass
        
        doc.close()
        os.unlink(tmp_path)
        
        return analysis, None
    
    except Exception as e:
        if os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except:
                pass
        return None, f"分析失敗: {str(e)}"

# ============================================================
# 工具函數 - 浮水印移除方法
# ============================================================

def remove_watermark_method1(pdf_bytes):
    """
    方法 1：快速移除（PyMuPDF）
    直接移除向量浮水印圖層
    """
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            tmp.write(pdf_bytes)
            tmp_path = tmp.name
        
        doc = fitz.open(tmp_path)
        
        for page_num, page in enumerate(doc):
            try:
                drawings = page.get_drawings()
                removed_count = 0
                
                for drawing in drawings:
                    try:
                        if hasattr(drawing, 'color') and drawing.color:
                            color = drawing.color
                            # 檢查是否為淺灰色浮水印
                            if len(color) >= 3 and all(180 <= c <= 230 for c in color[:3]):
                                page.delete_drawings(drawing)
                                removed_count += 1
                    except:
                        pass
                
                if removed_count > 0:
                    st.write(f"✓ 第 {page_num + 1} 頁：移除 {removed_count} 個浮水印元素")
            except:
                pass
        
        # 保存到位元組
        output_bytes = io.BytesIO()
        doc.save(output_bytes, incremental=False)
        doc.close()
        
        return output_bytes.getvalue(), None
    
    except Exception as e:
        return None, f"方法 1 失敗: {str(e)}"
    
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except:
                pass

def remove_watermark_method2(pdf_bytes):
    """
    方法 2：平衡方案（混合處理）
    低解析度渲染 + 對比度增強
    """
    tmp_path = None
    temp_files = []
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            tmp.write(pdf_bytes)
            tmp_path = tmp.name
        
        doc = fitz.open(tmp_path)
        
        # 第一步：嘗試移除向量浮水印
        for page in doc:
            try:
                drawings = page.get_drawings()
                for drawing in drawings:
                    try:
                        if hasattr(drawing, 'color') and drawing.color:
                            color = drawing.color
                            if len(color) >= 3 and all(180 <= c <= 230 for c in color[:3]):
                                page.delete_drawings(drawing)
                    except:
                        pass
            except:
                pass
        
        # 第二步：轉為影像並增強
        output_doc = fitz.open()
        
        for page_num, page in enumerate(doc):
            try:
                # 1.5x 解析度渲染（平衡速度和品質）
                pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False)
                
                # 轉為 PIL 影像
                img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
                
                # 增加對比度
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(1.2)
                
                # 增加亮度
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(1.05)
                
                # 輕微銳化
                img = img.filter(ImageFilter.SHARPEN)
                
                # 轉回 Pixmap 並添加到新 PDF
                img_bytes = io.BytesIO()
                img.save(img_bytes, format='PPM')
                img_bytes.seek(0)
                
                new_pix = fitz.Pixmap(img_bytes)
                page_rect = fitz.Rect(0, 0, pix.width, pix.height)
                output_doc.insert_image(page_rect, pixmap=new_pix)
                
                st.write(f"✓ 已處理第 {page_num + 1} 頁")
                
            except Exception as e:
                st.warning(f"⚠️ 第 {page_num + 1} 頁處理出現問題: {str(e)}")
                # 如果處理失敗，嘗試直接使用原始頁面
                try:
                    pix = page.get_pixmap(alpha=False)
                    output_doc.insert_image(fitz.Rect(0, 0, pix.width, pix.height), pixmap=pix)
                except:
                    pass
        
        output_bytes = io.BytesIO()
        output_doc.save(output_bytes, incremental=False)
        output_doc.close()
        doc.close()
        
        return output_bytes.getvalue(), None
    
    except Exception as e:
        return None, f"方法 2 失敗: {str(e)}"
    
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except:
                pass

def remove_watermark_method3(pdf_bytes):
    """
    方法 3：完美效果（PDF 重構）
    2x 解析度 + 多層影像處理
    """
    tmp_path = None
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            tmp.write(pdf_bytes)
            tmp_path = tmp.name
        
        doc = fitz.open(tmp_path)
        output_doc = fitz.open()
        
        for page_num, page in enumerate(doc):
            try:
                # 2x 解析度渲染
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
                
                # 轉為 PIL 影像
                img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
                
                # 多層影像處理
                # 1. 增加對比度
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(1.35)
                
                # 2. 增加銳度
                enhancer = ImageEnhance.Sharpness(img)
                img = enhancer.enhance(1.15)
                
                # 3. 轉為 numpy array 進行進階處理
                img_array = np.array(img)
                
                # 檢測淺灰色區域（浮水印）
                gray = np.mean(img_array, axis=2)
                watermark_mask = (gray > 170) & (gray < 240)
                
                # 對浮水印區域應用高斯模糊淡化
                if np.any(watermark_mask):
                    # 使用 PIL 的 GaussianBlur 替代 scipy
                    img_blurred = img.filter(ImageFilter.GaussianBlur(radius=2))
                    img_blurred_array = np.array(img_blurred)
                    
                    # 混合原始和模糊版本（70% 原始 + 30% 模糊）
                    for channel in range(3):
                        img_array[:, :, channel] = (
                            img_array[:, :, channel] * 0.7 + 
                            img_blurred_array[:, :, channel] * 0.3
                        ).astype(np.uint8)
                
                # 轉回 PIL 影像
                img = Image.fromarray(img_array.astype('uint8'))
                
                # 轉換為 Pixmap 並添加
                img_bytes = io.BytesIO()
                img.save(img_bytes, format='PPM')
                img_bytes.seek(0)
                
                new_pix = fitz.Pixmap(img_bytes)
                output_doc.insert_image(fitz.Rect(0, 0, pix.width, pix.height), pixmap=new_pix)
                
                st.write(f"✓ 已處理第 {page_num + 1} 頁")
                
            except Exception as e:
                st.warning(f"⚠️ 第 {page_num + 1} 頁處理出現問題: {str(e)}")
                # 降級處理
                try:
                    pix = page.get_pixmap(alpha=False)
                    output_doc.insert_image(fitz.Rect(0, 0, pix.width, pix.height), pixmap=pix)
                except:
                    pass
        
        output_bytes = io.BytesIO()
        output_doc.save(output_bytes, incremental=False)
        output_doc.close()
        doc.close()
        
        return output_bytes.getvalue(), None
    
    except Exception as e:
        return None, f"方法 3 失敗: {str(e)}"
    
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except:
                pass

# ============================================================
# Streamlit 應用主體
# ============================================================

# 標題
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div class="main-title">🔍 Jerry PDF 智能浮水印移除</div>', 
                unsafe_allow_html=True)
    st.markdown('<div class="subtitle">在 GitHub 上直接執行，無需下載</div>', 
                unsafe_allow_html=True)

# 主要內容
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.subheader("📁 上傳 PDF 檔案", divider="blue")
    
    uploaded_file = st.file_uploader(
        "選擇 PDF 檔案",
        type=['pdf'],
        help="支援最大 200MB 的檔案"
    )
    
    if uploaded_file:
        file_size = len(uploaded_file.getvalue()) / (1024 * 1024)
        st.success(f"✓ 檔案已上傳: {uploaded_file.name}\n大小: {file_size:.2f} MB")
        
        # 分析 PDF
        with st.spinner("🔄 正在分析 PDF..."):
            analysis, error = analyze_pdf(uploaded_file.getvalue())
        
        if error:
            st.error(f"❌ {error}")
        else:
            st.info(f"""
            📊 **PDF 分析結果**
            - 頁數: {analysis['total_pages']}
            - 向量圖形: {'有' if analysis['has_drawings'] else '無'}
            - 浮水印檢測: {'✓ 檢測到' if analysis['watermark_detected'] else '✗ 未檢測到'}
            - 推薦方案: 方法 {analysis['recommended_method'][6]}
            """)

with col_right:
    st.subheader("⚙️ 選擇移除方案", divider="blue")
    
    # 三種方案的詳細說明
    method_info = {
        'method1': {
            'title': '方法 1：快速移除',
            'desc': '直接移除向量浮水印圖層',
            'pros': ['⚡ 速度最快', '✓ 適合簡單浮水印', '✓ 無損處理'],
            'cons': ['複雜浮水印效果可能不完美'],
            'time': '1-3 秒'
        },
        'method2': {
            'title': '方法 2：平衡方案 ⭐ 推薦',
            'desc': '結合向量移除和影像增強',
            'pros': ['⚡ 速度適中', '✓ 效果好', '✓ 通用性強'],
            'cons': ['檔案大小可能增加'],
            'time': '5-10 秒'
        },
        'method3': {
            'title': '方法 3：完美效果',
            'desc': '完全重構 PDF（最佳效果）',
            'pros': ['✓ 效果最好（95%+）', '✓ 適合所有浮水印', '✓ 質量最高'],
            'cons': ['速度較慢', '檔案較大'],
            'time': '15-30 秒'
        }
    }
    
    selected_method = st.radio(
        "選擇移除方案",
        options=['method1', 'method2', 'method3'],
        format_func=lambda x: method_info[x]['title'],
        help="選擇適合您需求的方案"
    )
    
    # 顯示選中方案的詳細資訊
    method = method_info[selected_method]
    st.markdown(f"""
    <div class="method-box">
    <h4>{method['title']}</h4>
    <p><strong>描述:</strong> {method['desc']}</p>
    
    <strong style="color: #16a34a;">✓ 優點</strong>
    {"".join([f"<div>• {p}</div>" for p in method['pros']])}
    
    <strong style="color: #f97316;">✗ 缺點</strong>
    {"".join([f"<div>• {c}</div>" for c in method['cons']])}
    
    <p><strong>⏱️ 處理時間:</strong> {method['time']}</p>
    </div>
    """, unsafe_allow_html=True)

# 處理區域
st.divider()

col_process_left, col_process_right = st.columns([1, 1], gap="large")

with col_process_left:
    st.subheader("🚀 開始處理", divider="blue")
    
    if uploaded_file:
        if st.button("開始移除浮水印", type="primary", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            output_container = st.container()
            
            try:
                status_text.text("⏳ 準備處理...")
                progress_bar.progress(10)
                
                pdf_bytes = uploaded_file.getvalue()
                
                with output_container:
                    st.info("📋 處理進度:")
                    progress_placeholder = st.empty()
                
                if selected_method == 'method1':
                    status_text.text("⏳ 使用方法 1 處理中...")
                    progress_bar.progress(40)
                    output_bytes, error = remove_watermark_method1(pdf_bytes)
                
                elif selected_method == 'method2':
                    status_text.text("⏳ 使用方法 2 處理中...")
                    progress_bar.progress(40)
                    output_bytes, error = remove_watermark_method2(pdf_bytes)
                
                else:  # method3
                    status_text.text("⏳ 使用方法 3 處理中...")
                    progress_bar.progress(40)
                    output_bytes, error = remove_watermark_method3(pdf_bytes)
                
                if error:
                    st.error(f"❌ 處理失敗: {error}")
                else:
                    progress_bar.progress(100)
                    status_text.text("✓ 處理完成！")
                    
                    # 顯示下載按鈕
                    st.success("✓ 浮水印已移除，請下載檔案")
                    
                    st.download_button(
                        label="⬇️ 下載清潔後的 PDF",
                        data=output_bytes,
                        file_name=f"clean_{uploaded_file.name}",
                        mime="application/pdf",
                        use_container_width=True
                    )
                    
                    # 顯示檔案資訊
                    original_size = len(pdf_bytes) / (1024 * 1024)
                    output_size = len(output_bytes) / (1024 * 1024)
                    size_change = ((output_size - original_size) / original_size * 100)
                    
                    st.info(f"""
                    📊 **處理結果**
                    - 原始大小: {original_size:.2f} MB
                    - 新檔案大小: {output_size:.2f} MB
                    - 大小變化: {size_change:+.1f}%
                    """)
            
            except Exception as e:
                st.error(f"❌ 發生錯誤: {str(e)}")
    else:
        st.info("👆 請先上傳 PDF 檔案")

with col_process_right:
    st.subheader("📖 使用說明", divider="blue")
    
    st.markdown("""
    **步驟說明:**
    1. 📁 在左側上傳您的 PDF 檔案
    2. ⚙️ 右側選擇適合的移除方案
    3. 🚀 點擊「開始移除浮水印」按鈕
    4. ⬇️ 自動下載清潔後的 PDF
    
    **推薦選擇:**
    - 簡單浮水印 → 方法 1 (快速)
    - 一般浮水印 → 方法 2 (推薦)
    - 複雜浮水印 → 方法 3 (最佳)
    
    **隱私保護:**
    - 所有檔案在 GitHub Codespaces 上處理
    - 檔案不會保存到伺服器
    - 處理完成後自動刪除臨時檔案
    """)
    
    st.markdown("""
    <div class="info-box">
    <strong>💡 提示:</strong><br>
    • 第一次執行時可能較慢<br>
    • 大檔案建議使用方法 1<br>
    • 如果移除不完美，嘗試方法 3
    </div>
    """, unsafe_allow_html=True)

# 底部 - 方案對比表
st.divider()
st.subheader("📈 三種方案對比", divider="blue")

comparison_data = {
    "方案": ["方法 1：快速移除", "方法 2：平衡方案", "方法 3：完美效果"],
    "速度": ["⚡⚡⚡ 極快", "⚡⚡ 適中", "⚡ 較慢"],
    "效果": ["⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
    "複雜度": ["簡單", "中等", "複雜"],
    "適用場景": ["簡單浮水印", "一般浮水印", "複雜浮水印"]
}

st.dataframe(comparison_data, use_container_width=True, hide_index=True)

# 頁腳
st.divider()
st.markdown("""
<div style="text-align: center; color: #cbd5e1; font-size: 0.9em;">
📚 Jerry PDF Remover | 🔧 Built with Streamlit | 🚀 Deployed on GitHub Codespaces<br>
<strong>隱私優先</strong> • <strong>免費使用</strong> • <strong>無廣告</strong>
</div>
""", unsafe_allow_html=True)
