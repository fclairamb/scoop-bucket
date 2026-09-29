"""Bump bucket/solidping.json to the latest fclairamb/solidping release."""
import json, subprocess, sys, urllib.request

MANIFEST = "bucket/solidping.json"
tag = subprocess.check_output(
    ["gh", "release", "view", "-R", "fclairamb/solidping", "--json", "tagName", "-q", ".tagName"],
    text=True).strip()
version = tag.lstrip("v")
with open(MANIFEST) as f:
    manifest = json.load(f)
if manifest["version"] == version:
    print(f"up to date ({version})")
    sys.exit(0)

base = f"https://github.com/fclairamb/solidping/releases/download/{tag}"
asset = "solidping-windows-amd64.zip"
sums = urllib.request.urlopen(f"{base}/solidping-checksums.txt").read().decode()
digest = next((line.split()[0] for line in sums.splitlines() if line.endswith(" " + asset)), None)
if not digest:
    sys.exit(f"no checksum for {asset} in {tag}")

manifest["version"] = version
manifest["architecture"]["64bit"]["url"] = f"{base}/{asset}"
manifest["architecture"]["64bit"]["hash"] = digest
with open(MANIFEST, "w") as f:
    json.dump(manifest, f, indent=4)
    f.write("\n")
print(f"bumped to {version}")
