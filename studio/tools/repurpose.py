#!/usr/bin/env python3
"""Turn rendered videos into every sellable format.

    python3 studio/tools/repurpose.py package <id>            # per-platform upload kit for one video
    python3 studio/tools/repurpose.py compile <channel> [-n 10] # long-form 16:9 compilation + chapters
    python3 studio/tools/repurpose.py podcast <channel> [-n 10] # audio episode (mp3) + chapters
    python3 studio/tools/repurpose.py ebook <channel>           # EPUB of the channel's original stories

Inputs: item files in studio/pipeline/*/<id>.md, videos in studio/output/<id>.mp4, studio/monetize.json.
Outputs go to studio/output/ (gitignored). Nothing here uploads or posts anything.
"""
import argparse
import glob
import json
import os
import re
import subprocess
import tempfile
import urllib.parse

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "output")
CFG = json.load(open(os.path.join(ROOT, "monetize.json")))
# stages whose videos are finished enough to reuse
DONE_STAGES = ("04-approved", "05-produced", "06-scheduled", "07-published")


def ff(*args):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)


def duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def find_item(item_id):
    hits = glob.glob(os.path.join(ROOT, "pipeline", "*", f"{item_id}.md"))
    if not hits:
        raise SystemExit(f"no item file for {item_id}")
    return hits[0]


