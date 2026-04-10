import streamlit as st
import pytesseract
from PIL import Image
import os

# --- 設定網頁標題 ---
st.set_page_config(page_title="序號辨識小助手", page_icon="🔍")

st.title("截圖序號辨識")
st.markdown("截圖拖入下方，辨識結果會直接顯示並可一鍵複製。")

# --- 設定 Tesseract 路徑 (如果是部署到 Linux 伺服器則不需要這行) ---
pytesseract.pytesseract.tesseract_cmd = r'D:\JOE\Tool\PngToString\Tesseract-OCR\tesseract.exe'

# --- 側邊欄：辨識設定 ---
with st.sidebar:
    st.header("設定")
    psm_mode = st.selectbox("辨識模式", 
                            options=[1, 7, 3, 6], 
                            format_func=lambda x: { 1: "自動辨識", 7: "單行文字", 3: "全圖辨識", 6: "區塊辨識"}[x])

# --- 檔案上傳區 ---
uploaded_file = st.file_uploader("選擇圖片...", type=["png", "jpg", "jpeg", "bmp"])

if uploaded_file is not None:
    # 顯示圖片預覽
    image = Image.open(uploaded_file)
    st.image(image, caption='上傳的圖片', use_container_width=True)


    with st.spinner('正在精準辨識中...'):
        try:
            # OCR 處理 (轉成灰階)
            img_gray = image.convert('L')
            config = f'--psm {psm_mode}'
            result = pytesseract.image_to_string(img_gray, config=config).strip()
            
            if result:
                st.success("✅ 辨識成功！")
                # 顯示結果並提供點擊複製
                st.code(result, language=None)
                st.info("💡 提示：點擊上方文字框右上角的按鈕即可複製序號。")
            else:
                st.warning("⚠️ 抓不到文字，請確認圖片是否清晰。")
        except Exception as e:
            st.error(f"發生錯誤：{e}")
            st.info("請確認伺服器端是否已安裝 Tesseract OCR 套件。")

# --- 頁尾 ---
st.markdown("---")
st.caption("Powered by Streamlit & Tesseract OCR")