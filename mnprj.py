import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

devices = [
    {'id': 'M01', 'location': 'Mechanical Shop A', 'old_index': 1200, 'new_index': 4500, 'status': 'Normal'},
    {'id': 'M02', 'location': 'Assembly Line B', 'old_index': 2300, 'new_index': 8500, 'status': 'Overload'}
]

# 3. CÁC HÀM PHỤ TRỢ (HELPER FUNCTIONS)
def get_valid_number(prompt: str) -> float:
    """Hàm ép người dùng nhập số >= 0, dùng try-except để chống crash."""
    while True:
        try:
            value = float(input(prompt).strip())
            if value < 0:
                print("Lỗi: Số liệu phải lớn hơn hoặc bằng 0. Vui lòng nhập lại!")
                continue
            return value
        except ValueError:
            print("Lỗi: Dữ liệu nhập vào không hợp lệ. Vui lòng nhập số!")

def show_devices(device_list: list):
    """Chức năng 1: Hiển thị danh sách thiết bị"""
    if not device_list:
        print("\nHệ thống hiện chưa có thiết bị giám sát nào!")
        return

    print("\n--- DANH SÁCH THIẾT BỊ GIÁM SÁT ---")
    print(f"{'MÃ TB':<6} | {'VỊ TRÍ PHÂN XƯỞNG':<22} | {'CHỈ SỐ CŨ':<10} | {'CHỈ SỐ MỚI':<10} | {'TRẠNG THÁI'}")
    print("-" * 75)
    for dev in device_list:
        print(f"{dev['id']:<6} | {dev['location']:<22} | {dev['old_index']:<10.0f} | {dev['new_index']:<10.0f} | {dev['status']}")
    print("-" * 75)

def update_indices(device_list: list):
    """Chức năng 2: Cập nhật chỉ số điện"""
    print("\n--- CẬP NHẬT CHỈ SỐ ĐIỆN ---")
    dev_id = input("Nhập mã thiết bị: ").strip().upper()

    # Tìm kiếm thiết bị
    target_dev = next((d for d in device_list if d['id'] == dev_id), None)
    
    if not target_dev:
        print("[Lỗi] (ERR-E01): Mã thiết bị này không tồn tại trong danh sách hệ thống")
        return

    old_idx = get_valid_number("Nhập chỉ số cũ: ")
    
    # Ràng buộc chỉ số mới >= chỉ số cũ
    while True:
        new_idx = get_valid_number("Nhập chỉ số mới: ")
        if new_idx < old_idx:
            print("[Lỗi] (ERR-E02): Chỉ số mới không được nhỏ hơn chỉ số cũ!")
        else:
            break

    # Cập nhật trực tiếp vào list
    target_dev['old_index'] = old_idx
    target_dev['new_index'] = new_idx
    print(f"[Thành công]: Thiết bị {dev_id} đã được cập nhật số liệu mới")

def trigger_overload_warning(device_list: list):
    """Chức năng 3: Kích hoạt trạng thái cảnh báo"""
    print("\n--- KÍCH HOẠT TRẠNG THÁI CẢNH BÁO ---")
    dev_id = input("Nhập mã thiết bị cần duyệt: ").strip().upper()

    target_dev = next((d for d in device_list if d['id'] == dev_id), None)

    if not target_dev:
        print("[Lỗi] (ERR-E01): Mã thiết bị này không tồn tại trong danh sách hệ thống")
        return

    if target_dev['status'] == 'Overload':
        print("[Lỗi] (ERR-E04): Thao tác bị hủy! Thiết bị này đã được kích hoạt trạng thái OVERLOAD từ trước!")
        return

    consumption = target_dev['new_index'] - target_dev['old_index']
    print(f"Tìm thấy thiết bị tại: {target_dev['location']} (Lượng tiêu thụ: {consumption:,.0f} kWh)")

    if consumption > 5000:
        target_dev['status'] = 'Overload'
        logging.warning(f"[Cảnh báo]: Thiết bị {dev_id} đã vượt ngưỡng tiêu thụ an toàn, chuyển sang OVERLOAD!")
        print(f"[Thành công]: Thiết bị {dev_id} đã được kích hoạt trạng thái OVERLOAD!")
    else:
        print(f"[Thông báo]: Thiết bị {dev_id} vẫn trong ngưỡng an toàn.")

