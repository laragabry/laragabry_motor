from structures.hash_table import HashTable
from structures.heap import MinHeap, top_k
from algorithms.sorting import bubble_sort, merge_sort, benchmark_sorts
from algorithms.search import binary_search_range, kmp_search
from utils.helpers import print_table, ask, ask_int, ask_date, ask_datetime

def _ts_to_secs(ts):
    d   = ts[:10]
    hms = ts[11:]
    y, mo, day = int(d[:4]), int(d[5:7]), int(d[8:10])
    h, mi, s   = int(hms[:2]), int(hms[3:5]), int(hms[6:8])
    return ((y * 365 + mo * 30 + day) * 86400 + h * 3600 + mi * 60 + s)

def _filter_interval(events, ts_ini, ts_fim):
    return [e for e in events if ts_ini <= e.timestamp <= ts_fim]

def _sqrt(n):
    if n <= 0: return 0.0
    x = float(n)
    for _ in range(50):
        x = (x + n / x) / 2
    return x

def _mean(lst):
    return sum(lst) / len(lst) if lst else 0.0

def _std(lst):
    if len(lst) < 2: return 0.0
    m  = _mean(lst)
    v  = sum((x - m) ** 2 for x in lst) / len(lst)
    return _sqrt(v)


#  QUERY 1 — Ocupação por zona num intervalo

def q1_ocupacao_por_zona(events, idx_zone, idx_date, zones, zone_types):
    print("\n── Query 1: Ocupação por zona num intervalo ──")
    ts_ini = ask_datetime("Data/hora início", "2025-03-10 09:00:00")
    ts_fim = ask_datetime("Data/hora fim",   "2025-03-16 21:00:00")
    filtro_tipo = ask("Filtrar por tipo de zona (ou ENTER para todas)", "")

    contagem = HashTable(size=64)

    for ev in events:
        if ev.event_type != "entry":
            continue
        if not (ts_ini <= ev.timestamp <= ts_fim):
            continue
        if filtro_tipo:
            info = zones.get(ev.zone_id, {})
            if info.get("type", "") != filtro_tipo:
                continue
        cnt = contagem.get(ev.zone_id)
        contagem.insert(ev.zone_id, (cnt or 0) + 1)

    resultado = list(contagem.items())
    resultado, _ = merge_sort(resultado, key=lambda x: x[1], reverse=True)

    print(f"\n  Período: {ts_ini}  →  {ts_fim}")
    rows = []
    for zone_id, total in resultado:
        nome = zones.get(zone_id, {}).get("label", zone_id)
        tipo = zones.get(zone_id, {}).get("type", "-")
        rows.append((zone_id, nome, tipo, total))
    print_table(["ID Zona", "Nome", "Tipo", "Entradas"], rows)


#  QUERY 2 — Média de permanência por zona

def q2_media_permanencia(events, idx_zone, zones):
    print("\n── Query 2: Média de permanência por zona ──")
    zona_input = ask("Zona específica (ou ENTER para todas)", "")

    horas = list(range(9, 21))

    acc = HashTable(size=512)

    for ev in events:
        if ev.event_type != "linger":
            continue
        if zona_input and ev.zone_id != zona_input:
            continue
        key = f"{ev.zone_id}|{ev.hour}"
        lst = acc.get(key)
        if lst is None:
            lst = []
            acc.insert(key, lst)
        lst.append(ev.duration)

    zonas_set = HashTable(size=64)
    for k, _ in acc.items():
        z = k.split("|")[0]
        zonas_set.insert(z, 1)
    zonas = sorted(zonas_set.keys())

    print(f"\n  {'Zona':<10}", end="")
    for h in horas:
        print(f" {h:02d}-{h+1:02d}h", end="")
    print()
    print("  " + "-" * (10 + 8 * len(horas)))

    for z in zonas:
        nome = zones.get(z, {}).get("label", z)
        print(f"  {z:<10}", end="")
        for h in horas:
            lst = acc.get(f"{z}|{h}") or []
            media = int(_mean(lst)) if lst else 0
            print(f" {media:>7}", end="")
        print()
    print(f"\n  (valores em segundos)")

