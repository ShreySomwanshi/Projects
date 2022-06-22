from typing import Any, Text, Dict, List

import arrow 
import dateparser
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from bs4 import BeautifulSoup
import requests
import json
city_db = {'abidjan': 'Africa/Abidjan', 'accra': 'Africa/Accra', 'algiers': 'Africa/Algiers', 'bissau': 'Africa/Bissau', 'cairo': 'Africa/Cairo', 'casablanca': 'Africa/Casablanca', 'ceuta': 'Africa/Ceuta', 'el_aaiun': 'Africa/El_Aaiun', 'johannesburg': 'Africa/Johannesburg', 'juba': 'Africa/Juba', 'khartoum': 'Africa/Khartoum', 'lagos': 'Africa/Lagos', 'maputo': 'Africa/Maputo', 'monrovia': 'Africa/Monrovia', 'nairobi': 'Africa/Nairobi', 'ndjamena': 'Africa/Ndjamena', 'sao_tome': 'Africa/Sao_Tome', 'tripoli': 'Africa/Tripoli', 'tunis': 'Africa/Tunis', 'windhoek': 'Africa/Windhoek', 'adak': 'America/Adak', 'anchorage': 'America/Anchorage', 'araguaina': 'America/Araguaina', 'asuncion': 'America/Asuncion', 'atikokan': 'America/Atikokan', 'bahia': 'America/Bahia', 'bahia_banderas': 'America/Bahia_Banderas', 'barbados': 'America/Barbados', 'belem': 'America/Belem', 'belize': 'America/Belize', 'blanc': 'America/Blanc-Sablon', 'boa_vista': 'America/Boa_Vista', 'bogota': 'America/Bogota', 'boise': 'America/Boise', 'cambridge_bay': 'America/Cambridge_Bay', 'campo_grande': 'America/Campo_Grande', 'cancun': 'America/Cancun', 'caracas': 'America/Caracas', 'cayenne': 'America/Cayenne', 'chicago': 'America/Chicago', 'chihuahua': 'America/Chihuahua', 'costa_rica': 'America/Costa_Rica', 'creston': 'America/Creston', 'cuiaba': 'America/Cuiaba', 'curacao': 'America/Curacao', 'danmarkshavn': 'America/Danmarkshavn', 'dawson': 'America/Dawson', 'dawson_creek': 'America/Dawson_Creek', 'denver': 'America/Denver', 'detroit': 'America/Detroit', 'edmonton': 'America/Edmonton', 'eirunepe': 'America/Eirunepe', 'el_salvador': 'America/El_Salvador', 'fort_nelson': 'America/Fort_Nelson', 'fortaleza': 'America/Fortaleza', 'glace_bay': 'America/Glace_Bay', 'goose_bay': 'America/Goose_Bay', 'grand_turk': 'America/Grand_Turk', 'guatemala': 'America/Guatemala', 'guayaquil': 'America/Guayaquil', 'guyana': 'America/Guyana', 'halifax': 'America/Halifax', 'havana': 'America/Havana', 'hermosillo': 'America/Hermosillo', 'inuvik': 'America/Inuvik', 'iqaluit': 'America/Iqaluit', 'jamaica': 'America/Jamaica', 'juneau': 'America/Juneau', 'la_paz': 'America/La_Paz', 'lima': 'America/Lima', 'los_angeles': 'America/Los_Angeles', 'maceio': 'America/Maceio', 'managua': 'America/Managua', 'manaus': 'America/Manaus', 'martinique': 'America/Martinique', 'matamoros': 'America/Matamoros', 'mazatlan': 'America/Mazatlan', 'menominee': 'America/Menominee', 'merida': 'America/Merida', 'metlakatla': 'America/Metlakatla', 'mexico_city': 'America/Mexico_City', 'miquelon': 'America/Miquelon', 'moncton': 'America/Moncton', 'monterrey': 'America/Monterrey', 'montevideo': 'America/Montevideo', 'nassau': 'America/Nassau', 'new_york': 'America/New_York', 'nipigon': 'America/Nipigon', 'nome': 'America/Nome', 'noronha': 'America/Noronha', 'nuuk': 'America/Nuuk', 'ojinaga': 'America/Ojinaga', 'panama': 'America/Panama', 'pangnirtung': 'America/Pangnirtung', 'paramaribo': 'America/Paramaribo', 'phoenix': 'America/Phoenix', 'port': 'America/Port-au-Prince', 'port_of_spain': 'America/Port_of_Spain', 'porto_velho': 'America/Porto_Velho', 'puerto_rico': 'America/Puerto_Rico', 'punta_arenas': 'America/Punta_Arenas', 'rainy_river': 'America/Rainy_River', 'rankin_inlet': 'America/Rankin_Inlet', 'recife': 'America/Recife', 'regina': 'America/Regina', 'resolute': 'America/Resolute', 'rio_branco': 'America/Rio_Branco', 'santarem': 'America/Santarem', 'santiago': 'America/Santiago', 'santo_domingo': 'America/Santo_Domingo', 'sao_paulo': 'America/Sao_Paulo', 'scoresbysund': 'America/Scoresbysund', 'sitka': 'America/Sitka', 'st_johns': 'America/St_Johns', 'swift_current': 'America/Swift_Current', 'tegucigalpa': 'America/Tegucigalpa', 'thule': 'America/Thule', 'thunder_bay': 'America/Thunder_Bay', 'tijuana': 'America/Tijuana', 'toronto': 'America/Toronto', 'vancouver': 'America/Vancouver', 'whitehorse': 'America/Whitehorse', 'winnipeg': 'America/Winnipeg', 'yakutat': 'America/Yakutat', 'yellowknife': 'America/Yellowknife', 'casey': 'Antarctica/Casey', 'davis': 'Antarctica/Davis', 'dumontdurville': 'Antarctica/DumontDUrville', 'macquarie': 'Antarctica/Macquarie', 'mawson': 'Antarctica/Mawson', 'palmer': 'Antarctica/Palmer', 'rothera': 'Antarctica/Rothera', 'syowa': 'Antarctica/Syowa', 'troll': 'Antarctica/Troll', 'vostok': 'Antarctica/Vostok', 'almaty': 'Asia/Almaty', 'amman': 'Asia/Amman', 'anadyr': 'Asia/Anadyr', 'aqtau': 'Asia/Aqtau', 'aqtobe': 'Asia/Aqtobe', 'ashgabat': 'Asia/Ashgabat', 'atyrau': 'Asia/Atyrau', 'baghdad': 'Asia/Baghdad', 'baku': 'Asia/Baku', 'bangkok': 'Asia/Bangkok', 'barnaul': 'Asia/Barnaul', 'beirut': 'Asia/Beirut', 'bishkek': 'Asia/Bishkek', 'brunei': 'Asia/Brunei', 'chita': 'Asia/Chita', 'choibalsan': 'Asia/Choibalsan', 'colombo': 'Asia/Colombo', 'damascus': 'Asia/Damascus', 'dhaka': 'Asia/Dhaka', 'dili': 'Asia/Dili', 'dubai': 'Asia/Dubai', 'dushanbe': 'Asia/Dushanbe', 'famagusta': 'Asia/Famagusta', 'gaza': 'Asia/Gaza', 'hebron': 'Asia/Hebron', 'ho_chi_minh': 'Asia/Ho_Chi_Minh', 'hong_kong': 'Asia/Hong_Kong', 'hovd': 'Asia/Hovd', 'irkutsk': 'Asia/Irkutsk', 'jakarta': 'Asia/Jakarta', 'jayapura': 'Asia/Jayapura', 'jerusalem': 'Asia/Jerusalem', 'kabul': 'Asia/Kabul', 'kamchatka': 'Asia/Kamchatka', 'karachi': 'Asia/Karachi', 'kathmandu': 'Asia/Kathmandu', 'khandyga': 'Asia/Khandyga', 'kolkata': 'Asia/Kolkata', 'krasnoyarsk': 'Asia/Krasnoyarsk', 'kuala_lumpur': 'Asia/Kuala_Lumpur', 'kuching': 'Asia/Kuching', 'macau': 'Asia/Macau', 'magadan': 'Asia/Magadan', 'makassar': 'Asia/Makassar', 'manila': 'Asia/Manila', 'nicosia': 'Asia/Nicosia', 'novokuznetsk': 'Asia/Novokuznetsk', 'novosibirsk': 'Asia/Novosibirsk', 'omsk': 'Asia/Omsk', 'oral': 'Asia/Oral', 'pontianak': 'Asia/Pontianak', 'pyongyang': 'Asia/Pyongyang', 'qatar': 'Asia/Qatar', 'qostanay': 'Asia/Qostanay', 'qyzylorda': 'Asia/Qyzylorda', 'riyadh': 'Asia/Riyadh', 'sakhalin': 'Asia/Sakhalin', 'samarkand': 'Asia/Samarkand', 'seoul': 'Asia/Seoul', 'shanghai': 'Asia/Shanghai', 'singapore': 'Asia/Singapore', 'srednekolymsk': 'Asia/Srednekolymsk', 'taipei': 'Asia/Taipei', 'tashkent': 'Asia/Tashkent', 'tbilisi': 'Asia/Tbilisi', 'tehran': 'Asia/Tehran', 'thimphu': 'Asia/Thimphu', 'tokyo': 'Asia/Tokyo', 'tomsk': 'Asia/Tomsk', 'ulaanbaatar': 'Asia/Ulaanbaatar', 'urumqi': 'Asia/Urumqi', 'ust': 'Asia/Ust-Nera', 'vladivostok': 'Asia/Vladivostok', 'yakutsk': 'Asia/Yakutsk', 'yangon': 'Asia/Yangon', 'yekaterinburg': 'Asia/Yekaterinburg', 'yerevan': 'Asia/Yerevan', 'azores': 'Atlantic/Azores', 'bermuda': 'Atlantic/Bermuda', 'canary': 'Atlantic/Canary', 'cape_verde': 'Atlantic/Cape_Verde', 'faroe': 'Atlantic/Faroe', 'madeira': 'Atlantic/Madeira', 'reykjavik': 'Atlantic/Reykjavik', 'south_georgia': 'Atlantic/South_Georgia', 'stanley': 'Atlantic/Stanley', 'adelaide': 'Australia/Adelaide', 'brisbane': 'Australia/Brisbane', 'broken_hill': 'Australia/Broken_Hill', 'darwin': 'Australia/Darwin', 'eucla': 'Australia/Eucla', 'hobart': 'Australia/Hobart', 'lindeman': 'Australia/Lindeman', 'lord_howe': 'Australia/Lord_Howe', 'melbourne': 'Australia/Melbourne', 'perth': 'Australia/Perth', 'sydney': 'Australia/Sydney', 'amsterdam': 'Europe/Amsterdam', 'andorra': 'Europe/Andorra', 'astrakhan': 'Europe/Astrakhan', 'athens': 'Europe/Athens', 'belgrade': 'Europe/Belgrade', 'berlin': 'Europe/Berlin', 'brussels': 'Europe/Brussels', 'bucharest': 'Europe/Bucharest', 'budapest': 'Europe/Budapest', 'chisinau': 'Europe/Chisinau', 'copenhagen': 'Europe/Copenhagen', 'dublin': 'Europe/Dublin', 'gibraltar': 'Europe/Gibraltar', 'helsinki': 'Europe/Helsinki', 'istanbul': 'Europe/Istanbul', 'kaliningrad': 'Europe/Kaliningrad', 'kiev': 'Europe/Kiev', 'kirov': 'Europe/Kirov', 'lisbon': 'Europe/Lisbon', 'london': 'Europe/London', 'luxembourg': 'Europe/Luxembourg', 'madrid': 'Europe/Madrid', 'malta': 'Europe/Malta', 'minsk': 'Europe/Minsk', 'monaco': 'Europe/Monaco', 'moscow': 'Europe/Moscow', 'oslo': 'Europe/Oslo', 'paris': 'Europe/Paris', 'prague': 'Europe/Prague', 'riga': 'Europe/Riga', 'rome': 'Europe/Rome', 'samara': 'Europe/Samara', 'saratov': 'Europe/Saratov', 'simferopol': 'Europe/Simferopol', 'sofia': 'Europe/Sofia', 'stockholm': 'Europe/Stockholm', 'tallinn': 'Europe/Tallinn', 'tirane': 'Europe/Tirane', 'ulyanovsk': 'Europe/Ulyanovsk', 'uzhgorod': 'Europe/Uzhgorod', 'vienna': 'Europe/Vienna', 'vilnius': 'Europe/Vilnius', 'volgograd': 'Europe/Volgograd', 'warsaw': 'Europe/Warsaw', 'zaporozhye': 'Europe/Zaporozhye', 'zurich': 'Europe/Zurich', 'chagos': 'Indian/Chagos', 'christmas': 'Indian/Christmas', 'cocos': 'Indian/Cocos', 'kerguelen': 'Indian/Kerguelen', 'mahe': 'Indian/Mahe', 'maldives': 'Indian/Maldives', 'mauritius': 'Indian/Mauritius', 'reunion': 'Indian/Reunion', 'apia': 'Pacific/Apia', 'auckland': 'Pacific/Auckland', 'bougainville': 'Pacific/Bougainville', 'chatham': 'Pacific/Chatham', 'chuuk': 'Pacific/Chuuk', 'easter': 'Pacific/Easter', 'efate': 'Pacific/Efate', 'enderbury': 'Pacific/Enderbury', 'fakaofo': 'Pacific/Fakaofo', 'fiji': 'Pacific/Fiji', 'funafuti': 'Pacific/Funafuti', 'galapagos': 'Pacific/Galapagos', 'gambier': 'Pacific/Gambier', 'guadalcanal': 'Pacific/Guadalcanal', 'guam': 'Pacific/Guam', 'honolulu': 'Pacific/Honolulu', 'kiritimati': 'Pacific/Kiritimati', 'kosrae': 'Pacific/Kosrae', 'kwajalein': 'Pacific/Kwajalein', 'majuro': 'Pacific/Majuro', 'marquesas': 'Pacific/Marquesas', 'nauru': 'Pacific/Nauru', 'niue': 'Pacific/Niue', 'norfolk': 'Pacific/Norfolk', 'noumea': 'Pacific/Noumea', 'pago_pago': 'Pacific/Pago_Pago', 'palau': 'Pacific/Palau', 'pitcairn': 'Pacific/Pitcairn', 'pohnpei': 'Pacific/Pohnpei', 'port_moresby': 'Pacific/Port_Moresby', 'rarotonga': 'Pacific/Rarotonga', 'tahiti': 'Pacific/Tahiti', 'tarawa': 'Pacific/Tarawa', 'tongatapu': 'Pacific/Tongatapu', 'wake': 'Pacific/Wake', 'wallis': 'Pacific/Wallis'}


