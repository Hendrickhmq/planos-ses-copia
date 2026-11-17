"""Baixa da pesquisa pública do SEI-GDF os documentos do ciclo do plano de trabalho da APAE-DF.

Processo SEI 00060-00283642/2026-68 (Convênio 031636/2026). Coleta em 07/10/2026.
Os links abaixo são os da lista de protocolos da pesquisa pública e funcionam sem sessão.
Documentos nativos do SEI vêm em HTML e são salvos também como texto (.md); anexos vêm em PDF.
"""
import html
import re
import subprocess
from pathlib import Path

BASE = "https://sei.df.gov.br/sei/modulos/pesquisa/md_pesq_documento_consulta_externa.php?"
AQUI = Path(__file__).parent

DOCS = [
    # sei, data, tipo, token
    ("205222334", "2026-06-09", "oficio_11_2026_orc_parlamentar", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDeYWL7u-6pgCZuKlFw1jay6ieCScRnrtzicjl2izSgWJhYsiOeUCBheDpX5_XhJvsKP8ZsxSErESR4OLOZJRnZwl"),
    ("205222407", "2026-06-09", "oficio_200_2026_arins", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDeZsClLlHIIDSZeA4kYrn2XUDlru5zPkLWds0aF3cUhhpUC3I53xytqRHu_3fphVlNXEdRudSCZ33lqYzPyZKzLg"),
    ("205222734", "2026-06-12", "formulario_pt_simplificado_modelo_parceria", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDeZkkmKTnBfShHjlLveyOq98wzOxp2eYk6lqMMvjLb4XgyX02JumbBGJh7d0L7-rgOkj68y3QWN7whbEuJr_YZSb"),
    ("205905136", "2026-06-16", "email_arins_envio_oficio", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDeYJ4UboaVoR25Lu42dZRY6LbbRD10F7J7eVku7otcLeUUuw50psSh3jyvsHII6mwafbfQh0Pb5KN69z-3VuzM2Z"),
    ("206685837", "2026-06-24", "v1_pre_plano_apae", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDebHbgDWrw1Px5v-vxj87Kt6Tlwzd0g5_HNJMXKk0mblDg0LdKOszjVOW65QA3VnzDQ0BSBWZ60oBAxjD7Ve5AFM"),
    ("206708294", "2026-06-24", "v1_plano_integridade_e_risco", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDebw9_5gettQ-qaBS-K44teUviPvmtVUty6yO91N152NrDJDpjWyE_wGMNPhcKvWUX2SxN5xZtp5xL1Rr2fByV2t"),
    ("206708876", "2026-06-24", "v1_planilha", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDeafhNK35lENKsix7djPLds55p2InXy3gaPBqqI7lUYzx6qkZwA0wrsID1l3GRAPzbKxuyK-PL26d56MJNQ1gT5h"),
    ("206713653", "2026-06-24", "v1_email_envio_apae", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDeZu-Wm90cYNzVkVaOD2E8ROgPw8zwbcqiv1s1CwVoQ9aclFRQl7CjRMYqZAUmgTCXLXA_CZ6OLjuV1wlUI42yVX"),
    ("206711954", "2026-06-25", "despacho_arins_para_suconv", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDeZdcVcodrthmI_34UEl_rBk74UkDNLH8oB42QNXllJdIysZmYfGX5rPbW9zsT2PrkEr6R7XB2m8IvOMyInhelts"),
    ("206883297", "2026-06-26", "despacho_suconv", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDebzuGVVwCai0OzAeWdjmJirGPYQQwmDmJGowtoN1dF0QNvgfGbAIICjgtgYEh2oXhveBfCCCMrVEe0ohD9XkzbQ"),
    ("206905543", "2026-06-26", "despacho_dipcp_instrumento_convenio", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDeaIEZFJXIuUEvrd-P9eollVeUKWfIAYk_AyeE0lls4ujwoF3HjVxTp5hGX6i0uxLPUYM_8yN-CReSHLyKYlIqgl"),
    ("206958527", "2026-06-30", "v1_parecer_tecnico_04_gcd_rcpd", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDeb9k1g1LdO6aKEib4LvHVEVurYe9ZHX0aGfZlPdBW0Ef3v0QxiB09T_jsP3U8NH47hHKAxtWi7yVL6jtsc1jUwd"),
    ("207083027", "2026-06-30", "v1_despacho_gcd_rcpd", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDeal7_9xeUE4SduiOkcsYfNUq_vZinor9Pi2tDl5HZgCFwH-MWJ2hK9EUhbYSU7OtRwpFpX2PmugDjXf5eusDkjg"),
    ("207101650", "2026-06-30", "v1_despacho_aras", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDeYxaQUq5e2myAYl_YuIo6Y__t_Bz0L4GEokwHvXP71fjmHytzBuyezJF4wzNe21SSwAsrFTqRmFdcUx9s8hhBgZ"),
    ("207149798", "2026-07-01", "v1_despacho_sais", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDeZSWEQ7cwhost5FlMRDTTGIsRigIe8Q-Aow_EFyaAFj5nERzcjfb9xqIZj6gDUWpBsKyuqjqjjNpmghvPe1M_Kk"),
    ("207176407", "2026-07-01", "v1_relatorio_preliminar_suconv", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDeZh-Eh0BHcTHdQtozjxd4H5e2_aK9WMZNyIApNGFF9xKl8ra4-B8iaK3eTYlcL6_bHzjMj2y9DaP4lz08If4wrG"),
    ("207261161", "2026-07-01", "v1_email_suconv_diligencia", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDeYcfrHarG0SBf68EQy9018GQ0qIOD3b_gDJGuS4dANoVKs9OapO-tXHjw1JQtQzlcv0hrPixq4VRkql9uM-1Dcd"),
    ("208318109", "2026-07-13", "v2_planilha", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDebvseSMAQzA-Op-92mlMwJZGV6WbJvMvvnH1O-Wkt_XLJFjzOD8tvCXbpJuCfIvSA0oj6o0GzRQ21iLKkXvcSnu"),
    ("208318221", "2026-07-13", "v2_plano", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDeYisOw0TCDiQ9AeYrECrxevjvRuYzzVPkSBVifS3gij3I89zDCdPStg633YWhN8SSxLSaiBE_zSHn8AuU26zeSy"),
    ("208318280", "2026-07-13", "v2_email_tratativas_1", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDeZhpHCtUHxdEIN2EHwQt2ZW-b6rzGArQe3FwlS9vZoqZcA6k44USo6J6GTMaTBSinWfYswN34WEI85v1WAzYoMb"),
    ("208318332", "2026-07-13", "v2_email_tratativas_2", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDeaDhhj55TwSHQl2qtLigulL014YRsjhHxGzzcPPFCUxKtD37WI5-yARWu85W1fQXEKBq_r1yNThF-ybhV_Ku6s1"),
    ("208674986", "2026-07-17", "v2_parecer_tecnico_06_gcd_rcpd", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDebZAoEKygGcAGt6cZ4J0xPYhwMjxelMs0uDNF55hxWK19iMoAVqHCZCJwFZx9yW7QT4bZBuVX0FWuogdYgQow23"),
    ("208869604", "2026-07-20", "v2_quadro_conformidade", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDeZzl8BxIy9Ve8lFUaasLdZxKdKi_OHTN-J8QC7tb5VWYNilQmQdojKABziPjgZaLfpd5DyjSgXxudBMRXUQNvYk"),
    ("208885009", "2026-07-20", "v2_relatorio_preliminar_suconv", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDebcH0KuxaVM4C-VNpr-398llrXEpLNvdkQMlzE-2QCVy-dbudmewasx34gU8o7FzbrPDL2hpxrur6zg81C-y7Me"),
    ("208893740", "2026-07-20", "v2_email_suconv_diligencia", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDebUxDIMchHSHeIQFNP-5yNCFP3Y4H-E8MshcuhlC0n96DPZHGGlA3P1imAUxGSbCtqCBbWVHwnVtsYqYxhOPiJY"),
    ("209130291", "2026-07-22", "v3_plano", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDeYTsv4oygG3mlkpNsH8LW3neKya5aOHfaF_-LvMn6XoR6hh6PjwrSb0ZepTjhKl9Itnyri3BMvHTr8o9LCNr4ey"),
    ("209130364", "2026-07-22", "v3_planilha", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDeZvNdaBlmFr7z3o0l_Y-rOr0ndiqLys4_27Tcn1f5A5FFDmXk9x1Ry5g5qoM9W_J6pbpp751X1I0Fs6-IhU3IJQ"),
    ("209130630", "2026-07-22", "v3_email_tratativas", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDebtxmCk2OV7bZmNXe9CptG8svuMGbR4r_tdhqJ10wABX84UBJduHrd4aQvwDYotdtjT8Zh6LQp2V6T5JEmIqCpC"),
    ("209425519", "2026-07-24", "v3_parecer_tecnico_07_gcd_rcpd", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDeZU8tEKMcQYIjWJRG8Z5NEd3bzNaWdHvZK-J6GM2ggJJJdcA7OUpYl4uZoq6M23jWuJoBdzIH1h9TaYUJ_LmCgP"),
    ("209501292", "2026-07-27", "v3_quadro_consolidado_conformidades", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDeYKF-t35jDFVSshLr9rFEySVuFJCWFuIZjn3EPENYeG5AIjcwU_r_-TSY3upggvG8gJ48XpFQRm53adRS3p_C-M"),
    ("209499602", "2026-07-28", "v3_relatorio_preliminar_suconv", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDea8wX0CpZ2TO7yDpwnlmNV2OlMr4Q7Vu8nypkevxQQZ1O-oml1oHPX1_F1IpZEBPHmodxKG2YrIKnDNEUf_e0FJ"),
    ("209616770", "2026-07-28", "v3_email_suconv_diligencia", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDeYRARcI2VdLLtNEQT89HEMDbb9TukwtqoxlQVqWTjm9MnA3t_QUmT0JiyuQAoVc2DTeomly3BYxBLm8n8B-lPYi"),
    ("209758895", "2026-07-29", "v4_planilha", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDeYn-lEvseOMKI4WFiZMAg9uNhsRjG3Cz8XDRcaqZgm-xrK_Rtp211n1nz2qyxXcrG7-WYquaSmDyiU6zI3O1Fe3"),
    ("209865653", "2026-07-30", "v4_email_substituicao_plano", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDeYYyfmuf3i0PYSlxRidT0oN3s1LMjPxiLbFQ8Ejl50nWvJQE5n1987kBAIBJPgcCF-n_VrwxU8XZEG-EegdbVxT"),
    ("209874613", "2026-07-30", "v4_plano", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDeaSjUt3sqRLS83EC6X830JMEf1wel9ASKaRxuGkqlO1NNv_-rSKFvBuiZgPx96Hd3E42lUPkJBoc14RcnT6lT1D"),
    ("209867551", "2026-07-30", "v4_quadro_consolidado_conformidades", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDea19tj5mBYcnihgVaq1Qcs8Eu7NY5sGOmWawnhSWLdY0EgQ-QTPvKG0r-TN0b4BlzJisLP4YfjfeAV-A5IG9d-i"),
    ("209872515", "2026-07-30", "v4_parecer_tecnico_10_gcd_rcpd", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDebl02u_jBaiHQ4H1AN7z9YLDt2JHzT9IGBTzW3JHhQ-6Fjyqo1rdx3y1345YaVzlClOihpr-_pz6vN7YAHxRkZE"),
    ("209944605", "2026-07-30", "v4_parecer_tecnico_68_sais", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDeZN2L2eLEBjdnP7e3OJSt3LseR6fUDsSNeahJs9N7Mnxb99JoxQ3YYoB0UziP9E-bwVO6dJWqKUnauLCKDcVHGG"),
    ("209927509", "2026-07-31", "v4_parecer_tecnico_04_gpcp_custos", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDeYnk1EPKekQcLKCU_ru-NoHFt0380zLP_mm_PUiodGZdfT_kzRMOh2XtRPpM8ggVtAKcCxJWy5O0-Eu7yk1SeUr"),
    ("209985044", "2026-07-31", "v4_relatorio_13_suconv", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDeZR3eE8Q6XlR44EhAc0GKtgqnS90NpQ4hKOiU5oByqrdYaSHrtL20Nx-uHuLorG4X780aP9AeW4Xi_fkNojKpBs"),
    ("210032346", "2026-07-31", "termo_aprovacao_66_seas", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDebfXZdOZ2vVPfhnKpSM69iry20DxKPM7q2epUKYBK_GFTWKPbMO33iBqunJHtGtTaD15EkCHAjF32uTAQvQFTAR"),
    ("210043230", "2026-07-31", "termo_aprovacao_73_segea", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDebV8wEt3BO1A2ZoBl4QwP5zc4kpdXGuQkmjL43wIKanzgJyJccplW0C6mls8e8wvBmNSEQv3Tppbjj_MAlmdCb3"),
    ("210162622", "2026-08-04", "memoria_reuniao_suconv", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDebbDvY6HsN1SBh7XwSF2maMVd6ID_WIqVDRwvv1iC33pRwnx5__8woo0e86zdjtu63HHZF0DqlWtCOgao1MYsO2"),
    ("210728813", "2026-08-07", "nota_tecnica_07_seccic", "m7alazCD3Dj0ndcMCQbg5Vif3a_YbaPU0UGeHw4hDebgxOLbezq4TTNp-zvN0YPy3w27idZlTEhdcjmnD79CgnnjOOHzQspYFE48jUOSZi2-tOenZgEvFkW13U1X_EGl"),
]


def texto_sei(bruto: bytes) -> str:
    h = bruto.decode("iso-8859-1")
    h = re.sub(r"(?is)<(script|style).*?</\1>", "", h)
    h = re.sub(r"(?i)<br\s*/?>|</p>|</tr>|</h\d>|</div>|</li>", "\n", h)
    h = re.sub(r"(?i)</td>", " | ", h)
    t = html.unescape(re.sub(r"<[^>]+>", " ", h))
    t = re.sub(r"[ \t ]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n\n", t)
    return t.strip()


def main():
    linhas = ["sei,data,arquivo,content_type,bytes"]
    for sei, data, nome, token in DOCS:
        cab = AQUI / f".cab_{sei}"
        tmp = AQUI / f".tmp_{sei}"
        subprocess.run(["curl", "-sL", "-A", "Mozilla/5.0", "-D", str(cab), "-o", str(tmp), BASE + token], check=True)
        ct = re.search(r"(?im)^content-type:\s*([^;\r\n]+)", cab.read_text(errors="ignore"))
        ct = ct.group(1).strip() if ct else ""
        cab.unlink()
        base = f"{data}_{sei}_{nome}"
        if "html" in ct:
            destino = AQUI / f"{base}.html"
            tmp.rename(destino)
            (AQUI / f"{base}.md").write_text(texto_sei(destino.read_bytes()) + "\n", encoding="utf-8")
        else:
            destino = AQUI / f"{base}.pdf"
            tmp.rename(destino)
        linhas.append(f"{sei},{data},{destino.name},{ct},{destino.stat().st_size}")
        print(linhas[-1])
    (AQUI / "indice.csv").write_text("\n".join(linhas) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
