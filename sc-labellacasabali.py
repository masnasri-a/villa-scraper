from datetime import datetime
from datetime import timedelta
import requests, re, json

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Referer': 'https://labellacasabali.com/',
    'Sec-Fetch-Dest': 'script',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Storage-Access': 'active',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

date_str = '2025-07-10'
total_nights = 90
total_adults = 5
total_children = 0
date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
# print(date_obj)

villa_names = [
    "Villa Como",
    "Villa Kobe",
    "Villa Soho",
    "Villa Verde",
    "Villa Cruz",
    "Villa Sante"
]
new_data = []
for getoneyear in range(4):
    start_checkin = date_obj + timedelta(days=getoneyear * 90)
    print(start_checkin)
    # url = f'https://sjp.resonline.com.au/api/get-hotels-rooms-grids?q=599550,623530,598850,632902,632904,632905,632906,632903,635134,637236&webid=27281&checkin={date_str}&nights={total_nights}&adults={total_adults}&children={total_children}&currency=USD&voucherCode=&private=include&callback=jsonID0446D76A1188452392DB8519C88D5451&_=1749733332162-644'
    url = f'https://sjp.resonline.com.au/api/get-hotels-rooms-grids?q=599550,623530,598850,632902,632904,632905,632906,632903,635134,637236&webid=27281&checkin={start_checkin}&nights={total_nights}&adults={total_adults}&children={total_children}&currency=USD&voucherCode=&private=include&callback=jsonIDD1F131BA13154AC2B4EAF13EE88D958D&_=1749806671702-975'
    print(url)
    response = requests.get(
        url,
        headers=headers,
    )
    if response.status_code == 200:
        print("Request was successful.")
        match = re.search(r'^[a-zA-Z0-9_]+\((.*)\)$', response.text, re.DOTALL)
        if match:
            json_str = match.group(1)
            # print(json_str)
            try:
                data = json.loads(json_str)
                for idx, hotel in enumerate(data):
                    ## available_rooms = []
                    avail = hotel['RoomRates']["RoomRates"][0]['Availability']['Day']
                    avail_temp = {}
                    for day, avail_res in enumerate(avail):
                        temp = {
                            'name': villa_names[idx],
                        }
                        new_date = date_obj + timedelta(days=day)
                        temps = {}
                        if avail_res is 0:
                            temps[new_date.strftime('%d %B %Y')] = 'Not Available'
                        else:
                            temps[new_date.strftime('%d %B %Y')] = 'Available'
                    # temp['available_rooms'] = avail_temp
                        temp['available_rooms'] = temps
                        new_data.append(temp)
                print(new_data)

                # print(data)  # Sekarang data sudah berupa list of dict
            except json.JSONDecodeError as e:
                print("Gagal parsing JSON:", e)
        else:
            print("Format response tidak dikenali.")

    temps = {}
    for item in new_data:
        for date, status in item['available_rooms'].items():
            # print(f"  {date}: {status}")
            if date not in temps:
                temps[date] = {"Available": [], "Not Available": []}
                if status == 'Available':
                    temps[date]["Available"] = [item['name']]
                else:
                    temps[date]["Not Available"] = [item['name']]
            else:
                if status == 'Available':
                    temps[date]["Available"].append(item['name'])
                else:
                    temps[date]["Not Available"].append(item['name'])
                
    print(temps)  # Tambahkan baris kosong untuk pemisah antar villa

    with open('example/result-1.json', 'w') as file:
        json.dump(temps, file, indent=4)
    print("Data has been written to example/result-1.json")