import subprocess

def run_git(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return f"OK: {cmd}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}\n"
    except subprocess.CalledProcessError as e:
        return f"FAIL: {cmd}\nSTDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}\n"

with open("git_log.txt", "w") as f:
    f.write(run_git("git add ."))
    f.write(run_git('git commit -m "update code"'))
    f.write(run_git("git push origin main"))
    f.write(run_git("git push origin master"))
