from queries.aggregation import (
    q1_ocupacao_por_zona,
    q2_media_permanencia,
    q3_picos_ocupacao,
    q4_comparacao_dias,
    q5_topk_zonas,
    q6_topk_blocos,
    q7_topk_permanencia,
    q8_fluxo_entre_zonas,
    q9_sequencias_zonas,
    q10_anomalias,
    q11_query_composta,
    q12_perfil_demografico,
    run_benchmark,
)
from utils.helpers import measure_time
MENU = """
╔══════════════════════════════════════════════════════╗
║         MOTOR DE ANALYTICS — DADOS DE RETALHO        ║
╠══════════════════════════════════════════════════════╣
║  1 · Ocupação por zona                               ║
║  2 · Média de permanência                            ║
║  3 · Picos de ocupação                               ║
║  4 · Comparação entre dias                           ║
║  5 · Top-K zonas                                     ║
║  6 · Top-K blocos                                    ║
║  7 · Top-K permanência                               ║
║  8 · Fluxo entre zonas                               ║
║  9 · Sequências de zonas                             ║
║ 10 · Anomalias                                       ║
║ 11 · Query composta                                  ║
║ 12 · Perfil demográfico                              ║
║  B · Benchmark (Bubble vs Merge)                     ║
║  0 · Sair                                            ║
╚══════════════════════════════════════════════════════╝
"""


def start_menu(events, idx_zone, idx_date, idx_type, idx_zone_date, zones, zone_types):
    while True:
        print(MENU)
        opcao = input("  Escolha: ").strip().lower()
        dispatch = {
            "1":  lambda: q1_ocupacao_por_zona(events, idx_zone, idx_date, zones, zone_types),
            "2":  lambda: q2_media_permanencia(events, idx_zone, zones),
            "3":  lambda: q3_picos_ocupacao(events, idx_date),
            "4":  lambda: q4_comparacao_dias(events, idx_date, zones),
            "5":  lambda: q5_topk_zonas(events, zones),
            "6":  lambda: q6_topk_blocos(events, zones),
            "7":  lambda: q7_topk_permanencia(events, zones),
            "8":  lambda: q8_fluxo_entre_zonas(events, zones),
            "9":  lambda: q9_sequencias_zonas(events),
            "10": lambda: q10_anomalias(events, zones),
            "11": lambda: q11_query_composta(events, zones),
            "12": lambda: q12_perfil_demografico(events, idx_zone, zones),
            "b":  lambda: run_benchmark(events),
            "0":  None,
        }
        if opcao == "0":
            print("\n  Encerrando. Até logo!\n")
            break
        elif opcao in dispatch:
            try:
                measure_time(dispatch[opcao])
            except KeyboardInterrupt:
                print("\n  (interrompido)")
            except Exception as exc:
                print(f"\n  ⚠  Erro: {exc}")
        else:
            print("  ⚠  Opção inválida.")