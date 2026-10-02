# Nội dung cập nhật lý thuyết Hình Bình Hành
# Replace phần render_right_column bằng nội dung dưới đây

def render_right_column(data):
    st.subheader("📖 Giải Thích")

    st.markdown("#### Định Nghĩa")
    st.info(
        "Hình bình hành là tứ giác có các cạnh đối song song. "
        "Hình bình hành cũng là một hình thang đặc biệt."
    )

    st.markdown("#### Tính Chất")
    properties = [
        "Các cạnh đối song song: AB // CD, AD // BC.",
        "Các cạnh đối bằng nhau: AB = CD, AD = BC.",
        "Các góc đối bằng nhau: ∠A = ∠C, ∠B = ∠D.",
        "Hai đường chéo cắt nhau tại trung điểm của mỗi đường.",
        "Nếu O là giao điểm hai đường chéo thì OA = OC và OB = OD."
    ]

    st.write("🔹 " + "\n🔹 ".join(properties))

    st.markdown("#### Dấu Hiệu Nhận Biết")
    recognition = [
        "Tứ giác có các cạnh đối song song là hình bình hành.",
        "Tứ giác có các cạnh đối bằng nhau là hình bình hành.",
        "Tứ giác có một cặp cạnh đối vừa song song vừa bằng nhau là hình bình hành.",
        "Tứ giác có các góc đối bằng nhau là hình bình hành.",
        "Tứ giác có hai đường chéo cắt nhau tại trung điểm của mỗi đường là hình bình hành."
    ]

    st.write("🔸 " + "\n🔸 ".join(recognition))

    st.markdown("#### Công Thức")

    ab = float(st.session_state.ab)
    ad = float(st.session_state.ad)
    h = float(data["height"])
    area = float(data["area"])
    perimeter = float(data["perimeter"])

    st.write(f"Diện tích: S = a × h = {ab:.0f} × {h:.2f} = {area:.2f} cm²")
    st.write(f"Chu vi: P = 2(a+b) = 2({ab:.0f}+{ad:.0f}) = {perimeter:.2f} cm")

    if st.button("🤖 Giải Thích AI", use_container_width=True):
        ai_properties = {
            "cạnh_đối": "song song và bằng nhau",
            "góc_đối": "bằng nhau",
            "đường_chéo": "cắt nhau tại trung điểm",
            "OA_OC": "bằng nhau",
            "OB_OD": "bằng nhau"
        }