#  QUERY 3 — Picos de ocupação (sweep line)
def q3_picos_ocupacao(events, idx_date):
    print("\n── Query 3: Picos de ocupação ──")
    dia   = ask_date("Dia", "2025-03-10")
    k     = ask_int("Top-K picos", 5)

    evs_dia = idx_date.get(dia) or []
    sweep = []
    for ev in evs_dia:
        if ev.event_type == "entry":
            sweep.append((ev.timestamp, +1))
        elif ev.event_type == "exit":
            sweep.append((ev.timestamp, -1))

    if not sweep:
        print("  Sem dados para esse dia.")
        return

    sweep, _ = merge_sort(sweep, key=lambda x: x[0])

    momentos = []
    ocupacao = 0
    for ts, delta in sweep:
        ocupacao += delta
        momentos.append((ocupacao, ts))
    topk = top_k(momentos, k)
    print(f"\n  Top-{k} picos em {dia}:")
    print_table(["#", "Timestamp", "Pessoas simultâneas"],
                [(i+1, ts, occ) for i, (occ, ts) in enumerate(topk)])


#  QUERY 4 — Comparação entre dois dias

def q4_comparacao_dias(events, idx_date, zones):
    print("\n── Query 4: Comparação entre dias ──")
    dia1 = ask_date("Primeiro dia",  "2025-03-10")
    dia2 = ask_date("Segundo dia",   "2025-03-11")

    def stats_dia(dia):
        evs = idx_date.get(dia) or []
        visitantes   = sum(1 for e in evs if e.event_type == "entry")
        duracoes     = [e.duration for e in evs if e.event_type == "linger"]
        media_dur    = int(_mean(duracoes))

        cnt_zona = HashTable(size=64)
        for e in evs:
            if e.event_type == "entry":
                c = cnt_zona.get(e.zone_id)
                cnt_zona.insert(e.zone_id, (c or 0) + 1)

        best_zona, best_cnt = "-", 0
        for z, c in cnt_zona.items():
            if c > best_cnt:
                best_zona, best_cnt = z, c

        nome = zones.get(best_zona, {}).get("label", best_zona)
        return visitantes, media_dur, f"{nome} ({best_cnt})"

    v1, m1, z1 = stats_dia(dia1)
    v2, m2, z2 = stats_dia(dia2)

    print_table(
        ["Métrica", dia1, dia2],
        [
            ("Total visitantes", v1, v2),
            ("Permanência média (s)", m1, m2),
            ("Zona mais visitada", z1, z2),
        ]
    )


#  QUERY 5 — Top-K zonas mais visitadas
def q5_topk_zonas(events, zones):
    print("\n── Query 5: Top-K zonas mais visitadas ──")
    ts_ini = ask_datetime("Data/hora início", "2025-03-10 09:00:00")
    ts_fim = ask_datetime("Data/hora fim",   "2025-03-16 21:00:00")
    k      = ask_int("K", 5)

    cnt = HashTable(size=64)
    for ev in events:
        if ev.event_type != "entry":
            continue
        if not (ts_ini <= ev.timestamp <= ts_fim):
            continue
        c = cnt.get(ev.zone_id)
        cnt.insert(ev.zone_id, (c or 0) + 1)

    pairs  = list(cnt.items()) 
    topk   = top_k([(c, z) for z, c in pairs], k)

    print(f"\n  Top-{k} zonas entre {ts_ini[:10]} e {ts_fim[:10]}:")
    rows = []
    for rank, (cnt_val, zone_id) in enumerate(topk, 1):
        nome = zones.get(zone_id, {}).get("label", zone_id)
        rows.append((rank, zone_id, nome, cnt_val))
    print_table(["#", "ID", "Nome", "Entradas"], rows)


