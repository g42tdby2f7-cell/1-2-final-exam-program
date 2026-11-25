# -*- coding: utf-8 -*-
"""SVG 그림 도우미 (축 눈금·작은 눈금 포함)"""

def plot(xr, yr, xt, yt, xlabel='', ylabel='', curves=(), w=300, h=200, minor=(None, None),
         grid=False, marks=(), texts=(), xtl=None, ytl=None, pad=(42, 14, 14, 34), invert_y=False,
         invert_x=False, extra=''):
    L, R, T, B = pad
    x0, x1 = xr; y0, y1 = yr
    def X(x):
        f = (x - x0) / (x1 - x0)
        if invert_x: f = 1 - f
        return L + f * (w - L - R)
    def Y(y):
        f = (y - y0) / (y1 - y0)
        if invert_y: f = 1 - f
        return h - B - f * (h - T - B)
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="Noto Sans CJK KR" font-size="10">']
    # grid
    if grid:
        for xv in xt:
            s.append(f'<line x1="{X(xv):.1f}" y1="{Y(y0):.1f}" x2="{X(xv):.1f}" y2="{Y(y1):.1f}" stroke="#bbb" stroke-width="0.6"/>')
        for yv in yt:
            s.append(f'<line x1="{X(x0):.1f}" y1="{Y(yv):.1f}" x2="{X(x1):.1f}" y2="{Y(yv):.1f}" stroke="#bbb" stroke-width="0.6"/>')
        mx, my = minor
        if mx:
            v = x0
            while v <= x1 + 1e-9:
                s.append(f'<line x1="{X(v):.1f}" y1="{Y(y0):.1f}" x2="{X(v):.1f}" y2="{Y(y1):.1f}" stroke="#e2e2e2" stroke-width="0.4"/>'); v += mx
        if my:
            v = y0
            while v <= y1 + 1e-9:
                s.append(f'<line x1="{X(x0):.1f}" y1="{Y(v):.1f}" x2="{X(x1):.1f}" y2="{Y(v):.1f}" stroke="#e2e2e2" stroke-width="0.4"/>'); v += my
    # axes box (left/bottom)
    s.append(f'<line x1="{X(x0):.1f}" y1="{Y(y0) if not invert_y else Y(y0):.1f}" x2="{X(x1):.1f}" y2="{Y(y0):.1f}" stroke="#000" stroke-width="1"/>')
    s.append(f'<line x1="{X(x0):.1f}" y1="{Y(y0):.1f}" x2="{X(x0):.1f}" y2="{Y(y1):.1f}" stroke="#000" stroke-width="1"/>')
    # minor ticks
    mx, my = minor
    if mx:
        v = x0
        while v <= x1 + 1e-9:
            s.append(f'<line x1="{X(v):.1f}" y1="{Y(y0):.1f}" x2="{X(v):.1f}" y2="{Y(y0)-2.5:.1f}" stroke="#000" stroke-width="0.6"/>'); v += mx
    if my:
        v = y0
        while v <= y1 + 1e-9:
            s.append(f'<line x1="{X(x0):.1f}" y1="{Y(v):.1f}" x2="{X(x0)+2.5:.1f}" y2="{Y(v):.1f}" stroke="#000" stroke-width="0.6"/>'); v += my
    for i, xv in enumerate(xt):
        lab = xtl[i] if xtl else (('%g' % xv))
        s.append(f'<line x1="{X(xv):.1f}" y1="{Y(y0):.1f}" x2="{X(xv):.1f}" y2="{Y(y0)-5:.1f}" stroke="#000" stroke-width="1"/>')
        s.append(f'<text x="{X(xv):.1f}" y="{Y(y0)+12:.1f}" text-anchor="middle">{lab}</text>')
    for i, yv in enumerate(yt):
        lab = ytl[i] if ytl else (('%g' % yv))
        s.append(f'<line x1="{X(x0):.1f}" y1="{Y(yv):.1f}" x2="{X(x0)+5:.1f}" y2="{Y(yv):.1f}" stroke="#000" stroke-width="1"/>')
        s.append(f'<text x="{X(x0)-4:.1f}" y="{Y(yv)+3.5:.1f}" text-anchor="end">{lab}</text>')
    s.append(f'<text x="{(X(x0)+X(x1))/2:.1f}" y="{h-4}" text-anchor="middle">{xlabel}</text>')
    s.append(f'<text x="10" y="{(Y(y0)+Y(y1))/2:.1f}" text-anchor="middle" transform="rotate(-90 10 {(Y(y0)+Y(y1))/2:.1f})">{ylabel}</text>')
    for c in curves:
        pts, style = c[0], (c[1] if len(c) > 1 else '')
        d = ' '.join(f'{X(px):.1f},{Y(py):.1f}' for px, py in pts)
        st = style or 'stroke="#000" stroke-width="1.6" fill="none"'
        s.append(f'<polyline points="{d}" {st}/>')
    for (mxv, myv, r) in marks:
        s.append(f'<circle cx="{X(mxv):.1f}" cy="{Y(myv):.1f}" r="{r}" fill="#000"/>')
    for (tx, ty, txt, *opt) in texts:
        anchor = opt[0] if opt else 'start'
        s.append(f'<text x="{X(tx):.1f}" y="{Y(ty):.1f}" text-anchor="{anchor}">{txt}</text>')
    if extra:
        s.append(extra(X, Y) if callable(extra) else extra)
    s.append('</svg>')
    return ''.join(s)

def fn(f, a, b, n=120):
    return [(a + (b - a) * i / n, f(a + (b - a) * i / n)) for i in range(n + 1)]
