import streamlit as st

# ==============================
# CẤU HÌNH TRANG
# ==============================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# ==============================
# TIÊU ĐỀ
# ==============================
st.title("💰 Ứng dụng tính lãi tiền gửi tiết kiệm")
st.write("Tính tiền lãi theo **lãi đơn** hoặc **lãi kép**.")

st.divider()

# ==============================
# NHẬP DỮ LIỆU
# ==============================

so_tien = st.number_input(
    "💵 Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=10_000_000.0,
    step=500_000.0,
    format="%.0f"
)

ky_han = st.number_input(
    "📅 Kỳ hạn (tháng)",
    min_value=1,
    value=12,
    step=1
)

hinh_thuc_lai = st.selectbox(
    "📈 Hình thức tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ]
)

hinh_thuc_nhan = st.selectbox(
    "💳 Hình thức nhận lãi",
    [
        "Lãnh lãi theo tháng",
        "Lãnh lãi theo quý",
        "Lãnh lãi cuối kỳ"
    ]
)

lai_suat = st.number_input(
    "📊 Lãi suất (%/năm)",
    min_value=0.0,
    value=5.0,
    step=0.1,
    format="%.2f"
)

st.divider()

# ==============================
# HÀM ĐỊNH DẠNG TIỀN
# ==============================

def dinh_dang_tien(so_tien):
    return f"{so_tien:,.0f} VNĐ"


# ==============================
# TÍNH TOÁN
# ==============================

if st.button("🧮 Tính lãi", use_container_width=True):

    if so_tien <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
    elif lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
    else:

        # Đổi lãi suất năm sang dạng thập phân
        r_nam = lai_suat / 100

        # Kỳ hạn theo năm
        so_nam = ky_han / 12

        # Xác định số kỳ nhận lãi
        if hinh_thuc_nhan == "Lãnh lãi theo tháng":
            so_ky = ky_han
            lai_suat_ky = r_nam / 12
            ten_ky = "tháng"

        elif hinh_thuc_nhan == "Lãnh lãi theo quý":
            so_ky = ky_han / 3
            lai_suat_ky = r_nam / 4
            ten_ky = "quý"

        else:
            so_ky = 1
            lai_suat_ky = r_nam * so_nam
            ten_ky = "kỳ"

        # ==============================
        # LÃI ĐƠN
        # ==============================

        if hinh_thuc_lai == "Lãi đơn":

            tong_tien_lai = so_tien * r_nam * so_nam

            # Tiền lãi mỗi kỳ
            if hinh_thuc_nhan == "Lãnh lãi theo tháng":
                tien_lai_dinh_ky = so_tien * r_nam / 12

            elif hinh_thuc_nhan == "Lãnh lãi theo quý":
                tien_lai_dinh_ky = so_tien * r_nam / 4

            else:
                tien_lai_dinh_ky = tong_tien_lai

            tong_tien = so_tien + tong_tien_lai

        # ==============================
        # LÃI KÉP
        # ==============================

        else:

            if hinh_thuc_nhan == "Lãnh lãi theo tháng":

                lai_suat_ky = r_nam / 12
                so_ky = ky_han

            elif hinh_thuc_nhan == "Lãnh lãi theo quý":

                lai_suat_ky = r_nam / 4
                so_ky = ky_han / 3

            else:

                # Cuối kỳ: ghép lãi theo số tháng của kỳ hạn
                lai_suat_ky = r_nam
                so_ky = so_nam

            # Giá trị cuối kỳ
            tong_tien = so_tien * (1 + lai_suat_ky) ** so_ky

            tong_tien_lai = tong_tien - so_tien

            # Lãi của kỳ đầu tiên
            if hinh_thuc_nhan == "Lãnh lãi theo tháng":
                tien_lai_dinh_ky = so_tien * lai_suat_ky

            elif hinh_thuc_nhan == "Lãnh lãi theo quý":
                tien_lai_dinh_ky = so_tien * lai_suat_ky

            else:
                tien_lai_dinh_ky = tong_tien_lai

        # ==============================
        # HIỂN THỊ KẾT QUẢ
        # ==============================

        st.success("✅ Tính toán thành công!")

        st.subheader("📊 Kết quả")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Tiền lãi định kỳ",
                dinh_dang_tien(tien_lai_dinh_ky)
            )

        with col2:
            st.metric(
                "Tổng tiền lãi",
                dinh_dang_tien(tong_tien_lai)
            )

        st.metric(
            "💰 Tổng số tiền gốc + lãi",
            dinh_dang_tien(tong_tien)
        )

        # ==============================
        # THÔNG TIN CHI TIẾT
        # ==============================

        st.divider()

        st.subheader("📋 Thông tin khoản tiền gửi")

        st.write(f"**Số tiền gửi:** {dinh_dang_tien(so_tien)}")
        st.write(f"**Kỳ hạn:** {ky_han} tháng")
        st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
        st.write(f"**Phương pháp:** {hinh_thuc_lai}")
        st.write(f"**Hình thức nhận lãi:** {hinh_thuc_nhan}")

        # ==============================
        # CÔNG THỨC
        # ==============================

        st.divider()

        st.subheader("📐 Công thức sử dụng")

        if hinh_thuc_lai == "Lãi đơn":
            st.latex(
                r"I = P \times r \times t"
            )
            st.caption(
                "Trong đó: P là tiền gốc, r là lãi suất năm, "
                "t là số năm gửi."
            )

        else:
            st.latex(
                r"A = P(1+r)^n"
            )
            st.caption(
                "Trong đó: P là tiền gốc, r là lãi suất mỗi kỳ, "
                "n là số kỳ ghép lãi."
            )