#  QUERY 6 — Top-K blocos de 30 min com mais eventos

def q6_topk_blocos(events, zones):
    print("\n── Query 6: Top-K blocos de 30 min com mais eventos ──")
    k          = ask_int("K", 5)
    zona_filtro = ask("Zona específica (ou ENTER para todas)", "")

    cnt = HashTable(size=2048)

    for ev in events:
        if zona_filtro and ev.zone_id != zona_filtro:
            continue
        bloco_min = 0 if ev.minute < 30 else 30
        key       = f"{ev.date}|{ev.hour:02d}:{bloco_min:02d}"
        c         = cnt.get(key)
        cnt.insert(key, (c or 0) + 1)

    pairs = [(c, k_) for k_, c in cnt.items()]
    topk  = top_k(pairs, k)

    print(f"\n  Top-{k} blocos de 30 min:")
    rows = [(i+1, blk, ev_cnt) for i, (ev_cnt, blk) in enumerate(topk)]
    print_table(["#", "Bloco (início)", "Eventos"], rows)


#  QUERY 7 — Zonas com maior tempo médio de permanência
def q7_topk_permanencia(events, zones):
    print("\n── Query 7: Zonas com maior tempo médio de permanência ──")
    k              = ask_int("K", 5)
    gender_filtro  = ask("Género (M/F ou ENTER para todos)", "")
    age_filtro     = ask("Faixa etária (ou ENTER para todas)", "")

    acc = HashTable(size=64)
    for ev in events:
        if ev.event_type != "linger":
            continue
        if gender_filtro and ev.gender != gender_filtro:
            continue
        if age_filtro and ev.age != age_filtro:
            continue
        lst = acc.get(ev.zone_id)
        if lst is None:
            lst = []
            acc.insert(ev.zone_id, lst)
        lst.append(ev.duration)

    medias = []
    for z, durs in acc.items():
        medias.append((_mean(durs), z))

    topk = top_k(medias, k)
    rows = []
    for i, (media, z) in enumerate(topk, 1):
        nome = zones.get(z, {}).get("label", z)
        rows.append((i, z, nome, int(media)))
    print_table(["#", "ID", "Nome", "Permanência média (s)"], rows)


#  QUERY 8 — Fluxo entre zonas (matriz de transição)
def q8_fluxo_entre_zonas(events, zones):
    print("\n── Query 8: Fluxo entre zonas ──")
    threshold = ask_int("Threshold temporal (segundos)", 120)
    n_top     = ask_int("N transições mais frequentes", 10)

    sorted_evs, _ = merge_sort(events, key=lambda e: (e.gender, e.age, e.timestamp))

    transicoes = HashTable(size=1024)

    i = 0
    while i < len(sorted_evs) - 1:
        ev  = sorted_evs[i]
        nxt = sorted_evs[i + 1]
        if (ev.gender == nxt.gender and ev.age == nxt.age
                and ev.event_type == "exit" and nxt.event_type == "entry"):
            dt = _ts_to_secs(nxt.timestamp) - _ts_to_secs(ev.timestamp)
            if 0 <= dt <= threshold:
                key = f"{ev.zone_id}→{nxt.zone_id}"
                c   = transicoes.get(key)
                transicoes.insert(key, (c or 0) + 1)
        i += 1

    pairs = [(c, k_) for k_, c in transicoes.items()]
    topn  = top_k(pairs, n_top)

    print(f"\n  Top-{n_top} transições (threshold={threshold}s):")
    rows = [(i+1, tr, cnt) for i, (cnt, tr) in enumerate(topn)]
    print_table(["#", "Transição (A→B)", "Ocorrências"], rows)