class ActionTellTime(Action):

    def name(self) -> Text:
        return "action_tell_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_place = next(tracker.get_latest_entity_values("place"), None)
        utc = arrow.utcnow()
        
        if not current_place:
            msg = f"It's {utc.format('HH:mm')} utc now. You can also give me a place."
            dispatcher.utter_message(text=msg)
            return []
        current_place= current_place.lower()
        
        tz_string = city_db.get(current_place, None)
        if not tz_string:
            msg = f"I didn't recognize {current_place}. Is it spelled correctly?"
            dispatcher.utter_message(text=msg)
            return []
                
        msg = f"It's {utc.to(city_db[current_place]).format('HH:mm')} in {current_place} now."
        dispatcher.utter_message(text=msg)
        
        return []

class ActionTellaboutcountry(Action):
    def name(self) -> Text:
        return "action_tell_about_country"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ent = tracker.latest_message['entities'][0]['value']
        country=ent
        country=country.title()
        country=country.replace(" ",'-')
        url = requests.get("https://www.britannica.com/facts/"+country)
        htmltext = url.text
        soup = BeautifulSoup(htmltext , 'html.parser')
        x = soup.find('table',{'class': 'quick-facts-table table font-14'})
        y = x.find_all('th',{'class': 'col-30'})
        z = x.find_all('td')
        a = []
        b = []
        for i in y:
            c = i.text.strip()
            a.append(c)
        for i in z:
            c = i.text.strip()
            b.append(c)

        data = {}
        ans=""
        for i in range(len(a)):
            data[a[i]] = b[i]
            #result = json.dumps(data)
        for i in data:
            ans+=i+' : '+data[i]+'\n\n'
        dispatcher.utter_message(text=ans)

        return []