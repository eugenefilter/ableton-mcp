
# bridge.py
# Версия 1.0

import json
import socket
from flask import Flask, request, jsonify

# --- Конфигурация ---
# Адрес, на котором слушает этот бридж
BRIDGE_HOST = "127.0.0.1"
BRIDGE_PORT = 8787

# Адрес, на который бридж отправляет команды скрипту в Ableton
AGENT_HOST = "127.0.0.1"
AGENT_PORT = 8788

# Порт, на котором бридж будет слушать ответ от Ableton
REPLY_PORT = 8789

# --- Приложение Flask ---
app = Flask(__name__)

@app.route('/cmd', methods=['POST'])
def handle_command():
    """ Принимает команду, пересылает ее UDP-клиенту и возвращает ответ. """
    if not request.is_json:
        return jsonify({"ok": False, "error": {"code": "BAD_REQUEST", "message": "Request must be JSON"}}), 400

    command_data = request.get_json()
    action = command_data.get("action")

    if not action:
        return jsonify({"ok": False, "error": {"code": "VALIDATION", "message": "'action' field is required"}}), 400

    print(f"Received command: {command_data}")

    try:
        # Отправляем команду в Ableton Control Surface Script по UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(json.dumps(command_data).encode('utf-8'), (AGENT_HOST, AGENT_PORT))
        print(f"Sent command to {AGENT_HOST}:{AGENT_PORT}")

        # Возвращаем успешный ответ (без ожидания результата от Ableton)
        response = {
            "id": command_data.get("id", "unknown"),
            "ok": True,
            "result": {"message": "Command sent to Ableton"}
        }
        return jsonify(response), 200

    except Exception as e:
        print(f"Error sending UDP message: {e}")
        error_response = {
            "id": command_data.get("id", "unknown"),
            "ok": False,
            "error": {"code": "BRIDGE_ERROR", "message": str(e)}
        }
        return jsonify(error_response), 500

@app.route('/state', methods=['GET'])
def get_state():
    """ Запрашивает состояние у скрипта в Ableton и возвращает его. """
    reply_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    reply_sock.settimeout(2.0) # Ждем ответа не более 2 секунд
    reply_sock.bind((BRIDGE_HOST, REPLY_PORT))

    try:
        # 1. Отправляем команду на получение состояния
        command = {"action": "request_state", "args": {"reply_port": REPLY_PORT}}
        cmd_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        cmd_sock.sendto(json.dumps(command).encode('utf-8'), (AGENT_HOST, AGENT_PORT))
        print(f"Sent 'request_state' to {AGENT_HOST}:{AGENT_PORT}")

        # 2. Ждем ответа
        data, addr = reply_sock.recvfrom(65536)
        print(f"Received state from {addr}")

        # 3. Возвращаем ответ
        state_data = json.loads(data.decode('utf-8'))
        return jsonify({"ok": True, "state": state_data})

    except socket.timeout:
        print("Error: Timeout waiting for state from Ableton")
        return jsonify({"ok": False, "error": {"code": "TIMEOUT", "message": "Timed out waiting for state from Ableton script"}}), 504
    except Exception as e:
        print(f"Error in /state endpoint: {e}")
        return jsonify({"ok": False, "error": {"code": "BRIDGE_ERROR", "message": str(e)}}), 500
    finally:
        reply_sock.close()


if __name__ == '__main__':
    print(f"Starting bridge server on http://{BRIDGE_HOST}:{BRIDGE_PORT}")
    print(f"Forwarding commands to UDP {AGENT_HOST}:{AGENT_PORT}")
    app.run(host=BRIDGE_HOST, port=BRIDGE_PORT, debug=True)