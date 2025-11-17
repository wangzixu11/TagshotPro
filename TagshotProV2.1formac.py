# TagshotProV2.1formac_fixed_debug.py - 图片标签重命名工具 (修复布局并添加调试)
import customtkinter as ctk
from tkinter import filedialog, messagebox, Toplevel
import os
from PIL import Image, ImageTk, ImageDraw
import shutil
import platform
import sys

# 打印执行开始信息
print("--- Tagshot Pro V2 启动 ---")

class ModernImageRenamerApp:
    def __init__(self):
        # 设置外观模式和统一颜色主题
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
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
        self.root.title("Tagshot Pro V2 - 图片标签重命名工具")
        
        # 窗口尺寸和最小尺寸
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

        # 状态管理
        self.image_list = []
        self.current_image_index = -1
        self.current_directory = ""
        self.common_prefix = ""
        
        # UI 变量
        self.current_tags = ctk.StringVar(value="")
        self.current_filename_var = ctk.StringVar(value="当前文件名：N/A")
        self.new_filename_var = ctk.StringVar(value="新文件名预览：N/A")
        self.status_var = ctk.StringVar(value="欢迎使用 Tagshot Pro V2！请加载图片。")
        self.compression_quality = ctk.DoubleVar(value=85.0)
        self.compress_active = ctk.BooleanVar(value=False)
        self.is_mac = platform.system() == "Darwin"

        # 标签预设
        self.tag_presets = {
            "角度": ["前视", "后视", "侧面", "俯视"],
            "组件": ["发动机", "传动轴", "轮毂", "车架"],
            "特写": ["划痕", "接口", "铭牌", "密封圈"]
        }
        
        print("初始化：开始创建 UI 组件")
        self._create_widgets()
        print("初始化：UI 组件创建完成")
        self._set_default_tags()

    def _on_closing(self):
        """窗口关闭时的处理"""
        self.root.destroy()
    
    def _create_widgets(self):
        """创建和布局所有 UI 组件"""
        # 设置主网格布局
        self.root.grid_rowconfigure(0, weight=1) 
        self.root.grid_rowconfigure(1, weight=0) 
        self.root.grid_columnconfigure(0, weight=0) 
        self.root.grid_columnconfigure(1, weight=1) 

        # --- 1. 侧边栏 (Sidebar) ---
        self.sidebar_frame = ctk.CTkFrame(self.root, width=300, corner_radius=0, fg_color=self.colors["sidebar"])
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 1))
        self.sidebar_frame.grid_rowconfigure(2, weight=1) # 标签区权重最大

        # 标题
        ctk.CTkLabel(self.sidebar_frame, text="Tagshot Pro", font=ctk.CTkFont(size=24, weight="bold"), text_color=self.colors["text_primary"]).grid(row=0, column=0, padx=20, pady=(20, 10), sticky="n")

        # 加载按钮
        load_button = ctk.CTkButton(self.sidebar_frame, text="加载图片目录", command=self.load_images, fg_color=self.colors["accent"], hover_color=self.colors["accent_hover"])
        load_button.grid(row=1, column=0, padx=20, pady=(10, 20), sticky="ew")

        # --- 标签和前缀设置区 (可滚动) ---
        self.scrollable_tags_frame = ctk.CTkScrollableFrame(self.sidebar_frame, label_text="标签预设", label_fg_color=self.colors["sidebar"])
        self.scrollable_tags_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        row_counter = 0
        for category, tags in self.tag_presets.items():
            ctk.CTkLabel(self.scrollable_tags_frame, text=category, font=ctk.CTkFont(size=14, weight="bold"), text_color=self.colors["text_secondary"]).grid(row=row_counter, column=0, padx=5, pady=(10, 0), sticky="w")
            row_counter += 1
            
            btn_frame = ctk.CTkFrame(self.scrollable_tags_frame, fg_color="transparent")
            btn_frame.grid(row=row_counter, column=0, sticky="ew", padx=5)
            for i in range(len(tags)):
                btn_frame.grid_columnconfigure(i, weight=1)

            col_counter = 0
            for tag in tags:
                btn = ctk.CTkButton(btn_frame, text=tag, 
                                    command=lambda t=tag: self._add_tag(t),
                                    fg_color=self.colors["secondary"],
                                    hover_color=self.colors["secondary"])
                btn.grid(row=0, column=col_counter, padx=4, pady=4, sticky="ew")
                col_counter += 1
            
            row_counter += 1
        
        # --- 前缀和压缩选项 ---
        prefix_frame = ctk.CTkFrame(self.sidebar_frame, fg_color=self.colors["secondary"])
        prefix_frame.grid(row=3, column=0, padx=10, pady=(10, 5), sticky="ew")
        
        ctk.CTkLabel(prefix_frame, text="前缀设置", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))
        
        prefix_input = ctk.CTkEntry(prefix_frame, placeholder_text="输入项目/日期前缀", width=260)
        prefix_input.pack(padx=10, pady=(0, 5), fill="x")
        
        prefix_button = ctk.CTkButton(prefix_frame, text="设置/更新前缀", command=lambda: self.set_prefix(prefix_input.get()), 
                                        fg_color=self.colors["accent"], hover_color=self.colors["accent_hover"])
        prefix_button.pack(padx=10, pady=(0, 10), fill="x")

        # 压缩选项
        compression_check = ctk.CTkCheckBox(prefix_frame, text="启用压缩/优化", variable=self.compress_active)
        # 布局修复：pack() 必须使用 anchor
        compression_check.pack(padx=10, pady=(10, 5), anchor="w") 
        
        ctk.CTkLabel(prefix_frame, text="JPG 质量 (50-100)").pack(padx=10, pady=(5, 0), anchor="w")
        compression_slider = ctk.CTkSlider(prefix_frame, from_=50, to=100, variable=self.compression_quality)
        # 布局修复：pack() 必须使用 fill="x" 来扩展
        compression_slider.pack(padx=10, pady=(0, 10), fill="x")

        # --- 底部操作按钮 ---
        bottom_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        bottom_frame.grid(row=4, column=0, padx=10, pady=(5, 20), sticky="ew")
        bottom_frame.grid_columnconfigure((0, 1), weight=1)
        
        # 根据系统调整快捷键提示
        next_key = "Cmd+N" if self.is_mac else "Ctrl+N"
        batch_button = ctk.CTkButton(bottom_frame, text=f"重命名并下一张 ({next_key})", command=self.rename_and_next, fg_color=self.colors["success"], hover_color=self.colors["success_hover"])
        batch_button.grid(row=0, column=0, padx=(0, 5), pady=10, sticky="ew")

        batch_button = ctk.CTkButton(bottom_frame, text="批量重命名全部", command=self.batch_rename_all, fg_color=self.colors["danger"], hover_color=self.colors["danger_hover"])
        batch_button.grid(row=0, column=1, padx=(5, 0), pady=10, sticky="ew")

        # --- 2. 主内容区 (Main Content) ---
        self.main_content_frame = ctk.CTkFrame(self.root, fg_color=self.colors["primary"])
        self.main_content_frame.grid(row=0, column=1, sticky="nsew")
        self.main_content_frame.grid_rowconfigure(1, weight=1) # 预览图权重最大
        self.main_content_frame.grid_columnconfigure(0, weight=1)

        # 文件信息和预览区域
        info_frame = ctk.CTkFrame(self.main_content_frame, fg_color=self.colors["secondary"])
        info_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        info_frame.grid_columnconfigure(0, weight=1) 

        self.current_filename_label = ctk.CTkLabel(info_frame, textvariable=self.current_filename_var, font=ctk.CTkFont(size=14), text_color=self.colors["text_secondary"], anchor="w")
        self.current_filename_label.grid(row=0, column=0, padx=15, pady=(10, 0), sticky="w")

        self.new_filename_label = ctk.CTkLabel(info_frame, textvariable=self.new_filename_var, font=ctk.CTkFont(size=18, weight="bold"), text_color=self.colors["text_primary"], anchor="w")
        self.new_filename_label.grid(row=1, column=0, padx=15, pady=(0, 10), sticky="w")

        # 预览图区
        self.preview_canvas = ctk.CTkCanvas(self.main_content_frame, bg=self.colors["primary"], highlightthickness=0)
        self.preview_canvas.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.preview_canvas.bind("<Configure>", self.resize_image_preview)
        
        self.default_image = self._create_placeholder_image(800, 600)
        self.preview_canvas.image_tk = ImageTk.PhotoImage(self.default_image)
        self.preview_canvas.create_image(400, 300, image=self.preview_canvas.image_tk, anchor="center")
        
        # 标签输入和操作区
        tag_input_frame = ctk.CTkFrame(self.main_content_frame, fg_color=self.colors["secondary"])
        tag_input_frame.grid(row=2, column=0, padx=20, pady=(5, 20), sticky="ew")
        tag_input_frame.grid_columnconfigure(0, weight=1)
        tag_input_frame.grid_columnconfigure((1, 2), weight=0)

        # 当前标签输入框
        self.tag_entry = ctk.CTkEntry(tag_input_frame, textvariable=self.current_tags, placeholder_text="手动输入标签 (以 '-' 或 '_' 分隔)", font=ctk.CTkFont(size=16))
        self.tag_entry.grid(row=0, column=0, padx=15, pady=15, sticky="ew")
        self.tag_entry.bind("<KeyRelease>", self.update_preview_filename)

        # 清除按钮
        clear_button = ctk.CTkButton(tag_input_frame, text="清空标签", command=self.clear_tags, fg_color=self.colors["danger"], hover_color=self.colors["danger_hover"])
        clear_button.grid(row=0, column=1, padx=(0, 15), pady=15, sticky="e")
        
        # 上一张/下一张按钮
        nav_frame = ctk.CTkFrame(tag_input_frame, fg_color="transparent")
        nav_frame.grid(row=0, column=2, padx=(0, 15), pady=15, sticky="e")
        nav_frame.grid_columnconfigure((0, 1), weight=1)
        
        prev_key = "Cmd+L" if self.is_mac else "Ctrl+L"
        next_key = "Cmd+R" if self.is_mac else "Ctrl+R"
        
        prev_button = ctk.CTkButton(nav_frame, text=f"< 上一张 ({prev_key})", command=lambda: self.change_image(-1), fg_color=self.colors["accent"], hover_color=self.colors["accent_hover"])
        prev_button.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        next_button = ctk.CTkButton(nav_frame, text=f"下一张 > ({next_key})", command=lambda: self.change_image(1), fg_color=self.colors["accent"], hover_color=self.colors["accent_hover"])
        next_button.grid(row=0, column=1, padx=(5, 0), sticky="ew")
        
        # --- 3. 状态栏 ---
        self.status_bar = ctk.CTkLabel(self.root, textvariable=self.status_var, height=30, fg_color=self.colors["accent"], text_color=self.colors["text_primary"], font=ctk.CTkFont(size=12), corner_radius=0)
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")

        # 键盘绑定
        if self.is_mac:
            self.root.bind("<Command-n>", lambda event: self.rename_and_next())
            self.root.bind("<Command-l>", lambda event: self.change_image(-1))
            self.root.bind("<Command-r>", lambda event: self.change_image(1))
            self.root.bind("<Command-o>", lambda event: self.load_images())
        else:
            self.root.bind("<Control-n>", lambda event: self.rename_and_next())
            self.root.bind("<Control-l>", lambda event: self.change_image(-1))
            self.root.bind("<Control-r>", lambda event: self.change_image(1))
            self.root.bind("<Control-o>", lambda event: self.load_images())


    def _create_placeholder_image(self, width, height):
        """创建一个默认的占位符图片"""
        image = Image.new('RGB', (width, height), color=self.colors["secondary"])
        draw = ImageDraw.Draw(image)
        try:
            from PIL import ImageFont
            font = ctk.CTkFont(size=30, weight="bold").cget("font")
            if isinstance(font, str):
                font = ImageFont.load_default()
            else:
                font = ImageFont.truetype("Arial.ttf", 30) 
            text = "加载图片目录..."
            text_w, text_h = draw.textsize(text, font)
            draw.text(((width - text_w) / 2, (height - text_h) / 2), text, fill=self.colors["text_secondary"], font=font)
        except Exception:
             draw.text((width/2 - 100, height/2 - 15), "加载图片目录...", fill=self.colors["text_secondary"])
        return image

    def _set_default_tags(self):
        """设置默认标签，避免空标签"""
        self.current_tags.set("未命名")
        self.update_preview_filename()

    def load_images(self, directory=None):
        """选择目录并加载所有图片文件"""
        if not directory:
            directory = filedialog.askdirectory(title="选择包含图片的目录")
        
        if directory:
            self.current_directory = directory
            self.image_list = []
            supported_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
            
            for filename in os.listdir(directory):
                if filename.lower().endswith(supported_extensions):
                    path = os.path.join(directory, filename)
                    base_name = os.path.splitext(filename)[0]
                    tags_part = base_name.split('-')
                    if len(tags_part) > 1:
                        initial_tags = tags_part[-1]
                    else:
                        initial_tags = "未命名"
                        
                    self.image_list.append({
                        "path": path,
                        "original_name": filename,
                        "extension": os.path.splitext(filename)[1].lower(),
                        "tags": initial_tags
                    })
            
            self.image_list.sort(key=lambda x: x["original_name"].lower())
            
            if self.image_list:
                self.current_image_index = 0
                self.status_var.set(f"成功加载 {len(self.image_list)} 张图片。")
                self.display_current_image()
            else:
                self.current_image_index = -1
                self.status_var.set("所选目录中没有找到支持的图片文件。")
                self.current_filename_var.set("当前文件名：N/A")
                self.new_filename_var.set("新文件名预览：N/A")
                self.preview_canvas.delete("all")
        else:
            self.status_var.set("未选择任何目录。")

    def display_current_image(self):
        """在画布上显示当前图片"""
        if 0 <= self.current_image_index < len(self.image_list):
            img_info = self.image_list[self.current_image_index]
            self.current_filename_var.set(f"当前文件名：{img_info['original_name']} ({self.current_image_index + 1}/{len(self.image_list)})")
            self.current_tags.set(img_info['tags'])
            
            try:
                if hasattr(self, 'current_image_pil_handle'):
                    # 尝试关闭上一个文件的句柄
                    try:
                        self.current_image_pil_handle.close()
                    except:
                        pass # 忽略关闭错误

                self.current_image_pil_handle = Image.open(img_info['path'])
                self.current_image_pil = self.current_image_pil_handle.copy()
                self.current_image_pil_handle.close() # 立即关闭文件句柄
                self.resize_image_preview()
            except Exception as e:
                self.status_var.set(f"错误：无法打开图片 {img_info['original_name']}: {e}")
                self.preview_canvas.delete("all")
                self.current_image_pil = self._create_placeholder_image(800, 600)
                self.resize_image_preview()
            
            self.update_preview_filename()
        else:
            self.preview_canvas.delete("all")
            self.current_filename_var.set("当前文件名：N/A")
            self.new_filename_var.set("新文件名预览：N/A")

    def resize_image_preview(self, event=None):
        """根据画布大小调整图片并显示"""
        if not hasattr(self, 'current_image_pil') or not self.current_image_pil:
            return
        
        canvas_width = self.preview_canvas.winfo_width()
        canvas_height = self.preview_canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1: 
            return

        img_width, img_height = self.current_image_pil.size
        
        padding = 40
        ratio_w = (canvas_width - padding) / img_width
        ratio_h = (canvas_height - padding) / img_height
        ratio = min(ratio_w, ratio_h)
        
        ratio = min(ratio, 1.0) # 不放大图片
        
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)

        try:
            # 使用 Image.Resampling.LANCZOS
            resized_image = self.current_image_pil.resize((new_width, new_height), Image.Resampling.LANCZOS)
        except AttributeError:
             # 旧版本PIL兼容
            resized_image = self.current_image_pil.resize((new_width, new_height), Image.ANTIALIAS) 

        self.preview_canvas.image_tk = ImageTk.PhotoImage(resized_image)
        
        center_x = canvas_width / 2
        center_y = canvas_height / 2
        
        self.preview_canvas.delete("image") 
        self.preview_canvas.create_image(center_x, center_y, image=self.preview_canvas.image_tk, anchor="center", tag="image")

    def _add_tag(self, tag):
        """将标签添加到当前标签变量中"""
        current = self.current_tags.get().strip()
        
        if current == "未命名":
            current = ""
        
        if current and not current.endswith('-') and not current.endswith('_'):
            current += '-'
            
        tags_list = [t.strip() for t in current.replace('_', '-').split('-') if t.strip()]
        if tag not in tags_list:
            if current and current[-1] != '-':
                 current += '-'
            current += tag
        
        self.current_tags.set(current)
        self.update_preview_filename()

    def clear_tags(self):
        """清除所有标签并设置默认值"""
        self.current_tags.set("未命名")
        self.update_preview_filename()

    def set_prefix(self, prefix):
        """设置项目前缀"""
        sanitized_prefix = "".join(c for c in prefix if c.isalnum() or c in ('-', '_')).strip()
        self.common_prefix = sanitized_prefix
        if self.common_prefix and not self.common_prefix.endswith('-') and not self.common_prefix.endswith('_'):
            self.common_prefix += '-'
        
        self.status_var.set(f"新的项目前缀已设置: {self.common_prefix if self.common_prefix else '无'}")
        self.update_preview_filename()

    def update_preview_filename(self, event=None):
        """根据当前标签和前缀更新新文件名预览"""
        if self.current_image_index == -1:
            return

        tags = self.current_tags.get().strip()
        img_info = self.image_list[self.current_image_index]
        ext = img_info['extension']

        # 清理标签，确保分隔符一致，并去除首尾的'-'
        clean_tags = tags.replace('_', '-').strip('-')
        
        # 构建新文件名
        new_base_name = f"{self.common_prefix}{clean_tags}"
        
        if not new_base_name.strip('-'):
            new_base_name = os.path.splitext(img_info['original_name'])[0] + "-UNTAGGED" # 防止空文件名
        
        # 最终文件名，确保没有双重分隔符
        final_base_name = new_base_name.replace('--', '-').strip('-')
        
        new_filename = f"{final_base_name}{ext}"
        
        self.new_filename_var.set(f"新文件名预览：{new_filename}")
        # 将标签存回列表，以备重命名或批量操作
        img_info['tags'] = tags

    def _get_new_filename(self, img_info):
        """生成最终要写入的文件名"""
        tags = img_info['tags'].strip()
        ext = img_info['extension']

        # 清理标签
        clean_tags = tags.replace('_', '-').strip('-')
        
        # 构建新文件名
        new_base_name = f"{self.common_prefix}{clean_tags}"
        
        if not new_base_name.strip('-'):
            return None # 如果没有标签也没有前缀，则不重命名
        
        # 最终文件名，确保没有双重分隔符
        final_base_name = new_base_name.replace('--', '-').strip('-')
        
        return f"{final_base_name}{ext}"
        
    def _apply_compression(self, image_path, original_ext):
        """根据设置对图片进行压缩或格式转换"""
        if not self.compress_active.get():
            return

        quality = int(self.compression_quality.get())
        
        try:
            img = Image.open(image_path)
            
            # 目前只对 JPEG 格式应用压缩质量
            if original_ext in ('.jpg', '.jpeg'):
                temp_path = image_path + ".temp_comp"
                
                temp_img = img.copy()
                if temp_img.mode in ('RGBA', 'P'):
                    temp_img = temp_img.convert('RGB')
                    
                temp_img.save(temp_path, format="JPEG", quality=quality, optimize=True)
                temp_img.close()
                img.close()
                
                shutil.move(temp_path, image_path)
                
                self.status_var.set(f"应用了 {quality}% JPEG 压缩。")
            
            elif original_ext == '.png':
                 temp_path = image_path + ".temp_comp"
                 temp_img = img.copy()
                 if temp_img.mode == 'RGBA':
                     temp_img = temp_img.convert('P', palette=Image.Palette.ADAPTIVE, colors=256)
                 
                 temp_img.save(temp_path, format="PNG", optimize=True)
                 temp_img.close()
                 img.close()
                 shutil.move(temp_path, image_path)
                 self.status_var.set(f"应用了 PNG 优化。")
                 

        except Exception as e:
            self.status_var.set(f"压缩警告：{os.path.basename(image_path)} 失败: {str(e)}")


    def rename_and_next(self):
        """重命名当前文件并切换到下一张"""
        if self.current_image_index == -1:
            messagebox.showinfo("提示", "请先加载图片。")
            return

        img_info = self.image_list[self.current_image_index]
        old_path = img_info['path']
        original_ext = img_info['extension']
        new_filename = self._get_new_filename(img_info)
        
        if not new_filename:
            self.status_var.set("当前文件跳过重命名，切换到下一张。")
            self.change_image(1) 
            return

        try:
            directory = os.path.dirname(old_path)
            new_path_base = os.path.join(directory, new_filename)
            
            # --- 重名冲突处理 ---
            counter = 1
            temp_new_path = new_path_base
            while os.path.exists(temp_new_path) and temp_new_path != old_path:
                name, ext = os.path.splitext(new_filename)
                temp_new_path = os.path.join(directory, f"{name.split('_')[0]}_{counter}{ext}")
                counter += 1
            
            # 重命名文件
            if temp_new_path != old_path:
                os.rename(old_path, temp_new_path)
                img_info["path"] = temp_new_path 
                img_info["original_name"] = os.path.basename(temp_new_path) 
            
            # 应用压缩 (在重命名后操作)
            self._apply_compression(temp_new_path, original_ext)
            
            self.status_var.set(f"成功重命名: {os.path.basename(old_path)} -> {os.path.basename(temp_new_path)}")
            self.change_image(1) 

        except Exception as e:
            messagebox.showerror("重命名失败", f"无法重命名文件: {str(e)}")

    def batch_rename_all(self):
        """批量重命名所有已加载的图片"""
        if not self.image_list:
            messagebox.showinfo("提示", "请先加载图片。")
            return
        
        if not messagebox.askyesno("确认批量重命名", f"即将对 {len(self.image_list)} 张图片执行批量重命名。是否继续？\n\n注意：这会覆盖源文件并不可撤销。"):
            return

        errors = []
        success_count = 0
        
        self.update_preview_filename() 
        
        for i in range(len(self.image_list)):
            img_info = self.image_list[i]
            old_path = img_info['path']
            original_ext = img_info['extension']
            new_filename = self._get_new_filename(img_info)
            
            if not new_filename:
                continue

            try:
                directory = os.path.dirname(old_path)
                new_path_base = os.path.join(directory, new_filename)
                
                # --- 重名冲突处理 ---
                counter = 1
                temp_new_path = new_path_base
                while os.path.exists(temp_new_path) and temp_new_path != old_path:
                    name, ext = os.path.splitext(new_filename)
                    temp_new_path = os.path.join(directory, f"{name.split('_')[0]}_{counter}{ext}")
                    counter += 1
                
                # 重命名文件
                if temp_new_path != old_path:
                    os.rename(old_path, temp_new_path)
                    img_info["path"] = temp_new_path # 更新列表中的路径
                    img_info["original_name"] = os.path.basename(temp_new_path)

                # 应用压缩
                self._apply_compression(temp_new_path, original_ext)
                
                success_count += 1
                
            except Exception as e:
                errors.append(f"重命名/压缩 {os.path.basename(old_path)} 失败: {str(e)}")
        
        # 显示结果
        if errors:
            messagebox.showerror("错误", f"部分文件重命名失败，共成功 {success_count} 个。\n详细错误（仅显示前5个）：\n" + "\n".join(errors[:5]))
        else:
            messagebox.showinfo("成功", f"批量重命名完成: {success_count} 张图片。")
            
        if self.current_image_index != -1:
            self.display_current_image() 

        self.status_var.set(f"批量重命名操作完成。成功重命名 {success_count} 张图片。")

    def change_image(self, step):
        """切换到上一张或下一张图片"""
        if not self.image_list:
            return

        new_index = self.current_image_index + step
        
        if 0 <= new_index < len(self.image_list):
            self.current_image_index = new_index
            self.display_current_image()
        elif new_index >= len(self.image_list):
            self.current_image_index = 0
            self.display_current_image()
            self.status_var.set("已流转到图片列表开头。")
        elif new_index < 0:
            self.current_image_index = len(self.image_list) - 1
            self.display_current_image()
            self.status_var.set("已流转到图片列表末尾。")

    def run(self):
        """启动应用的主循环"""
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = ModernImageRenamerApp()
        print("启动：调用 app.run() 进入主循环")
        app.run()
        print("--- Tagshot Pro V2 正常退出 ---")
    except Exception as e:
        print("\nFATAL ERROR: 窗口启动失败！")
        print(f"请检查以下错误信息：{e}")
        # 在macOS上，如果依赖或环境配置有问题，有时需要强制退出
        sys.exit(1)
