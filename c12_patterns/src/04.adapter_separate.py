from typing import Iterator


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def draw(self) -> None:
        print(".", end="")

    def __repr__(self) -> str:
        return f"Point({self.x, self.y})"


class Line:
    def __init__(self, start: Point, end: Point) -> None:
        self.start = start
        self.end = end


class LineToPointAdapter:
    def __init__(self, line: Line):
        self.points = self._line_points(line.start, line.end)

    def _line_points(self, p0: Point, p1: Point) -> list[Point]:
        points = []
        x0, y0 = p0.x, p0.y
        x1, y1 = p1.x, p1.y

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            points.append(Point(x0, y0))
            if x0 == x1 and y0 == y1:
                return points
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def __iter__(self) -> Iterator[Point]:
        return iter(self.points)


if __name__ == "__main__":
    line = Line(Point(0, 0), Point(10, 5))
    for p in LineToPointAdapter(line):
        p.draw()
