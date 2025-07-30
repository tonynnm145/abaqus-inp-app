import streamlit as st
import pandas as pd
from backend import process_inp_file

st.set_page_config(page_title="Tính E(z) & Ep từ Abaqus .inp", layout="centered")
st.title("🔬 Tính E(z) và Ep từ file Abaqus .inp")

uploaded_file = st.file_uploader("📂 Bước 1: Tải lên file Abaqus (.inp)", type=["inp"])

if uploaded_file is not None:
    all_lines = uploaded_file.read().decode("utf-8").splitlines()

    result = process_inp_file(all_lines)
    
    if result.get("error"):
        st.error(result["error"])
        st.stop()

    df = result["df"]
    st.success(f"✅ Trích được {len(df)} giá trị toạ độ z khác nhau.")
    st.dataframe(df[["STT", "Toạ độ z"]])

    k = st.selectbox("⚙️ Bước 2: Chọn hệ số k", [0, 1, 2])
    df, Ep10 = result["calc_E_Ep"](df, k)

    st.subheader("📊 Bước 3: Bảng giá trị E(z)")
    st.dataframe(df[["STT", "Toạ độ z", f"E_k={k}"]].style.format({f"E_k={k}": "{:.2e}"}))

    st.subheader("📊 Bước 4: Bảng giá trị Ep")
    st.dataframe(df[["STT", f"Ep_k={k}"]].style.format({f"Ep_k={k}": "{:.2e}"}))

    if len(Ep10) < 10:
        st.error("❌ Không đủ 10 lớp Ep để tạo vật liệu.")
        st.stop()

    st.success("✅ Sinh vật liệu ALU1 - ALU10")
    for i, val in enumerate(Ep10, 1):
        st.write(f"ALU{i}: Elastic = {val:.2e} Pa")

    uploaded_file.seek(0)
    original_lines = uploaded_file.read().decode("utf-8").splitlines()
    modified_content = result["generate_modified_inp"](original_lines, Ep10)

    st.download_button(
        "📅 Tải file .inp đã chỉnh sửa",
        data=modified_content.encode('utf-8'),
        file_name="Modified_Slab.inp",
        mime="text/plain"
    )