#  QUERY 9 — Pesquisa de sequências de zonas (KMP)
def q9_sequencias_zonas(events):
    print("\n── Query 9: Pesquisa de sequências de zonas (KMP) ──")
    seq_str = ask("Sequência de zonas separadas por '-' (ex: Z_E1-Z_C1-Z_CK)", "Z_E1-Z_C1")
    pattern = seq_str.split("-")

    entries, _ = merge_sort(
        [e for e in events if e.event_type == "entry"],
        key=lambda e: e.timestamp
    )
    text = [e.zone_id for e in entries]

    ocorrencias = kmp_search(text, pattern)
    print(f"\n  Padrão: {' → '.join(pattern)}")
    print(f"  Ocorrências encontradas: {len(ocorrencias)}")

    if ocorrencias and ask("Mostrar até 10 primeiras ocorrências? (s/n)", "s") == "s":
        rows = []
        for idx in ocorrencias[:10]:
            ts = entries[idx].timestamp
            rows.append((idx, ts, " → ".join(text[idx:idx+len(pattern)])))
        print_table(["Índice", "Timestamp início", "Sequência"], rows)

#  QUERY 10 — Deteção de anomalias
def q10_anomalias(events, zones):
    print("\n── Query 10: Deteção de anomalias ──")

    cnt = HashTable(size=4096) 
    dias_por_zona_hora = HashTable(size=2048)

    for ev in events:
        if ev.event_type != "entry":
            continue
        key = f"{ev.zone_id}|{ev.date}|{ev.hour}"
        c   = cnt.get(key)
        cnt.insert(key, (c or 0) + 1)

        key2 = f"{ev.zone_id}|{ev.hour}"
        lst  = dias_por_zona_hora.get(key2)
        if lst is None:
            lst = HashTable(size=16)
            dias_por_zona_hora.insert(key2, lst)
        lst.insert(ev.date, 1)

    stats = HashTable(size=2048)

    acc = HashTable(size=2048)
    for key, c in cnt.items():
        parts   = key.split("|")
        zona, dia, hora = parts[0], parts[1], parts[2]
        key2    = f"{zona}|{hora}"
        lst     = acc.get(key2)
        if lst is None:
            lst = []
            acc.insert(key2, lst)
        lst.append(c)

    for key2, lst in acc.items():
        m = _mean(lst)
        s = _std(lst)
        stats.insert(key2, (m, s, lst))

    anomalias = []
    for key, c in cnt.items():
        parts = key.split("|")
        zona, dia, hora = parts[0], parts[1], parts[2]
        key2  = f"{zona}|{hora}"
        m, s, _ = stats.get(key2)
        if s > 0 and abs(c - m) > 2 * s:
            desvios = (c - m) / s
            nome    = zones.get(zona, {}).get("label", zona)
            anomalias.append((abs(desvios), zona, nome, dia, int(hora), c, round(m, 1), round(s, 1), round(desvios, 2)))

    anomalias, _ = merge_sort(anomalias, key=lambda x: x[0], reverse=True)

    if not anomalias:
        print("  Nenhuma anomalia detectada (limiar: 2 desvios padrão).")
        return

    print(f"\n  {len(anomalias)} anomalias detectadas:")
    rows = [(z, nm, d, f"{h:02d}h", c, m, s, f"{dv:+.2f}σ")
            for _, z, nm, d, h, c, m, s, dv in anomalias[:30]]
    print_table(["Zona", "Nome", "Data", "Hora", "Contagem", "Média", "DP", "Desvio"], rows)


