import streamlit as st
import pytesseract
from PIL import Image
import os

# --- 設定網頁標題 ---
st.set_page_config(page_title="序號辨識小助手", page_icon="🔍")

st.title("🔍 截圖序號辨識")
st.markdown("將截圖拖入下方，辨識結果會直接顯示並可一鍵複製。")

# --- 💡 重要修改：Tesseract 路徑處理 ---
# 判斷是否在本地執行（檢查路徑是否存在）
local_tesseract_path = r'D:\JOE\Tool\PngToString\Tesseract-OCR\tesseract.exe'

if os.path.exists(local_tesseract_path):
    # 如果是在你的電腦跑，使用 D 槽路徑
    pytesseract.pytesseract.tesseract_cmd = local_tesseract_path
else:
    # 如果在 Streamlit Cloud (Linux) 跑，通常不需要設定路徑
    # 只要你有準備 packages.txt，系統會自動將 tesseract 加入環境變數
    pass

# --- 側邊欄：辨識設定 ---
with st.sidebar:
    st.header("⚙️ 設定")
    psm_mode = st.selectbox(
        "辨識模式", 
        options=[7, 1, 3, 6], 
        format_func=lambda x: {1: "自動辨識", 7: "單行文字 (推薦)", 3: "全圖辨識", 6: "區塊辨識"}[x]
    )
    st.info("模式 7 最適合處理單一條長序號。")

# --- 檔案上傳區 ---
uploaded_file = st.file_uploader("選擇圖片...", type=["png", "jpg", "jpeg", "bmp"])

if uploaded_file is not None:
    # 顯示圖片預覽
    image = Image.open(uploaded_file)
    st.image(image, caption='上傳的圖片', use_container_width=True)

    # 執行辨識
    with st.spinner('正在精準辨識中...'):
        try:
            # OCR 處理 (轉成灰階提高對比)
            img_gray = image.convert('L')
            config = f'--psm {psm_mode}'
            result = pytesseract.image_to_string(img_gray, config=config).strip()
            
            if result:
                st.success("✅ 辨識成功！")
                # 顯示結果並提供一鍵複製功能
                st.code(result, language=None)
                st.info("💡 提示：點擊上方框框右上角的圖示即可複製。")
            else:
                st.warning("⚠️ 抓不到文字，請確認圖片是否清晰，或更換辨識模式。")
        except Exception as e:
            st.error(f"發生錯誤：{e}")
            st.info("如果是部署在雲端，請確認 GitHub 內是否有 packages.txt 並包含 tesseract-ocr。")

# --- 頁尾 ---
st.markdown("---")
st.caption("Powered by Streamlit & Tesseract OCR | Created by Joe")