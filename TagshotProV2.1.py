# image_renamer_enhanced.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from PIL import Image, ImageFilter, ImageTk, ImageDraw
import shutil

class ModernImageRenamerApp:
    def __init__(self):
        # 设置外观模式和统一颜色主题
        ctk.set_appearance_mode("Dark")
        
        # 自定义统一颜色方案
        self.colors = {
            "primary": "#2b2b2b",        # 主背景色
            "secondary": "#3c3c3c",      # 次要背景色
            "sidebar": "#252525",        # 侧边栏背景色
            "accent": "#1f6aa5",         # 主色调
            "accent_hover": "#144870",   # 主色调悬停
            "success": "#27AE60",        # 成功色
            "success_hover": "#219955",  # 成功色悬停
            "danger": "#E74C3C",         # 危险/警告色
            "danger_hover": "#C0392B",   # 危险色悬停
            "text_primary": "#ffffff",   # 主文字色
            "text_secondary": "#cccccc"  # 次要文字色
        }
        
        # 创建主窗口
        self.root = ctk.CTk()
        self.root.title("图片标签重命名工具")
        self.root.geometry("1400x900")
        
        # 设置窗口背景色
        self.root.configure(fg_color=self.colors["primary"])
        
        # 存储图片信息
        self.images = []
        self.current_index = 0
        self.common_prefix = ""  # 统一前缀
        
        # 压缩设置
        self.max_size = 1800  # 最大尺寸
        self.compression_quality = 85  # 默认压缩质量
        
        # 预设标签分类
        self.categories = {
            "外部视角": ["28_车顶", "2_正前方", "6_正后方", "29_右侧面", "4_左侧面", "3_右前45度", "7_右后45度", "1_左前45度", "5_左后45度"],
            "内部视角": ["17_驾驶位", "11_方向盘", "10_中控台", "12_组合仪表", "14_音响及空调面板", "19_车内顶棚", "18_后排", "16_驾驶员座椅", "26_右侧前座椅", "27_右侧后座椅", "20_后备箱"],
            "细节特写": ["15_变速杆", "21_发动机舱", "13_里程数特写", "9_钥匙", "8_右后大灯", "25_左前大灯", "24_左前轮胎轮毂", "22_右侧底大边", "23_左侧底大边", "30_车辆铭牌"]
        }
        
        # 存储标签按钮状态和已使用的标签
        self.tag_buttons = {}
        self.used_tags = set()  # 记录所有已使用的标签
        
        # 创建界面
        self.create_widgets()
        
    def create_widgets(self):
        # 创建主框架
        self.main_frame = ctk.CTkFrame(
            self.root, 
            fg_color=self.colors["primary"],
            corner_radius=0
        )
        self.main_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # 创建三栏布局：侧边栏、主内容区、标签区
        self.content_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.colors["primary"]
        )
        self.content_frame.pack(fill="both", expand=True, pady=0)
        
        # 左侧边栏 (垂直按钮区域)
        self.sidebar = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.colors["sidebar"],
            width=120,
            corner_radius=0
        )
        self.sidebar.pack(side="left", fill="y", padx=(0, 0))
        self.sidebar.pack_propagate(False)
        
        # 主内容区域 (图片操作区域)
        self.left_panel = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.colors["primary"]
        )
        self.left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # 右侧面板 (标签选择区域)
        self.right_panel = ctk.CTkFrame(
            self.content_frame, 
            width=500,
            fg_color=self.colors["primary"]
        )
        self.right_panel.pack(side="right", fill="y", padx=(10, 0))
        self.right_panel.pack_propagate(False)
        
        # 构建侧边栏
        self.build_sidebar()
        
        # 构建左侧面板
        self.build_left_panel()
        
        # 构建右侧面板
        self.build_right_panel()
        
    def build_sidebar(self):
        """构建左侧垂直按钮栏"""
        # 标题
        self.sidebar_title = ctk.CTkLabel(
            self.sidebar,
            text="图片工具",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors["text_primary"]
        )
        self.sidebar_title.pack(pady=(20, 10))
        
        # 上传按钮
        self.upload_btn = ctk.CTkButton(
            self.sidebar, 
            text="上传图片",
            command=self.upload_images,
            font=ctk.CTkFont(weight="bold"),
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            width=100,
            height=40
        )
        self.upload_btn.pack(pady=5)
        
        # 上一张按钮
        self.prev_btn = ctk.CTkButton(
            self.sidebar, 
            text="上一张",
            command=self.previous_image,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            width=100,
            height=40
        )
        self.prev_btn.pack(pady=5)
        
        # 下一张按钮
        self.next_btn = ctk.CTkButton(
            self.sidebar, 
            text="下一张",
            command=self.next_image,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            width=100,
            height=40
        )
        self.next_btn.pack(pady=5)
        
        # 模糊编辑按钮 - 新增功能
        self.blur_btn = ctk.CTkButton(
            self.sidebar, 
            text="模糊编辑",
            command=self.open_blur_editor,
            font=ctk.CTkFont(weight="bold"),
            fg_color="#9B59B6",
            hover_color="#8E44AD",
            width=100,
            height=40
        )
        self.blur_btn.pack(pady=5)
        
        # 批量重命名按钮
        self.rename_btn = ctk.CTkButton(
            self.sidebar, 
            text="批量重命名",
            command=self.batch_rename,
            font=ctk.CTkFont(weight="bold"),
            fg_color=self.colors["success"],
            hover_color=self.colors["success_hover"],
            width=100,
            height=40
        )
        self.rename_btn.pack(pady=5)
        
        # 清除列表按钮
        self.clear_btn = ctk.CTkButton(
            self.sidebar, 
            text="清除列表",
            command=self.clear_all_images,
            fg_color=self.colors["danger"],
            hover_color=self.colors["danger_hover"],
            width=100,
            height=40
        )
        self.clear_btn.pack(pady=5)
        
        # 删除当前按钮
        self.delete_btn = ctk.CTkButton(
            self.sidebar, 
            text="删除当前",
            command=self.delete_current_image,
            fg_color=self.colors["danger"],
            hover_color=self.colors["danger_hover"],
            width=100,
            height=40
        )
        self.delete_btn.pack(pady=5)
        
        # 添加空白区域使按钮居中
        self.sidebar_filler = ctk.CTkFrame(
            self.sidebar,
            fg_color=self.colors["sidebar"]
        )
        self.sidebar_filler.pack(fill="both", expand=True)
    
    def open_blur_editor(self):
        """打开模糊编辑窗口"""
        if not self.images:
            messagebox.showwarning("警告", "请先上传图片")
            return
            
        # 创建编辑窗口
        self.editor_window = ctk.CTkToplevel(self.root)
        self.editor_window.title("图片模糊编辑器")
        self.editor_window.geometry("1000x700")
        self.editor_window.configure(fg_color=self.colors["primary"])
        self.editor_window.transient(self.root)
        self.editor_window.grab_set()
        
        # 加载当前图片
        self.editor_image_path = self.images[self.current_index]["path"]
        self.original_image = Image.open(self.editor_image_path)
        self.editing_image = self.original_image.copy()
        
        # 创建编辑界面
        self.create_editor_interface()
    
    def create_editor_interface(self):
        """创建编辑界面"""
        # 主容器
        main_container = ctk.CTkFrame(
            self.editor_window,
            fg_color=self.colors["primary"]
        )
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 标题
        title_label = ctk.CTkLabel(
            main_container,
            text="图片模糊编辑器",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors["text_primary"]
        )
        title_label.pack(pady=(0, 10))
        
        # 内容区域
        content_frame = ctk.CTkFrame(
            main_container,
            fg_color=self.colors["primary"]
        )
        content_frame.pack(fill="both", expand=True)
        
        # 左侧图片区域
        left_frame = ctk.CTkFrame(
            content_frame,
            fg_color=self.colors["secondary"]
        )
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # 图片预览标题
        preview_title = ctk.CTkLabel(
            left_frame,
            text="图片预览 (点击四个点形成四边形区域)",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["text_primary"]
        )
        preview_title.pack(pady=10)
        
        # 图片显示区域
        self.canvas_frame = ctk.CTkFrame(
            left_frame,
            fg_color=self.colors["secondary"]
        )
        self.canvas_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # 使用Canvas显示图片
        from tkinter import Canvas
        self.canvas = Canvas(
            self.canvas_frame,
            bg=self.colors["secondary"],
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True, padx=5, pady=5)
        
        # 右侧控制区域
        right_frame = ctk.CTkFrame(
            content_frame,
            fg_color=self.colors["secondary"],
            width=300
        )
        right_frame.pack(side="right", fill="y", padx=(5, 0))
        right_frame.pack_propagate(False)
        
        # 操作说明
        instructions_frame = ctk.CTkFrame(
            right_frame,
            fg_color=self.colors["secondary"]
        )
        instructions_frame.pack(fill="x", padx=10, pady=10)
        
        instructions = ctk.CTkLabel(
            instructions_frame,
            text="操作说明:\n\n1. 在图片上依次点击四个点形成四边形\n2. 调整模糊强度\n3. 点击'应用模糊'按钮\n4. 重复操作添加多个模糊区域\n5. 裁剪时按住Shift键锁定1:1正方形\n6. 完成后点击'保存并关闭'",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_secondary"],
            justify="left"
        )
        instructions.pack(anchor="w")
        
        # 模糊强度设置
        blur_frame = ctk.CTkFrame(
            right_frame,
            fg_color=self.colors["secondary"]
        )
        blur_frame.pack(fill="x", padx=10, pady=10)
        
        blur_label = ctk.CTkLabel(
            blur_frame,
            text="模糊强度:",
            font=ctk.CTkFont(weight="bold"),
            text_color=self.colors["text_primary"]
        )
        blur_label.pack(anchor="w", pady=(5, 0))
        
        self.blur_slider = ctk.CTkSlider(
            blur_frame,
            from_=1,
            to=20,
            number_of_steps=19,
            command=self.update_blur_display
        )
        self.blur_slider.set(15)  # 默认模糊强度设为15
        self.blur_slider.pack(fill="x", padx=5, pady=5)
        
        self.blur_value = ctk.CTkLabel(
            blur_frame,
            text="15",
            text_color=self.colors["text_primary"]
        )
        self.blur_value.pack()
        
        # 四边形点信息
        self.points_info = ctk.CTkLabel(
            blur_frame,
            text="已选择点: 0/4",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_secondary"]
        )
        self.points_info.pack(pady=5)
        
        # 操作按钮
        buttons_frame = ctk.CTkFrame(
            right_frame,
            fg_color=self.colors["secondary"]
        )
        buttons_frame.pack(fill="x", padx=10, pady=10)
        
        self.apply_blur_btn = ctk.CTkButton(
            buttons_frame,
            text="应用模糊",
            command=self.apply_blur_to_polygon,
            fg_color="#9B59B6",
            hover_color="#8E44AD"
        )
        self.apply_blur_btn.pack(fill="x", pady=5)
        
        self.clear_points_btn = ctk.CTkButton(
            buttons_frame,
            text="清除点",
            command=self.clear_points,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"]
        )
        self.clear_points_btn.pack(fill="x", pady=5)
        
        self.crop_btn = ctk.CTkButton(
            buttons_frame,
            text="裁剪选中区域",
            command=self.crop_selection,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"]
        )
        self.crop_btn.pack(fill="x", pady=5)
        
        self.reset_btn = ctk.CTkButton(
            buttons_frame,
            text="重置图片",
            command=self.reset_editor_image,
            fg_color=self.colors["danger"],
            hover_color=self.colors["danger_hover"]
        )
        self.reset_btn.pack(fill="x", pady=5)
        
        self.save_btn = ctk.CTkButton(
            buttons_frame,
            text="保存并关闭",
            command=self.save_edited_image,
            fg_color=self.colors["success"],
            hover_color=self.colors["success_hover"]
        )
        self.save_btn.pack(fill="x", pady=5)
        
        self.cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="取消",
            command=self.editor_window.destroy,
            fg_color=self.colors["secondary"],
            hover_color=self.colors["primary"]
        )
        self.cancel_btn.pack(fill="x", pady=5)
        
        # 初始化选择区域变量
        self.polygon_points = []  # 存储四个点
        self.point_markers = []   # 存储点的标记
        self.polygon_line = None  # 多边形线条
        self.selection_start = None
        self.selection_rect = None
        self.selection_coords = None
        self.shift_pressed = False  # Shift键状态
        
        # 初始化图片显示
        self.display_editor_image()
        
        # 绑定鼠标事件
        self.canvas.bind("<ButtonPress-1>", self.on_canvas_click)
        self.canvas.bind("<ButtonPress-3>", self.on_canvas_right_click)  # 右键取消最后一个点
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        
        # 绑定键盘事件
        self.editor_window.bind("<KeyPress-Shift_L>", self.on_shift_press)
        self.editor_window.bind("<KeyRelease-Shift_L>", self.on_shift_release)
        self.editor_window.bind("<KeyPress-Shift_R>", self.on_shift_press)
        self.editor_window.bind("<KeyRelease-Shift_R>", self.on_shift_release)
        self.editor_window.focus_set()  # 确保窗口可以接收键盘事件
    
    def display_editor_image(self):
        """在编辑器中显示图片"""
        # 计算合适的显示尺寸
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            # 如果Canvas还没有正确尺寸，使用默认尺寸
            canvas_width, canvas_height = 600, 400
        
        # 调整图片大小以适应Canvas
        img_width, img_height = self.editing_image.size
        ratio = min(canvas_width / img_width, canvas_height / img_height)
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)
        
        self.display_image = self.editing_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(self.display_image)
        
        # 清除Canvas并显示图片
        self.canvas.delete("all")
        self.canvas.create_image(
            canvas_width // 2, 
            canvas_height // 2, 
            image=self.tk_image, 
            anchor="center"
        )
        
        # 保存缩放比例用于坐标转换
        self.scale_ratio = ratio
        self.canvas_offset_x = (canvas_width - new_width) // 2
        self.canvas_offset_y = (canvas_height - new_height) // 2
        
        # 重新绘制已有点
        self.redraw_points()
    
    def redraw_points(self):
        """重新绘制所有点和多边形连线"""
        # 清除之前的点和线
        for marker in self.point_markers:
            self.canvas.delete(marker)
        self.point_markers = []
        
        if self.polygon_line:
            self.canvas.delete(self.polygon_line)
            self.polygon_line = None
        
        # 绘制点
        for i, (x, y) in enumerate(self.polygon_points):
            # 绘制点
            marker = self.canvas.create_oval(
                x-4, y-4, x+4, y+4,
                fill="#9B59B6", outline="#FFFFFF", width=2
            )
            self.point_markers.append(marker)
            
            # 绘制点编号
            text = self.canvas.create_text(
                x, y-10,
                text=str(i+1),
                fill="#FFFFFF",
                font=("Arial", 10, "bold")
            )
            self.point_markers.append(text)
        
        # 绘制多边形连线（如果有至少2个点）
        if len(self.polygon_points) >= 2:
            points = self.polygon_points.copy()
            # 如果已经有4个点，闭合多边形
            if len(points) == 4:
                points.append(points[0])
            
            self.polygon_line = self.canvas.create_line(
                *[coord for point in points for coord in point],
                fill="#9B59B6", width=2, dash=(5, 2)
            )
    
    def on_canvas_click(self, event):
        """Canvas鼠标左键点击事件 - 添加点"""
        # 将Canvas坐标转换为图片坐标
        canvas_x, canvas_y = event.x, event.y
        
        # 检查是否在图片范围内
        if (self.canvas_offset_x <= canvas_x <= self.canvas_offset_x + self.display_image.width and
            self.canvas_offset_y <= canvas_y <= self.canvas_offset_y + self.display_image.height):
            
            # 如果已经有4个点，清除重新开始
            if len(self.polygon_points) >= 4:
                self.polygon_points = []
            
            # 添加新点
            self.polygon_points.append((canvas_x, canvas_y))
            self.redraw_points()
            
            # 更新点信息
            self.points_info.configure(text=f"已选择点: {len(self.polygon_points)}/4")
            
            # 如果已经有4个点，自动绘制闭合多边形
            if len(self.polygon_points) == 4:
                self.redraw_points()
    
    def on_canvas_right_click(self, event):
        """Canvas鼠标右键点击事件 - 删除最后一个点"""
        if self.polygon_points:
            self.polygon_points.pop()
            self.redraw_points()
            self.points_info.configure(text=f"已选择点: {len(self.polygon_points)}/4")
    
    def on_shift_press(self, event):
        """Shift键按下事件"""
        self.shift_pressed = True
    
    def on_shift_release(self, event):
        """Shift键释放事件"""
        self.shift_pressed = False
    
    def on_canvas_drag(self, event):
        """Canvas鼠标拖动事件 - 用于矩形选择"""
        if self.selection_start:
            # 删除旧的选择矩形
            if self.selection_rect:
                self.canvas.delete(self.selection_rect)
            
            # 绘制新的选择矩形
            x1, y1 = self.selection_start
            x2, y2 = event.x, event.y
            
            # 如果按住Shift键，锁定为正方形
            if self.shift_pressed:
                width = abs(x2 - x1)
                height = abs(y2 - y1)
                size = min(width, height)
                
                if x2 < x1:
                    x2 = x1 - size
                else:
                    x2 = x1 + size
                
                if y2 < y1:
                    y2 = y1 - size
                else:
                    y2 = y1 + size
            
            self.selection_rect = self.canvas.create_rectangle(
                x1, y1, x2, y2,
                outline="#3498DB",
                width=2,
                dash=(5, 5)
            )
    
    def on_canvas_release(self, event):
        """Canvas鼠标释放事件"""
        if self.selection_start:
            x1, y1 = self.selection_start
            x2, y2 = event.x, event.y
            
            # 如果按住Shift键，锁定为正方形
            if self.shift_pressed:
                width = abs(x2 - x1)
                height = abs(y2 - y1)
                size = min(width, height)
                
                if x2 < x1:
                    x2 = x1 - size
                else:
                    x2 = x1 + size
                
                if y2 < y1:
                    y2 = y1 - size
                else:
                    y2 = y1 + size
            
            # 确保坐标顺序正确
            left = min(x1, x2)
            right = max(x1, x2)
            top = min(y1, y2)
            bottom = max(y1, y2)
            
            # 保存选择区域坐标
            self.selection_coords = (left, top, right, bottom)
            
            # 重置选择起始点
            self.selection_start = None
    
    def update_blur_display(self, value):
        """更新模糊强度显示"""
        blur_intensity = int(float(value))
        self.blur_value.configure(text=str(blur_intensity))
    
    def clear_points(self):
        """清除所有点"""
        self.polygon_points = []
        self.redraw_points()
        self.points_info.configure(text="已选择点: 0/4")
    
    def apply_blur_to_polygon(self):
        """对四边形区域应用高斯模糊"""
        if len(self.polygon_points) != 4:
            messagebox.showwarning("警告", "请先选择四个点形成四边形")
            return
        
        # 获取模糊强度
        blur_radius = int(self.blur_slider.get())
        
        try:
            # 将Canvas坐标转换为图片坐标
            img_points = []
            for canvas_x, canvas_y in self.polygon_points:
                img_x = int((canvas_x - self.canvas_offset_x) / self.scale_ratio)
                img_y = int((canvas_y - self.canvas_offset_y) / self.scale_ratio)
                img_points.append((img_x, img_y))
            
            # 创建原图的副本进行处理
            img_with_blur = self.editing_image.copy()
            
            # 创建掩膜
            mask = Image.new('L', self.editing_image.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.polygon(img_points, fill=255)
            
            # 对原图应用模糊
            blurred_img = self.editing_image.filter(ImageFilter.GaussianBlur(blur_radius))
            
            # 将模糊后的区域合成到原图
            img_with_blur.paste(blurred_img, mask=mask)
            
            # 更新编辑图片
            self.editing_image = img_with_blur
            
            # 更新显示
            self.display_editor_image()
            
            # 清除点
            self.clear_points()
            
            messagebox.showinfo("成功", "已应用模糊效果")
            
        except Exception as e:
            messagebox.showerror("错误", f"应用模糊失败: {str(e)}")
    
    def crop_selection(self):
        """裁剪选中区域"""
        if not self.selection_coords:
            messagebox.showwarning("警告", "请先选择要裁剪的区域")
            return
        
        # 将Canvas坐标转换为图片坐标
        canvas_left, canvas_top, canvas_right, canvas_bottom = self.selection_coords
        
        # 调整坐标，考虑Canvas中的图片偏移
        img_left = int((canvas_left - self.canvas_offset_x) / self.scale_ratio)
        img_top = int((canvas_top - self.canvas_offset_y) / self.scale_ratio)
        img_right = int((canvas_right - self.canvas_offset_x) / self.scale_ratio)
        img_bottom = int((canvas_bottom - self.canvas_offset_y) / self.scale_ratio)
        
        # 确保坐标在图片范围内
        img_width, img_height = self.editing_image.size
        img_left = max(0, img_left)
        img_top = max(0, img_top)
        img_right = min(img_width, img_right)
        img_bottom = min(img_height, img_bottom)
        
        # 检查选择区域是否有效
        if img_right <= img_left or img_bottom <= img_top:
            messagebox.showwarning("警告", "选择区域无效")
            return
        
        # 执行裁剪
        self.editing_image = self.editing_image.crop((img_left, img_top, img_right, img_bottom))
        
        # 更新显示
        self.display_editor_image()
        
        # 清除选择区域
        if self.selection_rect:
            self.canvas.delete(self.selection_rect)
            self.selection_rect = None
        self.selection_coords = None
        
        messagebox.showinfo("成功", "已裁剪图片")
    
    def reset_editor_image(self):
        """重置编辑器中的图片为原始状态"""
        self.editing_image = self.original_image.copy()
        self.display_editor_image()
        
        # 清除所有点和选择区域
        self.clear_points()
        if self.selection_rect:
            self.canvas.delete(self.selection_rect)
            self.selection_rect = None
        self.selection_coords = None
        
        messagebox.showinfo("成功", "已重置图片")
    
    def save_edited_image(self):
        """保存编辑后的图片并关闭编辑器"""
        try:
            # 保存编辑后的图片，覆盖原文件
            self.editing_image.save(self.editor_image_path)
            
            # 更新主窗口中的图片显示
            self.display_current_image()
            
            # 关闭编辑器窗口
            self.editor_window.destroy()
            
            messagebox.showinfo("成功", "图片已保存")
            
        except Exception as e:
            messagebox.showerror("错误", f"保存图片失败: {str(e)}")

    # 以下为原有代码，保持不变...
    def build_left_panel(self):
        """构建主内容区域"""
        # 标题
        self.title_label = ctk.CTkLabel(
            self.left_panel, 
            text="图片标签重命名工具",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors["text_primary"]
        )
        self.title_label.pack(pady=10)
        
        # 统一前缀设置区域
        self.prefix_frame = ctk.CTkFrame(
            self.left_panel,
            fg_color=self.colors["secondary"]
        )
        self.prefix_frame.pack(fill="x", pady=10, padx=10)
        
        self.prefix_label = ctk.CTkLabel(
            self.prefix_frame,
            text="统一前缀:",
            font=ctk.CTkFont(weight="bold"),
            text_color=self.colors["text_primary"]
        )
        self.prefix_label.pack(side="left", padx=(10, 5), pady=10)
        
        self.prefix_entry = ctk.CTkEntry(
            self.prefix_frame,
            placeholder_text="输入统一前缀（将添加到所有文件名前）",
            fg_color=self.colors["primary"],
            text_color=self.colors["text_primary"]
        )
        self.prefix_entry.pack(side="left", fill="x", expand=True, padx=5, pady=10)
        self.prefix_entry.bind("<KeyRelease>", self.update_common_prefix)
        
        self.clear_prefix_btn = ctk.CTkButton(
            self.prefix_frame,
            text="清除前缀",
            command=self.clear_prefix,
            width=80,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"]
        )
        self.clear_prefix_btn.pack(side="left", padx=5, pady=10)
        
        # 图片预览区域 - 上移与压缩设置对齐
        self.preview_container = ctk.CTkFrame(
            self.left_panel,
            fg_color=self.colors["primary"]
        )
        self.preview_container.pack(fill="both", expand=True, pady=10, padx=10)
        
        # 图片预览标题
        self.preview_title = ctk.CTkLabel(
            self.preview_container,
            text="图片预览",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors["text_primary"]
        )
        self.preview_title.pack(anchor="w", pady=(0, 10))
        
        self.preview_frame = ctk.CTkFrame(
            self.preview_container,
            fg_color=self.colors["primary"],
            corner_radius=8
        )
        self.preview_frame.pack(fill="both", expand=True)
        
        self.preview_label = ctk.CTkLabel(
            self.preview_frame, 
            text="请上传图片开始编辑",
            font=ctk.CTkFont(size=14),
            text_color=self.colors["text_secondary"]
        )
        self.preview_label.pack(expand=True, fill="both", padx=20, pady=20)
        
        # 图片信息区域
        self.info_frame = ctk.CTkFrame(
            self.left_panel,
            fg_color=self.colors["primary"]
        )
        self.info_frame.pack(fill="x", pady=10, padx=10)
        
        # 标签输入
        self.tag_frame = ctk.CTkFrame(
            self.info_frame,
            fg_color=self.colors["secondary"]
        )
        self.tag_frame.pack(fill="x", pady=5)
        
        self.tag_label = ctk.CTkLabel(
            self.tag_frame, 
            text="当前标签:",
            font=ctk.CTkFont(weight="bold"),
            text_color=self.colors["text_primary"]
        )
        self.tag_label.pack(side="left", padx=(10, 5), pady=10)
        
        self.tag_entry = ctk.CTkEntry(
            self.tag_frame,
            placeholder_text="输入标签名称",
            fg_color=self.colors["primary"],
            text_color=self.colors["text_primary"]
        )
        self.tag_entry.pack(side="left", fill="x", expand=True, padx=5, pady=10)
        self.tag_entry.bind("<KeyRelease>", self.update_tag)
        
        # 图片列表区域
        self.list_frame = ctk.CTkFrame(
            self.left_panel,
            fg_color=self.colors["primary"]
        )
        self.list_frame.pack(fill="both", expand=True, pady=10, padx=10)
        
        self.list_label = ctk.CTkLabel(
            self.list_frame, 
            text="图片列表",
            font=ctk.CTkFont(weight="bold"),
            text_color=self.colors["text_primary"]
        )
        self.list_label.pack(anchor="w", padx=10, pady=5)
        
        # 创建滚动文本框用于显示图片列表
        self.image_list = ctk.CTkTextbox(
            self.list_frame,
            height=150,
            fg_color=self.colors["secondary"],
            text_color=self.colors["text_primary"]
        )
        self.image_list.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # 状态栏
        self.status_var = ctk.StringVar(value="就绪 - 请点击'上传图片'按钮选择图片")
        self.status_bar = ctk.CTkLabel(
            self.left_panel,
            textvariable=self.status_var,
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_secondary"]
        )
        self.status_bar.pack(fill="x", pady=5, padx=10)
        
    def build_right_panel(self):
        # 压缩设置区域
        self.build_compression_section()
        
        # 标签选择区域标题和重置按钮
        header_frame = ctk.CTkFrame(
            self.right_panel,
            fg_color=self.colors["primary"]
        )
        header_frame.pack(fill="x", padx=10, pady=10)
        
        # 重置按钮
        self.reset_tags_btn = ctk.CTkButton(
            header_frame,
            text="重置标签状态",
            command=self.reset_tag_states,
            fg_color=self.colors["danger"],
            hover_color=self.colors["danger_hover"],
            width=100
        )
        self.reset_tags_btn.pack(side="right")
        
        # 创建横向排列的分类容器
        self.categories_frame = ctk.CTkFrame(
            self.right_panel,
            fg_color=self.colors["primary"]
        )
        self.categories_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 配置网格布局，使三个分类平均分布
        self.categories_frame.columnconfigure(0, weight=1)
        self.categories_frame.columnconfigure(1, weight=1)
        self.categories_frame.columnconfigure(2, weight=1)
        self.categories_frame.rowconfigure(0, weight=1)
        
        # 为每个分类创建框架
        self.category_frames = {}
        for i, (category, tags) in enumerate(self.categories.items()):
            # 创建分类容器
            category_container = ctk.CTkFrame(
                self.categories_frame,
                fg_color=self.colors["secondary"],
                corner_radius=8
            )
            category_container.grid(row=0, column=i, sticky="nsew", padx=5, pady=5)
            
            # 分类标题
            category_label = ctk.CTkLabel(
                category_container,
                text=category,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=self.colors["text_primary"]
            )
            category_label.pack(pady=5)
            
            # 创建普通框架用于标签按钮（不再使用滚动框架）
            tag_frame = ctk.CTkFrame(
                category_container,
                fg_color=self.colors["secondary"]
            )
            tag_frame.pack(fill="both", expand=True, padx=5, pady=5)
            
            # 添加标签按钮
            for tag in tags:
                btn = ctk.CTkButton(
                    tag_frame,
                    text=tag,
                    command=lambda t=tag: self.apply_tag(t),
                    width=120,
                    height=35,
                    fg_color=self.colors["accent"],
                    hover_color=self.colors["accent_hover"],
                    text_color=self.colors["text_primary"]
                )
                btn.pack(pady=3)
                
                # 存储按钮引用以便后续管理状态
                self.tag_buttons[tag] = btn
    
    def build_compression_section(self):
        """构建压缩设置区域"""
        # 压缩设置框架
        self.compression_frame = ctk.CTkFrame(
            self.right_panel,
            fg_color=self.colors["secondary"],
            corner_radius=8
        )
        self.compression_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        # 标题
        self.compression_title = ctk.CTkLabel(
            self.compression_frame,
            text="图片压缩设置",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors["text_primary"]
        )
        self.compression_title.pack(anchor="w", pady=(5, 10), padx=10)
        
        # 压缩质量滑块
        self.quality_frame = ctk.CTkFrame(
            self.compression_frame,
            fg_color=self.colors["secondary"]
        )
        self.quality_frame.pack(fill="x", padx=10, pady=5)
        
        self.quality_label = ctk.CTkLabel(
            self.quality_frame,
            text="压缩质量:",
            font=ctk.CTkFont(weight="bold"),
            text_color=self.colors["text_primary"]
        )
        self.quality_label.pack(anchor="w")
        
        # 滑块和数值显示
        self.quality_slider_frame = ctk.CTkFrame(
            self.quality_frame,
            fg_color=self.colors["secondary"]
        )
        self.quality_slider_frame.pack(fill="x", pady=5)
        
        self.quality_slider = ctk.CTkSlider(
            self.quality_slider_frame,
            from_=1,
            to=100,
            number_of_steps=100,
            command=self.update_quality_display,
            fg_color=self.colors["primary"],
            progress_color=self.colors["accent"],
            button_color=self.colors["accent"],
            button_hover_color=self.colors["accent_hover"]
        )
        self.quality_slider.set(self.compression_quality)
        self.quality_slider.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.quality_value = ctk.CTkLabel(
            self.quality_slider_frame,
            text=f"{self.compression_quality}%",
            width=40,
            text_color=self.colors["text_primary"]
        )
        self.quality_value.pack(side="right")
        
        # 压缩信息
        self.compression_info = ctk.CTkLabel(
            self.compression_frame,
            text=f"图片将被压缩到最大 {self.max_size}×{self.max_size} 像素",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_secondary"]
        )
        self.compression_info.pack(anchor="w", pady=(0, 5), padx=10)
        
        # 压缩按钮
        self.compress_btn = ctk.CTkButton(
            self.compression_frame,
            text="压缩所有图片",
            command=self.compress_all_images,
            text_color=self.colors["text_primary"]
        )
        self.compress_btn.pack(fill="x", pady=5, padx=10)
    
    def update_quality_display(self, value):
        """更新质量显示"""
        quality = int(float(value))
        self.compression_quality = quality
        self.quality_value.configure(text=f"{quality}%")
    
    def compress_image(self, image_path):
        """压缩单张图片"""
        try:
            with Image.open(image_path) as img:
                # 获取原图格式
                original_format = img.format
                
                # 计算新的尺寸，保持宽高比
                width, height = img.size
                if width > self.max_size or height > self.max_size:
                    ratio = min(self.max_size / width, self.max_size / height)
                    new_width = int(width * ratio)
                    new_height = int(height * ratio)
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # 保存压缩后的图片（覆盖原文件）
                if original_format in ['JPEG', 'JPG']:
                    img.save(image_path, quality=self.compression_quality, optimize=True)
                elif original_format == 'PNG':
                    # PNG格式使用优化
                    img.save(image_path, optimize=True)
                else:
                    # 其他格式直接保存
                    img.save(image_path)
                
                return True, f"压缩成功: {os.path.basename(image_path)}"
                
        except Exception as e:
            return False, f"压缩失败 {os.path.basename(image_path)}: {str(e)}"
    
    def compress_all_images(self):
        """压缩所有图片"""
        if not self.images:
            messagebox.showwarning("警告", "没有图片可压缩")
            return
        
        # 确认对话框
        result = messagebox.askyesno(
            "确认压缩", 
            f"确定要压缩所有图片吗？\n"
            f"• 最大尺寸: {self.max_size}×{self.max_size}\n"
            f"• 压缩质量: {self.compression_quality}%\n"
            f"• 共 {len(self.images)} 张图片\n\n"
            f"此操作将覆盖原文件，建议先备份。"
        )
        if not result:
            return
        
        # 执行压缩
        success_count = 0
        errors = []
        
        for img_info in self.images:
            success, message = self.compress_image(img_info["path"])
            if success:
                success_count += 1
            else:
                errors.append(message)
        
        # 显示结果
        if errors:
            messagebox.showwarning("压缩完成", 
                f"成功压缩 {success_count} 张图片\n"
                f"失败 {len(errors)} 张:\n" + "\n".join(errors))
        else:
            messagebox.showinfo("成功", f"成功压缩所有 {success_count} 张图片")
        
        self.status_var.set(f"图片压缩完成: {success_count} 成功, {len(errors)} 失败")
        
        # 刷新当前图片显示
        if self.images:
            self.display_current_image()
    
    def upload_images(self):
        """上传图片"""
        file_types = [
            ("图片文件", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff"),
            ("所有文件", "*.*")
        ]
        
        filenames = filedialog.askopenfilenames(
            title="选择图片",
            filetypes=file_types
        )
        
        if filenames:
            self.add_images(filenames)
    
    def update_common_prefix(self, event=None):
        """更新统一前缀"""
        self.common_prefix = self.prefix_entry.get()
        # 更新图片列表显示，显示带前缀的文件名
        self.update_image_list()
    
    def clear_prefix(self):
        """清除统一前缀"""
        self.prefix_entry.delete(0, 'end')
        self.common_prefix = ""
        self.update_image_list()
        self.status_var.set("已清除统一前缀")
    
    def add_images(self, file_paths):
        """添加图片到应用"""
        for file_path in file_paths:
            # 获取文件名和扩展名
            name, ext = os.path.splitext(os.path.basename(file_path))
            self.images.append({
                "path": file_path,
                "original_name": name,
                "extension": ext,
                "tag": name  # 默认标签为原文件名
            })
        
        self.update_image_list()
        if self.images:
            self.current_index = 0
            self.display_current_image()
            
        self.status_var.set(f"成功添加 {len(file_paths)} 张图片")
    
    def clear_all_images(self):
        """清除所有图片"""
        if not self.images:
            return
            
        result = messagebox.askyesno("确认", "确定要清除所有图片吗？此操作不可撤销。")
        if result:
            self.images = []
            self.current_index = 0
            self.update_image_list()
            self.preview_label.configure(image='', text="请上传图片开始编辑")
            self.tag_entry.delete(0, 'end')
            self.status_var.set("已清除所有图片")
            
            # 重置所有标签按钮状态
            self.reset_tag_states()
    
    def reset_tag_states(self):
        """重置所有标签按钮状态"""
        self.used_tags.clear()
        for tag, button in self.tag_buttons.items():
            button.configure(
                state="normal",
                fg_color=self.colors["accent"],
                hover_color=self.colors["accent_hover"]
            )
        # 更新当前图片的标签按钮状态
        self.update_tag_buttons_state()
        self.status_var.set("已重置所有标签状态")
    
    def update_image_list(self):
        """更新图片列表"""
        self.image_list.delete("1.0", "end")
        for i, img in enumerate(self.images):
            status = "▶ " if i == self.current_index else "  "
            # 显示带前缀的文件名
            prefix_display = f"{self.common_prefix}_" if self.common_prefix else ""
            self.image_list.insert("end", f"{status}{i+1}. {img['original_name']} -> {prefix_display}{img['tag']}{img['extension']}\n")
    
    def display_current_image(self):
        """显示当前图片"""
        if not self.images:
            return
            
        img_info = self.images[self.current_index]
        
        # 加载并显示图片
        try:
            image = Image.open(img_info["path"])
            # 调整图片大小以适应预览区域
            max_size = (500, 400)
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # 将 PIL Image 转换为 CTkImage
            photo = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=image.size
            )
            
            self.preview_label.configure(
                image=photo,
                text=""
            )
            self.preview_label.image = photo  # 保持引用
            
            # 更新标签输入框
            self.tag_entry.delete(0, 'end')
            self.tag_entry.insert(0, img_info["tag"])
            
            # 更新状态
            prefix_display = f"{self.common_prefix}_" if self.common_prefix else ""
            self.status_var.set(f"第 {self.current_index+1}/{len(self.images)} 张图片: {prefix_display}{img_info['tag']}")
            
            # 更新图片列表显示当前选中项
            self.update_image_list()
            
            # 更新标签按钮状态
            self.update_tag_buttons_state()
            
        except Exception as e:
            messagebox.showerror("错误", f"无法加载图片: {str(e)}")
    
    def update_tag_buttons_state(self):
        """更新标签按钮状态"""
        # 更新已使用标签的状态
        for tag, button in self.tag_buttons.items():
            if tag in self.used_tags:
                # 已使用的标签设为红色
                button.configure(
                    state="normal",
                    fg_color=self.colors["danger"],  # 红色
                    hover_color=self.colors["danger_hover"]  # 深红色
                )
            else:
                # 未使用的标签恢复正常状态
                button.configure(
                    state="normal",
                    fg_color=self.colors["accent"],
                    hover_color=self.colors["accent_hover"]
                )
        
        # 当前图片的标签设为禁用状态
        if self.images:
            current_img = self.images[self.current_index]
            current_tag = current_img["tag"]
            if current_tag in self.tag_buttons:
                self.tag_buttons[current_tag].configure(
                    state="disabled"
                )
    
    def update_tag(self, event):
        """更新标签"""
        if self.images:
            new_tag = self.tag_entry.get()
            old_tag = self.images[self.current_index]["tag"]
            
            # 如果标签有变化，更新状态
            if new_tag != old_tag:
                self.images[self.current_index]["tag"] = new_tag
                self.update_image_list()
                
                # 更新标签按钮状态
                self.update_tag_buttons_state()
    
    def apply_tag(self, tag):
        """应用预设标签到当前图片"""
        if self.images:
            # 将标签添加到已使用集合
            self.used_tags.add(tag)
            
            # 更新当前图片的标签
            self.images[self.current_index]["tag"] = tag
            self.tag_entry.delete(0, 'end')
            self.tag_entry.insert(0, tag)
            self.update_image_list()
            self.status_var.set(f"已应用标签: {tag}")
            
            # 更新标签按钮状态
            self.update_tag_buttons_state()
            
            # 自动切换到下一张图片（如果不是最后一张）
            if self.current_index < len(self.images) - 1:
                self.current_index += 1
                self.display_current_image()
            else:
                # 如果是最后一张，显示提示信息
                messagebox.showinfo("完成", "所有图片已处理完成！")
    
    def previous_image(self):
        """上一张图片"""
        if self.images and self.current_index > 0:
            self.current_index -= 1
            self.display_current_image()
    
    def next_image(self):
        """下一张图片"""
        if self.images and self.current_index < len(self.images) - 1:
            self.current_index += 1
            self.display_current_image()
    
    def delete_current_image(self):
        """删除当前图片"""
        if not self.images:
            return
            
        result = messagebox.askyesno("确认", "确定要删除当前图片吗？")
        if result:
            # 如果当前图片使用了预设标签，从已使用标签中移除
            current_img = self.images[self.current_index]
            if current_img["tag"] in self.tag_buttons:
                self.used_tags.discard(current_img["tag"])
            
            del self.images[self.current_index]
            if self.images:
                if self.current_index >= len(self.images):
                    self.current_index = len(self.images) - 1
                self.display_current_image()
            else:
                self.current_index = 0
                self.preview_label.configure(
                    image=None,
                    text="请上传图片开始编辑"
                )
                self.tag_entry.delete(0, 'end')
                self.status_var.set("已删除所有图片")
                
                # 重置所有标签按钮状态
                self.reset_tag_states()
            
            self.update_image_list()
    
    def batch_rename(self):
        """批量重命名"""
        if not self.images:
            messagebox.showwarning("警告", "没有图片可重命名")
            return
        
        # 确认对话框
        result = messagebox.askyesno("确认", "确定要重命名所有图片吗？此操作不可撤销。")
        if not result:
            return
        
        success_count = 0
        errors = []
        
        for img_info in self.images:
            try:
                # 获取原文件路径
                old_path = img_info["path"]
                directory = os.path.dirname(old_path)
                
                # 构建新文件名（包含统一前缀）
                prefix_part = f"{self.common_prefix}_" if self.common_prefix else ""
                new_filename = f"{prefix_part}{img_info['tag']}{img_info['extension']}"
                new_path = os.path.join(directory, new_filename)
                
                # 如果新文件名已存在，添加数字后缀
                counter = 1
                temp_new_path = new_path
                while os.path.exists(temp_new_path) and temp_new_path != old_path:
                    name, ext = os.path.splitext(new_filename)
                    temp_new_path = os.path.join(directory, f"{name}_{counter}{ext}")
                    counter += 1
                
                # 重命名文件
                if temp_new_path != old_path:
                    os.rename(old_path, temp_new_path)
                    img_info["path"] = temp_new_path
                
                success_count += 1
                
            except Exception as e:
                errors.append(f"重命名 {os.path.basename(old_path)} 失败: {str(e)}")
        
        # 显示结果
        if errors:
            messagebox.showerror("错误", "\n".join(errors))
        else:
            messagebox.showinfo("成功", f"成功重命名 {success_count} 张图片")
            self.update_image_list()
            prefix_display = f"（前缀: {self.common_prefix}）" if self.common_prefix else ""
            self.status_var.set(f"批量重命名完成: {success_count} 张图片 {prefix_display}")
    
    def run(self):
        """运行应用"""
        self.root.mainloop()

# 运行应用
if __name__ == "__main__":
    try:
        app = ModernImageRenamerApp()
        app.run()
    except Exception as e:
        print(f"程序出错: {e}")
        input("按回车键退出...")