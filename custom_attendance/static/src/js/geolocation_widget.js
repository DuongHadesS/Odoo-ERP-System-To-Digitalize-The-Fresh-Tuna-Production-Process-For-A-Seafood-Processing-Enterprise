/** @odoo-module **/

import { registry } from "@web/core/registry";

function GeolocationAction(env, { params = {} }) {
    const notification = env.services.notification;

    function onGetLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                showPosition,
                showError,
                { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 }
            );
        } else {
            notification.add("Trình duyệt không hỗ trợ Geolocation.", { type: "danger" });
        }
    }

    async function showPosition(position) {
        const lat = position.coords.latitude;
        const lng = position.coords.longitude;

        const model = params.model;
        const resId = params.resId;
        const employeeId = params.employee_id;
        const mode = params.mode;   // "check_in" hoặc sau này có thể mở rộng

        if (!model) {
            notification.add("Không xác định được model.", { type: "danger" });
            return;
        }

        try {
            if (resId && mode === "check_in") {
                // Gọi hàm Python: action_check_in_with_coords
                await env.services.orm.call(model, "action_check_in_with_coords", [[resId], lat, lng]);
                notification.add(
                    `Check In thành công tại: Lat ${lat.toFixed(6)}, Lng ${lng.toFixed(6)}`,
                    { type: "success" }
                );
                env.bus.trigger("reload", { id: resId, reload: true });

            } else if (!resId) {
                // Nếu chưa có bản ghi → tạo mới
                if (!employeeId) {
                    notification.add("Vui lòng chọn nhân viên trước khi lấy vị trí.", { type: "danger" });
                    return;
                }
                const newRecord = await env.services.orm.call(model, "create", [[{
                    employee_id: employeeId,
                    latitude: lat,
                    longitude: lng,
                    state: "checked_in",
                    check_in: new Date().toISOString(),
                }]]);
                notification.add(
                    `Đã tạo bản ghi mới tại: Lat ${lat.toFixed(6)}, Lng ${lng.toFixed(6)}`,
                    { type: "success" }
                );
                env.bus.trigger("do_action", {
                    type: "ir.actions.act_window",
                    res_model: model,
                    res_id: newRecord,
                    views: [[false, "form"]],
                    target: "current",
                });
            }
        } catch (error) {
            notification.add(`Lỗi khi lưu vị trí: ${error.message || "Vui lòng thử lại."}`, { type: "danger" });
            console.error("Error in showPosition:", error);
        }
    }

    function showError(error) {
        let message = "";
        switch (error.code) {
            case error.PERMISSION_DENIED:
                message = "Người dùng từ chối chia sẻ vị trí.";
                break;
            case error.POSITION_UNAVAILABLE:
                message = "Thông tin vị trí không khả dụng.";
                break;
            case error.TIMEOUT:
                message = "Yêu cầu vị trí hết thời gian.";
                break;
            default:
                message = "Lỗi không xác định.";
        }
        notification.add(message, { type: "danger" });
        console.error("Geolocation error:", error);
    }

    onGetLocation();
}

registry.category("actions").add("get_location", GeolocationAction);
