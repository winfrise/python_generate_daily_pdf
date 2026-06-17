# relative_overlay.py

from reportlab.platypus import Flowable
from reportlab.lib.utils import ImageReader

class RelativeOverlay(Flowable):
    """
    一个通用的相对定位覆盖层组件。
    允许将一个覆盖元素（如图片、印章、水印等）相对于目标元素（如文本、表格）进行绝对偏移定位。
    无论目标元素在流式排版中被分配到页面的哪个位置，覆盖元素都会与其保持相对绑定。
    """
    def __init__(self, target_element, overlay_element, offset_x=0, offset_y=0):
        """
        初始化相对定位组件。
        
        :param target_element: 基准元素（Flowable 对象，如 Paragraph, Table 等）
        :param overlay_element: 覆盖元素（Flowable 对象，如 Image 等）
        :param offset_x: 覆盖元素相对于基准元素左下角的 X 轴偏移量（向右为正）
        :param offset_y: 覆盖元素相对于基准元素左下角的 Y 轴偏移量（向上为正）
        """
        Flowable.__init__(self)
        self.target_element = target_element
        self.overlay_element = overlay_element
        self.offset_x = offset_x
        self.offset_y = offset_y
        
    def wrap(self, availWidth, availHeight):
        # 容器的整体尺寸由基准元素（target_element）决定
        # 这样在流式排版中，它占据的空间和基准元素完全一样
        return self.target_element.wrap(availWidth, availHeight)

    def draw(self):
        # 1. 在当前位置绘制基准元素
        self.target_element.drawOn(self.canv, 0, 0)
        
        # 2. 保存画布状态（防止覆盖元素的绘制影响到基准元素或后续内容）
        self.canv.saveState()
        
        # 3. 绘制覆盖元素，加上相对偏移量
        self.overlay_element.drawOn(self.canv, self.offset_x, self.offset_y)
        
        # 4. 恢复画布状态
        self.canv.restoreState()