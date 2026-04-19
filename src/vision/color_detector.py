"""
Color Mask Configuration Tool for WRO 2026 Future Engineers
============================================================

This module provides an interactive GUI application for configuring 
color masks in LAB color space using live camera feed.

Author: WRO 2026 Team
Version: 1.0.0
License: MIT

Requirements:
    - opencv-python>=4.5.0
    - numpy>=1.20.0
    - tkinter (usually included with Python)

Usage:
    python mask_configurator_gui.py

Notes:
    - LAB color space is used for better illumination invariance
    - All docstrings are in English per documentation standards
    - Comments in Spanish are provided for team understanding
"""

import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict


@dataclass
class ColorMask:
    """
    Represents a color mask configuration in LAB color space.
    
    Attributes:
        name: Unique identifier for the mask
        L_min: Minimum Luminance value (0-100)
        L_max: Maximum Luminance value (0-100)
        A_min: Minimum A channel value (-128 to 127, green-red)
        A_max: Maximum A channel value (-128 to 127, green-red)
        B_min: Minimum B channel value (-128 to 127, blue-yellow)
        B_max: Maximum B channel value (-128 to 127, blue-yellow)
    
    Notes:
        LAB color space is preferred for WRO competitions because:
        - L channel separates brightness from color information
        - More robust to lighting changes than RGB/HSV
        - Perceptually uniform color distances
    """
    
    name: str
    L_min: int
    L_max: int
    A_min: int
    A_max: int
    B_min: int
    B_max: int
    
    def get_lower_bound(self) -> np.ndarray:
        """
        Returns the lower bound array for OpenCV inRange function.
        
        Returns:
            numpy.ndarray: Array with [L_min, A_min, B_min] values
        """
        return np.array([self.L_min, self.A_min, self.B_min], dtype=np.int16)
    
    def get_upper_bound(self) -> np.ndarray:
        """
        Returns the upper bound array for OpenCV inRange function.
        
        Returns:
            numpy.ndarray: Array with [L_max, A_max, B_max] values
        """
        return np.array([self.L_max, self.A_max, self.B_max], dtype=np.int16)
    
    def to_dict(self) -> Dict:
        """
        Converts the mask to a dictionary for JSON serialization.
        
        Returns:
            dict: Dictionary representation of the mask
        """
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ColorMask':
        """
        Creates a ColorMask instance from a dictionary.
        
        Args:
             Dictionary containing mask parameters
            
        Returns:
            ColorMask: New instance created from dictionary
        """
        return cls(**data)
    
    def get_center_values(self) -> Tuple[int, int, int]:
        """
        Calculates the center values of the mask ranges.
        
        Returns:
            tuple: (L_center, A_center, B_center) values
        """
        L_center = (self.L_min + self.L_max) // 2
        A_center = (self.A_min + self.A_max) // 2
        B_center = (self.B_min + self.B_max) // 2
        return L_center, A_center, B_center
    
    def get_tolerance(self) -> Tuple[int, int, int]:
        """
        Calculates the tolerance values for each channel.
        
        Returns:
            tuple: (L_tolerance, A_tolerance, B_tolerance) values
        """
        L_tol = (self.L_max - self.L_min) // 2
        A_tol = (self.A_max - self.A_min) // 2
        B_tol = (self.B_max - self.B_min) // 2
        return L_tol, A_tol, B_tol


