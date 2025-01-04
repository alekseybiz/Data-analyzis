import json

import requests


auth_key = "YWJkMDc5N2QtMzA3OC00Yjg3LWE2Y2EtYmQ3MzRkNDAxYTBiOmRjODJkZGQ2LWQwZTctNGM2Yi1iMTlhLTM0NjI4MWIzODUxNg=="
client_id = "abd0797d-3078-4b87-a6ca-bd734d401a0b"
scope = "GIGACHAT_API_PERS"
client_secret = "dc82ddd6-d0e7-4c6b-b19a-346281b38516"

access_token = "eyJjdHkiOiJqd3QiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiYWxnIjoiUlNBLU9BRVAtMjU2In0.T-t9ANq7PPcFOp1cUEl57NPMfG_EoCgnETSARw-uh7DtqAm6AJDlExLVALs3QVPCEbpB9muHbw8IzVkhGFcKct4s5DS0HYipJkVPMUwVjF6mPRAlCQAi963QEPRaQB7ujHraUVLvrUxCtSdnsbFJHGS2cKyqoFObuGartpFSuNlFgnbJ7hQMK663RjcC-V5C4jilXSIxMMhhmU5i86UbhuzPu9B_bvz189MwVjgPstoF9eGdz87wey0Zrz4M5dsN4ET7CknvUQnVvVOuUfYb-uYEztKlRICfQrEVGzQs419M816vZxgZBmulXzoyW6QU_KsgrV93uwTS_Yu360I6mA.1FB6l6HIXrGXlX_DxamuYw.6Kh64uzLNwTZc6gYkhfkGfusJ55Vm_608QlUGSH-ERtRoXLvpb0SyJyBarq_lHJH9s14zdRCi5QF-6QccHuB7MQZLhtBBW9Ff3JdSd_EiZyWc-AON3AwVopIEq3NMXr1BsD4eZrlcHXrJQKeezLdngMy17-90ey7PGYSpJC-1DpEzNKyItNPJ7Ar_-uhFH5G0RjTxQ2Zu9t1kFIWOINM9xjZ9oddkUMMPKZh6SoQR7EQ_BQ_IZG3gnu_-7MQA1EeGnVWNSLkdA3PePtg1ZBlJB7M8NMMqLwOK8G_G82F53Qi4_w9IJByz7usUvSW9LAezeYeanc-nvy-Ey0wF63IMNGIIRJv0xa7tLD1PEvQcknqoWB6PaG7IWdjLulYRmrdXAQFzaWa6v1fC_YSsLK7P_1XRBkgSfkMZnbh1JD8T0uKvTqErw8i6xJFl2bCjOsnoj0597TJchY8ha9gKSzjhGGwX84BeFcgwl2MIvn8JctDv5CZh3X-unvgKZDluttALEgxTheeVjSf2nnFsbkOYrRfAs2-tTgtb8RHNmvXa39lQNpAiBw0N28vX-6qFNj1N8MCIwe9KbHWHExzjb97I0jw7draQNKWyraxhLqGZ8qtuecfApzgnpHdDmGS1Y_Z6NiKtjc0JgoLZ3eU7cPLorf52xm79Ke2KxPXhfeOwKTp1E_uoP_ZiCmDTFDSrT_2MW_5sTiuvwidVGFH-RzaJeq3Kn4eJiz8LHy5wpRPrYI.TCEzbJfuZIn9iK2Le1MDyS6t0PIKRX73NQHhRVacq6g"

# Получение токена доступа
# url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
# response = requests.post(
#     url=url,
#     data={
#         'grant_type': 'client_credentials',
#         'client_id': client_id,
#         'client_secret': client_secret
#     },
#     verify=False
# )
#
# token = response.json()['access_token']
# print(f"token: {token}")


url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

data = {
    'model': 'GigaChat-Pro',
    'messages': [
        {'role': 'user',
         'content': 'Расскажи анекдот про Yandex GPT'}
    ],
    'temperature': 0.5
}

headers = {
        'Authorization': f'Bearer {access_token}',
        # 'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

response = requests.post(url, headers=headers, json=data, verify=False) # Обязательно надо: verify=False

if response.status_code == 200:
    # print(response.json())
    print(response
          .json()
          # .get("choices")
          # .get("message")
          # .get("content")
          # .get("text")
          )
else:
    print(f"Error: {response.status_code} - {response.text}")
