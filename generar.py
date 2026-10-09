# Genera las imágenes de Compra Ofertas con el diseño aprobado.
# Lo corre GitHub Actions cada vez que cambia ofertas.json.
import json, os, html, asyncio
from playwright.async_api import async_playwright

OUT = "img"
os.makedirs(OUT, exist_ok=True)
d = json.load(open("ofertas.json", encoding="utf-8"))
ofertas = [o for o in d.get("ofertas", []) if o.get("url")]
e = html.escape
fmt = lambda n: "$" + f"{float(n):,.0f}"
pct = lambda o: round((1 - float(o["ahora"]) / float(o["antes"])) * 100) if o.get("antes") else 0

BASE = """*{margin:0;box-sizing:border-box}body{font-family:'Inter',sans-serif;color:#0f1b2d}
.navy{background:#0f1b2d;color:#fff}.coral{color:#ff5a36}
.brand{display:flex;align-items:center;gap:12px;font-weight:800;letter-spacing:.05em;font-size:28px}.brand i{width:20px;height:20px;border-radius:6px;background:#ff5a36;display:block}
.num{background:#ff5a36;color:#0f1b2d;font-weight:900;border-radius:999px;padding:10px 22px;font-size:34px}"""

def foto(o):
    return e(o.get("foto") or "")

def lamina(o):
    p = pct(o)
    return f"""<style>{BASE}
body{{width:1080px;height:1350px;background:#f6f4f0;display:flex;flex-direction:column}}
.top{{height:120px;display:flex;justify-content:space-between;align-items:center;padding:0 56px}}
.ph{{flex:1;display:flex;align-items:center;justify-content:center;position:relative;padding:30px 90px}}
.ph img{{max-height:840px;max-width:100%;object-fit:contain;border-radius:18px;background:#fff}}
.off{{position:absolute;right:70px;top:30px;width:200px;height:200px;border-radius:50%;background:#ff5a36;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;font-weight:900;transform:rotate(-8deg)}}
.off b{{font-size:68px;line-height:1}}.off span{{font-size:26px;letter-spacing:.06em}}
.bot{{height:260px;padding:34px 56px;display:flex;justify-content:space-between;align-items:center}}
.now{{font-size:128px;font-weight:900;letter-spacing:-.03em;line-height:1}}.was{{font-size:40px;color:#9fb0c7;text-decoration:line-through;font-weight:700}}
.cta{{text-align:right;font-size:34px;font-weight:700;line-height:1.3}}</style>
<div class="top navy"><div class="brand"><i></i>COMPRA OFERTAS</div><div class="num">#{o['num']}</div></div>
<div class="ph"><img src="{foto(o)}">{'<div class="off"><b>-'+str(p)+'%</b><span>MENOS</span></div>' if p>0 else ''}</div>
<div class="bot navy"><div><div class="was">{'antes '+fmt(o['antes']) if o.get('antes') else ''}</div><div class="now">{fmt(o['ahora'])}</div></div>
<div class="cta">Es la <span class="coral">#{o['num']}</span><br>link en mi perfil 👆</div></div>"""

def historia(o):
    p = pct(o)
    return f"""<style>{BASE}
body{{width:1080px;height:1920px;background:#0f1b2d;color:#fff;display:flex;flex-direction:column;align-items:center;padding:120px 70px 0}}
.k{{font-size:44px;font-weight:800;color:#ffb199;letter-spacing:.04em;margin-top:10px}}
h1{{font-size:88px;font-weight:900;text-align:center;line-height:1.04;margin-top:20px}}
.ph{{margin-top:50px;background:#f6f4f0;border-radius:36px;padding:30px;width:760px;height:860px;display:flex;align-items:center;justify-content:center;position:relative}}
.ph img{{max-width:100%;max-height:100%;object-fit:contain}}
.off{{position:absolute;right:-30px;top:-30px;width:190px;height:190px;border-radius:50%;background:#ff5a36;display:flex;align-items:center;justify-content:center;font-size:62px;font-weight:900;transform:rotate(-8deg)}}
.pr{{margin-top:50px;display:flex;gap:26px;align-items:baseline}}.pr b{{font-size:120px;font-weight:900}}.pr s{{font-size:48px;color:#9fb0c7}}</style>
<div class="brand"><i></i>COMPRA OFERTAS</div><div class="k">OFERTA #{o['num']}</div><h1>{e(o.get('titulo',''))}</h1>
<div class="ph"><img src="{foto(o)}">{'<div class="off">-'+str(p)+'%</div>' if p>0 else ''}</div>
<div class="pr"><b>{fmt(o['ahora'])}</b>{'<s>'+fmt(o['antes'])+'</s>' if o.get('antes') else ''}</div>"""