class MaskConfiguratorGUI:
    """
    Main GUI application for interactive color mask configuration.
    
    This class manages the entire user interface including:
    - Live camera feed display
    - LAB value sliders for mask adjustment
    - Color sampling via mouse click
    - Mask saving and loading functionality
    - Real-time mask visualization
    
    Attributes:
        root: Tkinter root window
        camera: OpenCV VideoCapture object
        current_mask: Currently configured ColorMask
        masks: Dictionary of all saved masks
        sampled_points: List of color samples from mouse clicks
    
    Notes:
        - Designed for WRO 2026 Future Engineers competition
        - Supports multiple mask configurations per session
        - All configurations are exportable to JSON/TXT formats
    """
    
    def __init__(self):
        """
        Initializes the GUI application and all components.
        
        Sets up:
        - Main window configuration
        - Camera initialization
        - UI components (sliders, buttons, labels)
        - Event handlers
        """
        # Initialize main window
        self.root = tk.Tk()
        self.root.title("WRO 2026 - Configurador de Máscaras LAB")
        self.root.geometry("1400x900")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Camera initialization - Inicialización de cámara
        self.camera = None
        self.cap = None
        self.current_frame = None
        self.current_lab_frame = None
        
        # Mask management - Gestión de máscaras
        self.current_mask: Optional[ColorMask] = None
        self.masks: Dict[str, ColorMask] = {}
        self.sampled_points: List[Tuple[int, int, int, int, int]] = []  # (x, y, L, A, B)
        
        # Slider variables - Variables para sliders
        self.L_min_var = tk.IntVar(value=0)
        self.L_max_var = tk.IntVar(value=100)
        self.A_min_var = tk.IntVar(value=-128)
        self.A_max_var = tk.IntVar(value=127)
        self.B_min_var = tk.IntVar(value=-128)
        self.B_max_var = tk.IntVar(value=127)
        
        # UI components references - Referencias a componentes UI
        self.video_label = None
        self.mask_preview_label = None
        self.status_label = None
        
        # Build the interface - Construir la interfaz
        self._setup_ui()
        self._setup_camera()
        
        # Start video update loop - Iniciar bucle de actualización de video
        self._update_video()
    
    def _setup_ui(self):
        """
        Creates and arranges all UI components.
        
        Layout structure:
        - Left panel: Live video feed and mask preview
        - Right panel: Controls, sliders, and buttons
        - Bottom: Status bar
        
        Notes:
            Uses grid layout for responsive design
            All labels support both English and Spanish
        """
        # Main container - Contenedor principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for resizing - Configurar pesos de grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=2)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Left panel - Video display - Panel izquierdo: Video
        video_frame = ttk.LabelFrame(main_frame, text="Live Feed / Video en Vivo", padding="5")
        video_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        video_frame.columnconfigure(0, weight=1)
        video_frame.rowconfigure(0, weight=1)
        
        # Video label - Etiqueta de video
        self.video_label = ttk.Label(video_frame, background="black")
        self.video_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Mask preview - Vista previa de máscara
        mask_frame = ttk.LabelFrame(video_frame, text="Mask Preview / Vista Previa", padding="5")
        mask_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        mask_frame.columnconfigure(0, weight=1)
        
        self.mask_preview_label = ttk.Label(mask_frame, background="black")
        self.mask_preview_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Right panel - Controls - Panel derecho: Controles
        control_frame = ttk.LabelFrame(main_frame, text="Mask Configuration / Configuración", padding="10")
        control_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        control_frame.columnconfigure(0, weight=1)
        
        # Mask name input - Entrada de nombre de máscara
        name_frame = ttk.LabelFrame(control_frame, text="Mask Name / Nombre", padding="5")
        name_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        name_frame.columnconfigure(1, weight=1)
        
        ttk.Label(name_frame, text="Name:").grid(row=0, column=0, sticky=tk.W)
        self.mask_name_entry = ttk.Entry(name_frame)
        self.mask_name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # LAB Sliders - Sliders LAB
        sliders_frame = ttk.LabelFrame(control_frame, text="LAB Values / Valores LAB", padding="5")
        sliders_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        sliders_frame.columnconfigure(1, weight=1)
        
        # L Channel (Luminance) - Canal L (Luminancia)
        ttk.Label(sliders_frame, text="L (0-100):").grid(row=0, column=0, sticky=tk.W, pady=2)
        
        L_min_frame = ttk.Frame(sliders_frame)
        L_min_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        L_min_frame.columnconfigure(0, weight=1)
        
        self.L_min_slider = ttk.Scale(L_min_frame, from_=0, to=100, variable=self.L_min_var, 
                                       orient=tk.HORIZONTAL, command=self._on_slider_change)
        self.L_min_slider.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.L_min_label = ttk.Label(L_min_frame, text="0", width=4)
        self.L_min_label.grid(row=0, column=1, padx=5)
        
        L_max_frame = ttk.Frame(sliders_frame)
        L_max_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)
        L_max_frame.columnconfigure(0, weight=1)
        
        self.L_max_slider = ttk.Scale(L_max_frame, from_=0, to=100, variable=self.L_max_var,
                                       orient=tk.HORIZONTAL, command=self._on_slider_change)
        self.L_max_slider.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.L_max_label = ttk.Label(L_max_frame, text="100", width=4)
        self.L_max_label.grid(row=0, column=1, padx=5)
        
        # A Channel (Green-Red) - Canal A (Verde-Rojo)
        ttk.Label(sliders_frame, text="A (-128-127):").grid(row=2, column=0, sticky=tk.W, pady=2)
        
        A_min_frame = ttk.Frame(sliders_frame)
        A_min_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5)
        A_min_frame.columnconfigure(0, weight=1)
        
        self.A_min_slider = ttk.Scale(A_min_frame, from_=-128, to=127, variable=self.A_min_var,
                                       orient=tk.HORIZONTAL, command=self._on_slider_change)
        self.A_min_slider.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.A_min_label = ttk.Label(A_min_frame, text="-128", width=5)
        self.A_min_label.grid(row=0, column=1, padx=5)
        
        A_max_frame = ttk.Frame(sliders_frame)
        A_max_frame.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5)
        A_max_frame.columnconfigure(0, weight=1)
        
        self.A_max_slider = ttk.Scale(A_max_frame, from_=-128, to=127, variable=self.A_max_var,
                                       orient=tk.HORIZONTAL, command=self._on_slider_change)
        self.A_max_slider.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.A_max_label = ttk.Label(A_max_frame, text="127", width=5)
        self.A_max_label.grid(row=0, column=1, padx=5)
        
        # B Channel (Blue-Yellow) - Canal B (Azul-Amarillo)
        ttk.Label(sliders_frame, text="B (-128-127):").grid(row=4, column=0, sticky=tk.W, pady=2)
        
        B_min_frame = ttk.Frame(sliders_frame)
        B_min_frame.grid(row=4, column=1, sticky=(tk.W, tk.E), padx=5)
        B_min_frame.columnconfigure(0, weight=1)
        
        self.B_min_slider = ttk.Scale(B_min_frame, from_=-128, to=127, variable=self.B_min_var,
                                       orient=tk.HORIZONTAL, command=self._on_slider_change)
        self.B_min_slider.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.B_min_label = ttk.Label(B_min_frame, text="-128", width=5)
        self.B_min_label.grid(row=0, column=1, padx=5)
        
        B_max_frame = ttk.Frame(sliders_frame)
        B_max_frame.grid(row=5, column=1, sticky=(tk.W, tk.E), padx=5)
        B_max_frame.columnconfigure(0, weight=1)
        
        self.B_max_slider = ttk.Scale(B_max_frame, from_=-128, to=127, variable=self.B_max_var,
                                       orient=tk.HORIZONTAL, command=self._on_slider_change)
        self.B_max_slider.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.B_max_label = ttk.Label(B_max_frame, text="127", width=5)
        self.B_max_label.grid(row=0, column=1, padx=5)
        
        # Sampled color info - Información de color muestreado
        sample_frame = ttk.LabelFrame(control_frame, text="Sampled Color / Color Muestreado", padding="5")
        sample_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        sample_frame.columnconfigure(1, weight=1)
        
        ttk.Label(sample_frame, text="Last Click:").grid(row=0, column=0, sticky=tk.W)
        self.sample_label = ttk.Label(sample_frame, text="Click on video to sample", foreground="gray")
        self.sample_label.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # Buttons - Botones
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=10)
        button_frame.columnconfigure(0, weight=1)
        
        ttk.Button(button_frame, text="Create Mask / Crear Máscara", 
                   command=self._create_mask).grid(row=0, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(button_frame, text="Save Mask / Guardar Máscara", 
                   command=self._save_mask).grid(row=1, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(button_frame, text="Load Masks / Cargar Máscaras", 
                   command=self._load_masks).grid(row=2, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(button_frame, text="Export to TXT / Exportar a TXT", 
                   command=self._export_txt).grid(row=3, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(button_frame, text="Clear Sampled / Limpiar Muestras", 
                   command=self._clear_samples).grid(row=4, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # Saved masks list - Lista de máscaras guardadas
        list_frame = ttk.LabelFrame(control_frame, text="Saved Masks / Máscaras Guardadas", padding="5")
        list_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        self.masks_listbox = tk.Listbox(list_frame, height=8)
        self.masks_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.masks_listbox.bind('<<ListboxSelect>>', self._on_mask_select)
        
        # Status bar - Barra de estado
        self.status_label = ttk.Label(main_frame, text="Ready / Listo", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Instructions - Instrucciones
        instr_frame = ttk.LabelFrame(main_frame, text="Instructions / Instrucciones", padding="5")
        instr_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        instructions = (
            "1. Click on the video to sample a color point / Click en el video para muestrear un color\n"
            "2. Adjust LAB sliders to define the mask range / Ajusta sliders LAB para definir el rango\n"
            "3. Enter a name and click 'Create Mask' / Ingresa nombre y click en 'Crear Máscara'\n"
            "4. Save configuration to JSON file / Guarda configuración en archivo JSON\n"
            "5. Export to TXT for documentation / Exporta a TXT para documentación"
        )
        ttk.Label(instr_frame, text=instructions, justify=tk.LEFT).grid(row=0, column=0, sticky=tk.W)
    
    def _setup_camera(self):
        """
        Initializes the camera capture device.
        
        Notes:
            - Tries default camera (index 0) first
            - Sets resolution to 640x480 for performance
            - Displays error message if camera not found
        """
        try:
            self.cap = cv2.VideoCapture(0)
            
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Cannot open camera / No se pudo abrir la cámara")
                return
            
            # Set resolution - Configurar resolución
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            self.camera = self.cap
            self._update_status("Camera initialized / Cámara inicializada")
            
        except Exception as e:
            messagebox.showerror("Error", f"Camera error: {str(e)}")
    
    def _update_video(self):
        """
        Updates the video feed and mask preview in real-time.
        
        This method:
        - Captures frame from camera
        - Converts to LAB color space
        - Applies current mask if configured
        - Updates UI labels with images
        - Schedules next update (30 FPS)
        
        Notes:
            Uses after() for non-blocking updates
            Converts BGR to RGB for tkinter display
        """
        if self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()
            
            if ret:
                self.current_frame = frame
                
                # Convert to LAB - Convertir a LAB
                self.current_lab_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB).astype(np.int16)
                
                # Convert to RGB for tkinter display - Convertir a RGB para tkinter
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Resize for display - Redimensionar para mostrar
                display_height = 480
                display_width = int(display_height * frame.shape[1] / frame.shape[0])
                resized_frame = cv2.resize(rgb_frame, (display_width, display_height))
                
                # Convert to PhotoImage - Convertir a PhotoImage
                img = cv2.imencode('.png', resized_frame)[1].tobytes()
                photo = tk.PhotoImage(data=img)
                self.video_label.configure(image=photo)
                self.video_label.image = photo  # Keep reference - Mantener referencia
                
                # Bind mouse click for sampling - Vincular click del mouse para muestrear
                self.video_label.bind('<Button-1>', self._on_video_click)
                
                # Update mask preview if mask exists - Actualizar vista previa si existe máscara
                if self.current_mask:
                    self._update_mask_preview()
        
        # Schedule next update - Programar siguiente actualización
        self.root.after(33, self._update_video)  # ~30 FPS
    
    def _on_video_click(self, event):
        """
        Handles mouse click events on the video feed for color sampling.
        
        Args:
            event: Mouse click event containing x, y coordinates
        
        Notes:
            - Samples LAB values at click position
            - Updates status label with sampled values
            - Stores sample in sampled_points list
            - Can be used to auto-set slider values
        """
        if self.current_lab_frame is None:
            return
        
        # Get click coordinates - Obtener coordenadas del click
        x = event.x
        y = event.y
        
        # Check bounds - Verificar límites
        if 0 <= y < self.current_lab_frame.shape[0] and 0 <= x < self.current_lab_frame.shape[1]:
            # Get LAB values - Obtener valores LAB
            L = int(self.current_lab_frame[y, x, 0])
            A = int(self.current_lab_frame[y, x, 1])
            B = int(self.current_lab_frame[y, x, 2])
            
            # Store sample - Almacenar muestra
            self.sampled_points.append((x, y, L, A, B))
            
            # Update label - Actualizar etiqueta
            self.sample_label.configure(
                text=f"({x}, {y}) - L:{L}, A:{A}, B:{B}",
                foreground="green"
            )
            
            # Auto-set sliders with tolerance - Auto-configurar sliders con tolerancia
            tolerance = 20
            self.L_min_var.set(max(0, L - tolerance))
            self.L_max_var.set(min(100, L + tolerance))
            self.A_min_var.set(max(-128, A - tolerance))
            self.A_max_var.set(min(127, A + tolerance))
            self.B_min_var.set(max(-128, B - tolerance))
            self.B_max_var.set(min(127, B + tolerance))
            
            self._update_slider_labels()
            self._update_status(f"Color sampled / Color muestreado: L={L}, A={A}, B={B}")
    
    def _on_slider_change(self, value):
        """
        Handles slider value changes and updates labels.
        
        Args:
            value: New slider value (not used, reads from variables)
        
        Notes:
            Updates all slider value labels in real-time
            Ensures min <= max for each channel
        """
        self._update_slider_labels()
        
        # Ensure min <= max - Asegurar que min <= max
        if self.L_min_var.get() > self.L_max_var.get():
            self.L_max_var.set(self.L_min_var.get())
        if self.A_min_var.get() > self.A_max_var.get():
            self.A_max_var.set(self.A_min_var.get())
        if self.B_min_var.get() > self.B_max_var.get():
            self.B_max_var.set(self.B_min_var.get())
        
        # Update mask preview if exists - Actualizar vista previa si existe
        if self.current_mask:
            self._update_mask_preview()
    
    def _update_slider_labels(self):
        """
        Updates the numeric labels next to each slider.
        
        Notes:
            Called whenever slider values change
            Shows current min/max values for each channel
        """
        self.L_min_label.configure(text=str(self.L_min_var.get()))
        self.L_max_label.configure(text=str(self.L_max_var.get()))
        self.A_min_label.configure(text=str(self.A_min_var.get()))
        self.A_max_label.configure(text=str(self.A_max_var.get()))
        self.B_min_label.configure(text=str(self.B_min_var.get()))
        self.B_max_label.configure(text=str(self.B_max_var.get()))
    
    def _create_mask(self):
        """
        Creates a new ColorMask from current slider values.
        
        Notes:
            - Validates mask name is not empty
            - Creates ColorMask instance
            - Updates current_mask reference
            - Adds to masks dictionary
            - Updates listbox display
        """
        name = self.mask_name_entry.get().strip()
        
        if not name:
            messagebox.showwarning("Warning / Advertencia", 
                                   "Please enter a mask name / Por favor ingresa un nombre")
            return
        
        # Create mask - Crear máscara
        self.current_mask = ColorMask(
            name=name,
            L_min=self.L_min_var.get(),
            L_max=self.L_max_var.get(),
            A_min=self.A_min_var.get(),
            A_max=self.A_max_var.get(),
            B_min=self.B_min_var.get(),
            B_max=self.B_max_var.get()
        )
        
        # Add to dictionary - Agregar al diccionario
        self.masks[name] = self.current_mask
        
        # Update listbox - Actualizar listbox
        self.masks_listbox.insert(tk.END, name)
        
        self._update_status(f"Mask created / Máscara creada: {name}")
        messagebox.showinfo("Success / Éxito", f"Mask '{name}' created / Máscara '{name}' creada")
    
    def _update_mask_preview(self):
        """
        Updates the mask preview visualization.
        
        Notes:
            - Applies current mask to current frame
            - Displays binary mask result
            - Shows detection percentage
        """
        if self.current_frame is None or self.current_mask is None:
            return
        
        # Apply mask - Aplicar máscara
        lower = self.current_mask.get_lower_bound()
        upper = self.current_mask.get_upper_bound()
        mask_result = cv2.inRange(self.current_lab_frame, lower, upper)
        
        # Calculate detection percentage - Calcular porcentaje de detección
        total_pixels = mask_result.size
        white_pixels = cv2.countNonZero(mask_result)
        percentage = (white_pixels / total_pixels) * 100
        
        # Convert for display - Convertir para mostrar
        mask_bgr = cv2.cvtColor(mask_result, cv2.COLOR_GRAY2BGR)
        img = cv2.imencode('.png', mask_bgr)[1].tobytes()
        photo = tk.PhotoImage(data=img)
        self.mask_preview_label.configure(image=photo)
        self.mask_preview_label.image = photo
        
        # Update status with percentage - Actualizar estado con porcentaje
        self._update_status(f"Detection / Detección: {white_pixels} pixels ({percentage:.2f}%)")
    
    def _save_mask(self):
        """
        Saves all configured masks to a JSON file.
        
        Notes:
            - Opens file dialog for save location
            - Exports all masks in self.masks dictionary
            - Includes metadata (timestamp, version)
            - Format compatible with detection scripts
        """
        if not self.masks:
            messagebox.showwarning("Warning / Advertencia", 
                                   "No masks to save / No hay máscaras para guardar")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile="mask_config.json"
        )
        
        if file_path:
            try:
                config_data = {
                    'masks': [mask.to_dict() for mask in self.masks.values()],
                    'color_space': 'LAB',
                    'version': '1.0',
                    'created_at': datetime.now().isoformat(),
                    'total_masks': len(self.masks)
                }
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(config_data, f, indent=2, ensure_ascii=False)
                
                self._update_status(f"Saved to / Guardado en: {file_path}")
                messagebox.showinfo("Success / Éxito", 
                                    f"Configuration saved / Configuración guardada\n{file_path}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Save failed / Error al guardar: {str(e)}")
    
    def _load_masks(self):
        """
        Loads mask configurations from a JSON file.
        
        Notes:
            - Opens file dialog for file selection
            - Clears current masks before loading
            - Updates listbox with loaded masks
            - Validates file format
        """
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                # Clear current masks - Limpiar máscaras actuales
                self.masks.clear()
                self.masks_listbox.delete(0, tk.END)
                
                # Load masks - Cargar máscaras
                for mask_data in config_data.get('masks', []):
                    mask = ColorMask.from_dict(mask_data)
                    self.masks[mask.name] = mask
                    self.masks_listbox.insert(tk.END, mask.name)
                
                self._update_status(f"Loaded {len(self.masks)} masks from / Cargadas {len(self.masks)} máscaras desde {file_path}")
                messagebox.showinfo("Success / Éxito", 
                                    f"Loaded {len(self.masks)} masks / Cargadas {len(self.masks)} máscaras")
                
            except Exception as e:
                messagebox.showerror("Error", f"Load failed / Error al cargar: {str(e)}")
    
    def _export_txt(self):
        """
        Exports mask configurations to a human-readable TXT file.
        
        Notes:
            - Format suitable for documentation
            - Includes all mask parameters
            - Bilingual headers (English/Spanish)
            - Compatible with WRO documentation requirements
        """
        if not self.masks:
            messagebox.showwarning("Warning / Advertencia", 
                                   "No masks to export / No hay máscaras para exportar")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="mask_config.txt"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("=" * 70 + "\n")
                    f.write("WRO 2026 FUTURE ENGINEERS - COLOR MASK CONFIGURATION\n")
                    f.write("CONFIGURACIÓN DE MÁSCARAS DE COLOR - WRO 2026 FUTUROS INGENIEROS\n")
                    f.write("=" * 70 + "\n\n")
                    f.write(f"Export Date / Fecha de Exportación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Total Masks / Total de Máscaras: {len(self.masks)}\n")
                    f.write(f"Color Space / Espacio de Color: LAB (CIELAB)\n\n")
                    f.write("Channel Ranges / Rangos de Canal:\n")
                    f.write("  L: Luminance / Luminancia (0-100)\n")
                    f.write("  A: Green-Red / Verde-Rojo (-128 to 127)\n")
                    f.write("  B: Blue-Yellow / Azul-Amarillo (-128 to 127)\n\n")
                    f.write("=" * 70 + "\n\n")
                    
                    for i, mask in enumerate(self.masks.values(), 1):
                        f.write(f"MASK {i} / MÁSCARA {i}: {mask.name}\n")
                        f.write("-" * 50 + "\n")
                        f.write(f"  L Range / Rango L: [{mask.L_min:3d} - {mask.L_max:3d}]\n")
                        f.write(f"  A Range / Rango A: [{mask.A_min:4d} - {mask.A_max:4d}]\n")
                        f.write(f"  B Range / Rango B: [{mask.B_min:4d} - {mask.B_max:4d}]\n")
                        
                        L_center, A_center, B_center = mask.get_center_values()
                        L_tol, A_tol, B_tol = mask.get_tolerance()
                        
                        f.write(f"  Center / Centro: L={L_center:3d}, A={A_center:4d}, B={B_center:4d}\n")
                        f.write(f"  Tolerance / Tolerancia: L±{L_tol}, A±{A_tol}, B±{B_tol}\n\n")
                    
                    f.write("=" * 70 + "\n")
                    f.write("END OF CONFIGURATION / FIN DE CONFIGURACIÓN\n")
                    f.write("=" * 70 + "\n")
                
                self._update_status(f"Exported to / Exportado a: {file_path}")
                messagebox.showinfo("Success / Éxito", 
                                    f"Configuration exported / Configuración exportada\n{file_path}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Export failed / Error al exportar: {str(e)}")
    
    def _clear_samples(self):
        """
        Clears all sampled color points from memory.
        
        Notes:
            - Resets sampled_points list
            - Updates sample label
            - Does not affect saved masks
        """
        self.sampled_points.clear()
        self.sample_label.configure(text="Click on video to sample", foreground="gray")
        self._update_status("Samples cleared / Muestras limpiadas")
    
    def _on_mask_select(self, event):
        """
        Handles selection of a saved mask from the listbox.
        
        Args:
            event: Listbox selection event
        
        Notes:
            - Loads selected mask configuration
            - Updates sliders to match mask values
            - Sets as current_mask for preview
        """
        selection = self.masks_listbox.curselection()
        
        if selection:
            index = selection[0]
            mask_name = self.masks_listbox.get(index)
            
            if mask_name in self.masks:
                mask = self.masks[mask_name]
                self.current_mask = mask
                
                # Update sliders - Actualizar sliders
                self.L_min_var.set(mask.L_min)
                self.L_max_var.set(mask.L_max)
                self.A_min_var.set(mask.A_min)
                self.A_max_var.set(mask.A_max)
                self.B_min_var.set(mask.B_min)
                self.B_max_var.set(mask.B_max)
                
                # Update name entry - Actualizar entrada de nombre
                self.mask_name_entry.delete(0, tk.END)
                self.mask_name_entry.insert(0, mask.name)
                
                self._update_slider_labels()
                self._update_status(f"Loaded mask / Máscara cargada: {mask.name}")
    
    def _update_status(self, message: str):
        """
        Updates the status bar message.
        
        Args:
            message: Status message to display (bilingual recommended)
        """
        self.status_label.configure(text=message)
    
    def on_closing(self):
        """
        Handles application closing event.
        
        Notes:
            - Releases camera resources
            - Destroys tkinter window
            - Prevents memory leaks
        """
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()
        self.root.destroy()
    
    def run(self):
        """
        Starts the GUI application main loop.
        
        Notes:
            - Should be called after initialization
            - Blocks until window is closed
            - Entry point for the application
        """
        self._update_status("Ready / Listo - Click on video to sample colors")
        self.root.mainloop()


def main():
    """
    Main entry point for the application.
    
    Creates and runs the MaskConfiguratorGUI instance.
    Catches and displays any startup errors.
    """
    try:
        app = MaskConfiguratorGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Fatal Error / Error Fatal", 
                            f"Application failed / La aplicación falló:\n{str(e)}")


if __name__ == "__main__":
    main()