import time
import requests
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

back4ap_url = "https://api.containers.back4app.com/"
back4ap_headers = {"accept": "*/*", "accept-language": "en-US,en;q=0.9,vi-VN;q=0.8,vi;q=0.7", "content-type": "application/json", "priority": "u=1, i", "sec-ch-ua": "\"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"150\", \"Google Chrome\";v=\"150\"", "sec-ch-ua-mobile": "?1", "sec-ch-ua-platform": "\"Android\"", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-site", "cookie": "_ga=GA1.1.297086740.1784678688; __zlcmid=1Yeog1fh33pXB5A; _gcl_au=1.1.451592038.1784678725; landingPage=%7B%22origin%22%3A%22https%3A%2F%2Fwww.back4app.com%22%2C%22host%22%3A%22www.back4app.com%22%2C%22pathname%22%3A%22%2Flogin%22%7D; b4a_amplitude_device_id=yYml3l5mc9lUlUxrF83j9O; ab-XjkrUHOQKm=zDxr7CzuTJ!1; mp_c6a824c901de2d494f8f060d6753e1ae_mixpanel=%7B%22distinct_id%22%3A%22%24device%3Aa623dbe5-ee42-4be8-b9ff-16d0ec94b4f7%22%2C%22%24device_id%22%3A%22a623dbe5-ee42-4be8-b9ff-16d0ec94b4f7%22%2C%22%24initial_referrer%22%3A%22%24direct%22%2C%22%24initial_referring_domain%22%3A%22%24direct%22%2C%22__mps%22%3A%7B%7D%2C%22__mpso%22%3A%7B%22%24initial_referrer%22%3A%22%24direct%22%2C%22%24initial_referring_domain%22%3A%22%24direct%22%7D%2C%22__mpus%22%3A%7B%7D%2C%22__mpa%22%3A%7B%7D%2C%22__mpu%22%3A%7B%7D%2C%22__mpr%22%3A%5B%5D%2C%22__mpap%22%3A%5B%5D%7D; _twpid=tw.1784689987224.718368382490245585; _fbp=fb.1.1784689987975.957439148805855609; b4a_attr=%7B%22first%22%3A%7B%22gclid%22%3A%22CjwKCAjwsfzSBhB5EiwAOGyqSRt1qyNGJxHmZi6acdD_HZzHsC9H19FtWF0eH_caT91l5kLR7dXHfxoC3REQAvD_BwE%22%2C%22gbraid%22%3A%220AAAAADP9tF_H_8-vqlx0FBmj0CzIKS3lp%22%7D%2C%22last%22%3A%7B%22gclid%22%3A%22CjwKCAjwsfzSBhB5EiwAOGyqSaH4kF8jG2DO72ZXdcEHSpHg8ZaGFh-RA3g-8noILPggtvxAwrR8WRoCUo0QAvD_BwE%22%2C%22gbraid%22%3A%220AAAAADP9tF_H_8-vqlx0FBmj0CzIKS3lp%22%7D%7D; __gtm_campaign_url=https%3A%2F%2Fwww.back4app.com%2Fdocs-containers%2Fhow-to-create-a-dockerfile%3Fgad_source%3D1%26gad_campaignid%3D21648680552%26gbraid%3D0AAAAADP9tF_H_8-vqlx0FBmj0CzIKS3lp%26gclid%3DCjwKCAjwsfzSBhB5EiwAOGyqSaH4kF8jG2DO72ZXdcEHSpHg8ZaGFh-RA3g-8noILPggtvxAwrR8WRoCUo0QAvD_BwE; cf_clearance=.d6eAp.iskh5zj.Ljw9QwDzUDgIVW73ugZkoO6yXvjc-1784786227-1.2.1.1-SJy6fOT11FzHh6aoY8sJqIRBMpyd8LLRAQCwnchJHRJwz7C19jwNC8rAbXyaW9OtNj2.Uy87Ds5Gnd_2iTy3mGuYzTNXVrohseFYKZJJn4DTO1081YIi1L5ZAwaDy9adtStpuQi4Y0do_CQFfsXR4Fr.gg6CdXlpz2kntjNleOngKDn4Iok6XQIZERS0ZQcNV_IPQN0yRVDSwilku48DORGkkvkO_DDB.Dgx.I9F1uEsFgi7fc0gGFlfFPEiv.AQPQoRn9T4ltY_6Y44uSivpzydo98GHxrQG6JVd7GLGzg_HsQc7GoaFTnrSN2MSC1uSAX525FSRj9ha6VnccoOIptJ7sN9iJ2eHI_noFNRS1sFHy81ympscjNMM7brD3RKRgcZVf2a7_WfSF2h4Lqlra9Z8xvazCvXEW17k.nv2iqQWNqqKvOqmiuf6BLNDH"}
back4ap_body = b'{"operationName":"triggerManualDeployment","variables":{"serviceEnvironmentId":"0ddc4dd8-3dea-40c7-9e9b-dd80012f5f0b"},"query":"mutation triggerManualDeployment($serviceEnvironmentId: String!) {\\n  triggerManualDeployment(serviceEnvironmentId: $serviceEnvironmentId) {\\n    id\\n    status\\n    result\\n    error {\\n      message\\n      code\\n      __typename\\n    }\\n    __typename\\n  }\\n}"}'

def run_health_check_server():
    # Back4app uses HTTP, so bind to standard HTTP logic on the requested port
    server_address = ('0.0.0.0', 443)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("Health check server running on port 443...")
    httpd.serve_forever()

if __name__ == '__main__':
    health_thread = threading.Thread(target=run_health_check_server, daemon=True)
    health_thread.start()
    time.sleep(2100)
    response = requests.post(
    url=back4ap_url, 
    headers=back4ap_headers, 
    data=back4ap_body,
    timeout=160
    )
