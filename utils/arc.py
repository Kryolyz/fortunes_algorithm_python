
class Site:
  def __init__(self, x, y):
    self.x = x
    self.y = y
  
  def __str__(self) -> str:
      return f"Site {self.x} {self.y}"

class Arc:
  def __init__(self, site: Site, height = None):
    self.site: Site = site
    self.height = height if height else 1
    self.left = None
    self.right = None
    self.parent = None