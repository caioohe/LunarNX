#!/usr/bin/env python3
"""Source-level regression checks for low-data PlayStation Remote Play profiles."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
settings = (ROOT / "src/ui/ps_settings_activity.cpp").read_text()
activity = (ROOT / "src/ui/ps_activity.cpp").read_text()
session = (ROOT / "src/ps/ps_stream_session.cpp").read_text()

# Distinct, independently selectable 540p/720p/1080p profiles.
assert '{"540p", "720p", "1080p"}' in settings
assert "settings_.height == 540 ? 0 : 1" in settings
assert 'resolution->valueint == 540' in settings
assert "out.width = 960;" in settings and "out.height = 540;" in settings
for resolution in ("540", "720", "1080"):
    assert f"settings_.height = {resolution};" in settings
for width in ("960", "1280", "1920"):
    assert f"settings_.width = {width};" in settings

# Savings are only real when the video bitrate is reduced too.
assert '{"3 Mbps", "5 Mbps", "10 Mbps", "20 Mbps", "30 Mbps"}' in settings
assert "kBitrateChoicesKbps[] = {3000, 5000, 10000, 20000, 30000}" in settings
assert "std::clamp(selected, 0, 4)" in settings
assert 'cJSON_GetObjectItem(root, "ps_bitrate_kbps")' in settings
assert 'cJSON_AddNumberToObject(root, "ps_bitrate_kbps", settings.bitrate_kbps)' in settings

# Existing settings, LSFG, and user accounts must remain untouched.
assert 'cJSON_GetObjectItem(root, "ps_resolution")' in settings
assert 'cJSON_AddNumberToObject(root, "ps_resolution", settings.height)' in settings
for field in ("ps_video_codec", "ps_lsfg_30fps", "ps_vibration_enabled", "ps_rumble_strength_percent"):
    assert field in settings
assert 'new PsSettingsActivity(loadPsSettings())' in activity

# Actual stream setup must use the selected dimensions/bitrate.
assert "settings.width, settings.height, 60, settings.bitrate_kbps" in activity
assert "controller->setLsfg30fps(settings.lsfg_30fps)" in activity
for forwarded in ("width_", "height_", "bitrate_kbps_"):
    assert f"connect_info_.video_profile." in session
assert "connect_info_.video_profile.width = static_cast<unsigned int>(width_);" in session
assert "connect_info_.video_profile.height = static_cast<unsigned int>(height_);" in session
assert "connect_info_.video_profile.bitrate = static_cast<unsigned int>(bitrate_kbps_);" in session
print("PS 540p/mobile bitrate source regression checks passed")
