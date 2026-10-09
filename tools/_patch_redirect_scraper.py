from pathlib import Path

path = Path("tools/update_community_status.py")
text = path.read_text(encoding="utf-8")

target = '''            if (
                reachable is True and meta.get("expectsHtml") is True and markers and
                body
            ):
'''

insert = '''            if reachable is True and meta.get("expectsHtml") is True and final_url != dep:
                old_host = (urllib.parse.urlparse(dep).hostname or "").lower()
                new_host = (urllib.parse.urlparse(final_url).hostname or "").lower()
                if old_host and new_host and old_host != new_host and (not markers or not body):
                    reachable = False
                    definite_broken = True
                    reason = f"HTML scraper redirected to different host and selectors could not be verified: {final_url}"

'''

if insert in text:
    print("Redirected scraper rule already present")
elif target not in text:
    raise SystemExit("scraper validation target not found")
else:
    path.write_text(text.replace(target, insert + target, 1), encoding="utf-8")
    print("Redirected scraper rule inserted")
