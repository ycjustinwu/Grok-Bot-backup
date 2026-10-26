#!/usr/bin/env bash
# Probe a rendered video and pull check frames.
# Usage: probe.sh <video.mp4> <outdir> [t1 t2 t3 ...]   (default: 10% 50% 90% of duration)
# Prints duration, size, fps, frame count, codec, pix_fmt, audio; writes frame_<t>.png and contact.png.
set -euo pipefail
v="$1"; od="$2"; shift 2; mkdir -p "$od"
ffprobe -v error -count_frames -show_entries format=duration:stream=codec_type,codec_name,width,height,r_frame_rate,nb_read_frames,pix_fmt,color_range -of json "$v" > "$od/probe.json"
read -r D <<<"$(python3 - "$od/probe.json" <<'PY'
import json,sys
j=json.load(open(sys.argv[1])); d=float(j['format']['duration'])
v=[s for s in j['streams'] if s['codec_type']=='video'][0]; a=[s for s in j['streams'] if s['codec_type']=='audio']
n,dn=map(int,v['r_frame_rate'].split('/'))
print(f"{d}", file=sys.stdout)
print(f"duration={d:.3f}s size={v['width']}x{v['height']} fps={n/dn:g} frames={v.get('nb_read_frames')} codec={v['codec_name']} pix={v.get('pix_fmt')} range={v.get('color_range','?')} audio={'yes:'+a[0]['codec_name'] if a else 'no'}", file=sys.stderr)
PY
)"
TS=("$@"); [ ${#TS[@]} -eq 0 ] && TS=($(python3 -c "d=$D;print(' '.join(f'{d*p:.2f}' for p in (0.1,0.5,0.9)))"))
for t in "${TS[@]}"; do ffmpeg -v error -y -ss "$t" -i "$v" -frames:v 1 "$od/frame_${t}.png"; echo "frame $od/frame_${t}.png"; done
ffmpeg -v error -y -i "$v" -vf "fps=$(python3 -c "print(12/max(1e-3,$D))"),scale=480:-1,tile=4x3" -frames:v 1 "$od/contact.png" && echo "contact $od/contact.png"
