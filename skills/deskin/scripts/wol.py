#!/usr/bin/env python3
"""
Wake-on-LAN 腳本
發送魔法封包喚醒遠程電腦
"""

import socket
import struct
import argparse
import time


def create_magic_packet(mac_address):
    """
    創建 Wake-on-LAN 魔法封包
    
    Args:
        mac_address: MAC 地址（格式：00:11:22:33:44:55 或 001122334455）
    
    Returns:
        bytes: 魔法封包
    """
    # 移除分隔符號並轉為小寫
    mac_address = mac_address.replace(':', '').replace('-', '').lower()
    
    # 驗證 MAC 地址長度
    if len(mac_address) != 12:
        raise ValueError(f"無效的 MAC 地址：{mac_address}")
    
    # 將 MAC 地址轉換為字節
    mac_bytes = bytes.fromhex(mac_address)
    
    # 創建魔法封包
    # 6 字節的 FF + 16 次重複的 MAC 地址
    header = b'\xff' * 6
    payload = mac_bytes * 16
    
    return header + payload


def send_wol_packet(mac_address, ip_address="255.255.255.255", port=9):
    """
    發送 WoL 魔法封包
    
    Args:
        mac_address: 目標 MAC 地址
        ip_address: 廣播 IP（預設：255.255.255.255）
        port: 目標端口（預設：9）
    
    Returns:
        bool: 發送成功與否
    """
    # 創建魔法封包
    magic_packet = create_magic_packet(mac_address)
    
    # 創建 UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    try:
        # 發送封包
        sock.sendto(magic_packet, (ip_address, port))
        print(f"✅ WoL 封包已發送到 {ip_address}:{port}")
        print(f"   MAC 地址：{mac_address}")
        return True
    except Exception as e:
        print(f"❌ 發送失敗：{e}")
        return False
    finally:
        sock.close()


def send_multiple_wol(mac_address, count=3, interval=1, **kwargs):
    """
    發送多次 WoL 封包（提高成功率）
    
    Args:
        mac_address: 目標 MAC 地址
        count: 發送次數
        interval: 間隔秒數
        **kwargs: 其他參數傳給 send_wol_packet
    """
    print(f"📡 發送 {count} 次 WoL 封包...")
    
    for i in range(count):
        print(f"\n[{i+1}/{count}]")
        send_wol_packet(mac_address, **kwargs)
        if i < count - 1:
            time.sleep(interval)


def main():
    parser = argparse.ArgumentParser(description="Wake-on-LAN 喚醒電腦")
    parser.add_argument("--mac", required=True, help="目標電腦 MAC 地址")
    parser.add_argument("--ip", default="255.255.255.255", help="廣播 IP（預設：255.255.255.255）")
    parser.add_argument("--port", type=int, default=9, help="目標端口（預設：9）")
    parser.add_argument("--count", type=int, default=3, help="發送次數（預設：3）")
    parser.add_argument("--interval", type=float, default=1.0, help="發送間隔秒數（預設：1）")
    
    args = parser.parse_args()
    
    print(f"🔌 Wake-on-LAN 喚醒電腦")
    print(f"   MAC 地址：{args.mac}")
    print(f"   廣播 IP: {args.ip}")
    print(f"   端口：{args.port}")
    print(f"   發送次數：{args.count}")
    print("")
    
    send_multiple_wol(
        mac_address=args.mac,
        ip_address=args.ip,
        port=args.port,
        count=args.count,
        interval=args.interval
    )
    
    print("\n💡 提示：電腦可能需要 10-30 秒啟動")


if __name__ == "__main__":
    main()
