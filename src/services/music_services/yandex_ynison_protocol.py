import json
import random
import string


class YnisonProtocol:
    """Configuration class for Yandex Music Ynison websocket protocol"""

    YNISON_REDIRECT_URL = "wss://ynison.music.yandex.ru/redirector.YnisonRedirectService/GetRedirectToYnison"
    ORIGIN = "http://music.yandex.ru"

    @staticmethod
    def generate_device_id() -> str:
        """Generate random device ID"""
        return "".join(random.choice(string.ascii_lowercase) for _ in range(16))

    @staticmethod
    def create_websocket_protocol(device_id: str) -> tuple[dict, str]:
        """Create websocket protocol data"""
        device_info = {"app_name": "Chrome", "type": 1}
        ws_proto = {
            "Ynison-Device-Id": device_id,
            "Ynison-Device-Info": json.dumps(device_info),
        }
        return ws_proto, json.dumps(ws_proto)

    @staticmethod
    def get_initial_state(device_id: str) -> dict:
        """Get initial state for Ynison websocket"""
        return {
            "update_full_state": {
                "player_state": {
                    "player_queue": {
                        "current_playable_index": -1,
                        "entity_id": "",
                        "entity_type": "VARIOUS",
                        "playable_list": [],
                        "options": {"repeat_mode": "NONE"},
                        "entity_context": "BASED_ON_ENTITY_BY_DEFAULT",
                        "version": {
                            "device_id": device_id,
                            "version": 9021243204784341000,
                            "timestamp_ms": 0,
                        },
                        "from_optional": "",
                    },
                    "status": {
                        "duration_ms": 0,
                        "paused": True,
                        "playback_speed": 1,
                        "progress_ms": 0,
                        "version": {
                            "device_id": device_id,
                            "version": 8321822175199937000,
                            "timestamp_ms": 0,
                        },
                    },
                },
                "device": {
                    "capabilities": {
                        "can_be_player": True,
                        "can_be_remote_controller": False,
                        "volume_granularity": 16,
                    },
                    "info": {
                        "device_id": device_id,
                        "type": "WEB",
                        "title": "Chrome Browser",
                        "app_name": "Chrome",
                    },
                    "volume_info": {"volume": 0},
                    "is_shadow": True,
                },
                "is_currently_active": False,
            },
            "rid": "ac281c26-a047-4419-ad00-e4fbfda1cba3",
            "player_action_timestamp_ms": 0,
            "activity_interception_type": "DO_NOT_INTERCEPT_BY_DEFAULT",
        } 