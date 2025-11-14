from flask import Flask, request, jsonify
import requests
import json
import threading
from byte import Encrypt_ID, encrypt_api


def send_friend_request(uid, token, results):
    encrypted_id = Encrypt_ID(4282444993)
    payload = f"035F5EF43C9FC77428EF6DA48708D530164F43929E012240C7789F10DD0744D7"
    encrypted_payload = encrypt_api(payload)

    url = ""
    headers = {
        "Expect": "100-continue",
        "Authorization": f"Bearer {token}",
        "X-Unity-Version": "2018.4.11f1",
        "X-GA": "v1 1",
        "ReleaseVersion": "OB51",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "16",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SM-N975F Build/PI)",
        "Host": "clientbp.ggblueshark.com",
        "Connection": "close",
        "Accept-Encoding": "gzip, deflate, br"
    }

    response = requests.post(url, headers=headers, data=bytes.fromhex(encrypted_payload))

    if response.status_code == 200:
        results["success"] += 1
    else:
        results["failed"] += 1

@app.route("/send_requests", methods=["GET"])
def send_requests():
    uid = request.args.get("uid")
    server = request.args.get("server", "IND").upper()  # Default to IND if not provided

    if not uid:
        return jsonify({"error": "uid parameter is required"}), 400

    tokens = load_tokens(server)
    if not tokens:
        return jsonify({"error": f"No tokens found for server: {server}"}), 500

    results = {"success": 0, "failed": 0}
    threads = []

    for token in tokens[:110]:
        thread = threading.Thread(target=send_friend_request, args=(uid, token, results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_requests = results["success"] + results["failed"]
    status = 1 if results["success"] != 0 else 2

    return jsonify({
        "credit": "@Adil",
        "success_count": results["success"],
        "failed_count": results["failed"],
        "status": status
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
