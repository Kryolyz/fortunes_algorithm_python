from math import sqrt


class Site:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"Site {self.x} {self.y}"

    def find_circumcenter(self, B, C):
        # Calculate the midpoints of AB and BC
        D = ((self.x + B.x) / 2, (self.y + B.y) / 2)
        E = ((B.x + C.x) / 2, (B.y + C.y) / 2)

        # Calculate the slopes of AB and BC
        m_AB = (B.y - self.y) / (B.x - self.x) if B.x != self.x else float("inf")
        m_BC = (C.y - B.y) / (C.x - B.x) if C.x != B.x else float("inf")

        # Calculate the slopes of the perpendicular bisectors
        m_AB_perp = -1 / m_AB if m_AB != 0 else float("inf")
        m_BC_perp = -1 / m_BC if m_BC != 0 else float("inf")

        # Calculate the intersection of the perpendicular bisectors
        if m_AB_perp == float("inf"):
            circumcenter_x = D[0]
            circumcenter_y = m_BC_perp * (circumcenter_x - E[0]) + E[1]
        elif m_BC_perp == float("inf"):
            circumcenter_x = E[0]
            circumcenter_y = m_AB_perp * (circumcenter_x - D[0]) + D[1]
        else:
            try:
                circumcenter_x = (m_AB_perp * D[0] - m_BC_perp * E[0] + E[1] - D[1]) / (
                    m_AB_perp - m_BC_perp
                )
                circumcenter_y = m_AB_perp * (circumcenter_x - D[0]) + D[1]
            except:
                return Site(float("inf"), float("inf"))
        circumcradius = sqrt(
            (self.x - circumcenter_x) ** 2 + (self.y - circumcenter_y) ** 2
        )
        return Site(circumcenter_x, circumcenter_y), circumcradius


class Arc:
    def __init__(self, site: Site, height=None):
        self.site: Site = site
        self.height = height if height else 1
        self.left_child = None
        self.right_child = None
        self.left_neighbor = None
        self.right_neighbor = None
        self.right_edge = None
        self.left_edge = None

    def __str__(self) -> str:
        return f"Arc {self.site.x} {self.site.y}"

    def __eq__(self, other):
        if not isinstance(other, Arc):
            return False
        if self.site != other.site:
            return False
        if self.left_neighbor != other.left_neighbor:
            return False
        if self.right_neighbor != other.right_neighbor:
            return False
        if self.left_edge != other.left_edge:
            return False
        if self.right_edge != other.right_edge:
            return False
        return True