def portada(lst):
    cel = "".join(f"""<div class="c"><img src="{foto(o)}"><span class="n">#{o['num']}</span><span class="p">{fmt(o['ahora'])}</span>{'<span class="d">-'+str(pct(o))+'%</span>' if pct(o)>0 else ''}</div>""" for o in lst)
    return f"""<style>{BASE}
body{{width:1080px;height:1350px;background:#0f1b2d;color:#fff;padding:60px 56px;display:flex;flex-direction:column;gap:30px}}
h1{{font-size:96px;font-weight:900;line-height:1;letter-spacing:-.02em}}
.g{{display:grid;grid-template-columns:1fr 1fr;grid-template-rows:repeat(2,minmax(0,1fr));gap:20px;flex:1;min-height:0}}
.c{{background:#f6f4f0;border-radius:24px;position:relative;display:flex;align-items:center;justify-content:center;padding:26px 26px 70px;overflow:hidden;min-height:0}}
.c img{{max-width:100%;max-height:100%;object-fit:contain}}
.n{{position:absolute;top:14px;left:14px;background:#0f1b2d;color:#fff;font-weight:900;font-size:30px;padding:6px 14px;border-radius:999px}}
.d{{position:absolute;top:14px;right:14px;background:#ff5a36;color:#fff;font-weight:900;font-size:30px;padding:6px 14px;border-radius:999px}}
.p{{position:absolute;bottom:14px;left:14px;background:#0f1b2d;color:#fff;font-weight:900;font-size:40px;padding:6px 16px;border-radius:14px}}</style>
<div class="brand"><i></i>COMPRA OFERTAS</div><h1>Las {len(lst)} de <span class="coral">hoy</span></h1><div class="g">{cel}</div>"""

def cierre(lst):
    nums = " · ".join("#" + str(o["num"]) for o in lst)
    return f"""<style>{BASE}
body{{width:1080px;height:1350px;background:#0f1b2d;color:#fff;padding:90px 70px;display:flex;flex-direction:column;justify-content:center;gap:40px}}
h1{{font-size:110px;font-weight:900;line-height:1.02}}p{{font-size:46px;font-weight:600;color:#c4cfdf;line-height:1.3}}
.ns{{font-size:64px;font-weight:900;color:#ff5a36}}</style>
<div class="brand"><i></i>COMPRA OFERTAS</div><h1>Todas están en el link de mi perfil 👆</h1><div class="ns">{nums}</div>
<p>Entra, escribe el número y listo.<br>Síguenos para las de mañana.</p>"""

async def shot(b, html_, path, w, h):
    pg = await b.new_page(viewport={"width": w, "height": h})
    await pg.set_content("<html><head><meta charset='utf-8'></head><body>" + html_ + "</body></html>")
    try:
        await pg.wait_for_load_state("networkidle", timeout=20000)
    except Exception:
        pass
    await pg.screenshot(path=path, type="jpeg", quality=88)
    await pg.close()

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for o in ofertas:
            if not o.get("foto"):
                continue
            n = o["num"]
            if not os.path.exists(f"{OUT}/oferta{n}-1.jpg"):
                await shot(b, lamina(o), f"{OUT}/oferta{n}-1.jpg", 1080, 1350)
                await shot(b, historia(o), f"{OUT}/oferta{n}-historia.jpg", 1080, 1920)
        hoy = [o for o in ofertas if o.get("foto")][:4]
        if hoy:
            await shot(b, portada(hoy), f"{OUT}/hoy-portada.jpg", 1080, 1350)
            await shot(b, cierre(hoy), f"{OUT}/hoy-cierre.jpg", 1080, 1350)
            json.dump({"fecha": d.get("actualizado"), "nums": [o["num"] for o in hoy]}, open(f"{OUT}/hoy.json", "w"))
        await b.close()

asyncio.run(main())
