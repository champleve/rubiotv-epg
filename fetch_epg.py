#!/usr/bin/env python3
import json, gzip, xml.etree.ElementTree as ET, requests

# Load your channels.json
with open("channels.json", "r", encoding="utf-8") as f:
    channels = json.load(f)

tvg_ids = {ch["tvg-id"] for ch in channels if "tvg-id" in ch}

# Download the IPTV-org global EPG XML
url = "https://iptv-org.github.io/epg/index.xml.gz"
r = requests.get(url)
with open("index.xml.gz", "wb") as f:
    f.write(r.content)

# Decompress
with gzip.open("index.xml.gz", "rb") as f:
    tree = ET.parse(f)
    root = tree.getroot()

# Filter programmes
programs = {}
for prog in root.findall("programme"):
    cid = prog.attrib.get("channel")
    if cid in tvg_ids:
        start = prog.attrib.get("start")
        end = prog.attrib.get("end")
        title = prog.findtext("title") or ""
        desc = prog.findtext("desc") or ""
        programs.setdefault(cid, []).append({
            "title": title,
            "start": start,
            "end": end,
            "desc": desc
        })

with open("epg.json", "w", encoding="utf-8") as f:
    json.dump(programs, f, indent=2)

print("✅ epg.json generated successfully.")
