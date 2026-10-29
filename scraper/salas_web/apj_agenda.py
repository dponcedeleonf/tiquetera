"""Teatro Peruano Japonés: la agenda se arma por AJAX (POST a /teatro/agenda-teatro).

1. GET de la página para obtener la cookie de sesión y el token CSRF.
2. POST tipo=calendario por mes -> días con ids de publicaciones.
3. POST tipo=publicaciones con todos los ids del mes -> fichas de cada actividad.
Guarda las respuestas en raw/salas_web/www.apj.org.pe/ajax_*.html (caché). 1 petición/seg.
"""
import json, re, time, pathlib, collections, sys
import requests
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from comun import CACHE, UA

U = "https://www.apj.org.pe/teatro/agenda-teatro"
DIR = CACHE / "www.apj.org.pe"
MESES = [(2026, 9), (2026, 10), (2026, 11), (2026, 12), (2027, 1)]
# Ojo: si se pide un mes sin publicaciones, el servidor devuelve el mes actual.
# Por eso se revisa la lista de meses publicados (publicaciones_meses) del año.


def recolectar():
    DIR.mkdir(parents=True, exist_ok=True)
    s = requests.Session(); s.headers["User-Agent"] = UA
    tok = None
    salida = {}
    for anio, mes in MESES:
        f_cal = DIR / f"ajax_calendario_{anio}{mes:02d}.json"
        f_pub = DIR / f"ajax_publicaciones_{anio}{mes:02d}.html"
        if f_pub.exists() and f_cal.exists():
            salida[(anio, mes)] = (json.loads(f_cal.read_text()), f_pub.read_text())
            continue
        if tok is None:
            h = s.get(U, timeout=40).text; time.sleep(1.1)
            tok = re.search(r"X-CSRF-TOKEN': '([^']+)'", h).group(1)
        hdr = {"X-CSRF-TOKEN": tok, "X-Requested-With": "XMLHttpRequest"}
        cal = s.post(U, headers=hdr, data={"tipo": "calendario", "anio": anio, "mes": mes}, timeout=40).json(); time.sleep(1.1)
        publicados = {int(m) for m in re.findall(r'<option value="(\d+)"', cal.get("publicaciones_meses") or "")}
        if mes not in publicados:
            print(anio, mes, "sin publicaciones (meses publicados:", sorted(publicados), ")")
            continue
        dias = collections.defaultdict(list)
        for dia, pid in re.findall(r"<input type='hidden' class='(\d+)' value='(\d+)'>", cal["result"]):
            dias[int(dia)].append(pid)
        cal["dias"] = dias
        ids = sorted({p for v in dias.values() for p in v})
        pub = ""
        if ids:
            pub = s.post(U, headers=hdr, data={"tipo": "publicaciones", "anio": anio, "mes": mes, "dia": min(dias),
                                               "id_publicaciones[]": ids}, timeout=40).text; time.sleep(1.1)
        f_cal.write_text(json.dumps(cal, ensure_ascii=False)); f_pub.write_text(pub)
        print(anio, mes, "días con actividad:", len(dias), "ids:", len(ids))
        salida[(anio, mes)] = (cal, pub)
    return salida


def fichas():
    """Descarga la página de detalle de cada actividad encontrada."""
    from comun import bajar
    urls = []
    for cal, pub in recolectar().values():
        for u in re.findall(r'href="(https://www\.apj\.org\.pe/teatro/agenda_detalle/[^"]+)"', pub):
            if u not in urls:
                urls.append(u)
    return {u: bajar(u, "apj") for u in urls}


if __name__ == "__main__":
    for u, h in fichas().items():
        print(u, len(h))
