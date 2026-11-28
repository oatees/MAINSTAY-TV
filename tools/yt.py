#!/usr/bin/env python3
"""Small YouTube helper for the research/analyse skills.

Commands:
  watch <url> [--interval 2] [--cols 5]   download, frames every N s, contact sheets, transcript
  video <url>                             title/channel/views/length/publish date (scraped; API key optional)
  transcript <url>                        transcript -> research/<id>/transcript.txt
  channel <handle-or-url> [--days 120]    subs + recent upload stats (scraped)

No API key is required. If tools/.env has YOUTUBE_API_KEY it is used when present,
otherwise metadata is scraped from the public watch page.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import shutil
import subprocess
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESEARCH = ROOT / "research"
ENV_FILE = ROOT / "tools" / ".env"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"


def load_env() -> dict:
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def video_id(url: str) -> str:
    url = url.strip()
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", url):
        return url
    parsed = urllib.parse.urlparse(url)
    if parsed.hostname and "youtu.be" in parsed.hostname:
        return parsed.path.strip("/").split("/")[0]
    if parsed.path.startswith("/shorts/"):
        return parsed.path.split("/shorts/", 1)[1].split("/")[0]
    qs = urllib.parse.parse_qs(parsed.query)
    if "v" in qs:
        return qs["v"][0]
    raise SystemExit(f"Could not find a video id in {url!r}")


def http_get(url: str) -> str:
    import requests

    r = requests.get(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"}, timeout=30)
    r.raise_for_status()
    return r.text


def scrape_video(url: str) -> dict:
    vid = video_id(url)
    html = http_get(f"https://www.youtube.com/shorts/{vid}")
    out = {"id": vid, "url": f"https://youtu.be/{vid}"}
    # Prefer the structured videoDetails block; a plain "title" regex can hit UI strings.
    m = re.search(r'"videoDetails":\{[^{}]*?"title":"([^"]+)"', html)
    if m:
        out["title"] = m.group(1)
    else:
        try:
            import requests

            o = requests.get(
                f"https://www.youtube.com/oembed?url=https://www.youtube.com/shorts/{vid}&format=json",
                headers={"User-Agent": UA}, timeout=20,
            ).json()
            out["title"] = o.get("title", "")
            out["channel"] = o.get("author_name", "")
        except Exception:
            pass
    for key, pat in {
        "channel": r'"ownerChannelName":"([^"]+)"',
        "views": r'"viewCount":"(\d+)"',
        "length_seconds": r'"lengthSeconds":"(\d+)"',
        "publish_date": r'"publishDate":"([^"]+)"',
        "category": r'"category":"([^"]+)"',
    }.items():
        m = re.search(pat, html)
        if m:
            out[key] = m.group(1)
    m = re.search(r'"shortDescription":"(.*?)"(?=,"isCrawlable"|,"thumbnail")', html, re.S)
    if m:
        try:
            out["description"] = m.group(1).encode("utf-8").decode("unicode_escape")
        except Exception:
            out["description"] = m.group(1)
    out["thumbnail"] = f"https://i.ytimg.com/vi/{vid}/maxresdefault.jpg"
    return out


def scrape_channel(channel: str) -> dict:
    if channel.startswith("http"):
        url = channel
    elif channel.startswith("@"):
        url = f"https://www.youtube.com/{channel}"
    else:
        url = f"https://www.youtube.com/@{channel.lstrip('@')}"
    html = http_get(url)
    out = {"url": url}
    m = re.search(r'"subscriberCountText":\{"simpleText":"([^"]+)"\}', html)
    if not m:
        m = re.search(r'([\d.,]+[KMB]?)\s*subscribers', html, re.I)
    if m:
        out["subscribers"] = m.group(1)
    m = re.search(r'"title":"([^"]+)"', html)
    if m:
        out["title"] = m.group(1)
    return out


def fetch_transcript(vid: str) -> list[dict]:
    from youtube_transcript_api import YouTubeTranscriptApi

    api = YouTubeTranscriptApi()
    t = api.fetch(vid)
    return [{"start": round(s.start, 2), "duration": round(s.duration, 2), "text": s.text} for s in t.snippets]


def download(vid: str, outdir: Path) -> Path:
    outdir.mkdir(parents=True, exist_ok=True)
    target = outdir / "video.mp4"
    if target.exists():
        return target
    ffmpeg = find_ffmpeg()
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--no-playlist", "--quiet", "--no-warnings",
        "--ffmpeg-location", str(Path(ffmpeg).parent),
        "-f", "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/bv*[height<=1080]+ba/b",
        "--merge-output-format", "mp4",
        "-o", str(outdir / "video.%(ext)s"),
        f"https://youtu.be/{vid}",
    ]
    subprocess.run(cmd, check=True)
    if target.exists():
        return target
    # yt-dlp sometimes leaves the streams unmerged; merge them ourselves.
    vids = sorted(outdir.glob("video.f*.mp4"))
    auds = sorted(outdir.glob("video.f*.m4a")) + sorted(outdir.glob("video.f*.webm"))
    if vids and auds:
        subprocess.run(
            [ffmpeg, "-y", "-i", str(vids[0]), "-i", str(auds[0]), "-c", "copy", "-movflags", "+faststart", str(target)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        return target
    for p in outdir.glob("video.*"):
        if p.suffix.lower() in {".mp4", ".mkv", ".webm"}:
            if p != target:
                shutil.move(str(p), str(target))
            return target
    raise SystemExit("Download finished but no video file was found.")


def find_ffmpeg() -> str:
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    candidates = [
        Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WinGet" / "Links" / "ffmpeg.exe",
        Path("C:/ProgramData/chocolatey/bin/ffmpeg.exe"),
        Path("C:/ffmpeg/bin/ffmpeg.exe"),
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    # search winget packages
    base = Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WinGet" / "Packages"
    if base.exists():
        for p in base.rglob("ffmpeg.exe"):
            return str(p)
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        pass
    raise SystemExit("ffmpeg not found on PATH or in common install locations.")


def extract_frames(video: Path, outdir: Path, interval: float) -> list[Path]:
    ffmpeg = find_ffmpeg()
    frames_dir = outdir / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    pattern = str(frames_dir / "frame_%04d.jpg")
    cmd = [ffmpeg, "-y", "-i", str(video), "-vf", f"fps=1/{interval}", "-q:v", "2", pattern]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return sorted(frames_dir.glob("frame_*.jpg"))


def make_contact_sheets(frames: list[Path], outdir: Path, interval: float, cols: int = 5, rows: int = 4) -> list[Path]:
    from PIL import Image, ImageDraw, ImageFont

    if not frames:
        return []
    per_sheet = cols * rows
    thumb_w = 320
    pad = 6
    label_h = 22
    sheets = []
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except Exception:
        font = ImageFont.load_default()
    for sheet_idx in range(0, len(frames), per_sheet):
        chunk = frames[sheet_idx:sheet_idx + per_sheet]
        with Image.open(chunk[0]) as first:
            ratio = first.height / first.width
        thumb_h = int(thumb_w * ratio)
        sheet_w = cols * (thumb_w + pad) + pad
        sheet_h = rows * (thumb_h + label_h + pad) + pad
        sheet = Image.new("RGB", (sheet_w, sheet_h), (18, 18, 18))
        draw = ImageDraw.Draw(sheet)
        for i, f in enumerate(chunk):
            r, c = divmod(i, cols)
            x = pad + c * (thumb_w + pad)
            y = pad + r * (thumb_h + label_h + pad)
            with Image.open(f) as im:
                im = im.convert("RGB")
                im.thumbnail((thumb_w, thumb_h))
                sheet.paste(im, (x, y))
            t = int((sheet_idx + i) * interval)
            draw.text((x + 3, y + thumb_h + 2), f"{t // 60}:{t % 60:02d}", fill=(240, 240, 240), font=font)
        path = outdir / f"contact_{sheet_idx // per_sheet + 1:02d}.jpg"
        sheet.save(path, quality=88)
        sheets.append(path)
    return sheets


def cmd_watch(args) -> None:
    vid = video_id(args.url)
    outdir = RESEARCH / vid
    outdir.mkdir(parents=True, exist_ok=True)
    meta = scrape_video(args.url)
    meta["frames_interval_seconds"] = args.interval
    (outdir / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

    try:
        transcript = fetch_transcript(vid)
        (outdir / "transcript.json").write_text(json.dumps(transcript, indent=2, ensure_ascii=False), encoding="utf-8")
        (outdir / "transcript.txt").write_text(
            "\n".join(f"{t['start']:.2f} | {t['text']}" for t in transcript), encoding="utf-8"
        )
        print(f"transcript: {len(transcript)} snippets")
    except Exception as exc:
        print(f"transcript unavailable: {exc}")

    video = download(vid, outdir)
    print(f"video: {video}")
    frames = extract_frames(video, outdir, args.interval)
    print(f"frames: {len(frames)}")
    sheets = make_contact_sheets(frames, outdir, args.interval, cols=args.cols)
    for s in sheets:
        print(f"contact sheet: {s}")
    meta["frames"] = len(frames)
    meta["contact_sheets"] = [str(s) for s in sheets]
    (outdir / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")


def cmd_video(args) -> None:
    print(json.dumps(scrape_video(args.url), indent=2, ensure_ascii=False))


def cmd_transcript(args) -> None:
    vid = video_id(args.url)
    outdir = RESEARCH / vid
    outdir.mkdir(parents=True, exist_ok=True)
    transcript = fetch_transcript(vid)
    (outdir / "transcript.json").write_text(json.dumps(transcript, indent=2, ensure_ascii=False), encoding="utf-8")
    (outdir / "transcript.txt").write_text(
        "\n".join(f"{t['start']:.2f} | {t['text']}" for t in transcript), encoding="utf-8"
    )
    print(f"{len(transcript)} snippets -> {outdir / 'transcript.txt'}")


def cmd_channel(args) -> None:
    print(json.dumps(scrape_channel(args.channel), indent=2, ensure_ascii=False))


def main() -> None:
    p = argparse.ArgumentParser(description="YouTube research helper")
    sub = p.add_subparsers(dest="cmd", required=True)

    w = sub.add_parser("watch", help="download, frames, contact sheets, transcript")
    w.add_argument("url")
    w.add_argument("--interval", type=float, default=2.0)
    w.add_argument("--cols", type=int, default=5)
    w.set_defaults(func=cmd_watch)

    v = sub.add_parser("video", help="video metadata")
    v.add_argument("url")
    v.set_defaults(func=cmd_video)

    t = sub.add_parser("transcript", help="save transcript")
    t.add_argument("url")
    t.set_defaults(func=cmd_transcript)

    c = sub.add_parser("channel", help="channel metadata")
    c.add_argument("channel")
    c.add_argument("--days", type=int, default=120)
    c.set_defaults(func=cmd_channel)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
