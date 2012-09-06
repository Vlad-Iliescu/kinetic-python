__author__ = 'Vlad'

from util.global_options import write_output
from shape import Shape
from util.type import Type
from math import radians, cos, sin, sqrt, acos, pi
from util.storage import Storage

class Path(Shape):
    def __init__(self, name, **kwargs):
        super(Path, self).__init__(**kwargs)

        self.shape_type = 'Path'

        self._parse_path_config(kwargs)
        self.data_array = Path.parse_path_data(self.attrs.data)

        self._make_constructor()

    def get_data(self):
        """get SVG path data string"""
        return self.attrs.data

    @write_output
    def set_data(self, svg):
        """
        Set SVG path data string. This method also automatically parses the data string into a data array.
        Currently supported SVG data: M, m, L, l, H, h, V, v, Q, q, T, t, C, c, S, s, A, a, Z, z
        """
        self.attrs.data = svg
        self.data_array = Path.parse_path_data(svg)

    @classmethod
    def parse_path_data(cls, data):
        """
        Get parsed data array from the data string. V, v, H, h, and l data are converted to L data
        for the purpose of high performance Path rendering
        """
        if not data:
            return []

        cs = data
        cc = ['m', 'M', 'l', 'L', 'v', 'V', 'h', 'H', 'z', 'Z', 'c', 'C', 'q', 'Q', 't', 'T', 's', 'S', 'a', 'A']
        cs = cs.replace(' ', ',')
        for n in xrange(len(cc)):
            cs = cs.replace(cc[n], '|'+cc[n])

        arr = cs.split('|')
        ca = []
        cpx = 0
        cpy = 0
        for n in xrange(1, len(arr)):
            _str = arr[n]
            c = _str[0]

            _str = _str[1:]

            _str = _str.replace(',-', '-').replace('-', ',-').replace('e,-', ',e-')

            p = _str.split(',')
            if len(p) > 0 and p[0] == '':
                p.pop(0)

            for i in xrange(len(p)):
                try:
                    p[i] = float(p[i])
                except ValueError as e:
                    p[i] = None

            while len(p) > 0:
                if p[0] is None:
                    break

                cmd = None
                points = []
                start_x = cpx
                start_y = cpy
                if c == 'l':
                    cpx += p.pop(0)
                    cpy += p.pop(0)
                    cmd = 'L'
                    points.extend([cpx,cpy])
                elif c == 'L':
                    cpx += p.pop(0)
                    cpy += p.pop(0)
                    points.extend([cpx,cpy])
                elif c == 'm':
                    cpx += p.pop(0)
                    cpy += p.pop(0)
                    cmd = 'M'
                    points.extend([cpx,cpy])
                    c = 'l'
                elif c == 'M':
                    cpx += p.pop(0)
                    cpy += p.pop(0)
                    cmd = 'M'
                    points.extend([cpx,cpy])
                    c = 'L'
                elif c == 'h':
                    cpx += p.pop(0)
                    cmd = 'L'
                    points.extend([cpx,cpy])
                elif c == 'H':
                    cpx += p.pop(0)
                    cmd = 'L'
                    points.extend([cpx,cpy])
                elif c =='v':
                    cpy += p.pop(0)
                    cmd = 'L'
                    points.extend([cpx,cpy])
                elif c == 'V':
                    cpy += p.pop(0)
                    cmd = 'L'
                    points.extend([cpx,cpy])
                elif c =='C':
                    points.extend([p.pop(0), p.pop(0), p.pop(0), p.pop(0)])
                    cpx += p.pop(0)
                    cpy += p.pop(0)
                    points.extend([cpx,cpy])
                elif c == 'c':
                    points.extend([cpx+p.pop(0), cpy+p.pop(0), cpx+p.pop(0), cpy+p.pop(0)])
                    cpx += p.pop(0)
                    cpy += p.pop(0)
                    cmd = 'C'
                    points.extend([cpx,cpy])
                elif c == 'S':
                    ctrl_px = cpx
                    ctrl_py = cpy
                    prev_cmd = ca[len(ca)-1]
                    if prev_cmd.command == 'C':
                        ctrl_px = cpx + (cpx - prev_cmd.points[2])
                        ctrl_py = cpy + (cpy - prev_cmd.points[3])
                    points.extend([ctrl_px, ctrl_py, p.pop(0), p.pop(0)])
                    cpx += p.pop(0)
                    cpy += p.pop(0)
                    cmd = 'C'
                    points.extend([cpx,cpy])
                elif c == 's':
                    ctrl_px = cpx
                    ctrl_py = cpy
                    prev_cmd = ca[len(ca)-1]
                    if prev_cmd.command == 'C':
                        ctrl_px = cpx + (cpx - prev_cmd.points[2])
                        ctrl_py = cpy + (cpy - prev_cmd.points[3])
                    points.append([ctrl_px, ctrl_py, p.pop(0), p.pop(0)])
                    cpx += p.pop(0)
                    cpy += p.pop(0)
                    cmd = 'C'
                    points.extend([cpx, cpy])
                elif c == 'Q':
                    points.extend([p.pop(0), p.pop(0)])
                    cpx += p.pop(0)
                    cpy += p.pop(0)
                    points.extend([cpx, cpy])
                elif c == 'q':
                    points.extend([cpx+p.pop(0), cpy+p.pop(0)])
                    cpx += p.pop(0)
                    cpy += p.pop(0)
                    cmd = 'Q'
                    points.extend([cpx, cpy])
                elif c == 'T':
                    ctrl_px = cpx
                    ctrl_py = cpy
                    prev_cmd = ca[len(ca)-1]
                    if prev_cmd == 'Q':
                        ctrl_px = cpx + (cpx - prev_cmd.points[0])
                        ctrl_py = cpy + (cpy - prev_cmd.points[1])
                    cpx += p.pop(0)
                    cpy += p.pop(0)
                    cmd = 'Q'
                    points.extend([ctrl_px, ctrl_py, cpx, cpy])
                elif c == 't':
                    ctrl_px = cpx
                    ctrl_py = cpy
                    prev_cmd = ca[len(ca)-1]
                    if prev_cmd == 'Q':
                        ctrl_px = cpx + (cpx - prev_cmd.points[0])
                        ctrl_py = cpy + (cpy - prev_cmd.points[1])
                    cpx += p.pop(0)
                    cpy += p.pop(0)
                    cmd = 'Q'
                    points.extend([ctrl_px, ctrl_py, cpx, cpy])
                elif c == 'A':
                    rx = p.pop(0)
                    ry = p.pop(0)
                    psi = p.pop(0)
                    fa = p.pop(0)
                    fs = p.pop(0)
                    x1 = cpx
                    y1 = cpy
                    cpx += p.pop(0)
                    cpy += p.pop(0)
                    cmd = 'A'
                    points = Path.convert_endpoint_to_center_parameterization(x1, y1, cpx, cpy, fa, fs, rx, ry, psi)
                elif c == 'a':
                    rx = p.pop(0)
                    ry = p.pop(0)
                    psi = p.pop(0)
                    fa = p.pop(0)
                    fs = p.pop(0)
                    x1 = cpx
                    y1 = cpy
                    points = Path.convert_endpoint_to_center_parameterization(x1, y1, cpx, cpy, fa, fs, rx, ry, psi)

                ca.append(Storage({
                    'command': cmd or c,
                    'points': points,
                    'start': Storage({
                        'x': start_x,
                        'y': start_y
                    }),
                    'path_length': Path.calc_length(start_x, start_y, cmd or c, points)

                }))
            if c == 'z' or c== 'Z':
                ca.append(Storage({
                    'command': 'z',
                    'points': [],
                    'start': Storage(),
                    'path_length': 0
                }))
        return ca

    @classmethod
    def convert_endpoint_to_center_parameterization(cls, x1, y1, x2, y2, fa, fs, rx, ry, psi_deg):
        psi = radians(psi_deg)
        xp = cos(psi) * (x1 - x2) / 2.0 + sin(psi) * (y1 - y2) / 2.0
        yp = -1 * sin(psi) * (x1 - x2) / 2.0 + cos(psi) * (y1 - y2) / 2.0

        _lambda = (xp * xp) / (rx * rx) + (yp * yp) / (ry * ry)

        if _lambda > 1:
            rx *= sqrt(_lambda)
            ry *= sqrt(_lambda)

        try:
            f = sqrt((((rx * rx) * (ry * ry)) - ((rx * rx) * (yp * yp)) - ((ry * ry) * (xp * xp))) /
                 ((rx * rx) * (yp * yp) + (ry * ry) * (xp * xp)))
        except ValueError as e:
            f = None

        if f is None:
            f = 0

        if fa == fs:
            f *= -1

        cxp = f * rx * yp / ry
        cyp = f * -ry * xp / rx

        cx = (x1 + x2) / 2.0 + cos(psi) * cxp - sin(psi) * cyp
        cy = (y1 + y2) / 2.0 + sin(psi) * cxp + cos(psi) * cyp

        v_mag = lambda v: sqrt(v[0] * v[0] + v[1] * v[1])
        v_ratio = lambda u,v: (u[0] * v[0] + u[1] * v[1]) / (v_mag(u) * v_mag(v))
        v_angle = lambda u,v: ( -1 if u[0] * v[1] < u[1] * v[0] else 1) * acos(v_ratio(u, v))
        theta =  v_angle([1, 0], [(xp - cxp) / rx, (yp - cyp) / ry])
        u = [(xp - cxp) / rx, (yp - cyp) / ry]
        v = [(-1 * xp - cxp) / rx, (-1 * yp - cyp) / ry]
        d_theta = v_angle(u, v)

        if v_ratio(u, v) <= -1:
            d_theta = pi
        if v_ratio(u, v) >= 1:
            d_theta = 0
        if fs == 0 and d_theta > 0:
            d_theta -= 2 * pi
        if fs == 1 and d_theta < 0:
            d_theta += 2 * pi
        return [cx, cy, rx, ry, theta, d_theta, psi, fs]

    @classmethod
    def calc_length(cls, x, y, cmd, points):
        path = Path
        
        if cmd == 'L':
            return  path.get_line_length(x, y, points[0], points[1])
        elif cmd == 'C':
            len = 0.0
            p1 = path.get_point_on_cubic_bazier(0, x, y, points[0], points[1], points[2], points[3], points[4], points[5])
            for i in xrange(1, 101):
                t = i / 100.0
                p2 = path.get_point_on_cubic_bazier(t, x, y, points[0], points[1], points[2], points[3], points[4], points[5])
                len += path.get_line_length(p1.x, p1.y, p2.x, p2.y)
                p1 = p2
            return len
        elif cmd == 'Q':
            len = 0.0
            p1 = path.get_point_on_cubic_bazier(0, x, y, points[0], points[1], points[2], points[3])
            for i in xrange(1, 101):
                t = i / 100.0
                p2 = path.get_point_on_cubic_bazier(t, x, y, points[0], points[1], points[2], points[3])
                len += path.get_line_length(p1.x, p1.y, p2.x, p2.y)
                p1 = p2
            return len
        elif cmd == 'A':
            len = 0.0
            start = points[4]
            d_theta = points[5]
            end = points[4] + d_theta
            inc = pi / 180.0
            if abs(start - end) < inc:
                inc = abs(start - end)
            p1 = path.get_point_on_eliptical_arc(points[0], points[1], points[2], points[3], start, 0)
            if d_theta < 0:
                t = start - inc
                while t > end:
                    p2 = path.get_point_on_eliptical_arc(points[0], points[1], points[2], points[3], t, 0)
                    len += path.get_line_length(p1.x, p1.y, p2.x, p2.y)
                    p1 = p2
                    t -= inc
            else:
                t = start + inc
                while t < end:
                    p2 = path.get_point_on_eliptical_arc(points[0], points[1], points[2], points[3], t, 0)
                    len += path.get_line_length(p1.x, p1.y, p2.x, p2.y)
                    p1 = p2
                    t += inc
            p2 = path.get_point_on_eliptical_arc(points[0], points[1], points[2], points[3], end, 0)
            len += path.get_line_length(p1.x, p1.y, p2.x, p2.y)
            return len
        return 0

    def _parse_path_config(self, kwargs):
        if 'data' in kwargs:
            self.attrs.data = kwargs['data']
        else:
            raise NameError('parameter "data" is required')

    @classmethod
    def get_line_length(cls, x1, y1, x2, y2):
        return sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))

    @classmethod
    def get_point_on_cubic_bazier(cls, pct, p1x, p1y, p2x, p2y, p3x, p3y, p4x, p4y):
        cb1 = lambda t: t*t*t
        cb2 = lambda t: 3 * t * t * (1 - t)
        cb3 = lambda t: 3 * t * (1 - t) * (1 - t)
        cb4 = lambda t:  (1 - t) * (1 - t) * (1 - t)

        x = p4x * cb1(pct) + p3x * cb2(pct) + p2x * cb3(pct) + p1x * cb4(pct)
        y = p4y * cb1(pct) + p3y * cb2(pct) + p2y * cb3(pct) + p1y * cb4(pct)

        return Storage({
            'x': x,
            'y': y
        })

    @classmethod
    def get_point_on_eliptical_arc(cls, cx, cy, rx, ry, theta, psi):
        cos_psi = cos(psi)
        sin_psi = sin(psi)
        pt = {
            'x': rx * cos(theta),
            'y': ry * sin(theta)
        }
        return Storage({
            'x': cx + (pt['x'] * cos_psi - pt['y'] * sin_psi),
            'y': cy + (pt['x'] * sin_psi + pt['y'] * cos_psi)
        })