def section(text, name):
    m = re.search(rf"^## {re.escape(name)}.*?\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else ""


def field(block, label):
    m = re.search(rf"\*\*{re.escape(label)}[^*]*\*\*:?\s*(.*?)(?=\n\s*[-*]*\s*\*\*|\Z)", block, re.S)
    return m.group(1).strip() if m else ""


def item_info(path):
    text = open(path).read()
    fm = dict(re.findall(r"^(\w+):\s*(.*)$", text.split("---")[1], re.M)) if text.startswith("---") else {}
    title = re.search(r"^# (.+)$", text, re.M).group(1).strip()
    script = section(text, "Script")
    narration = field(script, "Narration")
    sources = re.findall(r"https?://\S+", section(text, "Fact check"))
    return {"id": fm.get("id", "").strip(), "channel": fm.get("channel", "").strip(), "title": title,
            "narration": narration, "package": section(text, "Package"), "sources": sources,
            "affiliate_query": fm.get("affiliate_query", "").strip(),
            "disclosure": fm.get("disclosure_synthetic", "").strip()}


def affiliate_link(info):
    q = info["affiliate_query"] or CFG["channels"].get(info["channel"], {}).get("affiliate_query", "")
    if not q:
        return ""
    return f"https://www.amazon.com/s?k={urllib.parse.quote_plus(q)}&tag={CFG['amazon_tag']}"


def channel_videos(channel, n):
    items = []
    for stage in DONE_STAGES:
        for p in sorted(glob.glob(os.path.join(ROOT, "pipeline", stage, f"{channel}-*.md"))):
            info = item_info(p)
            mp4 = os.path.join(OUT, f"{info['id']}.mp4")
            if os.path.exists(mp4):
                items.append((info, mp4))
    if not items:
        raise SystemExit(f"no rendered videos for channel {channel}")
    return items[:n]


def cmd_package(item_id):
    info = item_info(find_item(item_id))
    src = os.path.join(OUT, f"{item_id}.mp4")
    if not os.path.exists(src):
        raise SystemExit(f"render first: {src} missing")
    dest = os.path.join(OUT, item_id)
    os.makedirs(dest, exist_ok=True)
    dur = duration(src)
    pkg = info["package"]
    yt_title = field(pkg, "YouTube title") or info["title"][:60]
    tt_caption = field(pkg, "TikTok caption") or info["title"]
    tags = " ".join(CFG["channels"].get(info["channel"], {}).get("hashtags", []))
    aff = affiliate_link(info)
    src_lines = "\n".join(f"- {u}" for u in info["sources"][:4])
    desc = f"{field(pkg, 'Description') or info['title']}\n\n"
    if src_lines:
        desc += f"Sources:\n{src_lines}\n\n"
    if aff:
        desc += f"Read more (affiliate link, we may earn a commission): {aff}\n\n"
    desc += f"{CFG['ai_note']}\n\n#shorts {tags}"
    # same master file works for every vertical platform; thumbnail from the hook
    ff("-ss", "1.5", "-i", src, "-frames:v", "1", "-q:v", "2", os.path.join(dest, "thumbnail.jpg"))
    ff("-i", src, "-vn", "-ac", "1", "-b:a", "128k", os.path.join(dest, "audio.mp3"))
    platforms = [
        ("YouTube Shorts", dur <= 180, f"Title: {yt_title}\n\n{desc}"),
        ("TikTok", True, f"{tt_caption} {tags} #fyp"),
        ("Instagram Reels", dur <= 180, f"{tt_caption}\n\n{CFG['ai_note']}\n{tags}"),
        ("Facebook Reels", True, f"{tt_caption}\n\n{CFG['ai_note']}"),
        ("Snapchat Spotlight", dur <= 60, f"{tt_caption} {tags}"),
    ]
    lines = [f"# Upload kit: {info['title']}", "",
             f"Video: `../{item_id}.mp4` ({dur:.1f}s, 1080x1920) · thumbnail.jpg · audio.mp3", "",
             f"AI/synthetic disclosure toggle: **{'ON' if info['disclosure'] == 'true' else 'OFF (no realistic synthetic people)'}** · "
             "Made for kids: **No**", "",
             "🔴 Nothing here is posted automatically. Tony approves and posts.", ""]
    for name, ok, text in platforms:
        lines += [f"## {name}", "" if ok else f"_Not eligible: {dur:.0f}s is over this platform's limit._", ""]
        if ok:
            lines += ["```", text, "```", ""]
            with open(os.path.join(dest, f"{name.lower().replace(' ', '-')}.txt"), "w") as fh:
                fh.write(text + "\n")
    if not field(pkg, "YouTube title"):
        lines += ["> Package section is empty: titles/captions fell back to the working title. Run the packager agent."]
    open(os.path.join(dest, "UPLOAD.md"), "w").write("\n".join(lines) + "\n")
    print(f"wrote {dest}/UPLOAD.md")


def cmd_compile(channel, n):
    items = channel_videos(channel, n)
    dest = os.path.join(OUT, f"{channel}-compilation.mp4")
    ins, filt, t, chapters = [], [], 0.0, []
    for i, (info, mp4) in enumerate(items):
        ins += ["-i", mp4]
        # 9:16 clip centered on a blurred 16:9 copy of itself
        filt.append(f"[{i}:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=30:3,"
                    f"eq=brightness=-0.15[bg{i}];[{i}:v]scale=-2:1080[fg{i}];[bg{i}][fg{i}]overlay=(W-w)/2:0,"
                    f"setsar=1,fps=30[v{i}];[{i}:a]aresample=48000[a{i}]")
        chapters.append(f"{int(t // 60)}:{int(t % 60):02d} {info['title']}")
        t += duration(mp4)
    filt.append("".join(f"[v{i}][a{i}]" for i in range(len(items))) + f"concat=n={len(items)}:v=1:a=1[v][a]")
    ff(*ins, "-filter_complex", ";".join(filt), "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset",
       "medium", "-crf", "23", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", dest)
    open(dest.replace(".mp4", "-chapters.txt"), "w").write("\n".join(chapters) + "\n")
    print(f"wrote {dest} ({t / 60:.1f} min, {len(items)} stories); chapters in -chapters.txt")
    if t < 480:
        print("note: under 8 minutes; mid-roll ads need 8+ min, so add more videos before uploading")


def cmd_podcast(channel, n):
    items = channel_videos(channel, n)
    tmp = tempfile.mkdtemp()
    lst, t, chapters = [], 0.0, []
    for i, (info, mp4) in enumerate(items):
        a = os.path.join(tmp, f"{i}.wav")
        ff("-i", mp4, "-vn", "-ac", "1", "-ar", "44100", "-af", "apad=pad_dur=1.5", a)
        lst.append(f"file '{a}'")
        chapters.append(f"{int(t // 60)}:{int(t % 60):02d} {info['title']}")
        t += duration(a)
    open(os.path.join(tmp, "list.txt"), "w").write("\n".join(lst))
    dest = os.path.join(OUT, f"{channel}-podcast.mp3")
    ff("-f", "concat", "-safe", "0", "-i", os.path.join(tmp, "list.txt"), "-af", "loudnorm=I=-16:TP=-1.5",
       "-b:a", "128k", dest)
    open(dest.replace(".mp3", "-chapters.txt"), "w").write("\n".join(chapters) + "\n")
    print(f"wrote {dest} ({t / 60:.1f} min, {len(items)} stories)")


def cmd_ebook(channel):
    stories = []
    for stage in DONE_STAGES:
        for p in sorted(glob.glob(os.path.join(ROOT, "pipeline", stage, f"{channel}-*.md"))):
            info = item_info(p)
            if info["narration"]:
                stories.append(info)
    if not stories:
        raise SystemExit(f"no approved stories for {channel}")
    name = channel.replace("-", " ").title()
    md = [f"% {name}: Short Stories", "% Written by the studio team, narrated with AI voice in our videos", ""]
    for s in stories:
        md += [f"# {s['title']}", "", s["narration"].replace("\n", "\n\n"), ""]
        if s["sources"]:
            md += ["*Sources:* " + ", ".join(s["sources"][:3]), ""]
    src = os.path.join(OUT, f"{channel}-ebook.md")
    open(src, "w").write("\n".join(md))
    dest = src.replace(".md", ".epub")
    subprocess.run(["pandoc", src, "-o", dest, "--toc"], check=True)
    print(f"wrote {dest} ({len(stories)} stories). Amazon KDP asks you to disclose AI-generated content.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("package").add_argument("id")
    for c in ("compile", "podcast"):
        p = sub.add_parser(c)
        p.add_argument("channel")
        p.add_argument("-n", type=int, default=10)
    sub.add_parser("ebook").add_argument("channel")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    {"package": lambda: cmd_package(a.id), "compile": lambda: cmd_compile(a.channel, a.n),
     "podcast": lambda: cmd_podcast(a.channel, a.n), "ebook": lambda: cmd_ebook(a.channel)}[a.cmd]()
