import time
import requests
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

back4ap_url = "https://api.containers.back4app.com/"
back4ap_headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9,vi-VN;q=0.8,vi;q=0.7",
    "content-type": "application/json",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"150\", \"Google Chrome\";v=\"150\"",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "\"Android\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "cookie": "_ga=GA1.1.297086740.1784678688; __zlcmid=1Yeog1fh33pXB5A; _gcl_au=1.1.451592038.1784678725; landingPage=%7B%22origin%22%3A%22https%3A%2F%2Fwww.back4app.com%22%2C%22host%22%3A%22www.back4app.com%22%2C%22pathname%22%3A%22%2Flogin%22%7D; b4a_amplitude_device_id=yYml3l5mc9lUlUxrF83j9O; ab-XjkrUHOQKm=zDxr7CzuTJ!1; mp_c6a824c901de2d494f8f060d6753e1ae_mixpanel=%7B%22distinct_id%22%3A%22%24device%3Aa623dbe5-ee42-4be8-b9ff-16d0ec94b4f7%22%2C%22%24device_id%22%3A%22a623dbe5-ee42-4be8-b9ff-16d0ec94b4f7%22%2C%22%24initial_referrer%22%3A%22%24direct%22%2C%22%24initial_referring_domain%22%3A%22%24direct%22%2C%22__mps%22%3A%7B%7D%2C%22__mpso%22%3A%7B%22%24initial_referrer%22%3A%22%24direct%22%2C%22%24initial_referring_domain%22%3A%22%24direct%22%7D%2C%22__mpus%22%3A%7B%7D%2C%22__mpa%22%3A%7B%7D%2C%22__mpu%22%3A%7B%7D%2C%22__mpr%22%3A%5B%5D%2C%22__mpap%22%3A%5B%5D%7D; _twpid=tw.1784689987224.718368382490245585; _fbp=fb.1.1784689987975.957439148805855609; b4a_attr=%7B%22first%22%3A%7B%22gclid%22%3A%22CjwKCAjwsfzSBhB5EiwAOGyqSRt1qyNGJxHmZi6acdD_HZzHsC9H19FtWF0eH_caT91l5kLR7dXHfxoC3REQAvD_BwE%22%2C%22gbraid%22%3A%220AAAAADP9tF_H_8-vqlx0FBmj0CzIKS3lp%22%7D%2C%22last%22%3A%7B%22gclid%22%3A%22CjwKCAjwsfzSBhB5EiwAOGyqSaH4kF8jG2DO72ZXdcEHSpHg8ZaGFh-RA3g-8noILPggtvxAwrR8WRoCUo0QAvD_BwE%22%2C%22gbraid%22%3A%220AAAAADP9tF_H_8-vqlx0FBmj0CzIKS3lp%22%7D%7D; __gtm_campaign_url=https%3A%2F%2Fwww.back4app.com%2Fdocs-containers%2Fhow-to-create-a-dockerfile%3Fgad_source%3D1%26gad_campaignid%3D21648680552%26gbraid%3D0AAAAADP9tF_H_8-vqlx0FBmj0CzIKS3lp%26gclid%3DCjwKCAjwsfzSBhB5EiwAOGyqSaH4kF8jG2DO72ZXdcEHSpHg8ZaGFh-RA3g-8noILPggtvxAwrR8WRoCUo0QAvD_BwE; cf_clearance=.d6eAp.iskh5zj.Ljw9QwDzUDgIVW73ugZkoO6yXvjc-1784786227-1.2.1.1-SJy6fOT11FzHh6aoY8sJqIRBMpyd8LLRAQCwnchJHRJwz7C19jwNC8rAbXyaW9OtNj2.Uy87Ds5Gnd_2iTy3mGuYzTNXVrohseFYKZJJn4DTO1081YIi1L5ZAwaDy9adtStpuQi4Y0do_CQFfsXR4Fr.gg6CdXlpz2kntjNleOngKDn4Iok6XQIZERS0ZQcNV_IPQN0yRVDSwilku48DORGkkvkO_DDB.Dgx.I9F1uEsFgi7fc0gGFlfFPEiv.AQPQoRn9T4ltY_6Y44uSivpzydo98GHxrQG6JVd7GLGzg_HsQc7GoaFTnrSN2MSC1uSAX525FSRj9ha6VnccoOIptJ7sN9iJ2eHI_noFNRS1sFHy81ympscjNMM7brD3RKRgcZVf2a7_WfSF2h4Lqlra9Z8xvazCvXEW17k.nv2iqQWNqqKvOqmiuf6BLNDHGNmL0Zn08AUT7yDHw1qzokRzNv87vrC4olb4NJscRVhRuy67_g4P3hrIuRpfwhn73DJE_1kJ01fJ.cdGInDtqVJgHZavfN7SPIqfKvJ33Y4nmWXBX5Ww_VwlYZtGrQUpSozvWnB8k6zZaENyIvyF85qw; connect.sid=s%3AXeCYVUodds_YE_BYqNODixyZXSch3ZG9.ns13SGzBkzilJsPNVAJPfeoKtkqNXsvb1WGsOndZt64; _gcl_aw=GCL.1784786848.CjwKCAjw1IHTBhAaEiwA4AYNFi59_lZv-ns3lWARFBWhXY7x6OTMRALLyvzTq4HMKx_2cVd6R2EBURoC-msQAvD_BwE; _gcl_gs=2.1.k1$i1784786845$u244048342; __gtm_referrer=https%3A%2F%2Fdashboard.back4app.com%2F; AMP_MKTG_bf3379918c=JTdCJTdE; amp_bf3379=ZakbKYstsTYOMo7-L93wIL...1juch48ad.1juch48al.0.2.2; _ga_FJK5KX97E0=GS2.1.s1784979530$o19$g0$t1784979530$j60$l0$h2115181136; amp_bf3379_back4app.com=yYml3l5mc9lUlUxrF83j9O.amFzbWFydGRldnJlZ2lzdHJ5QGdtYWlsLmNvbQ==..1juch497v.1juch497v.41.2.43; _rdt_uuid=1784678725268.da8abe97-acc3-46aa-96cd-8799850f0514; _rdt_em=:8f658d1cda45c4b3c840466ac470120bd21ab27bc0194d8166259caf2c2f8f04,f142c843ea11979b69ceb44397f8ef2a818f818080d728a6232bc807b5904002,fa0d6f03c5934e21d8dd65e6a3f8c9978b358bf91a77445ab7c5c8384636ae3f,fa0d6f03c5934e21d8dd65e6a3f8c9978b358bf91a77445ab7c5c8384636ae3f,ef5a28916d5644e0daf21c567167432e4f1ee306d95979b0fe036a266c43e667; _rdt_pn=:125~857f3d4f407a4d943c5a919685ce077b3f89186acbf9a6a59ea1ad2e527e40c6|125~0a433919373204b5506622d1357ebc11993beeea8480f04fcbb8bc4bfaf3f396|125~909502c8a241216c3d2ad500977cae3e635e6efd01494f9c2b6516dd1dd5eff4|125~a8c9e6c199ae06704e587258cb3a4908058e74b40c25f3669e1eb8559b65bcf6|125~e451e12902de1e464c460fa7b072df2c04e19137218d5a0f54c5868a34799efd; AMP_bf3379918c=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJ5WW1sM2w1bWM5bFVsVXhyRjgzajlPJTIyJTJDJTIydXNlcklkJTIyJTNBJTIyamFzbWFydGRldnJlZ2lzdHJ5JTQwZ21haWwuY29tJTIyJTJDJTIyc2Vzc2lvbklkJTIyJTNBMTc4NDk3OTUyOTM2MCUyQyUyMm9wdE91dCUyMiUzQWZhbHNlJTJDJTIybGFzdEV2ZW50VGltZSUyMiUzQTE3ODQ5Nzk1ODAzMzUlN0Q="
  }
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
    first_timestamp = time.time()
    while True:
        time.sleep(600)
        response = requests.post(
        url=back4ap_url, 
        headers=back4ap_headers, 
        data=back4ap_body,
        timeout=160
        )
        data = response.json()
        if data.get('data') and data.get('data').get('triggerManualDeployment') and data.get('data').get('triggerManualDeployment').get('status') == 'DOING':
            first_timestamp = time.time()
            time.sleep(3000)