def calculate_energy_financials(device_list: list) -> tuple:
    """
    Chức năng 4: Tính toán tài chính.
    Bắt buộc trả về Tuple: (tổng_điện, phần_trăm_chiết_khấu, tổng_tiền)
    """
    total_energy = sum((d['new_index'] - d['old_index']) for d in device_list)
    base_price = 3000  # VND/kWh
    discount_rate = 0.03 if total_energy >= 50000 else 0.0
    
    total_cost = total_energy * base_price * (1 - discount_rate)
    
    return total_energy, discount_rate, total_cost

# 5. HÀM ĐIỀU PHỐI CHÍNH
def main():
    while True:
        print("\n" + "="*55)
        print("    SMART ENERGY MONITOR - PHÒNG CƠ ĐIỆN")
        print("="*55)
        print("1. Xem danh sách thiết bị giám sát")
        print("2. Cập nhật chỉ số điện tiêu thụ (Check-in)")
        print("3. Kích hoạt trạng thái cảnh báo quá tải")
        print("4. Tính tổng lượng điện & Chi phí năng lượng")
        print("5. Thoát chương trình")
        print("="*55)
        
        choice = input("Mời chọn chức năng (1-5): ").strip()
        
        if choice == '1':
            show_devices(devices)
        elif choice == '2':
            update_indices(devices)
        elif choice == '3':
            trigger_overload_warning(devices)
        elif choice == '4':
            # Gọi hàm lấy Tuple, sau đó giải nén (unpack) để in kết quả
            energy, discount, cost = calculate_energy_financials(devices)
            print("\n--- BÁO CÁO TÀI CHÍNH NĂNG LƯỢNG ---")
            print(f"+ Tổng lượng điện tiêu thụ thực tế: {energy:,.0f} kWh")
            print(f"+ Tỷ lệ chiết khấu áp dụng từ nhà nước: {discount * 100:.0f}%")
            print(f"+ Tổng chi phí năng lượng phải trả sau chiết khấu: {cost:,.0f} VND")
        elif choice == '5':
            print("\nCảm ơn bạn đã sử dụng phần mềm Smart Energy Monitor!")
            print("[Chương trình kết thúc]")
            break
        else:
            print("[Lỗi]: Lựa chọn không hợp lệ. Vui lòng nhập số từ 1 đến 5!")

if __name__ == "__main__":
    main()

# File test
# Import hàm tính toán từ file main.py
from mnprj import calculate_energy_financials

def test_no_discount_scenario():
    """Trường hợp lượng điện tiêu thụ < 50,000 kWh (0% chiết khấu)"""
    devices_mock = [
        {'new_index': 30000, 'old_index': 10000}, # Tiêu thụ 20,000
        {'new_index': 20000, 'old_index': 10000}  # Tiêu thụ 10,000
    ]
    # Tổng điện = 30,000. Tiền = 30,000 * 3000 = 90,000,000
    energy, discount, cost = calculate_energy_financials(devices_mock)
    
    assert energy == 30000
    assert discount == 0.0
    assert cost == 90000000.0

def test_discount_scenario():
    """Trường hợp lượng điện tiêu thụ >= 50,000 kWh (3% chiết khấu)"""
    devices_mock = [
        {'new_index': 50000, 'old_index': 10000}, # Tiêu thụ 40,000
        {'new_index': 30000, 'old_index': 10000}  # Tiêu thụ 20,000
    ]
    # Tổng điện = 60,000. Chiết khấu 3%. 
    # Tiền = 60,000 * 3000 * 0.97 = 174,600,000
    energy, discount, cost = calculate_energy_financials(devices_mock)
    
    assert energy == 60000
    assert discount == 0.03
    assert cost == 174600000.0

def test_zero_consumption():
    """Trường hợp lượng điện tiêu thụ = 0 kWh (Edge Case)"""
    devices_mock = [
        {'new_index': 1000, 'old_index': 1000}
    ]
    energy, discount, cost = calculate_energy_financials(devices_mock)
    
    assert energy == 0
    assert discount == 0.0
    assert cost == 0.0