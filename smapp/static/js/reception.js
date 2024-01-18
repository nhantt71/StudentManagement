function confirm_admission(r_student_id) {
    if (check_admission_condition(r_student_id)) {
        alert("Xác nhận nhập học thành công!");
    }
    if (!check_admission_condition(r_student_id)) {
        alert("Không đủ điều kiện nhập học!");
    }
}