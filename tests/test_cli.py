import os, subprocess, sys, tempfile

ROOT = os.path.join(os.path.dirname(__file__), "..")
ENV = dict(os.environ, DEADLINEGUARDIAN_TODAY="2026-11-18")
passed = 0

def run(*args, stdin=""):
    return subprocess.run([sys.executable, os.path.join(ROOT, "src", "cli.py"), *args],
                          input=stdin, capture_output=True, text=True, env=ENV, timeout=30)

# demo mode: end-to-end, shows all three documents + batch summary
r = run("demo")
assert r.returncode == 0, r.stderr
for needle in ["Bill due", "Benefits", "Medical", "Batch summary", "Next action"]:
    assert needle in r.stdout, (needle, r.stdout)
passed += 1

# once mode: stdin document -> triage card
r = run("once", stdin="Property tax notice from the treasurer: $1,200 due 02/14/2027.")
assert r.returncode == 0 and "Tax" in r.stdout and "88" in r.stdout, r.stdout
passed += 1

# batch mode: '---'-separated file, sorted most-urgent first
with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as fh:
    fh.write("Clinic appointment reminder for your prescription refill.\n---\n"
             "Final notice: your electric bill is past due. Amount due $90.00, payment due December 18, 2026.\n")
    path = fh.name
try:
    r = run("batch", path)
    assert r.returncode == 0, r.stderr
    assert r.stdout.index("Bill due") < r.stdout.index("Medical"), r.stdout
    assert "Batch summary" in r.stdout
finally:
    os.unlink(path)
passed += 1

print(f"ALL PASS (python cli: {passed} checks)")
