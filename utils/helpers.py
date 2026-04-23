import time
import json

# Timer 
def measure_time(func, *args, **kwargs):
    t0 = time.time()
    result = func(*args, **kwargs)
    elapsed = time.time() - t0
    if elapsed < 1:
        print(f"\n  ⏱  Tempo de execução: {elapsed*1000:.2f} ms")
    else:
        print(f"\n  ⏱  Tempo de execução: {elapsed:.4f} s")
    return result
def load_zones(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["zones"], data.get("zone_types", {})
def print_table(headers, rows, col_width=None):
    if not rows:
        print("  (sem resultados)")
        return

    if col_width is None:
        widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                widths[i] = max(widths[i], len(str(cell)))

        col_width = widths
    sep = "+-" + "-+-".join("-" * w for w in col_width) + "-+"
    hdr = "| " + " | ".join(str(h).ljust(w) for h, w in zip(headers, col_width)) + " |"
    print(sep)
    print(hdr)
    print(sep)
    for row in rows:
        line = "| " + " | ".join(str(c).ljust(w) for c, w in zip(row, col_width)) + " |"
        print(line)

    print(sep)
def ask(prompt, default=None):
    val = input(f"  {prompt}" + (f" [{default}]" if default else "") + ": ").strip()
    return val if val else default


def ask_int(prompt, default=None):
    while True:
        val = ask(prompt, default=str(default) if default is not None else None)

        try:
            return int(val)
        except (TypeError, ValueError):
            print("  ⚠  Por favor insira um número inteiro.")


def ask_date(prompt, default=None):
    while True:
        val = ask(prompt + " (YYYY-MM-DD)", default=default)

        if val and len(val) == 10 and val[4] == "-" and val[7] == "-":
            return val

        print("  ⚠  Formato inválido. Use YYYY-MM-DD.")


def ask_datetime(prompt, default=None):
    while True:
        val = ask(prompt + " (YYYY-MM-DD HH:MM:SS)", default=default)

        if val and len(val) == 19:
            return val

        print("  ⚠  Formato inválido. Use YYYY-MM-DD HH:MM:SS.")