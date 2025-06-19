
import streamlit as st
from collections import Counter

st.set_page_config(page_title="Baccarat Cầu Analyzer v3", layout="centered")

st.title("🎯 Baccarat Analyzer V3 - Phân Tích & Chấm Điểm Bàn")

st.write("🔤 Nhập kết quả liên tiếp các ván Baccarat (VD: BBPBPBPBBP):")
input_data = st.text_input("Kết quả (B = Banker, P = Player):", "")

def detect_cau_types(results):
    types = []
    streak = 1
    for i in range(1, len(results)):
        if results[i] == results[i - 1]:
            streak += 1
        else:
            if streak >= 3:
                types.append(("Cầu Bệt", results[i - 1], streak))
            streak = 1

    # Kiểm tra 1-1
    if len(results) >= 4:
        last_4 = results[-4:]
        if all(last_4[i] != last_4[i+1] for i in range(3)):
            types.append(("Cầu 1-1", "-", 2))

    # Kiểm tra Dính Kép (B-B-P-P-B-B)
    if len(results) >= 6:
        pattern = results[-6:]
        if pattern[0] == pattern[1] and pattern[2] == pattern[3] and pattern[4] == pattern[5]:
            types.append(("Cầu Dính Kép", "-", 3))

    # Kiểm tra nghiêng
    b_count = results.count("B")
    p_count = results.count("P")
    total = len(results)
    if b_count / total >= 0.7:
        types.append(("Cầu Nghiêng B", "B", b_count))
    elif p_count / total >= 0.7:
        types.append(("Cầu Nghiêng P", "P", p_count))

    return types

def score_board(cau_types):
    score = 0
    details = []
    for cau in cau_types:
        if cau[0] == "Cầu Bệt":
            score += 3
            details.append("✅ Cầu Bệt: +3")
        elif cau[0] == "Cầu 1-1":
            score += 2
            details.append("✅ Cầu 1-1: +2")
        elif cau[0] == "Cầu Dính Kép":
            score += 1
            details.append("✅ Cầu Dính Kép: +1")
        elif "Cầu Nghiêng" in cau[0]:
            score += 2
            details.append(f"✅ {cau[0]}: +2")

    if score == 0:
        score -= 2
        details.append("⚠️ Không rõ cầu: -2")

    return score, details

def classify_score(score):
    if score >= 6:
        return "🟢 BÀN RẤT TỐT - Nên vào tiền"
    elif 3 <= score < 6:
        return "🟡 BÀN TRUNG BÌNH - Cân nhắc"
    else:
        return "🔴 BÀN RỦI RO - Không nên vào"

if input_data:
    results = list(input_data.upper())
    valid_results = [r for r in results if r in ['B', 'P']]

    if len(valid_results) != len(results) or len(results) < 6:
        st.error("❌ Chỉ nhập ký tự B hoặc P, tối thiểu 6 ván để phân tích.")
    else:
        st.subheader("📊 Phân tích các loại cầu")
        cau_types = detect_cau_types(valid_results)
        if cau_types:
            for ct in cau_types:
                st.write(f"- {ct[0]} ({ct[1]}) - xuất hiện {ct[2]} lần")
        else:
            st.info("Không phát hiện loại cầu rõ ràng.")

        st.subheader("📈 Thống kê xác suất")
        stats = Counter(valid_results)
        total = len(valid_results)
        for k in ['B', 'P']:
            pct = (stats[k] / total) * 100 if k in stats else 0
            st.write(f"{k}: {pct:.2f}%")

        st.subheader("🎯 Chấm điểm bàn")
        score, reasons = score_board(cau_types)
        for reason in reasons:
            st.write(reason)

        st.success(f"✅ Tổng điểm: {score} điểm")
        st.markdown(f"### {classify_score(score)}")