#  QUERY 11 — Query composta com até 4 filtros
def q11_query_composta(events, zones):
    print("\n── Query 11: Query composta (até 4 filtros) ──")
    ts_ini       = ask_datetime("Data/hora início", "2025-03-10 09:00:00")
    ts_fim       = ask_datetime("Data/hora fim",   "2025-03-16 21:00:00")
    zona_filtro  = ask("Zona (ou ENTER para todas)", "")
    gender_filtro= ask("Género M/F (ou ENTER)", "")
    age_filtro   = ask("Faixa etária (ou ENTER)", "")

    filtrados = []
    for ev in events:
        if not (ts_ini <= ev.timestamp <= ts_fim):
            continue
        if zona_filtro and ev.zone_id != zona_filtro:
            continue
        if gender_filtro and ev.gender != gender_filtro:
            continue
        if age_filtro and ev.age != age_filtro:
            continue
        filtrados.append(ev)

    total       = len(filtrados)
    duracoes    = [e.duration for e in filtrados if e.event_type == "linger"]
    media_dur   = int(_mean(duracoes)) if duracoes else 0

    por_hora = HashTable(size=24)
    for ev in filtrados:
        c = por_hora.get(ev.hour)
        por_hora.insert(ev.hour, (c or 0) + 1)

    print(f"\n  Total de eventos: {total}")
    print(f"  Permanência média: {media_dur} s")
    print(f"\n  Distribuição por hora:")
    horas = sorted(por_hora.keys())
    rows  = [(f"{h:02d}h-{h+1:02d}h", por_hora.get(h)) for h in horas]
    print_table(["Faixa Horária", "Eventos"], rows)



#  QUERY 12 — Perfil demográfico por zona
def q12_perfil_demografico(events, idx_zone, zones):
    print("\n── Query 12: Perfil demográfico por zona ──")
    zona_input   = ask("Zona (ou ENTER para todas)", "")
    dia_semana   = ask("Dia da semana 0=seg..6=dom (ou ENTER)", "")
    hora_ini     = ask("Hora início (9-20, ou ENTER)", "")
    hora_fim     = ask("Hora fim (9-20, ou ENTER)", "")

    acc_gender = HashTable(size=4)
    acc_age    = HashTable(size=8)

    for ev in events:
        if ev.event_type != "entry":
            continue
        if zona_input and ev.zone_id != zona_input:
            continue
        if dia_semana and str(ev.weekday) != dia_semana:
            continue
        if hora_ini and ev.hour < int(hora_ini):
            continue
        if hora_fim and ev.hour > int(hora_fim):
            continue

        g = acc_gender.get(ev.gender)
        acc_gender.insert(ev.gender, (g or 0) + 1)

        a = acc_age.get(ev.age)
        acc_age.insert(ev.age, (a or 0) + 1)

    total = sum(v for _, v in acc_gender.items())
    if total == 0:
        print("  Sem dados para os filtros indicados.")
        return

    print(f"\n  Total de visitas: {total}")
    print(f"\n  Por género:")
    rows = [(g, c, f"{100*c//total}%") for g, c in acc_gender.items()]
    print_table(["Género", "Visitas", "%"], rows)

    print(f"\n  Por faixa etária:")
    age_items, _ = merge_sort(list(acc_age.items()), key=lambda x: x[1], reverse=True)
    rows = [(a, c, f"{100*c//total}%") for a, c in age_items]
    print_table(["Faixa etária", "Visitas", "%"], rows)


#  BENCHMARK — comparação dos dois algoritmos de ordenação
def run_benchmark(events):
    print("\n── Benchmark: Bubble Sort vs Merge Sort ──")
    print("  A preparar amostras...")

    samples = [100, 500, 1000, 5000, min(len(events), 20000)]
    keys    = ["event_type", "zone_id", "timestamp"]
    key_fn  = lambda e: e.timestamp

    print_table(
        ["n", "Bubble (ms)", "Cmp Bubble", "Merge (ms)", "Cmp Merge", "Speedup"],
        []
    )
    rows = []
    for n in samples:
        subset = events[:n]
        r      = benchmark_sorts(subset, key=key_fn)
        bms    = round(r["bubble"]["time_s"] * 1000, 2)
        mms    = round(r["merge"]["time_s"]  * 1000, 2)
        speedup= round(bms / mms, 1) if mms > 0 else "∞"
        rows.append((n, bms, r["bubble"]["comparisons"], mms, r["merge"]["comparisons"], speedup))

    print_table(
        ["n", "Bubble (ms)", "Cmp Bubble", "Merge (ms)", "Cmp Merge", "Speedup"],
        rows
    )
    print("  (Speedup = Bubble / Merge em tempo)")