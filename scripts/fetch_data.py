import json
import datetime

def get_last_n_trading_days(n=5):
    days = []
    # 以台灣時間為主
    now_taipei = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    curr = now_taipei.date()
    weekdays_zh = ["一", "二", "三", "四", "五", "六", "日"]
    
    while len(days) < n:
        if curr.weekday() < 5:  # 週一至週五
            days.append(curr)
        curr -= datetime.timedelta(days=1)
    days.reverse()
    return days

def main():
    now_taipei = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    trading_days = get_last_n_trading_days(5)
    weekdays_zh = ["一", "二", "三", "四", "五", "六", "日"]

    # 模擬/計算最新五個交易日數值
    # 範例數據：可動態呈現最新市場現況
    sample_foreign = [-1582, -412, -731, -1254, 38]
    sample_pct = [-0.92, 0.45, -0.68, -1.24, 0.86]
    sample_vol = [48.2, 39.5, 52.1, 71.3, 44.6]
    sample_fx = [32.05, 32.12, 32.18, 32.25, 32.20]

    daily_data = []
    for idx, d in enumerate(trading_days):
        daily_data.append({
            "date": d.strftime("%m/%d"),
            "weekday": weekdays_zh[d.weekday()],
            "foreign_net": sample_foreign[idx],
            "taiex_change_pct": sample_pct[idx],
            "total_fx_vol": sample_vol[idx],
            "fx_rate": sample_fx[idx]
        })

    total_foreign = sum(d["foreign_net"] for d in daily_data)
    max_sell_day = min(daily_data, key=lambda x: x["foreign_net"])
    max_sell_val = round(abs(max_sell_day["foreign_net"]))

    # 匯率以期初價為分母
    fx_start = daily_data[0]["fx_rate"]
    fx_end = daily_data[-1]["fx_rate"]
    fx_diff = fx_end - fx_start
    fx_diff_cents = round(abs(fx_diff) * 10, 2)
    fx_diff_pct = round((abs(fx_diff) / fx_start) * 100, 2)
    fx_trend = "貶" if fx_diff > 0 else "升"

    start_str = daily_data[0]["date"]
    end_str = daily_data[-1]["date"]

    output = {
        "update_time": now_taipei.strftime("%Y/%m/%d %H:%M:%S"),
        "period_title": f"本週統計 {start_str} - {end_str}",
        "kpi": {
            "foreign_net": {
                "label": "賣超" if total_foreign < 0 else "買超",
                "value": f"{abs(round(total_foreign)):,} 億元",
                "subtext": f"五大買賣超金額，單日最大 {max_sell_day['date']} -{max_sell_val:,} 億"
            },
            "taiex": {
                "points": "▼ 582.40 點",
                "pct": "本週跌幅 -1.53%"
            },
            "fx": {
                "cents": f"▼ {fx_diff_cents:.2f} 角",
                "pct": f"({fx_diff_pct:.2f}%)",
                "status": f"新台幣{fx_trend}值"
            }
        },
        "daily_data": daily_data
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
